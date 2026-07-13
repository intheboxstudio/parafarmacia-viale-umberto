"""
Blog Agent — Parafarmacia Erboristeria Viale Umberto 1°
=========================================================

Agente AI che il martedì, il giovedì e il sabato alle 10:00 (Europe/Rome):
  1. Scopre un argomento ricercato dalle persone nei settori
     naturopatia, omeopatia, erboristeria, cura del corpo.
  2. Cerca fonti autorevoli sull'argomento.
  3. Genera un articolo originale via Claude API (claude-sonnet-4-6).
  4. Trova un'immagine di copertina coerente su Unsplash (foto stock pro).
  5. Aggiorna articles.json e pubblica via Git push su GitHub.

Variabili d'ambiente richieste:
  - ANTHROPIC_API_KEY    : chiave API Anthropic
  - UNSPLASH_ACCESS_KEY  : Access Key Unsplash (unsplash.com/developers)
  - GITHUB_TOKEN         : personal access token con permessi `repo`
  - GITHUB_REPO          : es. "intheboxstudio/parafarmacia-viale-umberto"
  - GITHUB_BRANCH        : default "main"

Variabili d'ambiente opzionali:
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

# Marchi e prodotti attualmente approvati per i consigli a fine articolo.
# IMPORTANTE: la parafarmacia NON ha tutto il catalogo di ogni marchio, quindi
# l'agente può citare SOLO questi brand e, dove indicato, SOLO questi prodotti
# (o queste linee di prodotti). Altri marchi non presenti qui non vanno mai usati.
#
# Ogni voce di APPROVED_PRODUCTS è:
#   - None                -> l'intero catalogo del brand è disponibile in negozio,
#                            l'agente è libero di scegliere qualsiasi prodotto pertinente.
#   - lista di stringhe    -> whitelist chiusa. Una voce che termina con "*" indica
#                            un'intera LINEA di prodotti (es. "No Dol*" ammette
#                            "No Dol capsule", "No Dol crema", "No Dol cerotti", ecc.);
#                            una voce senza "*" richiede il nome esatto (invariato).
#
# PRODUCT_NOTES contiene, dove utile, brevi indicazioni reali (verificate su siti
# ufficiali/rivenditori) su cosa fa ciascun prodotto o linea, così l'agente scrive
# consigli precisi invece di inventare funzioni plausibili ma sbagliate.
APPROVED_PRODUCTS: dict[str, list[str] | None] = {
    # Reggio Emilia, integratori a base di microalghe (spirulina, chlorella).
    # Catalogo reale (28 referenze) invece di "libero": i nomi sono poco
    # intuitivi (es. "Timeless", "Dream"), quindi l'agente deve pescare da
    # qui e non inventare varianti.
    "Algàdemy": [
        "Màgnesium ADVANCED", "Bròmelina ULTRA", "Shìne", "Mìndful", "Nàtive Skin",
        "Tìmeless", "Flèx Care", "Dàily Nutrients", "Inner Bèauty", "Immùnity",
        "Skìn Defence", "Lèg Relief", "Òsteo Aid", "Drèam", "Làdy", "Astàxantina",
        "Spirulìna PRIME", "Dètox", "Klàmath Multibiotics", "Clorèlla PRIME",
        "Rèlease", "Pòwer", "Pòwer PLUS", "Thèrmo", "Slìm", "Rèlax",
        "Cyst Rèmedy", "Lìpid Balance (Àureum)", "Glùtatione PLUS",
    ],
    "Solime": [
        "RELAX (Passiflora, Valeriana e Biancospino)",
        "Colostrum Gel",
        "Colostrum Reflugel",
        "Gelevital",
        "Colostrum Colluttorio",
        "Colostrum Dentifricio",
        "Remargin Detergente Intimo",
        "Remargin Crema Intima Idratante",
        "Shampoo*", "Balsamo*", "Siero Protettivo*",  # linea capelli completa
    ],
    "Esi": [
        "Omega 3",
        "No Dol*",        # intera linea: dolori articolari e muscolari
        "Le 10 Erbe*",    # intera linea: transito intestinale/digestione
        "Propolaid*",     # intera linea: propoli, difese immunitarie, gola
    ],
    "Farmaderbe": [
        "Bromelina Ananas 5000",
        "Bromelina Drenante Digestivo",
        "Mucolid Bronc*",       # caramelle/granulare per gola e vie respiratorie
        "Beauty Collagene*",    # stick collagene per pelle
        "Boswellia Complex",
    ],
    "Biosnail": [
        "Crema*",  # tutta la linea creme viso/corpo/mani alla bava di lumaca
    ],
    "CeraVe": None,  # catalogo globale noto (ceramidi, tecnologia MVE): libero
    "Florinda Soaps": [
        "Sapone Liquido*",  # sapone liquido mani e corpo
    ],
    "Pool Pharma": [
        "MG K Vis*",  # magnesio, potassio, creatina — stanchezza fisica e mentale
    ],
    "Cetilar": [
        "Cetilar*",  # linea sport: crema muscoli/articolazioni + nutrition da sforzo
    ],
    "Lovrén": None,  # cosmesi viso/corpo made in Italy: libero
    "Natural Salus": [
        "Serenis*",       # gocce rilassanti (passiflora, biancospino, melissa, rodiola)
        "Arnica 30",      # crema-gel 30% arnica per dolori muscolari/articolari
    ],
    "Biokyma": [
        "Tisana*", "Tisane*",  # tutte le tisane della linea
    ],
    "Bromatech": None,  # probiotici (Enterelle, Bifiselle, Ramnoselle...): libero
}

# Marchi presenti in parafarmacia — derivato da APPROVED_PRODUCTS, tenuto
# come lista separata solo per compatibilità con il resto del codice.
PARAFARMACIA_BRANDS = list(APPROVED_PRODUCTS.keys())


def _product_name_allowed(name: str, allowed_names: list[str]) -> str | None:
    """Verifica se `name` rispetta una whitelist che può contenere sia nomi
    esatti sia pattern-linea che terminano con "*" (prefix match). Restituisce
    il nome normalizzato (quello in whitelist) se valido, altrimenti None.
    """
    name_norm = name.strip().lower()
    for allowed in allowed_names:
        if allowed.endswith("*"):
            prefix = allowed[:-1].strip().lower()
            if name_norm.startswith(prefix):
                return name.strip()  # linea libera: teniamo il nome generato
        elif allowed.lower() == name_norm:
            return allowed  # nome esatto: normalizziamo alla forma canonica
    return None


def sanitize_products(products: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Filtra i prodotti generati dal modello mantenendo solo quelli che
    rispettano rigorosamente APPROVED_PRODUCTS (nomi esatti o pattern-linea
    con "*"). Brand con valore None sono a catalogo libero. Prodotti di
    brand non whitelistati, o nomi fuori whitelist, vengono scartati.
    """
    clean: list[dict[str, Any]] = []
    for p in products:
        brand = str(p.get("brand", "")).strip()
        name = str(p.get("name", "")).strip()

        if brand not in APPROVED_PRODUCTS:
            log.warning("Prodotto scartato: brand non approvato %r", brand)
            continue

        allowed_names = APPROVED_PRODUCTS[brand]
        if allowed_names is not None:
            match = _product_name_allowed(name, allowed_names)
            if match is None:
                log.warning(
                    "Prodotto scartato: %r non è nel catalogo approvato per %s", name, brand
                )
                continue
            p = {**p, "name": match}

        clean.append(p)

    return clean


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


# Giorni della settimana in cui l'agente pubblica.
# weekday(): 0=lunedì, 1=martedì, 2=mercoledì, 3=giovedì, 4=venerdì, 5=sabato, 6=domenica
PUBLISH_WEEKDAYS = {1, 3, 5}  # martedì, giovedì, sabato


def can_publish_today() -> tuple[bool, str]:
    """Verifica che oggi sia un giorno valido per pubblicare.

    Restituisce (ok, motivo). Se ok=False, il motivo spiega perché.

    NOTA: NON controlliamo più l'ora esatta. GitHub Actions cron ha
    drift fino a 60 min sotto carico — se pretendessimo "esattamente
    le 10" finiremmo per skippare quasi sempre (è il bug che hai visto
    sui run da 16-34 secondi sempre verdi e mai produttivi).
    Il controllo "giorno della settimana" + "anti-doppione" via
    articles.json sono sufficienti a garantire una sola pubblicazione
    nei giorni voluti.
    """
    if os.getenv("FORCE_RUN", "").lower() in {"1", "true", "yes"}:
        return True, "FORCE_RUN attivo"
    if os.getenv("SKIP_TIME_CHECK", "").lower() in {"1", "true", "yes"}:
        return True, "SKIP_TIME_CHECK attivo"

    now = datetime.now(ROME_TZ)
    if now.weekday() not in PUBLISH_WEEKDAYS:
        days_it = {0: "lunedì", 1: "martedì", 2: "mercoledì",
                   3: "giovedì", 4: "venerdì", 5: "sabato", 6: "domenica"}
        return False, f"oggi è {days_it[now.weekday()]} (pubblichiamo solo mar/gio/sab)"

    return True, "giorno di pubblicazione"


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

- imageKeywords: 2-5 parole chiave in INGLESE per cercare una foto stock professionale su Unsplash. Pensa a parole concrete che un fotografo professionista userebbe come tag per la sua foto. NON usare parole troppo astratte o italiane. Esempi:
  * tisana per dormire → ["herbal tea", "chamomile flowers", "evening relax"]
  * pelle secca → ["skincare routine", "moisturizer cream", "self care"]
  * stress lavoro → ["stressed woman", "office burnout", "tired professional"]
  * vitamina D → ["sunlight window", "yellow capsules", "supplements"]
  * mal di testa → ["tired woman", "headache temple", "migraine relief"]
  Mai usare nomi commerciali, mai "italian" o nomi di brand. Privilegia singoli soggetti chiari su composizioni complesse.

- products: esattamente 3 prodotti, scelti SOLO dal catalogo chiuso qui sotto — non esistono altri marchi o prodotti in negozio, non inventare nulla. Preferisci prodotti realmente pertinenti al topic dell'articolo; se più marchi sono ugualmente pertinenti, varia nella misura del possibile invece di ripetere sempre gli stessi.

  * Algàdemy (Reggio Emilia, integratori a base di microalghe): scegli SOLO tra questi nomi esatti, in base a cosa fanno davvero — Màgnesium ADVANCED (magnesio, stanchezza), Bròmelina ULTRA (drenante, digestione), Shìne (bellezza capelli/pelle/unghie), Mìndful (stress, concentrazione), Nàtive Skin (pelle), Tìmeless (anti-age pelle), Flèx Care (articolazioni), Dàily Nutrients (multivitaminico quotidiano), Inner Bèauty (bellezza dall'interno), Immùnity (difese immunitarie), Skìn Defence (protezione pelle), Lèg Relief (circolazione gambe pesanti), Òsteo Aid (ossa e articolazioni), Drèam (sonno), Làdy (benessere femminile), Astàxantina (antiossidante), Spirulìna PRIME (energia, ricostituente), Dètox (depurativo), Klàmath Multibiotics (probiotici), Clorèlla PRIME (depurativo), Rèlease (tensione, relax muscolare), Pòwer / Pòwer PLUS (energia, sportivi), Thèrmo (metabolismo, termogenico), Slìm (controllo peso), Rèlax (relax, sonno), Cyst Rèmedy (ciclo, ormonale femminile), Lìpid Balance (Àureum) (omega3 vegano, colesterolo), Glùtatione PLUS (antiossidante).
  * Solime: SOLO questi prodotti, nome esatto e invariato — "RELAX (Passiflora, Valeriana e Biancospino)" (rilassante, sonno, stress), "Colostrum Gel" (pelle irritata/danneggiata, herpes, piccole scottature), "Colostrum Reflugel" (reflusso gastrico, bruciore), "Gelevital" (multivitaminico naturale), "Colostrum Colluttorio" (igiene orale), "Colostrum Dentifricio" (igiene orale), "Remargin Detergente Intimo" (igiene intima quotidiana), "Remargin Crema Intima Idratante" (secchezza intima), e la linea Shampoo/Balsamo/Siero Protettivo per capelli (qualsiasi prodotto di questa linea capelli, es. "Shampoo equilibrante Rosmarino e Menta").
  * Esi: "Omega 3" (nome esatto), oppure qualsiasi prodotto delle linee No Dol (dolori articolari e muscolari), Le 10 Erbe (transito intestinale, digestione), Propolaid (propoli, difese immunitarie, gola e vie respiratorie) — per queste tre linee puoi scegliere liberamente il prodotto specifico purché il nome inizi con "No Dol", "Le 10 Erbe" o "Propolaid".
  * Farmaderbe: SOLO questi prodotti, nome esatto e invariato — "Bromelina Ananas 5000" (drenante, digestione, gambe pesanti), "Bromelina Drenante Digestivo" (drenante, gonfiore), "Mucolid Bronc" o varianti (gola, vie respiratorie), "Beauty Collagene" o varianti (collagene per la pelle), "Boswellia Complex" (infiammazione, articolazioni).
  * Biosnail: qualsiasi crema della linea (bava di lumaca — anti-age, idratante, rigenerante, cicatrizzante; viso, corpo o mani), il nome deve iniziare con "Crema".
  * CeraVe: catalogo completo disponibile (ceramidi, tecnologia MVE) — scegli liberamente il prodotto CeraVe più pertinente (es. Crema Idratante, Lozione Idratante, Detergente Idratante, Schiuma Detergente, linea SA, Crema Contorno Occhi, Crema Mani, linea solare).
  * Florinda Soaps: solo il sapone liquido mani e corpo, il nome deve iniziare con "Sapone Liquido".
  * Pool Pharma: solo MG K Vis (magnesio, potassio, creatina — stanchezza fisica e mentale, sudorazione, sport), il nome deve iniziare con "MG K Vis".
  * Cetilar: linea sportivi — crema per muscoli/articolazioni/tendini o prodotti Cetilar Nutrition per lo sforzo fisico, il nome deve iniziare con "Cetilar".
  * Lovrén: catalogo completo disponibile (cosmesi viso/corpo made in Italy) — scegli liberamente il prodotto più pertinente.
  * Natural Salus: solo "Serenis" (gocce rilassanti, ansia, stress — nome deve iniziare con "Serenis") oppure "Arnica 30" (crema-gel 30% arnica, dolori muscolari e articolari, nome esatto).
  * Biokyma: qualsiasi tisana della linea, il nome deve iniziare con "Tisana" o "Tisane".
  * Bromatech: catalogo completo disponibile (probiotici mirati, es. Enterelle, Bifiselle, Ramnoselle) — scegli liberamente il prodotto più pertinente al topic (equilibrio intestinale, difese immunitarie, benessere del microbiota).

  Se il topic dell'articolo non si presta bene a nessuno di questi prodotti, scegli comunque i 3 più vicini possibile — mai forzare marchi o nomi fuori da questa lista. Per ciascuno: brand, name (nel formato indicato sopra), description (max 25 parole, basata su cosa fa davvero il prodotto).

- sources: 2-3 fonti dai domini autorevoli (iss.it, salute.gov.it, aifa.gov.it, humanitas.it, fondazioneveronesi.it, ieo.it, mayoclinic.org, ncbi.nlm.nih.gov, cochranelibrary.com, who.int, examine.com, sciencedirect.com, nature.com, thelancet.com, bmj.com, frontiersin.org, harvard.edu, medlineplus.gov). Per ciascuna: name, url."""

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
                "imageKeywords": {
                    "type": "array",
                    "description": (
                        "2-5 keyword IN INGLESE per cercare la foto di copertina "
                        "su Unsplash. Devono evocare un'immagine fotografica concreta "
                        "coerente col tema dell'articolo. Es: ['herbal tea', 'chamomile'] "
                        "per un articolo sul sonno; ['skincare routine', 'moisturizer'] "
                        "per un articolo sulla pelle."
                    ),
                    "items": {"type": "string"},
                    "minItems": 2,
                    "maxItems": 5
                },
                "products": {
                    "type": "array",
                    "description": (
                        "Esattamente 3 prodotti consigliati, SOLO dal catalogo approvato "
                        "descritto sopra nel system prompt (dettagli per marchio e prodotti "
                        "esatti/linee ammesse). Non citare mai marchi o prodotti fuori da "
                        "questo elenco."
                    ),
                    "items": {
                        "type": "object",
                        "properties": {
                            "brand": {
                                "type": "string",
                                "enum": [
                                    "Algàdemy", "Solime", "Esi", "Farmaderbe", "Biosnail",
                                    "CeraVe", "Florinda Soaps", "Pool Pharma", "Cetilar",
                                    "Lovrén", "Natural Salus", "Biokyma", "Bromatech"
                                ]
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
            "required": ["title", "excerpt", "content", "imageKeywords", "products", "sources"]
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
                    data["products"] = sanitize_products(data.get("products", []))
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
# 4. IMAGE GENERATOR (Unsplash API — foto stock professionali)
# ============================================================================

class ImageGenerator:
    """Cerca un'immagine di copertina su Unsplash basandosi su keyword.

    Strategia: combina le keyword fornite da Claude in una query, cerca su
    Unsplash, prende la foto con più download (proxy della qualità), scarica
    la versione regular (1080px wide), salva in locale. Rispetta i terms of
    use Unsplash chiamando l'endpoint di "track download" come da policy.

    Fallback se Unsplash è giù o non trova foto: SVG placeholder.

    Documentazione API: https://unsplash.com/documentation
    Rate limit free tier: 50 richieste/ora — sovrabbondante per 1 articolo/giorno.
    """

    SEARCH_URL = "https://api.unsplash.com/search/photos"
    DOWNLOAD_TRIGGER_URL = "https://api.unsplash.com/photos/{id}/download"
    TIMEOUT = 30
    PER_PAGE = 15  # Quanti risultati chiedere a Unsplash per ogni search

    def __init__(self, api_key: str | None, output_dir: Path):
        self.access_key = api_key  # Unsplash Access Key
        self.output_dir = output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def generate(self, keywords: list[str], slug: str) -> tuple[str, Path | None]:
        """Cerca, scarica e salva un'immagine da Unsplash.

        Args:
            keywords: lista di parole chiave in inglese (es. ["herbal tea", "chamomile"]).
            slug: identificatore univoco per il filename.

        Returns:
            Tupla (path_per_json, path_locale_o_None). Se fallisce, ritorna
            (placeholder_svg_data_uri, None) come fallback.
        """
        if not self.access_key:
            log.error("UNSPLASH_ACCESS_KEY mancante — uso placeholder SVG")
            return self._placeholder_svg(slug), None

        if not keywords:
            log.warning("Nessuna keyword fornita — uso placeholder SVG")
            return self._placeholder_svg(slug), None

        query = " ".join(keywords).strip()
        log.info("Ricerca Unsplash: %r", query)

        try:
            # 1. Search
            r = requests.get(
                self.SEARCH_URL,
                params={
                    "query": query,
                    "per_page": self.PER_PAGE,
                    "orientation": "landscape",
                    "content_filter": "high",  # Filtro contenuti sicuri
                },
                headers={
                    "Authorization": f"Client-ID {self.access_key}",
                    "Accept-Version": "v1",
                },
                timeout=self.TIMEOUT,
            )
            r.raise_for_status()
            results = r.json().get("results", [])

            if not results:
                # Fallback: prova con la prima keyword soltanto
                if len(keywords) > 1:
                    log.info("Zero risultati per '%s', riprovo con '%s'",
                             query, keywords[0])
                    return self.generate([keywords[0]], slug)
                log.warning("Unsplash: nessuna foto trovata per %r", query)
                return self._placeholder_svg(slug), None

            # 2. Scegli la "migliore": quella con più likes tra le prime 5
            # (le prime 5 sono le più rilevanti; tra queste, ordino per qualità)
            top_candidates = results[:5]
            chosen = max(top_candidates, key=lambda p: p.get("likes", 0))

            photo_id = chosen["id"]
            image_url = chosen["urls"]["regular"]  # ~1080px wide, ottimo per cover
            attribution = (
                chosen.get("user", {}).get("name", "Anonymous"),
                chosen.get("user", {}).get("links", {}).get("html", "")
            )
            log.info("Scelta foto Unsplash id=%s di %s (%d likes)",
                     photo_id, attribution[0], chosen.get("likes", 0))

            # 3. Trigger download endpoint (richiesto dai T&C Unsplash)
            try:
                requests.get(
                    self.DOWNLOAD_TRIGGER_URL.format(id=photo_id),
                    headers={
                        "Authorization": f"Client-ID {self.access_key}",
                        "Accept-Version": "v1",
                    },
                    timeout=10,
                )
            except Exception as exc:
                log.warning("Trigger download Unsplash fallito (non bloccante): %s", exc)

            # 4. Scarica l'immagine vera
            img_resp = requests.get(image_url, timeout=self.TIMEOUT, stream=True)
            img_resp.raise_for_status()
            image_bytes = img_resp.content

            filename = f"{slug}.jpg"
            out_path = self.output_dir / filename
            out_path.write_bytes(image_bytes)
            log.info("Immagine salvata: %s (%d KB) — foto di %s",
                     out_path, len(image_bytes) // 1024, attribution[0])
            return f"./assets/blog/{filename}", out_path

        except Exception as exc:
            log.error("Unsplash error: %s — uso placeholder SVG", exc)
            return self._placeholder_svg(slug), None

    @staticmethod
    def _placeholder_svg(slug: str) -> str:
        """Fallback: SVG decorativo se Unsplash è giù o non trova foto."""
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

    def already_published_today(self) -> bool:
        """Anti-doppione: True se articles.json contiene già un articolo
        con data odierna (Europe/Rome).

        Indispensabile perché il workflow schedula due cron (CEST + CET)
        per coprire il cambio d'ora. Nei giorni in cui entrambi partono,
        questo check fa skippare il secondo run.
        """
        result = self._get_file("articles.json")
        if result is None:
            return False
        content, _sha = result
        try:
            feed = json.loads(content)
        except json.JSONDecodeError:
            log.warning("articles.json non parsabile, procedo come se vuoto")
            return False

        today = datetime.now(ROME_TZ).strftime("%Y-%m-%d")
        for art in feed.get("articles", []):
            art_date = (art.get("date") or "")[:10]
            if art_date == today:
                log.info("Articolo di oggi (%s) già presente: %s",
                         today, art.get("slug", "?"))
                return True
        return False


# ============================================================================
# AGENT ORCHESTRATION
# ============================================================================

class BlogAgent:
    """Orchestra l'intera pipeline di generazione e pubblicazione."""

    def __init__(self) -> None:
        self.anthropic_key = self._require_env("ANTHROPIC_API_KEY")
        self.unsplash_key = self._require_env("UNSPLASH_ACCESS_KEY")
        self.github_token = self._require_env("GITHUB_TOKEN")
        self.github_repo = self._require_env("GITHUB_REPO")
        self.github_branch = os.getenv("GITHUB_BRANCH", "main")
        self.brave_key = os.getenv("BRAVE_SEARCH_API_KEY")

        self.assets_dir = Path("./assets/blog")

        self.discoverer = TopicDiscoverer()
        self.source_finder = SourceFinder(self.brave_key)
        self.generator = ArticleGenerator(self.anthropic_key)
        self.image_gen = ImageGenerator(self.unsplash_key, self.assets_dir)
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

        # Check giorno: pubblichiamo solo martedì/giovedì/sabato.
        ok, reason = can_publish_today()
        if not ok:
            log.info("Skip: %s. Usa FORCE_RUN=true per testare.", reason)
            return

        # Anti-doppione: se l'altro cron del giorno (CEST/CET) ha già
        # pubblicato, abortiamo silenziosamente. In FORCE_RUN bypassiamo
        # questo check così possiamo testare a piacere.
        force_run = os.getenv("FORCE_RUN", "").lower() in {"1", "true", "yes"}
        if not force_run and self.publisher.already_published_today():
            log.info("Articolo di oggi già pubblicato. Skip.")
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
                data.get("imageKeywords", []), article_id
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
