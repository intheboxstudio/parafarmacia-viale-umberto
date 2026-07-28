#!/usr/bin/env python3
"""
generate_pages.py
==================
Genera una cartella fisica indicizzabile per ognuna delle pagine principali
del sito (servizi/, tisane/, primus/, blog/, instagram/, contatti/,
scrivici/, privacy/, fitoterapia/, erboristeria/, cosmesi/, omeopatia/) più
la home (index.html), ognuna con il proprio <title>, <meta description>,
canonical, Open Graph e JSON-LD.

Perché serve: il sito è una SPA — tutte le pagine sono nello stesso
index.html e vengono mostrate/nascoste da JavaScript in base all'URL.
Google vedeva quindi sempre lo stesso title/description, qualunque pagina
fosse in realtà. Lo stesso identico problema era già stato risolto per gli
articoli del blog da generate_blog_pages.py — questo script applica lo
stesso schema alle pagine principali.

Come funziona: index.html resta la sorgente di verità per il contenuto
(il <body> — nav, tutte le sezioni .page, footer — è identico su ogni
pagina generata: è assets/site.js, non questo script, a rendere attiva
la sezione giusta in base al path). Questo script legge quel <body> da
index.html e lo re-incapsula in un <head> diverso per ogni pagina.

Come si usa:
    python3 generate_pages.py

Da rilanciare ogni volta che cambia il <body> di index.html (nuova
sezione, nuovo pillar, nuovo testo) o l'elenco PAGES qui sotto. Le due
liste sotto (qui e in assets/site.js → PAGE_META) devono restare
allineate: qui generano il primo caricamento server-side, in site.js
aggiornano document.title durante la navigazione client-side.
"""

import html as html_lib
import re
from pathlib import Path

from site_config import BASE_URL, SITE_NAME


def esc(text: str) -> str:
    return html_lib.escape(text or "", quote=True)

INDEX_HTML = Path("index.html")
SITE_TITLE_SUFFIX = f" — {SITE_NAME}"

# (slug, title, description) — slug "" = home.
PAGES = [
    ("", "Parafarmacia Emy — Erboristeria e Omeopatia a Reggio Emilia, Viale Umberto 1°",
        "Parafarmacia Emy – Parafarmacia Erboristeria in Viale Umberto 1°, Reggio Emilia (Reggio nell'Emilia). "
        "Fitoterapia, erboristeria, cosmesi, omeopatia. Tisane artigianali, nutrizionista e naturopatia a Reggio "
        "Emilia, farmacista cosmetologa, punto vendita Pane Primus e stanze per consulenze su appuntamento."),
    ("servizi", "Nutrizionista e Naturopatia a Reggio Emilia — Servizi" + SITE_TITLE_SUFFIX,
        "Nutrizionista e naturopatia a Reggio Emilia (Reggio nell'Emilia), in Parafarmacia Viale Umberto 1°: "
        "consulenze su appuntamento per alimentazione, benessere naturale e cosmesi. Due stanze attrezzate per "
        "professionisti del settore."),
    ("tisane", "Le Tisane della Dottoressa Emy" + SITE_TITLE_SUFFIX,
        "Miscele artigianali composte a mano in negozio, mai online: ingredienti selezionati uno a uno. Scopri la "
        "storia e gli ingredienti delle Tisane della Dottoressa Emy."),
    ("primus", "Pane Primus — Punto Vendita Ufficiale" + SITE_TITLE_SUFFIX,
        "Uno dei pochi punti vendita ufficiali del Pane Primus a Reggio Emilia: grano a basso indice glicemico, "
        "lievito madre, fermentazione lunga oltre 24h. Prenota il tuo pane."),
    ("blog", "Blog: Consigli di Erboristeria, Omeopatia e Naturopatia" + SITE_TITLE_SUFFIX,
        "Un articolo nuovo martedì, giovedì e sabato: erboristeria, omeopatia, naturopatia e cura del corpo, a cura "
        "della Parafarmacia Viale Umberto 1° di Reggio Emilia."),
    ("instagram", "Instagram — @parafarmacia.viale.umberto" + SITE_TITLE_SUFFIX,
        "Segui la Parafarmacia Erboristeria Viale Umberto 1° su Instagram: consigli, novità e tisane della "
        "Dottoressa Emy, da Reggio Emilia."),
    ("contatti", "Dove Trovarci — Orari e Indirizzo" + SITE_TITLE_SUFFIX,
        "Viale Umberto 1°, 17/D a Reggio Emilia. Orari di apertura, telefono, email e indicazioni per raggiungerci. "
        "Aperti dal lunedì al sabato."),
    ("scrivici", "Scrivici un Messaggio" + SITE_TITLE_SUFFIX,
        "Scrivi alla Parafarmacia Viale Umberto 1° di Reggio Emilia: risposta personale entro 24 ore, per "
        "consulenze, prenotazioni o informazioni sui prodotti."),
    ("privacy", "Privacy & Cookie" + SITE_TITLE_SUFFIX,
        "Informativa sul trattamento dei dati personali ai sensi del Regolamento (UE) 2016/679 (GDPR) e della "
        "normativa italiana vigente."),
    ("fitoterapia", "Fitoterapia: Storia, Metodo e Cosa Dice la Scienza" + SITE_TITLE_SUFFIX,
        "Dalle prime farmacopee vegetali alla ricerca clinica di oggi: cos'è la fitoterapia, cos'è il fitocomplesso "
        "e cosa dice davvero la scienza, spiegato con onestà."),
    ("erboristeria", "Erboristeria a Reggio Emilia — Storia di un Mestiere Antico" + SITE_TITLE_SUFFIX,
        "Erboristeria a Reggio Emilia (Reggio nell'Emilia), in Viale Umberto 1°: storia, normativa italiana e "
        "metodi di preparazione (infuso, decotto, macerato), spiegati con chiarezza."),
    ("cosmesi", "Cosmesi: Come Nasce (e si Legge) un Prodotto Sicuro" + SITE_TITLE_SUFFIX,
        "Dalle argille dell'Antico Egitto agli INCI di oggi: come nasce un cosmetico sicuro, i principi attivi più "
        "richiesti e come sceglierlo davvero."),
    ("omeopatia", "Omeopatia a Reggio Emilia — Origini e Dibattito Scientifico" + SITE_TITLE_SUFFIX,
        "Omeopatia a Reggio Emilia (Reggio nell'Emilia), in Parafarmacia Viale Umberto 1°: Samuel Hahnemann, il "
        "principio del simile, come si preparano i rimedi e cosa dice oggi la scienza, spiegato con chiarezza."),
]

HEAD_TEMPLATE = """<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-JS9H2L4VD5"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){{dataLayer.push(arguments);}}
  gtag('js', new Date());

  gtag('config', 'G-JS9H2L4VD5');
</script>

<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<meta name="description" content="{description}" />
<title>{title}</title>
<link rel="canonical" href="{canonical}" />

<!-- ===== ANTEPRIMA LINK (WhatsApp / Facebook / social) ===== -->
<meta property="og:type" content="website" />
<meta property="og:site_name" content="{site_name}" />
<meta property="og:title" content="{title}" />
<meta property="og:description" content="{description}" />
<meta property="og:url" content="{canonical}" />
<meta property="og:image" content="{base}/assets/og-image.png" />
<meta property="og:image:width" content="1200" />
<meta property="og:image:height" content="630" />
<meta property="og:image:type" content="image/png" />
<meta property="og:locale" content="it_IT" />
<meta name="twitter:card" content="summary_large_image" />
<meta name="twitter:title" content="{title}" />
<meta name="twitter:image" content="{base}/assets/og-image.png" />
<script type="application/ld+json">
{json_ld}
</script>

<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,300;0,9..144,400;0,9..144,500;0,9..144,600;0,9..144,700;1,9..144,300;1,9..144,400&family=Manrope:wght@300;400;500;600;700&display=swap" rel="stylesheet">

<link rel="stylesheet" href="/assets/site.css">
"""

PAGE_HTML = """<!DOCTYPE html>
<html lang="it">
<head>
{head}</head>
<body>
{body}</body>
</html>
"""

ORG_JSON_LD = {
    "@context": "https://schema.org",
    "@type": "Pharmacy",
    "name": SITE_NAME,
    "alternateName": ["Parafarmacia Emy", "Parafarmacia Viale Umberto"],
    "url": BASE_URL + "/",
    "telephone": "+39 0522 081652",
    "email": "parafarmaciavialeumberto@gmail.com",
    "areaServed": {
        "@type": "City",
        "name": "Reggio Emilia",
    },
    "sameAs": [
        "https://www.instagram.com/parafarmacia.viale.umberto/",
    ],
    "address": {
        "@type": "PostalAddress",
        "streetAddress": "Viale Umberto 1°, 17/D",
        "addressLocality": "Reggio Emilia",
        "postalCode": "42121",
        "addressRegion": "RE",
        "addressCountry": "IT",
    },
    "openingHoursSpecification": [
        {
            "@type": "OpeningHoursSpecification",
            "dayOfWeek": day,
            "opens": "09:00",
            "closes": "13:00",
        }
        for day in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
    ] + [
        {
            "@type": "OpeningHoursSpecification",
            "dayOfWeek": day,
            "opens": "15:30",
            "closes": "19:30",
        }
        for day in ["Monday", "Tuesday", "Wednesday", "Friday", "Saturday"]
    ],
}


def build_json_ld(slug: str, title: str, description: str, canonical: str) -> str:
    import json

    if slug == "":
        data = ORG_JSON_LD
    else:
        data = {
            "@context": "https://schema.org",
            "@type": "WebPage",
            "name": title,
            "description": description,
            "url": canonical,
            "isPartOf": {"@type": "WebSite", "name": SITE_NAME, "url": BASE_URL + "/"},
        }
    return json.dumps(data, ensure_ascii=False, indent=2)


def extract_body(html: str) -> str:
    m = re.search(r"<body>\n(.*)</body>\n", html, re.DOTALL)
    if not m:
        raise SystemExit("Impossibile trovare <body>...</body> in index.html")
    return m.group(1)


def main() -> None:
    if not INDEX_HTML.exists():
        raise SystemExit(f"File non trovato: {INDEX_HTML} — lancia lo script dalla root del repo.")

    html = INDEX_HTML.read_text(encoding="utf-8")
    body = extract_body(html)

    for slug, title, description in PAGES:
        canonical = f"{BASE_URL}/{slug + '/' if slug else ''}"
        head = HEAD_TEMPLATE.format(
            description=esc(description),
            title=esc(title),
            canonical=canonical,
            site_name=esc(SITE_NAME),
            base=BASE_URL,
            json_ld=build_json_ld(slug, title, description, canonical),
        )
        page = PAGE_HTML.format(head=head, body=body)

        out = Path(slug) / "index.html" if slug else INDEX_HTML
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(page, encoding="utf-8")
        print(f"  ✓ {out.as_posix()}")

    print(f"\nGenerate {len(PAGES)} pagine (home inclusa). Rilancia anche generate_blog_pages.py per il sitemap.xml completo.")


if __name__ == "__main__":
    main()
