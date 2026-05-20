"""
Blog Agent — Parafarmacia Erboristeria Viale Umberto 1°
=========================================================

Agente AI che ogni mattina alle 10:00 (Europe/Rome):
  1. Scopre un argomento ricercato dalle persone nei settori
     naturopatia, omeopatia, erboristeria, cura del corpo.
  2. Cerca fonti autorevoli sull'argomento.
  3. Genera un articolo originale via Claude API (claude-sonnet-4-6).
  4. Genera un'immagine coerente via Pollinations.ai (modello Flux).
  5. Aggiorna articles.json e pubblica via Git push su GitHub.

Variabili d'ambiente richieste:
  - ANTHROPIC_API_KEY   : chiave API Anthropic
  - GITHUB_TOKEN        : personal access token con permessi `repo`
  - GITHUB_REPO         : es. "intheboxstudio/parafarmacia-viale-umberto"
  - GITHUB_BRANCH       : default "main"

Variabili d'ambiente opzionali:
  - GEMINI_API_KEY       : non più usata (image-gen passata a Pollinations).
                           Mantenuta per backward compat con setup esistenti.
  - BRAVE_SEARCH_API_KEY : per ricerca fonti autorevoli (gratis 2k/mese)
  - FORCE_RUN            : "true" per eseguire fuori orario (test manuali)
  - SKIP_TIME_CHECK      : alias di FORCE_RUN per CI/CD

Deploy: GitHub Actions con doppio cron (gestisce CET/CEST automaticamente).
"""

from __future__ import annotations

import base64
import json
import logging
import os
import random
import re
import sys
import unicodedata
from dataclasses import dataclass, field, asdict
from datetime import datetime
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo

import requests
from anthropic import Anthropic

# ============================================================================
# CONFIGURAZIONE
# ============================================================================

ROME_TZ = ZoneInfo("Europe/Rome")
PUBLISH_HOUR = 10  # 10:00 ora italiana

# Marchi presenti in parafarmacia — il modello li conosce e li suggerisce
# nei contenuti quando pertinente.
PARAFARMACIA_BRANDS = [
    "Solime",       # apicoltura, integratori naturali
    "Lovrèn",       # cosmesi marina premium
    "Algàdemy",     # skincare avanzato
    "Naturalsalus", # integrazione naturale
    "Cetilar",      # performance, dolore
    "Esi",          # fitoterapia clinica
    "Biokyma",      # erboristeria toscana
    "Bromatech",    # microbiota e probiotici
]

# Domini autorevoli — l'agente cita SOLO fonti da questo elenco.
AUTHORITATIVE_DOMAINS = [
    # Istituzionali italiani
    "iss.it",
    "salute.gov.it",
    "aifa.gov.it",
    "epicentro.iss.it",

    # Ospedali e istituti di ricerca italiani
    "humanitas.it",
    "auxologico.it",
    "ieo.it",
    "ospedalebambinogesu.it",
    "fondazioneveronesi.it",
    "gimbe.org",
    "policlinico.mi.it",
    "smartsantagostino.it",

    # Internazionali
    "who.int",
    "ema.europa.eu",
    "nih.gov",
    "ncbi.nlm.nih.gov",
    "pubmed.ncbi.nlm.nih.gov",
    "cochranelibrary.com",
    "mayoclinic.org",
    "medlineplus.gov",
    "harvard.edu",
    "examine.com",

    # Editorie scientifiche
    "sciencedirect.com",
    "nature.com",
    "thelancet.com",
    "bmj.com",
    "nejm.org",
    "jamanetwork.com",
    "frontiersin.org",
]

# Tematiche-seed per la discovery
TOPIC_SEEDS = {
    "erboristeria": [
        "tisana per dormire", "rimedi naturali insonnia", "tisana digestiva",
        "erbe per ansia", "valeriana effetti", "melissa proprietà",
        "passiflora utilizzo", "tisana per dimagrire", "tisana drenante",
        "rimedi naturali raffreddore", "echinacea funziona",
    ],
    "omeopatia": [
        "omeopatia stress", "rimedio omeopatico ansia", "gelsemium 9 ch",
        "ignatia omeopatia", "arnica omeopatia", "argentum nitricum quando",
        "omeopatia bambini", "omeopatia per dormire",
    ],
    "naturopatia": [
        "naturopatia stress", "fitoterapia menopausa", "integratori magnesio",
        "vitamina d carenza", "omega 3 benefici", "rimedi naturali emicrania",
        "naturopatia colon irritabile", "intolleranze alimentari naturopatia",
    ],
    "cura-del-corpo": [
        "pelle secca rimedi", "couperose cosa fare", "acne adulta",
        "rughe rimedi naturali", "capelli che cadono donna", "forfora rimedi",
        "smagliature prevenzione", "macchie viso rimedi", "skincare routine sera",
        "olio essenziale piedi",
    ],
}

# Tempo medio di lettura: ~220 parole/min
WORDS_PER_MINUTE = 220

# Modelli
CLAUDE_MODEL = "claude-sonnet-4-6"
# L'image generation è gestita da Pollinations.ai (Flux), vedi ImageGenerator.
# Non serve API key Gemini né nessun'altra chiave per le immagini.

# Limite articoli mantenuti nel JSON (i più vecchi vengono archiviati)
MAX_ARTICLES_IN_FEED = 30


# ============================================================================
# LOGGING
# ============================================================================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
log = logging.getLogger("blog_agent")


# ============================================================================
# MODELLI DATI
# ============================================================================

@dataclass
class Product:
    """Prodotto consigliato nell'articolo."""
    brand: str
    name: str
    description: str


@dataclass
class Source:
    """Fonte citata nell'articolo."""
    name: str
    url: str


@dataclass
class Article:
    """Articolo completo del blog."""
    id: str
    slug: str
    title: str
    category: str
    categoryLabel: str
    excerpt: str
    content: str
    image: str
    date: str
    readingTime: str
    products: list[Product] = field(default_factory=list)
    sources: list[Source] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "slug": self.slug,
            "title": self.title,
            "category": self.category,
            "categoryLabel": self.categoryLabel,
            "excerpt": self.excerpt,
            "content": self.content,
            "image": self.image,
            "date": self.date,
            "readingTime": self.readingTime,
            "products": [asdict(p) for p in self.products],
            "sources": [asdict(s) for s in self.sources],
        }


# ============================================================================
# UTILITY
# ============================================================================

def slugify(text: str) -> str:
    """Converte stringa in slug URL-friendly."""
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode()
    text = re.sub(r"<[^>]+>", "", text)  # rimuove HTML
    text = re.sub(r"[^\w\s-]", "", text.lower())
    text = re.sub(r"[\s_-]+", "-", text).strip("-")
    return text[:80]


def estimate_reading_time(content_html: str) -> str:
    """Stima tempo di lettura dall'HTML del contenuto."""
    plain = re.sub(r"<[^>]+>", " ", content_html)
    words = len(plain.split())
    minutes = max(1, round(words / WORDS_PER_MINUTE))
    return f"{minutes} min"


def category_label(category: str) -> str:
    """Mappa slug categoria → label italiana."""
    return {
        "erboristeria": "Erboristeria",
        "omeopatia": "Omeopatia",
        "naturopatia": "Naturopatia",
        "cura-del-corpo": "Cura del corpo",
    }.get(category, category.capitalize())


def is_publish_time() -> bool:
    """Verifica che siano effettivamente le 10:00 ora italiana.

    GitHub Actions cron è in UTC: in CEST le 10:00 IT = 08:00 UTC,
    in CET le 10:00 IT = 09:00 UTC. Il workflow YAML schedula entrambi
    e questa funzione lascia passare solo il run "giusto" del giorno.
    """
    if os.getenv("FORCE_RUN", "").lower() in {"1", "true", "yes"}:
        return True
    if os.getenv("SKIP_TIME_CHECK", "").lower() in {"1", "true", "yes"}:
        return True
    now = datetime.now(ROME_TZ)
    return now.hour == PUBLISH_HOUR


# ============================================================================
# 1. TOPIC DISCOVERY
# ============================================================================

class TopicDiscoverer:
    """Trova domande/problemi ricercati dagli utenti.

    Strategia: usa l'endpoint pubblico Google Suggest (autocomplete) per
    ottenere le query più comuni a partire da seed tematici.
    """

    SUGGEST_URL = "https://suggestqueries.google.com/complete/search"

    def discover(self) -> tuple[str, str]:
        """Restituisce (categoria, problema specifico)."""
        category = random.choice(list(TOPIC_SEEDS.keys()))
        seed = random.choice(TOPIC_SEEDS[category])

        log.info("Discovery: categoria=%s, seed=%s", category, seed)

        candidates: list[str] = []
        try:
            r = requests.get(
                self.SUGGEST_URL,
                params={"client": "firefox", "q": seed, "hl": "it", "gl": "it"},
                timeout=10,
            )
            r.raise_for_status()
            data = r.json()
            if isinstance(data, list) and len(data) >= 2:
                candidates = data[1]
        except Exception as exc:
            log.warning("Google Suggest fallito: %s. Uso seed diretto.", exc)

        candidates = [
            c for c in candidates
            if isinstance(c, str) and len(c.split()) >= 2 and len(c) <= 90
        ]

        topic = random.choice(candidates) if candidates else seed
        log.info("Topic scelto: %r", topic)
        return category, topic


# ============================================================================
# 2. SOURCE FINDER
# ============================================================================

class SourceFinder:
    """Trova fonti autorevoli sul topic via Brave Search API (opzionale)."""

    def __init__(self, brave_api_key: str | None = None):
        self.brave_key = brave_api_key

    def find(self, topic: str) -> list[Source]:
        """Trova 2-4 fonti autorevoli pertinenti al topic."""
        if not self.brave_key:
            return []

        try:
            r = requests.get(
                "https://api.search.brave.com/res/v1/web/search",
                params={"q": topic, "country": "IT", "search_lang": "it", "count": 10},
                headers={"X-Subscription-Token": self.brave_key, "Accept": "application/json"},
                timeout=10,
            )
            r.raise_for_status()
            results = r.json().get("web", {}).get("results", [])

            authoritative = [
                Source(name=res.get("title", "")[:80], url=res.get("url", ""))
                for res in results
                if any(d in (res.get("url") or "") for d in AUTHORITATIVE_DOMAINS)
            ][:4]

            log.info("Fonti autorevoli trovate: %d", len(authoritative))
            return authoritative
        except Exception as exc:
            log.warning("Brave Search fallita: %s", exc)
            return []


# ============================================================================
# 3. CONTENT GENERATOR (Claude API)
# ============================================================================

class ArticleGenerator:
    """Genera l'articolo via Claude API.

    Usa il meccanismo nativo di Anthropic "tool use" per ottenere un output
    strutturato. Il modello restituisce direttamente un dict Python validato
    dal JSON schema dichiarato qui sotto — nessun parsing fragile, nessun
    rischio di virgolette zoppe nell'HTML.
    """

    SYSTEM_PROMPT = """Sei la voce editoriale del blog di una parafarmacia italiana di alta qualità (Parafarmacia Erboristeria Viale Umberto 1°, Reggio Emilia, di proprietà della Dottoressa Emy). La tua scrittura è:

- Professionale ma calda, mai sterile
- Citata e fondata su evidenze (non "secondo alcuni studi" ma "una meta-analisi pubblicata su Sleep Medicine Reviews ha mostrato che…")
- In italiano elegante, lessico colto ma comprensibile
- Mai promozionale o medicinale: divulgativa
- Onesta sui limiti dei rimedi naturali (es: "non sostituisce il parere medico")

Quando ti viene fornito un topic, usa il tool `publish_article` per pubblicarlo. Il tool richiede questi campi:

- title: titolo accattivante in HTML con <em>...</em> intorno al problema specifico. Usa uno dei pattern: "Hai <em>{problema}</em> e non sai come risolverlo?" / "Vuoi risolvere <em>{problema}</em>?" / "<em>{problema}</em> non ti lascia vivere serena?" / "Soffri di <em>{problema}</em>? Ecco cosa fare davvero".

- excerpt: 1-2 frasi sintetiche, max 200 caratteri.

- content: HTML del corpo dell'articolo. Solo tag inline (<p>, <h2>, <h3>, <ul>, <ol>, <li>, <blockquote>, <em>, <strong>). NIENTE <html>, <body>, <head>. NIENTE attributi (no class, no style, no href). Almeno 600 parole. Struttura: intro con dato/contesto, 2-3 sezioni con sottotitoli <h2>, una sezione "cosa NON fare" o "cosa fare invece", chiusura che richiama l'esperienza in parafarmacia.

- imagePrompt: SEGUI LE REGOLE DETTAGLIATE QUI SOTTO.

- products: 3 prodotti pertinenti dai marchi della whitelist (Solime, Lovrèn, Algàdemy, Naturalsalus, Cetilar, Esi, Biokyma, Bromatech). Per ciascuno: brand, name, description (max 25 parole).

- sources: 2-3 fonti dai domini autorevoli (iss.it, salute.gov.it, aifa.gov.it, humanitas.it, fondazioneveronesi.it, ieo.it, mayoclinic.org, ncbi.nlm.nih.gov, cochranelibrary.com, who.int, examine.com, sciencedirect.com, nature.com, thelancet.com, bmj.com, frontiersin.org, harvard.edu, medlineplus.gov). Per ciascuna: name, url.

REGOLE PER L'IMAGE PROMPT (importante):

Decidi tu se l'immagine deve mostrare una persona o essere uno still-life, in base al topic.

A) STILL-LIFE — quando il topic ruota attorno a una pianta, sostanza, rimedio, prodotto, alimento (tisana, valeriana, magnesio, omega 3, vitamina D, melissa, echinacea, arnica, integratori, ecc.). Descrivi una composizione fotografica elegante: pianta/foglia/tisana/oggetto come protagonista, su superficie naturale (legno chiaro, lino, ceramica), con elementi coerenti (cucchiaino, tazza fumante, foglie sparse, libro aperto sfocato sullo sfondo). Vista dall'alto o tre quarti. NIENTE persone.

B) FRAMMENTO DI PERSONA — quando il topic riguarda un'esperienza vissuta dal corpo (skincare, capelli, stress, sonno, postura, dolore, massaggi, menopausa, acne). MAI volti riconoscibili a fuoco, MAI primi piani di facce intere. Mostra la persona SOLO attraverso: mani che fanno qualcosa, profilo sfocato/silhouette controluce, dettagli del corpo a contesto, persona di spalle, mezza inquadratura della parte interessata.

Specifica sempre: "anonymous, no recognizable face, soft natural light, editorial photography style". Aggiungi etnia "Mediterranean" per coerenza col pubblico italiano.

Esempi di buoni image prompt:
- Valeriana: "A bunch of fresh valerian flowers and dried roots on a light oak wood table, a glass jar with herbal infusion next to it, a small ceramic spoon, soft morning light from the left, top-down view, minimal composition with negative space."
- Skincare pelle secca: "Close-up of Mediterranean woman's hands applying a dollop of cream on the back of her other hand, anonymous, no face visible, soft natural side light, white marble bathroom counter with a green leaf and a small amber glass bottle in soft focus background, editorial photography style."
- Stress lavorativo: "Mediterranean woman's silhouette from behind, sitting at a wooden desk near a sunlit window, hand resting on her forehead, laptop slightly out of focus, warm afternoon light, anonymous, no face visible, editorial photography style, calm muted palette."

In tutti i casi NIENTE testo nell'immagine, NIENTE loghi, NIENTE marchi visibili."""

    USER_TEMPLATE = """Topic di oggi: "{topic}"
Categoria: {category}

Genera l'articolo completo e pubblicalo usando il tool `publish_article`."""

    # JSON schema del tool — Anthropic forza il modello a generare un output
    # che rispetta esattamente questa struttura. Niente più parsing manuale.
    TOOL_SCHEMA = {
        "name": "publish_article",
        "description": (
            "Pubblica un articolo sul blog della parafarmacia con tutti i campi "
            "richiesti: titolo HTML, excerpt, contenuto HTML, prompt immagine, "
            "prodotti consigliati e fonti autorevoli."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "title": {
                    "type": "string",
                    "description": "Titolo HTML con <em>...</em> attorno al problema specifico"
                },
                "excerpt": {
                    "type": "string",
                    "description": "Sommario testuale di 1-2 frasi, max 200 caratteri"
                },
                "content": {
                    "type": "string",
                    "description": (
                        "HTML del corpo dell'articolo. Solo tag <p>, <h2>, <h3>, "
                        "<ul>, <ol>, <li>, <blockquote>, <em>, <strong> senza attributi. "
                        "Almeno 600 parole."
                    )
                },
                "imagePrompt": {
                    "type": "string",
                    "description": "Prompt in inglese per Gemini Imagen, segue le regole A/B nel system prompt"
                },
                "products": {
                    "type": "array",
                    "description": "Esattamente 3 prodotti consigliati",
                    "items": {
                        "type": "object",
                        "properties": {
                            "brand": {
                                "type": "string",
                                "enum": ["Solime", "Lovrèn", "Algàdemy", "Naturalsalus",
                                         "Cetilar", "Esi", "Biokyma", "Bromatech"]
                            },
                            "name": {"type": "string"},
                            "description": {
                                "type": "string",
                                "description": "Perché lo consigliamo, max 25 parole"
                            }
                        },
                        "required": ["brand", "name", "description"]
                    },
                    "minItems": 2,
                    "maxItems": 4
                },
                "sources": {
                    "type": "array",
                    "description": "2-3 fonti autorevoli",
                    "items": {
                        "type": "object",
                        "properties": {
                            "name": {"type": "string"},
                            "url": {
                                "type": "string",
                                "description": "URL completo, deve appartenere a un dominio autorevole"
                            }
                        },
                        "required": ["name", "url"]
                    },
                    "minItems": 1,
                    "maxItems": 4
                }
            },
            "required": ["title", "excerpt", "content", "imagePrompt", "products", "sources"]
        }
    }

    def __init__(self, api_key: str):
        self.client = Anthropic(api_key=api_key)

    def generate(self, topic: str, category: str, sources_hint: list[Source]) -> dict[str, Any]:
        """Genera l'articolo strutturato via tool use. Restituisce dict pronto per Article."""
        log.info("Generazione articolo per topic: %r", topic)

        user_msg = self.USER_TEMPLATE.format(topic=topic, category=category)
        if sources_hint:
            user_msg += "\n\nFonti suggerite (cita queste se pertinenti):\n"
            for s in sources_hint:
                user_msg += f"- {s.name}: {s.url}\n"

        try:
            response = self.client.messages.create(
                model=CLAUDE_MODEL,
                max_tokens=8192,
                system=self.SYSTEM_PROMPT,
                tools=[self.TOOL_SCHEMA],
                tool_choice={"type": "tool", "name": "publish_article"},
                messages=[{"role": "user", "content": user_msg}],
            )

            # Con tool_choice forzato, la response contiene un blocco tool_use
            # con un dict già parsato in `input`. Niente più json.loads.
            for block in response.content:
                if block.type == "tool_use" and block.name == "publish_article":
                    data = block.input
                    log.info("Articolo generato: %s", str(data.get("title", ""))[:60])
                    return data

            raise RuntimeError(
                f"Nessun tool_use trovato nella response. "
                f"stop_reason={response.stop_reason}, "
                f"content_types={[b.type for b in response.content]}"
            )

        except Exception as exc:
            log.error("Errore generazione articolo: %s", exc)
            raise


# ============================================================================
# 4. IMAGE GENERATOR (Pollinations.ai con modello Flux)
# ============================================================================

class ImageGenerator:
    """Genera l'immagine di copertina via Pollinations.ai (Flux).

    Pollinations è un servizio gratuito che proxa modelli image-gen open source
    (Flux di Black Forest Labs in questo caso). Niente API key, niente billing,
    niente quota giornaliera per uso modesto. Endpoint REST semplicissimo.
    Trade-off: occasionali downtime, latenza variabile (3-15s).

    Se Pollinations non risponde, fallback a SVG placeholder.
    """

    POLLINATIONS_BASE = "https://image.pollinations.ai/prompt"

    # Style suffix calibrato per Flux: il modello risponde meglio a prompt
    # fotografici con dettagli tecnici di camera/obiettivo (a differenza di
    # Gemini che preferiva descrizioni più narrative).
    STYLE_SUFFIX = (
        ". Editorial photography style, shot on Hasselblad H6D medium format, "
        "85mm lens, f/2.8 shallow depth of field, soft natural window light. "
        "Premium Italian pharmacy and wellness brand aesthetic. "
        "Color palette: powder blue, dusty pink, sage green, warm white, oak wood. "
        "Composition: 16:9 horizontal frame, clean minimal, generous negative space. "
        "If a person appears, they MUST be anonymous: no recognizable face in focus, "
        "shown only through hands, silhouette, profile, or back view, "
        "generic Mediterranean features. "
        "No text overlay, no logos, no brand names, no celebrities, no children. "
        "Hyper-realistic, magazine quality, professional retouching."
    )

    # Dimensioni 16:9 ideali per cover da blog su index.html
    IMAGE_WIDTH = 1280
    IMAGE_HEIGHT = 720

    # Timeout generoso: Flux può prendersela comoda nei picchi
    TIMEOUT = 90
    MAX_ATTEMPTS = 3

    def __init__(self, api_key: str | None, output_dir: Path):
        # api_key è ignorato (Pollinations è gratuito) ma manteniamo la
        # firma del costruttore per non rompere chi orchestra l'agente.
        self.output_dir = output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def generate(self, prompt: str, slug: str) -> tuple[str, Path | None]:
        """Genera l'immagine.

        Restituisce (path_per_json, path_locale_o_None).
        Il path_per_json è quello che finisce in articles.json (relativo).
        Il path_locale serve al publisher per uploadare il file binario.
        """
        full_prompt = (prompt or "").strip() + self.STYLE_SUFFIX
        log.info("Generazione immagine (Pollinations/Flux), prompt[..80]=%s",
                 full_prompt[:80])

        # Costruisci URL: prompt va URL-encoded, parametri di query in chiaro.
        # `nologo=true` rimuove il watermark Pollinations.
        # `enhance=false` evita che il servizio "migliori" il prompt cambiandolo.
        # `seed` random previene caching di prompt simili e garantisce variety.
        from urllib.parse import quote

        seed = random.randint(1, 10_000_000)
        url = (
            f"{self.POLLINATIONS_BASE}/{quote(full_prompt)}"
            f"?width={self.IMAGE_WIDTH}"
            f"&height={self.IMAGE_HEIGHT}"
            f"&model=flux"
            f"&nologo=true"
            f"&enhance=false"
            f"&seed={seed}"
        )

        # Retry con backoff esponenziale (Pollinations può essere lento sotto carico)
        last_exc: Exception | None = None
        for attempt in range(1, self.MAX_ATTEMPTS + 1):
            try:
                log.info("Pollinations attempt %d/%d (seed=%d)",
                         attempt, self.MAX_ATTEMPTS, seed)
                r = requests.get(
                    url,
                    timeout=self.TIMEOUT,
                    headers={"Accept": "image/png,image/jpeg,image/*"},
                )
                r.raise_for_status()

                ctype = r.headers.get("Content-Type", "")
                if not ctype.startswith("image/"):
                    raise RuntimeError(
                        f"Pollinations ha risposto con content-type non immagine: "
                        f"{ctype}. Body[:200]={r.content[:200]!r}"
                    )

                image_bytes = r.content
                # Pollinations restituisce di solito JPEG, ma talvolta PNG.
                # Salviamo sempre con estensione coerente al magic number.
                ext = "png" if image_bytes[:8].startswith(b"\x89PNG") else "jpg"
                filename = f"{slug}.{ext}"
                out_path = self.output_dir / filename
                out_path.write_bytes(image_bytes)
                log.info("Immagine salvata: %s (%d KB)",
                         out_path, len(image_bytes) // 1024)
                return f"./assets/blog/{filename}", out_path

            except Exception as exc:
                last_exc = exc
                log.warning("Pollinations attempt %d fallito: %s", attempt, exc)
                if attempt < self.MAX_ATTEMPTS:
                    import time
                    backoff = 2 ** attempt  # 2s, 4s, 8s
                    time.sleep(backoff)

        log.error("Pollinations ha fallito %d volte: %s — uso placeholder SVG",
                  self.MAX_ATTEMPTS, last_exc)
        return self._placeholder_svg(slug), None

    @staticmethod
    def _placeholder_svg(slug: str) -> str:
        """Fallback: SVG decorativo se Pollinations è giù."""
        return (
            "data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' "
            "viewBox='0 0 800 600'><defs><linearGradient id='g' x1='0%' y1='0%' "
            "x2='100%' y2='100%'><stop offset='0%' stop-color='%23C9DEEC'/>"
            "<stop offset='100%' stop-color='%234A88AD'/></linearGradient></defs>"
            "<rect width='800' height='600' fill='url(%23g)'/></svg>"
        )


# ============================================================================
# 5. PUBLISHER (Git push su GitHub)
# ============================================================================

class GitPublisher:
    """Aggiorna articles.json e committa su GitHub via API REST."""

    def __init__(self, token: str, repo: str, branch: str = "main"):
        self.token = token
        self.repo = repo
        self.branch = branch
        self.api_base = "https://api.github.com"
        self.headers = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
        }

    def _get_file(self, path: str) -> tuple[str, str] | None:
        """Restituisce (content_decoded, sha) o None se non esiste."""
        url = f"{self.api_base}/repos/{self.repo}/contents/{path}?ref={self.branch}"
        r = requests.get(url, headers=self.headers, timeout=15)
        if r.status_code == 404:
            return None
        r.raise_for_status()
        data = r.json()
        content = base64.b64decode(data["content"]).decode("utf-8")
        return content, data["sha"]

    def _put_file(self, path: str, content: str, sha: str | None, message: str) -> None:
        """Crea o aggiorna un file via API."""
        url = f"{self.api_base}/repos/{self.repo}/contents/{path}"
        payload: dict[str, Any] = {
            "message": message,
            "content": base64.b64encode(content.encode("utf-8")).decode("ascii"),
            "branch": self.branch,
        }
        if sha:
            payload["sha"] = sha
        r = requests.put(url, headers=self.headers, json=payload, timeout=15)
        r.raise_for_status()

    def publish_article(self, article: Article) -> None:
        """Aggiorna articles.json con il nuovo articolo in testa."""
        log.info("Pubblicazione articolo: %s", article.slug)

        result = self._get_file("articles.json")
        if result is None:
            feed = {"version": "1.0", "articles": []}
            sha = None
        else:
            content, sha = result
            feed = json.loads(content)

        existing_ids = {a.get("id") for a in feed.get("articles", [])}
        if article.id in existing_ids:
            log.warning("Articolo già presente, skip: %s", article.id)
            return

        feed.setdefault("articles", []).insert(0, article.to_dict())

        if len(feed["articles"]) > MAX_ARTICLES_IN_FEED:
            feed["articles"] = feed["articles"][:MAX_ARTICLES_IN_FEED]

        feed["lastUpdated"] = datetime.now(ROME_TZ).isoformat()
        feed["version"] = "1.0"

        commit_msg = f"blog: pubblicato '{article.slug}' ({article.date[:10]})"
        new_content = json.dumps(feed, ensure_ascii=False, indent=2)
        self._put_file("articles.json", new_content, sha, commit_msg)
        log.info("articles.json aggiornato su GitHub")

    def publish_image(self, local_path: Path, remote_path: str) -> None:
        """Carica un'immagine binaria nel repo."""
        if not local_path.exists():
            log.warning("Immagine locale non trovata: %s — skip", local_path)
            return

        log.info("Upload immagine: %s → %s", local_path, remote_path)
        data = local_path.read_bytes()
        url = f"{self.api_base}/repos/{self.repo}/contents/{remote_path}"

        existing = requests.get(url + f"?ref={self.branch}", headers=self.headers, timeout=15)
        sha = existing.json().get("sha") if existing.status_code == 200 else None

        payload: dict[str, Any] = {
            "message": f"blog: immagine {local_path.name}",
            "content": base64.b64encode(data).decode("ascii"),
            "branch": self.branch,
        }
        if sha:
            payload["sha"] = sha

        r = requests.put(url, headers=self.headers, json=payload, timeout=30)
        r.raise_for_status()
        log.info("Immagine pubblicata")


# ============================================================================
# AGENT ORCHESTRATION
# ============================================================================

class BlogAgent:
    """Orchestra l'intera pipeline di generazione e pubblicazione."""

    def __init__(self) -> None:
        self.anthropic_key = self._require_env("ANTHROPIC_API_KEY")
        self.github_token = self._require_env("GITHUB_TOKEN")
        self.github_repo = self._require_env("GITHUB_REPO")
        self.github_branch = os.getenv("GITHUB_BRANCH", "main")
        self.brave_key = os.getenv("BRAVE_SEARCH_API_KEY")
        # GEMINI_API_KEY è opzionale e attualmente ignorata
        # (immagini servite da Pollinations.ai). Mantenuta per backward
        # compat con setup Railway/Actions già configurati.
        self.gemini_key = os.getenv("GEMINI_API_KEY")

        self.assets_dir = Path("./assets/blog")

        self.discoverer = TopicDiscoverer()
        self.source_finder = SourceFinder(self.brave_key)
        self.generator = ArticleGenerator(self.anthropic_key)
        self.image_gen = ImageGenerator(self.gemini_key, self.assets_dir)
        self.publisher = GitPublisher(self.github_token, self.github_repo, self.github_branch)

    @staticmethod
    def _require_env(name: str) -> str:
        val = os.getenv(name)
        if not val:
            log.error("Variabile d'ambiente mancante: %s", name)
            sys.exit(1)
        return val

    def run(self) -> None:
        """Esegue l'intera pipeline."""
        now = datetime.now(ROME_TZ)
        log.info("=" * 70)
        log.info("Blog Agent — run del %s", now.isoformat())
        log.info("=" * 70)

        # Check ora: GitHub Actions schedula due cron (8 e 9 UTC) per coprire
        # CET/CEST. Solo l'esecuzione che cade alle 10:00 IT procede.
        if not is_publish_time():
            log.info(
                "Non è l'ora di pubblicare (ora IT: %02d:%02d). Skip silenzioso. "
                "Usa FORCE_RUN=true per testare manualmente.",
                now.hour, now.minute
            )
            return

        try:
            # 1. Discovery
            category, topic = self.discoverer.discover()

            # 2. Sources
            sources_hint = self.source_finder.find(topic)

            # 3. Genera articolo
            data = self.generator.generate(topic, category, sources_hint)

            # 4. Genera immagine
            slug = slugify(re.sub(r"<[^>]+>", "", data["title"]))
            today_str = now.strftime("%Y-%m-%d")
            article_id = f"{today_str}-{slug[:40]}"

            image_path_rel, local_image = self.image_gen.generate(
                data["imagePrompt"], article_id
            )

            # 5. Crea Article object
            article = Article(
                id=article_id,
                slug=slug,
                title=data["title"],
                category=category,
                categoryLabel=category_label(category),
                excerpt=data["excerpt"],
                content=data["content"],
                image=image_path_rel,
                date=now.isoformat(),
                readingTime=estimate_reading_time(data["content"]),
                products=[Product(**p) for p in data.get("products", [])],
                sources=[Source(**s) for s in data.get("sources", [])],
            )

            # 6. Pubblica immagine (se generata localmente)
            if local_image is not None and local_image.exists():
                self.publisher.publish_image(
                    local_image, f"assets/blog/{article_id}.jpg"
                )

            # 7. Pubblica articolo (aggiorna JSON su GitHub)
            self.publisher.publish_article(article)

            log.info("✓ Pubblicazione completata: %s", article.slug)

        except Exception as exc:
            log.exception("✗ Pipeline fallita: %s", exc)
            sys.exit(1)


# ============================================================================
# ENTRYPOINT
# ============================================================================

if __name__ == "__main__":
    BlogAgent().run()
