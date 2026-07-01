# Aggiornamenti sito — parte 2

## File in questo pacchetto
```
parafarmacia-updates-2/
├── index.html                              (sostituisce l'originale)
├── reviews_agent.py                        (NUOVO)
├── reviews.json                            (NUOVO — placeholder vuoto)
├── .github/workflows/reviews-agent.yml     (NUOVO)
└── assets/rooms/stanza-raccolta-1..4.jpg   (NUOVE — foto Stanza 02)
```

## 1. Copia i file
Come la volta scorsa: copia tutto nella cartella locale del repo,
sovrascrivendo `index.html`. Gli altri file sono nuovi, vanno solo
aggiunti nelle rispettive posizioni (mantieni la struttura di cartelle,
`.github/workflows/` incluso).

## 2. Gallery Stanza 02
Ho fatto lo stesso lavoro della Stanza 01: raddrizzate, ritagliate in
quadrati simmetrici, bilanciate nei colori. Ho scelto il tavolo con le
sedie, l'angolo con il quadro, la vetrata con la tenda e il poster
Shiatsu Meridian Chart (un bel dettaglio "professionale" per una stanza
di consulenza). Le 3 foto del corridoio con l'armadio bianco non le ho
usate: sembravano l'ingresso comune, non la stanza in sé — dimmi se
invece vuoi che le includa comunque.

## 3. Recensioni Google — cosa ho fatto e cosa serve a te

Ho aggiunto in fondo alla home page una sezione "Cosa dicono di noi"
che mostra automaticamente le recensioni Google, con lo stesso
meccanismo già usato per il blog: uno script Python (`reviews_agent.py`)
gira una volta al giorno su GitHub Actions, va a prendere le recensioni
da Google e aggiorna un file `reviews.json` che il sito legge da solo.
Nessuna manutenzione manuale, si aggiorna da sé ogni giorno.

**Limite tecnico di Google, non mio:** l'API restituisce al massimo
**5 recensioni** per scheda (le sceglie Google, di solito le più
rilevanti/recenti), non tutte quelle che avete. Per averle tutte
servirebbe un servizio a pagamento di terze parti — se lo vuoi, dimmelo
e vediamo le opzioni.

### Cosa devi fare tu (una tantum, ~15 minuti)

Serve una chiave API Google. Va creata sul tuo account Google (quello
con cui gestisci la scheda dell'attività), io non posso farlo al posto
tuo. Passi:

**A. Crea un progetto Google Cloud**
1. Vai su https://console.cloud.google.com/
2. Accedi con l'account Google della parafarmacia (o il tuo)
3. In alto, menu progetti → "Nuovo progetto" → chiamalo es. "Parafarmacia sito"
4. Crea

**B. Abilita la Places API**
1. Nel menu laterale → "API e servizi" → "Libreria"
2. Cerca "Places API" (quella classica, non "Places API (New)")
3. Aprila → "Abilita"

**C. Attiva la fatturazione**
Google richiede una carta di credito collegata anche se resti nella
fascia gratuita (hanno 200$/mese di credito gratuito, e con 1 richiesta
al giorno per le recensioni non lo supererai mai — costo reale atteso:
€0). "Fatturazione" nel menu laterale → collega una carta.

**D. Crea la chiave API**
1. "API e servizi" → "Credenziali" → "Crea credenziali" → "Chiave API"
2. Copiala da qualche parte al sicuro
3. Consigliato: clicca sulla chiave appena creata → "Limitazioni API" →
   seleziona solo "Places API" (così anche se qualcuno la intercetta
   non può usarla per altro)

**E. Trova il Place ID della parafarmacia**
1. Vai su https://developers.google.com/maps/documentation/places/web-service/place-id
2. Nel riquadro mappa in quella pagina, cerca "Parafarmacia Erboristeria
   Viale Umberto 1° Reggio Emilia"
3. Clicca sul segnaposto giusto: comparirà un "Place ID" tipo
   `ChIJ...` — copialo

**F. Aggiungi i 2 segreti su GitHub**
Sul repo GitHub (`intheboxstudio/parafarmacia-viale-umberto`):
1. Settings → Secrets and variables → Actions → "New repository secret"
2. Crea `GOOGLE_PLACES_API_KEY` → incolla la chiave del punto D
3. Crea `GOOGLE_PLACE_ID` → incolla il Place ID del punto E
4. Il segreto `GH_PAT` dovrebbe già esistere (lo usa già il blog agent) —
   se non c'è, serve un token con permesso `repo`, come quello che usi
   già da CMD.

### Dopo aver fatto questi passaggi
Vai su GitHub → tab "Actions" → workflow "Reviews Agent — aggiornamento
recensioni Google" → "Run workflow" per farlo partire subito la prima
volta (altrimenti aspetta il cron delle 07:30). Se tutto va bene, vedrai
un nuovo commit "reviews: aggiornamento recensioni Google (...)" con
`reviews.json` aggiornato, e le recensioni appariranno in fondo alla
home page entro 1-2 minuti (tempo di build di GitHub Pages).

Se qualcosa va storto, il log del workflow su Actions dice esattamente
cosa (chiave sbagliata, Place ID sbagliato, fatturazione non attiva,
ecc.) — mandami lo screenshot dell'errore e ti aiuto.

## Riepilogo modifiche in questo pacchetto
1. Gallery fotografica aggiunta anche alla card "Stanza 02 — La stanza raccolta".
2. Nuova sezione "Cosa dicono di noi" in fondo alla home page (recensioni
   Google, aggiornamento automatico giornaliero, attribuzione "Recensioni
   da Google" come richiesto dalle linee guida di Google).
3. Nuovo script `reviews_agent.py` + workflow GitHub Actions dedicato.
4. `reviews.json` di partenza (vuoto, con messaggio "Le recensioni sono
   in arrivo" finché non fai il primo run).
