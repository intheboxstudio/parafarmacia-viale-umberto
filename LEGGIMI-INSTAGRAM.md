# Griglia Instagram sul sito — come funziona e come si attiva

La pagina `/instagram/` ora mostra i **post veri** del profilo
[@parafarmacia.viale.umberto](https://www.instagram.com/parafarmacia.viale.umberto/)
in una griglia a 3 colonne, uguale a quella dell'app: foto, caroselli e reel
in ordine cronologico, con l'iconcina nell'angolo che distingue i reel dai
caroselli. **Cliccando su un riquadro si apre quel post specifico**, non il
profilo generale.

Prima c'erano 9 riquadri decorativi (gradiente + icona disegnata) che
puntavano tutti al profilo: quelli restano come rete di sicurezza, ma
spariscono appena il feed vero risponde.

---

## Come funziona

Stesso schema già collaudato con le recensioni Google:

```
ogni notte alle 08:00
        │
        ▼
GitHub Actions ──▶ instagram_agent.py ──▶ API ufficiali Instagram
                          │
                          ├──▶ scarica le foto in assets/instagram/
                          └──▶ scrive instagram.json
                                      │
                                      ▼
                          il sito legge instagram.json
                          e costruisce la griglia
```

**Perché le foto vengono scaricate invece di linkarle direttamente:** gli URL
delle immagini che Instagram restituisce sono firmati e **scadono dopo pochi
giorni**. Se li linkassimo, nel giro di una settimana la griglia si
riempirebbe di riquadri rotti. Copiandole nel repo la pagina è anche più
veloce, perché le immagini arrivano dallo stesso dominio del sito.

Ogni foto viene scaricata **una volta sola**: ai run successivi, se il post è
già in `assets/instagram/`, non viene ri-scaricato. Le immagini dei post
usciti dalla griglia vengono cancellate.

### File coinvolti

| File | Ruolo |
|---|---|
| `instagram_agent.py` | L'agente: interroga Instagram, scarica, committa |
| `.github/workflows/instagram-agent.yml` | Lo schedula ogni giorno |
| `instagram.json` | Il feed generato (non modificare a mano) |
| `assets/instagram/` | Le immagini scaricate |
| `assets/site.js` → `initInstagramFeed()` | Costruisce la griglia nel browser |
| `assets/site.css` → `.ig-real-grid`, `.ig-tile` | Lo stile della griglia |
| `instagram/index.html` | La pagina, con il fallback decorativo |

---

## Configurazione iniziale (una volta sola)

Serve **un'ora scarsa**, la maggior parte è attesa nei pannelli Meta.

### 1. L'account Instagram dev'essere Business o Creator

Con un account **personale** le API non restituiscono i post: è un limite di
Meta, non aggirabile. La conversione è gratuita, reversibile e non cambia
niente di come si usa il profilo.

Dall'app Instagram: **Impostazioni → Account → Tipo di account e strumenti →
Passa a un account professionale** → scegli *Azienda*.

### 2. Crea un'app su Meta for Developers

1. Vai su [developers.facebook.com/apps](https://developers.facebook.com/apps)
   e accedi (va bene un account Facebook personale, non serve una Pagina).
2. **Crea un'app** → come caso d'uso scegli quello che parla di
   **Instagram / API con accesso Instagram**.
3. Dai un nome all'app (es. "Sito Parafarmacia") e crea.

> I nomi delle voci nel pannello Meta cambiano ogni pochi mesi. Se non trovi
> l'etichetta esatta, cerca la sezione **Instagram** nel menu di sinistra:
> è sempre lì che si arriva.

### 3. Collega il profilo e genera il token

Dentro l'app, sezione **Instagram → Configurazione API con accesso Instagram**:

1. **Aggiungi account** → accedi con le credenziali di
   `@parafarmacia.viale.umberto` e autorizza.
2. Nel campo degli URI di reindirizzamento OAuth metti
   `https://www.parafarmaciaemy.it/` (serve solo formalmente, l'agente non lo usa).
3. Il permesso necessario è **`instagram_business_basic`** — leggere i propri
   post. Nient'altro.
4. Premi **Genera token** e **copia il token**. È lungo, comincia per `IG...`.

> **Non serve la revisione dell'app da parte di Meta.** La revisione serve per
> accedere ai dati di *altri* utenti; qui leggiamo solo il profilo che ha
> autorizzato, quindi l'app può restare in modalità sviluppo per sempre.

### 4. Metti il token fra i secret di GitHub

Sul repository: **Settings → Secrets and variables → Actions → New repository
secret**

- **Name:** `INSTAGRAM_ACCESS_TOKEN`
- **Secret:** il token copiato al punto 3

### 5. Permetti all'agente di rinnovare il token da solo

Il token Instagram dura **60 giorni**. L'agente lo rinnova a ogni run e
riscrive il secret con quello nuovo, così la catena non si interrompe mai —
ma per riscrivere un secret il PAT `GH_PAT` (quello che già usi per il blog e
le recensioni) deve avere il permesso **`Secrets: read and write`** sul
repository.

Se non glielo dai non si rompe niente subito: il sito continua ad
aggiornarsi, ma **fra 60 giorni il token scade** e dovrai rigenerarlo a mano
dal punto 3. Nei log del workflow trovi un avviso esplicito.

Per aggiungerlo: [github.com/settings/tokens](https://github.com/settings/tokens)
→ il tuo token → **Repository permissions** → *Secrets* → **Read and write**.

### 6. Primo avvio

Su GitHub: **Actions → "Instagram Agent — aggiornamento griglia post" →
Run workflow**.

Al termine trovi `instagram.json` popolato e le immagini in
`assets/instagram/`. Ricarica `/instagram/`: la griglia vera ha sostituito
quella decorativa e il tag sotto il titolo passa da "Aggiornato dal profilo"
a "Feed dal vivo".

> Al primissimo run il **rinnovo del token può fallire** con un avviso:
> Instagram accetta il rinnovo solo se il token ha più di 24 ore. È normale,
> non è un errore: il feed viene comunque pubblicato e dal giorno dopo il
> rinnovo funziona.

---

## Uso quotidiano

**Non devi fare niente.** Pubblichi su Instagram come sempre e il giorno dopo
il post è sul sito.

Se hai pubblicato qualcosa e lo vuoi vedere subito, lancia il workflow a mano
da **Actions → Instagram Agent → Run workflow**.

### Provarlo dal tuo computer

```bash
pip install -r requirements.txt
```

```bash
INSTAGRAM_ACCESS_TOKEN=il_tuo_token python instagram_agent.py --local
```

Su PowerShell:

```bash
$env:INSTAGRAM_ACCESS_TOKEN = "il_tuo_token"; python instagram_agent.py --local
```

Con `--local` scrive `instagram.json` e le immagini sul disco senza committare
niente: utile per vedere il risultato prima di pubblicarlo.

---

## Regolazioni

**Quanti post mostrare** — in `.github/workflows/instagram-agent.yml`,
`INSTAGRAM_MAX_POSTS` (default 12). Meglio un multiplo di 3, così l'ultima
riga della griglia è piena.

**Ogni quanto aggiornare** — sempre nel workflow, la riga `cron: '0 6 * * *'`
(è in UTC: `0 6` = le 8 del mattino in Italia d'estate).

**Quanto sono grandi le immagini salvate** — in `instagram_agent.py`,
`THUMB_WIDTH` (720px) e `THUMB_QUALITY` (82).

---

## Se qualcosa non va

| Sintomo | Causa quasi sempre |
|---|---|
| Restano i riquadri decorativi | `instagram.json` ha `posts: []` — guarda i log del workflow |
| Errore API con `code: 190` | Token scaduto o revocato: rigeneralo (punto 3) |
| L'API non restituisce media | L'account è ancora personale, non Business (punto 1) |
| Avviso "secret NON aggiornato" | Al `GH_PAT` manca `Secrets: read and write` (punto 5) |
| Griglia con buchi | Un'immagine non si è caricata: il riquadro viene tolto apposta, invece di lasciare l'icona rotta |
