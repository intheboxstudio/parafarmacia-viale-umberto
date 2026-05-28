# Patch Parafarmacia Viale Umberto 1° — Guida operativa

Tutto quello che serve per risolvere i 7 punti del messaggio. Lo script Python fa il grosso del lavoro; tu fai 4 `git` e qualche minuto di test. Backup automatico incluso, perché chi non fa backup poi piange.

## File inclusi nel pacchetto

```
parafarmacia-patches/
├── ISTRUZIONI.md            ← stai leggendo questo
├── blog-agent.yml           ← nuovo workflow GitHub Actions
├── patch_blog_agent.py      ← script che modifica blog_agent.py
└── patch_index_html.py      ← script che modifica index.html
```

## Diagnosi del problema (utile per capire perché succedeva)

**Punto 1 — Blog che non si aggiornava**: il workflow GitHub Actions diventava verde ma non produceva nulla. Causa: `is_publish_time()` controllava `now.hour == 10`, ma GitHub Actions cron ha drift sotto carico anche di 30–60 minuti. Il run partiva fra le 8:30 e le 9:15 UTC (cioè 10:30–11:15 italiane), e lo script faceva skip silenzioso ogni volta. I run da 16-34 secondi che vedevi nello screenshot erano tutti aborti senza commit. In aggiunta, GitHub Pages serve `articles.json` dietro un CDN con cache: anche se il file fosse stato aggiornato, il browser ne avrebbe pescato la vecchia versione per qualche minuto.

**Punto 2 — Esegue due volte al giorno**: il workflow scheduliava due cron (8 UTC e 9 UTC) per coprire CET e CEST. In teoria solo uno passava il check dell'ora; in pratica con il drift skippavano tutti e due, ma il workflow continuava ad apparire eseguito due volte.

La fix: rimuovere il check rigido sull'ora, aggiungere un controllo del giorno della settimana, e un anti-doppione idempotente che legge `articles.json` per verificare se ha già pubblicato oggi.

## Prerequisiti

- Repo `parafarmacia-viale-umberto` clonato in locale.
- Python 3 installato (lo usi già per `blog_agent.py`).
- I tuoi soliti permessi `git` sul repo.

## Procedura passo-passo

### 1. Copia gli script nella cartella del repo

```bash
# dalla cartella dove hai scaricato i patch:
cp blog-agent.yml          /percorso/del/repo/.github/workflows/blog-agent.yml
cp patch_blog_agent.py     /percorso/del/repo/patch_blog_agent.py
cp patch_index_html.py     /percorso/del/repo/patch_index_html.py

cd /percorso/del/repo
```

### 2. Esegui le patch

```bash
python patch_blog_agent.py blog_agent.py
python patch_index_html.py index.html
```

Output atteso (l'ordine dei `⊝` / `✓` varia):

```
Backup salvato in: blog_agent.py.bak

Applico patch...
  ✓ patch 'is_publish_time → can_publish_today' applicata
  ✓ patch 'GitPublisher.already_published_today' applicata
  ✓ patch 'BlogAgent.run guard' applicata

✓ blog_agent.py aggiornato.
```

```
Applico 14 patch su index.html...

  ✓ 01 cache-buster articles.json
  ✓ 02 orari mercoledì
  ✓ 03 footer orari
  ...
  ✓ 13 JS rooms form (mailto)

— Riepilogo —
  Applicate:    14
  Fallite:      0
✓ index.html aggiornato.
```

**Se qualche patch fallisce** (es. perché qualcosa nell'`index.html` è già stato ritoccato a mano), lo script te lo dice esplicitamente. In quel caso fammi sapere quale patch ha fallito e ti passo la sostituzione manuale aggiornata.

### 3. Aggiungi la foto del Pane Primus

Lo script ha già inserito la sezione, ma il file immagine non posso fornirtelo io. Mettilo in:

```
/percorso/del/repo/assets/primus.jpg
```

Tre raccomandazioni per la foto:

- formato 1:1 (quadrata) o quasi, almeno 1200×1200 px;
- compressa (JPEG ~85% di qualità, sotto i 300 KB se possibile);
- luce naturale, pane sezionato visibile per mostrare la mollica.

Se non metti il file, la sezione mostra automaticamente un'illustrazione SVG di fallback già pronta — niente immagine rotta. La sostituzione avviene non appena carichi il jpg.

### 4. Test in locale (opzionale ma consigliato)

```bash
# Apri index.html in un browser locale (anche un semplice doppio click).
# Controlla:
#   - la sezione Pane Primus (home, sotto i brand)
#   - la sezione Stanze (pagina Servizi, sotto i 3 servizi)
#   - i nuovi Servizio 02 (Naturopata) e Servizio 03 (Cosmetologa)
#   - gli orari in /contatti e nel footer
#   - il menu mobile: restringi la finestra sotto 980px e clicca l'hamburger
```

Per testare il blog agent in locale, con le tue env vars già esportate:

```bash
FORCE_RUN=true python blog_agent.py
```

Se va a buon fine, vedrai un nuovo articolo in `articles.json` e una jpg in `assets/blog/`. Ricordati di non committare quello che è stato generato in locale se non vuoi un articolo aggiuntivo in produzione.

### 5. Commit e push

```bash
git add .github/workflows/blog-agent.yml blog_agent.py index.html assets/primus.jpg
git commit -m "feat: stanze consulenze + Pane Primus + servizi rivisti; fix: blog agent (drift cron + anti-doppione + cache buster)"
git push origin main
```

I file `.bak` generati dagli script sono ignorabili — se vuoi puliscili:

```bash
rm blog_agent.py.bak index.html.bak
```

### 6. Verifica post-deploy (5 minuti)

1. **Sito**: vai su https://intheboxstudio.github.io/parafarmacia-viale-umberto/ e fai un hard refresh (`Ctrl+Shift+R` o `Cmd+Shift+R`). Controlla home → Primus, Servizi → Stanze, Contatti → orari mercoledì.

2. **Menu mobile**: apri da telefono (o DevTools in modalità mobile) e tocca le tre linee. Deve aprirsi un overlay pulito, voci impilate, lo sfondo del sito che non scrolla.

3. **Blog Agent**: vai su `https://github.com/intheboxstudio/parafarmacia-viale-umberto/actions`, clicca su "Blog Agent — daily post", "Run workflow" con `force_run = true`. Il run dovrebbe durare 60–120 secondi (non più 16) e finire con un commit "blog: pubblicato …".

4. **Sito blog**: torna sul sito (hard refresh) e vai su /blog. Il nuovo articolo deve apparire come "in evidenza".

5. **Schedule attivo**: il prossimo giorno utile (martedì, giovedì o sabato) verifica che alle 10 del mattino (più/meno mezz'ora di drift) sia partito da solo. Se vuoi essere prudente, il martedì successivo controlla che `articles.json` abbia un articolo nuovo con data di quel giorno.

## Cosa è cambiato nel dettaglio

| # | Punto richiesto | Soluzione applicata |
|---|---|---|
| 1 | Blog non si aggiorna | Cache-buster nel fetch + rimosso il check rigido sull'ora (drift cron) |
| 2 | Solo martedì/giovedì/sabato | Cron `* * 2,4,6` + `PUBLISH_WEEKDAYS = {1,3,5}` + anti-doppione su `articles.json` |
| 3 | Orari mercoledì allineati | `15:30 — 19:30` in pagina contatti, raggruppato con Lun/Mar/Ven/Sab nel footer |
| 4 | Menu mobile rotto | Overlay full-screen scrollabile, tipografia coerente, body scroll bloccato |
| 5 | Stanze + modulo email | Nuova sezione nella pagina Servizi + mini-form `mailto:` |
| 6 | Pane Primus | Nuova sezione nella home con descrizione + slot foto + fallback SVG |
| 7 | Servizi rivisti | Naturopata (era Shiatsu), Cosmetologa (era Meditazione), Nutrizionista invariata |

## Note finali

Il workflow ora rispetta sia il giorno della settimana sia la "regola del primo arrivato": nei giorni in cui parte due volte (cambio d'ora), il secondo run trova l'articolo di oggi già in `articles.json` e abortisce silenziosamente. Niente più articoli doppi, niente più "non pubblica mai".

Se vuoi cambiare giorni o orari in futuro, modifica:
- `.github/workflows/blog-agent.yml` → riga `cron:`
- `blog_agent.py` → `PUBLISH_WEEKDAYS = {1, 3, 5}`

I due valori devono restare coerenti: il cron decide quando *parte* il workflow, `PUBLISH_WEEKDAYS` decide se *pubblica*. Tienili allineati e non avrai sorprese.

Buon refactoring.
