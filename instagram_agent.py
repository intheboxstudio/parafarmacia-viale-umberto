"""
Instagram Agent — Parafarmacia Erboristeria Viale Umberto 1°
=============================================================

Script che una volta al giorno:
  1. Interroga le API ufficiali Instagram ("Instagram API with Instagram
     Login", endpoint graph.instagram.com) per il profilo
     @parafarmacia.viale.umberto.
  2. Legge gli ultimi post — foto, caroselli e reel — con il loro
     permalink, cioè l'indirizzo del SINGOLO post.
  3. Scarica la foto (o la copertina del reel) dentro assets/instagram/,
     ridimensionata, perché gli URL restituiti da Instagram sono firmati
     e scadono dopo pochi giorni: linkarli direttamente farebbe comparire
     dei riquadri rotti sul sito nel giro di una settimana.
  4. Scrive/aggiorna instagram.json e pubblica tutto via API REST di
     GitHub, con lo stesso meccanismo già usato da reviews_agent.py.
  5. Rinnova il token di accesso (dura 60 giorni) e — se ha i permessi —
     riscrive il GitHub secret con il token nuovo, così la catena non si
     interrompe mai.

Il sito (assets/site.js) legge instagram.json lato client e costruisce la
griglia 3 colonne nella pagina /instagram/. Ogni riquadro linka al proprio
permalink, quindi il click apre quel post specifico e non il profilo.

Variabili d'ambiente richieste:
  - INSTAGRAM_ACCESS_TOKEN : token long-lived del profilo (60 giorni, auto-rinnovato)
  - GITHUB_TOKEN           : stesso PAT già usato da blog_agent.py / reviews_agent.py
  - GITHUB_REPO            : es. "intheboxstudio/parafarmacia-viale-umberto"
  - GITHUB_BRANCH          : default "main"

Variabili opzionali:
  - INSTAGRAM_MAX_POSTS    : quanti post pubblicare (default 12, multiplo di 3)
  - INSTAGRAM_SECRET_NAME  : nome del GitHub secret da aggiornare col token
                             rinnovato (default "INSTAGRAM_ACCESS_TOKEN")

Note importanti:
  - Serve un account Instagram Business o Creator (la conversione è gratuita
    e si fa dall'app). Con un account personale le API non restituiscono i
    media. Vedi LEGGIMI-INSTAGRAM.md per la procedura completa.
  - Le immagini vengono scaricate UNA SOLA VOLTA: al run successivo, se un
    post è già in assets/instagram/, non viene ri-scaricato né ri-committato.
    Quelle dei post usciti dalla griglia vengono cancellate.
  - Le condizioni Meta vietano di conservare i media oltre il necessario a
    mostrarli: la sincronizzazione giornaliera + la cancellazione dei post
    non più in feed rispettano il requisito.

Uso locale (scrive su disco invece che su GitHub, utile per provare):
    python instagram_agent.py --local

Deploy: GitHub Actions, workflow .github/workflows/instagram-agent.yml
(cron giornaliero + esecuzione manuale).
"""

from __future__ import annotations

import base64
import io
import json
import logging
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo

import requests

ROME_TZ = ZoneInfo("Europe/Rome")

GRAPH_BASE = "https://graph.instagram.com"
GRAPH_VERSION = "v21.0"

FEED_FILE = "instagram.json"
MEDIA_DIR = "assets/instagram"

# Quanti post mostrare in griglia. Multiplo di 3 così l'ultima riga è piena.
DEFAULT_MAX_POSTS = 12

# Le tile della griglia sono ~360px al massimo su desktop: 720px di larghezza
# coprono anche gli schermi retina senza appesantire la pagina.
THUMB_WIDTH = 720
THUMB_QUALITY = 82

PROFILE_URL = "https://www.instagram.com/parafarmacia.viale.umberto/"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
log = logging.getLogger("instagram_agent")


# ============================================================================
# 1. FETCH DALLE API INSTAGRAM
# ============================================================================

MEDIA_FIELDS = ",".join([
    "id",
    "caption",
    "media_type",       # IMAGE | VIDEO | CAROUSEL_ALBUM
    "media_url",        # per VIDEO è l'mp4, non l'immagine
    "thumbnail_url",    # presente solo sui VIDEO: è la copertina
    "permalink",        # l'URL del singolo post — quello che ci serve
    "timestamp",
])


def _graph_get(path: str, token: str, **params: Any) -> dict[str, Any]:
    """GET su graph.instagram.com con gestione uniforme degli errori Meta."""
    url = f"{GRAPH_BASE}/{GRAPH_VERSION}/{path.lstrip('/')}"
    params["access_token"] = token
    r = requests.get(url, params=params, timeout=25)

    if r.status_code >= 400:
        # Meta restituisce un JSON con la causa: molto più utile del solo 400.
        try:
            err = r.json().get("error", {})
        except ValueError:
            err = {}
        raise RuntimeError(
            f"Instagram API {r.status_code} su /{path}: "
            f"{err.get('message', r.text[:200])} "
            f"(type={err.get('type')}, code={err.get('code')})"
        )
    return r.json()


def fetch_profile(token: str) -> dict[str, Any]:
    """Dati del profilo collegato al token."""
    log.info("Richiesta profilo a Instagram...")
    data = _graph_get("me", token, fields="id,username,media_count")
    return {
        "username": data.get("username"),
        "mediaCount": data.get("media_count"),
        "profileUrl": (
            f"https://www.instagram.com/{data['username']}/"
            if data.get("username") else PROFILE_URL
        ),
    }


def fetch_media(token: str, limit: int) -> list[dict[str, Any]]:
    """Ultimi post del profilo, dal più recente. Foto, caroselli e reel."""
    log.info("Richiesta ultimi %d media a Instagram...", limit)
    data = _graph_get("me/media", token, fields=MEDIA_FIELDS, limit=limit)
    return data.get("data", [])


def refresh_access_token(token: str) -> tuple[str, int] | None:
    """
    Rinnova il token long-lived (torna a 60 giorni di validità).

    Instagram accetta il rinnovo solo se il token ha almeno 24 ore di vita:
    al primissimo run subito dopo la generazione può quindi fallire. Non è un
    errore bloccante — il feed si aggiorna comunque — quindi restituiamo None
    e proseguiamo.
    """
    try:
        r = requests.get(
            f"{GRAPH_BASE}/refresh_access_token",
            params={"grant_type": "ig_refresh_token", "access_token": token},
            timeout=20,
        )
        r.raise_for_status()
        data = r.json()
        new_token = data.get("access_token")
        expires_in = int(data.get("expires_in", 0))
        if not new_token:
            return None
        log.info("Token rinnovato, valido per altri %d giorni", expires_in // 86400)
        return new_token, expires_in
    except Exception as exc:  # noqa: BLE001 — mai bloccare l'aggiornamento del feed
        log.warning("Rinnovo token non riuscito (non bloccante): %s", exc)
        return None


# ============================================================================
# 2. IMMAGINI
# ============================================================================

def image_url_for(media: dict[str, Any]) -> str | None:
    """
    L'immagine da mostrare in griglia.

    Per i reel/video media_url è il file mp4: la copertina sta in
    thumbnail_url. Per foto e caroselli media_url è già l'immagine
    (nei caroselli, quella della prima slide — come fa Instagram stesso).
    """
    if media.get("media_type") == "VIDEO":
        return media.get("thumbnail_url") or media.get("media_url")
    return media.get("media_url")


def download_thumbnail(url: str) -> bytes:
    """Scarica l'immagine e la rimpicciolisce a THUMB_WIDTH, se Pillow c'è."""
    r = requests.get(url, timeout=40)
    r.raise_for_status()
    raw = r.content

    try:
        from PIL import Image  # import locale: senza Pillow si salva l'originale
    except ImportError:
        log.warning("Pillow non installato: salvo l'immagine a piena risoluzione")
        return raw

    try:
        img = Image.open(io.BytesIO(raw))
        img = img.convert("RGB")
        if img.width > THUMB_WIDTH:
            height = round(img.height * THUMB_WIDTH / img.width)
            img = img.resize((THUMB_WIDTH, height), Image.LANCZOS)
        buf = io.BytesIO()
        img.save(buf, format="JPEG", quality=THUMB_QUALITY, optimize=True, progressive=True)
        return buf.getvalue()
    except Exception as exc:  # noqa: BLE001 — meglio l'originale che nessuna immagine
        log.warning("Ridimensionamento fallito (%s): salvo l'originale", exc)
        return raw


def clean_caption(caption: str | None, max_len: int = 220) -> str:
    """Caption su una riga sola, accorciata: in griglia c'è poco spazio."""
    if not caption:
        return ""
    text = " ".join(caption.split())
    if len(text) <= max_len:
        return text
    return text[:max_len].rsplit(" ", 1)[0].rstrip(" .,;:—-") + "…"


# ============================================================================
# 3. PUBLISHER (GitHub API REST — stesso pattern di reviews_agent.py)
# ============================================================================

class GitPublisher:
    """Aggiorna instagram.json e le immagini, e committa su GitHub via API."""

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

    # ---- lettura -----------------------------------------------------------

    def get_file_sha(self, path: str) -> str | None:
        url = f"{self.api_base}/repos/{self.repo}/contents/{path}?ref={self.branch}"
        r = requests.get(url, headers=self.headers, timeout=15)
        if r.status_code == 404:
            return None
        r.raise_for_status()
        return r.json()["sha"]

    def list_dir(self, path: str) -> dict[str, str]:
        """{nome_file: sha} del contenuto di una cartella. {} se non esiste."""
        url = f"{self.api_base}/repos/{self.repo}/contents/{path}?ref={self.branch}"
        r = requests.get(url, headers=self.headers, timeout=15)
        if r.status_code == 404:
            return {}
        r.raise_for_status()
        entries = r.json()
        if not isinstance(entries, list):
            return {}
        return {e["name"]: e["sha"] for e in entries if e.get("type") == "file"}

    # ---- scrittura ---------------------------------------------------------

    def put_bytes(self, path: str, content: bytes, sha: str | None, message: str) -> None:
        url = f"{self.api_base}/repos/{self.repo}/contents/{path}"
        payload: dict[str, Any] = {
            "message": message,
            "content": base64.b64encode(content).decode("ascii"),
            "branch": self.branch,
        }
        if sha:
            payload["sha"] = sha
        r = requests.put(url, headers=self.headers, json=payload, timeout=60)
        r.raise_for_status()

    def put_text(self, path: str, content: str, sha: str | None, message: str) -> None:
        self.put_bytes(path, content.encode("utf-8"), sha, message)

    def delete_file(self, path: str, sha: str, message: str) -> None:
        url = f"{self.api_base}/repos/{self.repo}/contents/{path}"
        r = requests.delete(
            url,
            headers=self.headers,
            json={"message": message, "sha": sha, "branch": self.branch},
            timeout=20,
        )
        r.raise_for_status()


class LocalPublisher:
    """Stessa interfaccia di GitPublisher, ma scrive sul filesystem locale."""

    def __init__(self, root: Path):
        self.root = root

    def get_file_sha(self, path: str) -> str | None:
        return "local" if (self.root / path).exists() else None

    def list_dir(self, path: str) -> dict[str, str]:
        d = self.root / path
        if not d.is_dir():
            return {}
        return {p.name: "local" for p in d.iterdir() if p.is_file()}

    def put_bytes(self, path: str, content: bytes, sha: str | None, message: str) -> None:
        target = self.root / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(content)

    def put_text(self, path: str, content: str, sha: str | None, message: str) -> None:
        self.put_bytes(path, content.encode("utf-8"), sha, message)

    def delete_file(self, path: str, sha: str, message: str) -> None:
        (self.root / path).unlink(missing_ok=True)


# ============================================================================
# 4. AGGIORNAMENTO DEL SECRET COL TOKEN RINNOVATO
# ============================================================================

def update_github_secret(repo: str, gh_token: str, name: str, value: str) -> bool:
    """
    Riscrive un GitHub Actions secret col token appena rinnovato.

    Richiede PyNaCl (per cifrare il valore con la chiave pubblica del repo) e
    un PAT con permesso di scrittura sui secrets. Se manca l'uno o l'altro non
    è un problema immediato: il feed continua ad aggiornarsi, ma il token
    scadrà dopo 60 giorni e andrà rigenerato a mano. Per questo la mancata
    scrittura viene loggata come WARNING ben visibile.
    """
    try:
        from nacl import encoding, public
    except ImportError:
        log.warning(
            "PyNaCl non installato: secret %s NON aggiornato. "
            "Il token scadrà tra 60 giorni.", name,
        )
        return False

    headers = {
        "Authorization": f"Bearer {gh_token}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    base = f"https://api.github.com/repos/{repo}/actions/secrets"

    try:
        r = requests.get(f"{base}/public-key", headers=headers, timeout=15)
        r.raise_for_status()
        key_data = r.json()

        sealed = public.SealedBox(
            public.PublicKey(key_data["key"].encode("utf-8"), encoding.Base64Encoder())
        ).encrypt(value.encode("utf-8"))

        r = requests.put(
            f"{base}/{name}",
            headers=headers,
            json={
                "encrypted_value": base64.b64encode(sealed).decode("utf-8"),
                "key_id": key_data["key_id"],
            },
            timeout=15,
        )
        r.raise_for_status()
        log.info("Secret %s aggiornato col token rinnovato", name)
        return True
    except Exception as exc:  # noqa: BLE001
        log.warning(
            "Impossibile aggiornare il secret %s (%s). Il token scadrà tra 60 "
            "giorni: serve un PAT con permesso 'Secrets: read and write'.",
            name, exc,
        )
        return False


# ============================================================================
# 5. SINCRONIZZAZIONE
# ============================================================================

def sync(publisher: GitPublisher | LocalPublisher, token: str, max_posts: int) -> int:
    """Scarica il feed, aggiorna immagini e instagram.json. Torna il n. di post."""
    profile = fetch_profile(token)
    media = fetch_media(token, max_posts)
    log.info("Ricevuti %d media dal profilo @%s", len(media), profile.get("username"))

    existing = publisher.list_dir(MEDIA_DIR)
    today = datetime.now(ROME_TZ).strftime("%Y-%m-%d")

    posts: list[dict[str, Any]] = []
    keep: set[str] = set()

    for item in media:
        src = image_url_for(item)
        if not src:
            log.warning("Media %s senza immagine utilizzabile, saltato", item.get("id"))
            continue

        filename = f"{item['id']}.jpg"
        keep.add(filename)

        # Le immagini dei post non cambiano mai: se ce l'abbiamo già, non la
        # riscarichiamo. Così ogni foto entra nel repo una volta sola.
        if filename not in existing:
            log.info("Nuovo post %s (%s): scarico l'immagine", item["id"], item["media_type"])
            try:
                data = download_thumbnail(src)
            except Exception as exc:  # noqa: BLE001
                log.warning("Download immagine fallito per %s (%s), post saltato", item["id"], exc)
                continue
            publisher.put_bytes(
                f"{MEDIA_DIR}/{filename}", data, None,
                f"instagram: immagine post {item['id']} ({today})",
            )

        caption = clean_caption(item.get("caption"))
        posts.append({
            "id": item["id"],
            "type": item.get("media_type", "IMAGE"),
            "permalink": item.get("permalink"),
            "image": f"/{MEDIA_DIR}/{filename}",
            "caption": caption,
            "alt": caption[:120] if caption else "Post Instagram della Parafarmacia Erboristeria Viale Umberto 1°",
            "timestamp": item.get("timestamp"),
        })

    # Immagini di post non più in griglia: via, non servono più a nessuno.
    for name, sha in existing.items():
        if name not in keep:
            log.info("Post non più in feed: rimuovo %s", name)
            publisher.delete_file(
                f"{MEDIA_DIR}/{name}", sha,
                f"instagram: rimozione immagine non più in feed ({today})",
            )

    feed = {
        "lastUpdated": datetime.now(ROME_TZ).isoformat(),
        "_comment": (
            "File generato e aggiornato automaticamente da instagram_agent.py "
            "una volta al giorno. NON modificare manualmente, le modifiche "
            "andranno perse al prossimo run."
        ),
        "profile": profile,
        "posts": posts,
    }

    publisher.put_text(
        FEED_FILE,
        json.dumps(feed, ensure_ascii=False, indent=2),
        publisher.get_file_sha(FEED_FILE),
        f"instagram: aggiornamento feed profilo ({today})",
    )
    log.info("%s aggiornato con %d post", FEED_FILE, len(posts))
    return len(posts)


# ============================================================================
# ENTRYPOINT
# ============================================================================

def main() -> None:
    local_mode = "--local" in sys.argv

    ig_token = os.environ.get("INSTAGRAM_ACCESS_TOKEN")
    gh_token = os.environ.get("GITHUB_TOKEN")
    gh_repo = os.environ.get("GITHUB_REPO")
    gh_branch = os.environ.get("GITHUB_BRANCH", "main")
    secret_name = os.environ.get("INSTAGRAM_SECRET_NAME", "INSTAGRAM_ACCESS_TOKEN")

    try:
        max_posts = int(os.environ.get("INSTAGRAM_MAX_POSTS", DEFAULT_MAX_POSTS))
    except ValueError:
        max_posts = DEFAULT_MAX_POSTS

    required = [("INSTAGRAM_ACCESS_TOKEN", ig_token)]
    if not local_mode:
        required += [("GITHUB_TOKEN", gh_token), ("GITHUB_REPO", gh_repo)]

    missing = [name for name, val in required if not val]
    if missing:
        log.error("Variabili d'ambiente mancanti: %s", ", ".join(missing))
        sys.exit(1)

    publisher: GitPublisher | LocalPublisher
    if local_mode:
        publisher = LocalPublisher(Path(__file__).resolve().parent)
        log.info("Modalità --local: scrivo sul filesystem, nessun commit su GitHub")
    else:
        publisher = GitPublisher(gh_token, gh_repo, gh_branch)

    try:
        count = sync(publisher, ig_token, max_posts)

        # Il rinnovo va fatto DOPO la sincronizzazione: se fallisse, il feed
        # di oggi è già stato pubblicato.
        refreshed = refresh_access_token(ig_token)
        if refreshed and not local_mode:
            update_github_secret(gh_repo, gh_token, secret_name, refreshed[0])

        log.info("✓ Aggiornamento Instagram completato (%d post in griglia)", count)

    except Exception as exc:
        log.exception("✗ Aggiornamento Instagram fallito: %s", exc)
        sys.exit(1)


if __name__ == "__main__":
    main()
