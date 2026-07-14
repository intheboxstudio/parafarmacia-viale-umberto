#!/usr/bin/env python3
"""
generate_blog_pages.py
======================
Genera una pagina HTML statica per ogni articolo di articles.json
(cartella blog/<slug>/index.html) + la sitemap.xml del sito.

Perché serve: gli articoli caricati via JavaScript con routing #blog/slug
NON vengono indicizzati da Google. Queste pagine statiche sì.

Come si usa:
    python3 generate_blog_pages.py

Da integrare nel tuo blog_agent.py: chiamalo alla fine di ogni run
(mar/gio/sab), subito dopo aver aggiornato articles.json, così ogni
nuovo articolo ha subito la sua pagina indicizzabile.

    import subprocess
    subprocess.run(["python3", "generate_blog_pages.py"], check=True)

SWITCH-DOMAIN: quando attivi www.parafarmaciaemy.it cambia BASE_URL
qui sotto e rilancia lo script (rigenera tutto in pochi secondi).
"""

import json
import html as html_lib
import re
from pathlib import Path
from datetime import datetime, timezone

# ============================================================
# CONFIGURAZIONE
# ============================================================
BASE_URL = "https://intheboxstudio.github.io/parafarmacia-viale-umberto"
# BASE_URL = "https://www.parafarmaciaemy.it"   # <-- SWITCH-DOMAIN: decommenta questa e commenta quella sopra

SITE_NAME = "Parafarmacia Erboristeria Viale Umberto 1°"
ARTICLES_JSON = Path("articles.json")
OUT_DIR = Path("blog")
SITEMAP = Path("sitemap.xml")

# ============================================================


def strip_tags(text: str) -> str:
    """Rimuove i tag HTML (es. <em>) per usare il testo in <title> e meta."""
    return re.sub(r"<[^>]+>", "", text or "").strip()


def esc(text: str) -> str:
    return html_lib.escape(text or "", quote=True)


PAGE_TEMPLATE = """<!DOCTYPE html>
<html lang="it">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} — {site}</title>
<meta name="description" content="{description}">
<link rel="canonical" href="{canonical}">
<link rel="icon" type="image/png" sizes="48x48" href="{base}/assets/favicon.png">
<meta property="og:type" content="article">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{description}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{og_image}">
<meta property="og:locale" content="it_IT">
<meta name="twitter:card" content="summary_large_image">
<script type="application/ld+json">
{json_ld}
</script>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,300;0,9..144,400;0,9..144,600;1,9..144,400&family=Manrope:wght@400;500;600&display=swap" rel="stylesheet">
<style>
:root {{
  --azzurro-aria: #F2F8FC; --azzurro-deep: #4A88AD; --azzurro-ink: #2E6489;
  --inchiostro: #1F3A4D; --testo: #34526A; --grigio: #6B8090;
}}
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{ font-family: 'Manrope', sans-serif; background: var(--azzurro-aria);
       color: var(--testo); line-height: 1.75; }}
.wrap {{ max-width: 720px; margin: 0 auto; padding: 48px 24px 80px; }}
.back {{ display: inline-block; margin-bottom: 32px; color: var(--azzurro-deep);
        text-decoration: none; font-weight: 600; font-size: 14px; }}
.back:hover {{ text-decoration: underline; }}
.category {{ display: inline-block; font-size: 12px; letter-spacing: .12em;
            text-transform: uppercase; color: var(--azzurro-deep);
            font-weight: 600; margin-bottom: 16px; }}
h1 {{ font-family: 'Fraunces', serif; font-weight: 400; font-size: clamp(30px, 5vw, 42px);
     color: var(--inchiostro); line-height: 1.2; margin-bottom: 12px; }}
h1 em {{ color: var(--azzurro-deep); font-style: italic; }}
.meta {{ font-size: 13px; color: var(--grigio); margin-bottom: 36px; }}
.content h2, .content h3 {{ font-family: 'Fraunces', serif; font-weight: 500;
     color: var(--inchiostro); margin: 36px 0 14px; }}
.content p {{ margin-bottom: 18px; }}
.content ul, .content ol {{ margin: 0 0 18px 22px; }}
.content a {{ color: var(--azzurro-deep); }}
.cta {{ margin-top: 48px; padding: 28px; background: #fff; border-radius: 16px;
       box-shadow: 0 2px 14px rgba(31,58,77,.06); }}
.cta strong {{ color: var(--inchiostro); }}
.cta a {{ color: var(--azzurro-deep); font-weight: 600; text-decoration: none; }}
footer {{ margin-top: 56px; padding-top: 24px; border-top: 1px solid #dbe8f1;
         font-size: 13px; color: var(--grigio); }}
</style>
</head>
<body>
<div class="wrap">
  <a class="back" href="{base}/#blog">&larr; Torna al sito</a>
  <span class="category">{category}</span>
  <h1>{title_html}</h1>
  <div class="meta">{date_human} · {reading_time} di lettura · {site}</div>
  <div class="content">
{content}
  </div>
  <div class="cta">
    <strong>Hai domande su questo argomento?</strong><br>
    Passa a trovarci in Viale Umberto 1°, 17/D a Reggio Emilia,
    chiamaci allo <a href="tel:0522081652">0522&nbsp;081652</a>
    oppure <a href="{base}/#scrivici">scrivici dal sito</a>.
  </div>
  <footer>
    {site} · Viale Umberto 1°, 17/D — 42121 Reggio Emilia ·
    <a href="{base}/#privacy" style="color:inherit;">Privacy &amp; Cookie</a>
  </footer>
</div>
</body>
</html>
"""


def build_json_ld(article: dict, canonical: str, og_image: str) -> str:
    data = {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": strip_tags(article["title"])[:110],
        "description": strip_tags(article.get("excerpt", ""))[:250],
        "datePublished": article.get("date", ""),
        "image": og_image,
        "mainEntityOfPage": canonical,
        "author": {"@type": "Organization", "name": SITE_NAME},
        "publisher": {
            "@type": "Organization",
            "name": SITE_NAME,
            "logo": {"@type": "ImageObject",
                     "url": f"{BASE_URL}/assets/logo-ginkgo-azzurro.png"},
        },
    }
    return json.dumps(data, ensure_ascii=False, indent=2)


def date_human(iso_date: str) -> str:
    months = ["gennaio", "febbraio", "marzo", "aprile", "maggio", "giugno",
              "luglio", "agosto", "settembre", "ottobre", "novembre", "dicembre"]
    try:
        d = datetime.fromisoformat(iso_date)
        return f"{d.day} {months[d.month - 1]} {d.year}"
    except (ValueError, TypeError):
        return ""


def main() -> None:
    if not ARTICLES_JSON.exists():
        raise SystemExit(f"File non trovato: {ARTICLES_JSON} — lancia lo script dalla root del repo.")

    data = json.loads(ARTICLES_JSON.read_text(encoding="utf-8"))
    articles = data.get("articles", [])
    print(f"Trovati {len(articles)} articoli in {ARTICLES_JSON}")

    urls = [(f"{BASE_URL}/", datetime.now(timezone.utc).date().isoformat(), "weekly", "1.0")]

    for art in articles:
        slug = art["slug"]
        canonical = f"{BASE_URL}/blog/{slug}/"
        # immagine: il JSON usa percorsi relativi tipo ./assets/blog/x.jpg
        image_rel = (art.get("image") or "").lstrip("./")
        og_image = f"{BASE_URL}/{image_rel}" if image_rel else f"{BASE_URL}/assets/primus.webp"

        page = PAGE_TEMPLATE.format(
            title=esc(strip_tags(art["title"])),
            title_html=art["title"],  # mantiene gli <em> nel corpo pagina
            site=esc(SITE_NAME),
            description=esc(strip_tags(art.get("excerpt", ""))[:158]),
            canonical=canonical,
            base=BASE_URL,
            og_image=og_image,
            json_ld=build_json_ld(art, canonical, og_image),
            category=esc(art.get("categoryLabel", "")),
            date_human=date_human(art.get("date", "")),
            reading_time=esc(art.get("readingTime", "")),
            content=art.get("content", ""),
        )

        out = OUT_DIR / slug / "index.html"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(page, encoding="utf-8")
        print(f"  ✓ blog/{slug}/index.html")

        lastmod = (art.get("date") or "")[:10]
        urls.append((canonical, lastmod, "monthly", "0.7"))

    # ---- sitemap.xml ----
    entries = "\n".join(
        f"  <url>\n    <loc>{esc(loc)}</loc>\n    <lastmod>{lastmod}</lastmod>\n"
        f"    <changefreq>{freq}</changefreq>\n    <priority>{prio}</priority>\n  </url>"
        for loc, lastmod, freq, prio in urls
    )
    SITEMAP.write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        f"{entries}\n</urlset>\n",
        encoding="utf-8",
    )
    print(f"  ✓ {SITEMAP} ({len(urls)} URL)")
    print("\nFatto. Committa le cartelle blog/ e sitemap.xml insieme ad articles.json.")


if __name__ == "__main__":
    main()
