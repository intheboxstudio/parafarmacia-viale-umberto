# Blog Agent — Parafarmacia Viale Umberto 1°

Agente AI che pubblica un nuovo articolo ogni mattina alle **10:00 (Europe/Rome)** sul blog del sito. Discovery automatico dei topic, fonti autorevoli, contenuto generato via Claude, immagine generata via Gemini 2.5 Flash Image (Nano Banana).

## Architettura

```
┌─ Cron 10:00 IT ──┐
│                  │
│  blog_agent.py   │  →  Anthropic API   (testo)
│   (Railway)      │  →  Gemini API      (immagine)
│                  │  →  GitHub API      (commit)
└──────────────────┘
        │
        ▼
articles.json + assets/blog/*.jpg  (su GitHub)
        │
        ▼
Sito statico (index.html) fetcha articles.json
```

## Setup locale (test prima del deploy)

### 1. Clona il repo
```bash
git clone https://github.com/intheboxstudio/parafarmacia-viale-umberto.git
cd parafarmacia-viale-umberto
```

### 2. Installa dipendenze
```bash
python -m venv .venv
source .venv/bin/activate    # macOS/Linux
# .venv\Scripts\activate     # Windows
pip install -r requirements.txt
```

### 3. Configura variabili d'ambiente
Crea un file `.env` (non committarlo):

```bash
ANTHROPIC_API_KEY=sk-ant-...                  # console.anthropic.com
GEMINI_API_KEY=AIza...                        # aistudio.google.com/apikey
GITHUB_TOKEN=ghp_...                          # github.com/settings/tokens (scope: repo)
GITHUB_REPO=intheboxstudio/parafarmacia-viale-umberto
GITHUB_BRANCH=main

# Opzionale: search.brave.com/api (gratis fino a 2k/mese)
BRAVE_SEARCH_API_KEY=BSA...
```

Poi:
```bash
export $(cat .env | xargs)    # carica nella shell
python blog_agent.py          # esegui una volta
```

Se tutto va bene, vedrai un nuovo articolo in `articles.json` e l'immagine in `assets/blog/`. Verifica anche su GitHub che il commit sia stato pushato.

## Deploy su Railway (consigliato)

### 1. Nuovo servizio Python
- Vai sul progetto Railway esistente (quello di Normia)
- Click su "+ New" → "GitHub Repo"
- Seleziona il repo `parafarmacia-viale-umberto`
- Imposta come servizio Python (Railway lo riconosce dal `requirements.txt`)

### 2. Variabili d'ambiente
Nel servizio appena creato, "Variables":
```
ANTHROPIC_API_KEY=sk-ant-...
GEMINI_API_KEY=AIza...
GITHUB_TOKEN=ghp_...
GITHUB_REPO=intheboxstudio/parafarmacia-viale-umberto
GITHUB_BRANCH=main
```

### 3. Configura Cron
Railway supporta cron job nativamente.
- Service settings → "Cron Schedule"
- Schedule: `0 10 * * *`  (ogni giorno alle 10:00)
- Timezone: `Europe/Rome`
- Start Command: `python blog_agent.py`

### 4. Verifica primo run
- Settings → "Trigger Run" per eseguire subito un test
- Logs → controlla che la pipeline arrivi fino a "✓ Pubblicazione completata"

## Deploy alternativo su GitHub Actions (gratuito)

Se preferisci tenerlo tutto su GitHub senza Railway:

`.github/workflows/blog-agent.yml`:
```yaml
name: Blog Agent — daily post
on:
  schedule:
    - cron: '0 8 * * *'      # 08:00 UTC = 10:00 Europe/Rome
  workflow_dispatch:           # bottone manuale

jobs:
  publish:
    runs-on: ubuntu-latest
    permissions:
      contents: write
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - run: pip install -r requirements.txt
      - run: python blog_agent.py
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
          GEMINI_API_KEY: ${{ secrets.GEMINI_API_KEY }}
          GITHUB_TOKEN: ${{ secrets.GH_PAT }}    # usa un PAT, non GITHUB_TOKEN
          GITHUB_REPO: ${{ github.repository }}
          GITHUB_BRANCH: main
```

Settings → Secrets → aggiungi `ANTHROPIC_API_KEY`, `GEMINI_API_KEY`, `GH_PAT` (personal access token).

## Configurazione del frontend

In `index.html`, cerca la riga:
```javascript
const BLOG_ARTICLES_URL = "./articles.json";
```

Sostituisci con l'URL pubblico del JSON. Esempi:

| Hosting | URL |
|---|---|
| Stesso dominio | `./articles.json` |
| GitHub raw | `https://raw.githubusercontent.com/USER/REPO/main/articles.json` |
| jsDelivr CDN | `https://cdn.jsdelivr.net/gh/USER/REPO@main/articles.json` |
| Railway endpoint | `https://normia.tech/blog/articles.json` |

**Consigliato**: jsDelivr CDN — è gratuito, veloce, ha cache globale e supporta CORS.

## Personalizzare l'agente

### Modificare le tematiche
In `blog_agent.py`, sezione `TOPIC_SEEDS`: aggiungi seed per nuove sottocategorie.

### Aggiungere domini autorevoli
`AUTHORITATIVE_DOMAINS`: aggiungi domini fidati. Più sono mirati, migliore è la qualità delle fonti.

### Cambiare i pattern dei titoli
`TITLE_PATTERNS`: aggiungi varianti. L'agente sceglie quello più adatto al topic.

### Modificare il system prompt
`ArticleGenerator.SYSTEM_PROMPT`: il cuore stilistico dell'agente. Modificalo per cambiare tono, lunghezza, struttura.

## Costi stimati

| Servizio | Quota | Costo mese (1 post/giorno) |
|---|---|---|
| Anthropic Claude (claude-opus-4-7) | ~4K input + 4K output per articolo | ~€5-8 |
| Gemini Flash Image | ~1 immagine 1024×1024 | ~€1-2 |
| Brave Search API | ~30 query | gratis (fino a 2k) |
| Railway Python service | sempre attivo, cron | ~€2 (sul piano hobby già attivo) |
| **Totale** | | **~€8-12/mese** |

## Supervisione consigliata

L'AI può sbagliare, soprattutto su contenuti sanitari. Ti consiglio di:

1. **Review settimanale**: la prima settimana, leggi ogni articolo generato prima che resti pubblico. Se trovi errori, correggili nel JSON e committa.
2. **Aggiungi un "review delay"**: nello script, salva l'articolo come `draft: true` e pubblicalo solo dopo conferma manuale. Modifica `GitPublisher.publish_article` per questo.
3. **Whitelist prodotti**: l'agente può inventare nomi prodotto. Se preferisci, fornisci nel system prompt un elenco preciso dei prodotti che hai a magazzino.

## Disclaimer legale

Gli articoli generati hanno carattere divulgativo. La pagina blog include automaticamente un disclaimer in calce a ogni articolo. Se la parafarmacia consiglia prodotti, verifica sempre che le indicazioni siano conformi al regolamento UE 2017/745 (dispositivi medici) e alla normativa sui cosmetici (Reg. 1223/2009) — l'AI può generare claim oltre il consentito.

## Supporto

Per problemi tecnici, controlla i log Railway/GitHub Actions. Per qualsiasi domanda:
- Email: parafarmaciavialeumberto@gmail.com
- Tel: 0522 081652
