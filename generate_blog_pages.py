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

Serve a rigenerare tutto in blocco (es. dopo aver cambiato il template o
per recuperare articoli rimasti indietro). Nel funzionamento normale non
va lanciato a mano: blog_agent.py importa render_article_page() e
build_sitemap() da qui e pubblica pagina e sitemap su GitHub subito dopo
articles.json, dentro lo stesso run.

Perché l'agente importa le funzioni invece di lanciare questo script:
blog_agent.py aggiorna articles.json via API REST di GitHub, non nella
copia di lavoro. Nel runner di Actions il file su disco resta quello
vecchio, quindi uno `subprocess.run` qui rigenererebbe le pagine SENZA
l'articolo appena pubblicato. Le funzioni invece lavorano sui dati in
memoria, quelli giusti.

BASE_URL e SITE_NAME vivono in site_config.py, condivisi con
generate_pages.py — per cambiare dominio basta aggiornare quel file.
Il sitemap.xml generato qui include anche le pagine principali del sito
(vedi PAGES in generate_pages.py), non solo gli articoli del blog.
"""

import json
import html as html_lib
import re
from pathlib import Path
from datetime import datetime, timezone

from site_config import BASE_URL, SITE_NAME
from generate_pages import PAGES as SITE_PAGES

# ============================================================
# CONFIGURAZIONE
# ============================================================
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
<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-JS9H2L4VD5"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){{dataLayer.push(arguments);}}
  gtag('js', new Date());

  gtag('config', 'G-JS9H2L4VD5');
</script>

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
  <a class="back" href="{base}/blog/">&larr; Torna al sito</a>
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
    oppure <a href="{base}/scrivici/">scrivici dal sito</a>.
  </div>
  <footer>
    {site} · Viale Umberto 1°, 17/D — 42121 Reggio Emilia ·
    <a href="{base}/privacy/" style="color:inherit;">Privacy &amp; Cookie</a>
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


def article_path(article: dict) -> str:
    """Percorso della pagina dell'articolo, relativo alla root del repo."""
    return f"{OUT_DIR.as_posix()}/{article['slug']}/index.html"


def render_article_page(article: dict) -> str:
    """
    L'HTML completo della pagina di un articolo.

    Usata sia da main() (scrittura su disco) sia da blog_agent.py, che la
    pubblica su GitHub via API: il template resta uno solo.
    """
    canonical = f"{BASE_URL}/blog/{article['slug']}/"
    # immagine: il JSON usa percorsi relativi tipo ./assets/blog/x.jpg
    image_rel = (article.get("image") or "").lstrip("./")
    og_image = f"{BASE_URL}/{image_rel}" if image_rel else f"{BASE_URL}/assets/primus.webp"

    return PAGE_TEMPLATE.format(
        title=esc(strip_tags(article["title"])),
        title_html=article["title"],  # mantiene gli <em> nel corpo pagina
        site=esc(SITE_NAME),
        description=esc(strip_tags(article.get("excerpt", ""))[:158]),
        canonical=canonical,
        base=BASE_URL,
        og_image=og_image,
        json_ld=build_json_ld(article, canonical, og_image),
        category=esc(article.get("categoryLabel", "")),
        date_human=date_human(article.get("date", "")),
        reading_time=esc(article.get("readingTime", "")),
        content=article.get("content", ""),
    )


def build_sitemap(articles: list[dict]) -> str:
    """La sitemap completa: pagine principali del sito + articoli del blog."""
    today = datetime.now(timezone.utc).date().isoformat()
    urls = [
        (f"{BASE_URL}/{slug + '/' if slug else ''}", today,
         "weekly" if slug == "" else "monthly", "1.0" if slug == "" else "0.8")
        for slug, _title, _description in SITE_PAGES
    ]
    urls += [
        (f"{BASE_URL}/blog/{art['slug']}/", (art.get("date") or "")[:10], "monthly", "0.7")
        for art in articles
    ]

    entries = "\n".join(
        f"  <url>\n    <loc>{esc(loc)}</loc>\n    <lastmod>{lastmod}</lastmod>\n"
        f"    <changefreq>{freq}</changefreq>\n    <priority>{prio}</priority>\n  </url>"
        for loc, lastmod, freq, prio in urls
    )
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        f"{entries}\n</urlset>\n"
    )


def main() -> None:
    if not ARTICLES_JSON.exists():
        raise SystemExit(f"File non trovato: {ARTICLES_JSON} — lancia lo script dalla root del repo.")

    data = json.loads(ARTICLES_JSON.read_text(encoding="utf-8"))
    articles = data.get("articles", [])
    print(f"Trovati {len(articles)} articoli in {ARTICLES_JSON}")

    for art in articles:
        out = Path(article_path(art))
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(render_article_page(art), encoding="utf-8")
        print(f"  ✓ {out.as_posix()}")

    sitemap = build_sitemap(articles)
    SITEMAP.write_text(sitemap, encoding="utf-8")
    print(f"  ✓ {SITEMAP} ({sitemap.count('<url>')} URL)")
    print("\nFatto. Committa le cartelle blog/ e sitemap.xml insieme ad articles.json.")


if __name__ == "__main__":
    main()
