#!/usr/bin/env python3
"""
patch_blog_agent.py
===================

Applica modifiche idempotenti a blog_agent.py:

  1. Sostituisce is_publish_time() con can_publish_today() che:
     - Verifica che oggi sia martedì (1), giovedì (3) o sabato (5)
     - Rimuove il check rigido sull'ora (GitHub Actions cron ha drift
       fino a 60 min: chi pretende che siano "esattamente le 10" si
       autocondanna allo skip silenzioso, come ti è successo finora).
     - Mantiene FORCE_RUN/SKIP_TIME_CHECK per i test manuali.

  2. Aggiunge un metodo anti-doppione su GitPublisher che legge
     articles.json e segnala se c'è già un articolo di oggi.
     Così anche se entrambi i cron (CEST + CET) partono lo stesso
     giorno, solo uno pubblica davvero.

  3. Aggiorna il metodo run() per usare i nuovi controlli.

Uso:
    python patch_blog_agent.py path/to/blog_agent.py

Lo script è idempotente: lanciarlo due volte sullo stesso file non rompe
nulla (riconosce le sue stesse patch già applicate e abortisce).
"""

from __future__ import annotations

import re
import sys
from pathlib import Path


# ─────────────────────────────────────────────────────────────────────────────
# PATCH 1 — Sostituisce is_publish_time() con can_publish_today()
# ─────────────────────────────────────────────────────────────────────────────

OLD_IS_PUBLISH_TIME = '''def is_publish_time() -> bool:
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
    return now.hour == PUBLISH_HOUR'''

NEW_CAN_PUBLISH_TODAY = '''# Giorni della settimana in cui l'agente pubblica.
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

    return True, "giorno di pubblicazione"'''


# ─────────────────────────────────────────────────────────────────────────────
# PATCH 2 — Aggiunge metodo anti-doppione a GitPublisher
#
# Lo iniettiamo subito dopo la chiusura di publish_image (che è l'ultimo
# metodo di GitPublisher). Lo facciamo usando un'ancora testuale unica.
# ─────────────────────────────────────────────────────────────────────────────

ANCHOR_AFTER_PUBLISH_IMAGE = '''        r = requests.put(url, headers=self.headers, json=payload, timeout=30)
        r.raise_for_status()
        log.info("Immagine pubblicata")'''

NEW_METHOD_ALREADY_PUBLISHED = '''        r = requests.put(url, headers=self.headers, json=payload, timeout=30)
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
        return False'''


# ─────────────────────────────────────────────────────────────────────────────
# PATCH 3 — Aggiorna BlogAgent.run() per usare i nuovi controlli
# ─────────────────────────────────────────────────────────────────────────────

OLD_RUN_GUARD = '''        # Check ora: GitHub Actions schedula due cron (8 e 9 UTC) per coprire
        # CET/CEST. Solo l'esecuzione che cade alle 10:00 IT procede.
        if not is_publish_time():
            log.info(
                "Non è l'ora di pubblicare (ora IT: %02d:%02d). Skip silenzioso. "
                "Usa FORCE_RUN=true per testare manualmente.",
                now.hour, now.minute
            )
            return'''

NEW_RUN_GUARD = '''        # Check giorno: pubblichiamo solo martedì/giovedì/sabato.
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
            return'''


# ─────────────────────────────────────────────────────────────────────────────
# Esecuzione
# ─────────────────────────────────────────────────────────────────────────────

def apply_patch(content: str, old: str, new: str, name: str) -> tuple[str, bool]:
    """Applica una patch. Restituisce (nuovo_contenuto, applicata)."""
    if new in content:
        print(f"  ⊝ patch '{name}' già applicata — skip")
        return content, False
    if old not in content:
        print(f"  ✗ patch '{name}' NON applicata: blocco originale non trovato")
        print(f"    (probabilmente blog_agent.py è già stato modificato a mano)")
        return content, False
    new_content = content.replace(old, new, 1)
    print(f"  ✓ patch '{name}' applicata")
    return new_content, True


def main() -> int:
    if len(sys.argv) != 2:
        print("Uso: python patch_blog_agent.py path/to/blog_agent.py")
        return 1

    target = Path(sys.argv[1])
    if not target.exists():
        print(f"File non trovato: {target}")
        return 1

    original = target.read_text(encoding="utf-8")
    backup = target.with_suffix(target.suffix + ".bak")
    backup.write_text(original, encoding="utf-8")
    print(f"Backup salvato in: {backup}")

    content = original
    print("\nApplico patch...")

    content, _ = apply_patch(
        content, OLD_IS_PUBLISH_TIME, NEW_CAN_PUBLISH_TODAY,
        "is_publish_time → can_publish_today"
    )
    content, _ = apply_patch(
        content, ANCHOR_AFTER_PUBLISH_IMAGE, NEW_METHOD_ALREADY_PUBLISHED,
        "GitPublisher.already_published_today"
    )
    content, _ = apply_patch(
        content, OLD_RUN_GUARD, NEW_RUN_GUARD,
        "BlogAgent.run guard"
    )

    if content == original:
        print("\nNessuna modifica applicata.")
        return 0

    target.write_text(content, encoding="utf-8")
    print(f"\n✓ {target} aggiornato.")
    print(f"  (in caso di problemi, ripristina da {backup})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
