"""
Reviews Agent — Parafarmacia Erboristeria Viale Umberto 1°
=============================================================

Script che una volta al giorno:
  1. Interroga la Google Places API (Place Details) per la scheda
     Google Business della parafarmacia.
  2. Legge valutazione media, numero totale di recensioni e le
     recensioni restituite da Google (fino a un massimo di 5 — è un
     limite dell'API stessa, non del nostro codice).
  3. Scrive/aggiorna reviews.json e lo pubblica via Git push su GitHub,
     con lo stesso meccanismo (API REST di GitHub) già usato da
     blog_agent.py per articles.json.

Il sito (index.html) legge reviews.json lato client e mostra le
recensioni nella sezione "Cosa dicono di noi" in fondo alla home page.

Variabili d'ambiente richieste:
  - GOOGLE_PLACES_API_KEY : chiave API Google Cloud con "Places API" abilitata
  - GOOGLE_PLACE_ID       : Place ID della parafarmacia su Google Maps
  - GITHUB_TOKEN          : stesso PAT già usato da blog_agent.py (repo)
  - GITHUB_REPO           : es. "intheboxstudio/parafarmacia-viale-umberto"
  - GITHUB_BRANCH         : default "main"

Note importanti:
  - L'API Google Places restituisce SOLO fino a 5 recensioni per scheda,
    scelte da Google (non tutte quelle esistenti). È un limite noto e
    documentato dell'API, non aggirabile senza servizi terzi a pagamento.
  - Le linee guida di Google richiedono di mostrare l'attribuzione
    "Recensioni da Google" con link alla scheda quando si visualizzano
    questi dati: il markup già pronto in index.html lo fa.
  - Le condizioni di Google richiedono di non conservare i dati delle
    recensioni per più di 30 giorni senza un refresh: la schedulazione
    giornaliera di questo script rispetta ampiamente il limite.

Deploy: GitHub Actions, workflow .github/workflows/reviews-agent.yml
(cron giornaliero + esecuzione manuale).
"""

from __future__ import annotations

import base64
import json
import logging
import os
import sys
from datetime import datetime
from typing import Any
from zoneinfo import ZoneInfo

import requests

ROME_TZ = ZoneInfo("Europe/Rome")
PLACE_DETAILS_URL = "https://maps.googleapis.com/maps/api/place/details/json"
REVIEWS_FILE = "reviews.json"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
log = logging.getLogger("reviews_agent")


# ============================================================================
# 1. FETCH DA GOOGLE PLACES API
# ============================================================================

def fetch_reviews(api_key: str, place_id: str) -> dict[str, Any]:
    """Chiama Place Details e restituisce i campi utili per il sito."""
    params = {
        "place_id": place_id,
        "fields": "name,rating,user_ratings_total,reviews,url",
        "language": "it",
        "reviews_no_translations": "true",
        "key": api_key,
    }
    log.info("Richiesta Place Details a Google...")
    r = requests.get(PLACE_DETAILS_URL, params=params, timeout=20)
    r.raise_for_status()
    data = r.json()

    if data.get("status") != "OK":
        raise RuntimeError(
            f"Google Places API status={data.get('status')} "
            f"error_message={data.get('error_message')!r}"
        )

    result = data["result"]
    reviews = []
    for rv in result.get("reviews", []):
        reviews.append({
            "author": rv.get("author_name", "Cliente Google"),
            "authorPhoto": rv.get("profile_photo_url"),
            "authorUrl": rv.get("author_url"),
            "rating": rv.get("rating"),
            "relativeTime": rv.get("relative_time_description"),
            "text": rv.get("text", "").strip(),
            "time": rv.get("time"),  # unix timestamp, utile per ordinare
        })

    # Più recenti prima
    reviews.sort(key=lambda r: r.get("time") or 0, reverse=True)

    return {
        "placeName": result.get("name"),
        "rating": result.get("rating"),
        "userRatingsTotal": result.get("user_ratings_total"),
        "mapsUrl": result.get("url"),
        "reviews": reviews,
    }


# ============================================================================
# 2. PUBLISHER (Git push su GitHub — stesso pattern di blog_agent.py)
# ============================================================================

class GitPublisher:
    """Aggiorna reviews.json e committa su GitHub via API REST."""

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
        url = f"{self.api_base}/repos/{self.repo}/contents/{path}?ref={self.branch}"
        r = requests.get(url, headers=self.headers, timeout=15)
        if r.status_code == 404:
            return None
        r.raise_for_status()
        data = r.json()
        content = base64.b64decode(data["content"]).decode("utf-8")
        return content, data["sha"]

    def _put_file(self, path: str, content: str, sha: str | None, message: str) -> None:
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

    def publish_reviews(self, payload: dict[str, Any]) -> None:
        log.info("Pubblicazione reviews.json su GitHub...")
        existing = self._get_file(REVIEWS_FILE)
        sha = existing[1] if existing else None

        feed = {
            "$schema": "https://parafarmacia-viale-umberto.it/reviews/schema.json",
            "lastUpdated": datetime.now(ROME_TZ).isoformat(),
            "_comment": (
                "File generato e aggiornato automaticamente da reviews_agent.py "
                "una volta al giorno. NON modificare manualmente, le modifiche "
                "andranno perse al prossimo run."
            ),
            **payload,
        }

        new_content = json.dumps(feed, ensure_ascii=False, indent=2)
        commit_msg = f"reviews: aggiornamento recensioni Google ({datetime.now(ROME_TZ).strftime('%Y-%m-%d')})"
        self._put_file(REVIEWS_FILE, new_content, sha, commit_msg)
        log.info("reviews.json aggiornato su GitHub")


# ============================================================================
# ENTRYPOINT
# ============================================================================

def main() -> None:
    api_key = os.environ.get("GOOGLE_PLACES_API_KEY")
    place_id = os.environ.get("GOOGLE_PLACE_ID")
    gh_token = os.environ.get("GITHUB_TOKEN")
    gh_repo = os.environ.get("GITHUB_REPO")
    gh_branch = os.environ.get("GITHUB_BRANCH", "main")

    missing = [
        name for name, val in [
            ("GOOGLE_PLACES_API_KEY", api_key),
            ("GOOGLE_PLACE_ID", place_id),
            ("GITHUB_TOKEN", gh_token),
            ("GITHUB_REPO", gh_repo),
        ] if not val
    ]
    if missing:
        log.error("Variabili d'ambiente mancanti: %s", ", ".join(missing))
        sys.exit(1)

    try:
        payload = fetch_reviews(api_key, place_id)
        log.info(
            "Trovate %d recensioni (rating medio %.1f su %d totali)",
            len(payload["reviews"]), payload.get("rating") or 0,
            payload.get("userRatingsTotal") or 0,
        )

        publisher = GitPublisher(gh_token, gh_repo, gh_branch)
        publisher.publish_reviews(payload)

        log.info("✓ Aggiornamento recensioni completato")

    except Exception as exc:
        log.exception("✗ Aggiornamento recensioni fallito: %s", exc)
        sys.exit(1)


if __name__ == "__main__":
    main()
