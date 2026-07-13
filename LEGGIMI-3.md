# Aggiornamenti sito — parte 3

## File in questo pacchetto
```
parafarmacia-updates-3/
├── index.html                    (sostituisce l'originale)
├── blog_agent.py                 (sostituisce l'originale)
└── assets/tisane/*.svg           (16 NUOVE illustrazioni ingredienti)
```

Nessun file da eliminare questa volta.

## 1. Copia i file
```
copy /Y "%USERPROFILE%\Desktop\parafarmacia-updates-3\index.html" "index.html"
copy /Y "%USERPROFILE%\Desktop\parafarmacia-updates-3\blog_agent.py" "blog_agent.py"
mkdir "assets\tisane" 2>nul
copy /Y "%USERPROFILE%\Desktop\parafarmacia-updates-3\assets\tisane\*.svg" "assets\tisane\"
```

## 2. Commit e push
```
git add -A
git commit -m "Blog: catalogo prodotti completo 13 brand. Home: nome + Dottoressa Emy. Tisane: 16 ingredienti con schede dedicate. Stanze: allineamento perfetto"
git push origin main
```

## Riepilogo di cosa ho fatto

### 1. Catalogo prodotti del blog — 13 brand
Ho controllato i siti ufficiali/rivenditori di ogni marca per scrivere consigli
precisi, non generici. `blog_agent.py` ora sa esattamente cosa può consigliare:

- **Algàdemy**: le 28 referenze reali del catalogo (Timeless, Dream, Slim,
  Leg Relief, ecc.), ognuna con l'indicazione di cosa fa davvero — invece di
  lasciare l'agente libero di inventare nomi plausibili ma sbagliati.
- **Solime**: Relax, Colostrum Gel, Colostrum Reflugel, Gelevital, Colostrum
  Colluttorio, Colostrum Dentifricio, Remargin Detergente Intimo, Remargin
  Crema Intima, più tutta la linea Shampoo/Balsamo/Siero.
- **Esi**: Omega 3, più intere linee No Dol, Le 10 Erbe, Propolaid.
- **Farmaderbe**: Bromelina Ananas 5000, Bromelina Drenante Digestivo,
  Mucolid Bronc, Beauty Collagene, Boswellia Complex.
- **Biosnail**: tutta la linea creme (bava di lumaca).
- **CeraVe**: catalogo libero (marchio globale, rischio di errore basso).
- **Florinda Soaps**: sapone liquido mani e corpo.
- **Pool Pharma**: MG K Vis (ho corretto "Pulfarma" nel nome ufficiale
  dell'azienda, Pool Pharma — il prodotto MG K Vis è lo stesso).
- **Cetilar**: linea sportivi.
- **Lovrén**: catalogo libero.
- **Natural Salus**: Serenis, Arnica 30.
- **Biokyma**: tutte le tisane.
- **Bromatech**: catalogo libero (probiotici, es. Enterelle, Bifiselle).

Ho anche rinforzato il controllo automatico (`sanitize_products`): oltre ai
nomi esatti, ora riconosce anche le "linee libere" (es. tutto ciò che inizia
per "No Dol" viene accettato, un nome a caso no) — così anche se il modello
sbaglia, il filtro scarta comunque ciò che non è coerente.

### 2. Home page — intestazione
"Viale Umberto" → "Viale Umberto 1°", e sotto "Parafarmacia · Erboristeria"
ho aggiunto una riga con "Dottoressa Emy". L'ho aggiornato sia nel logo in
alto (su tutte le pagine, non solo la home) sia nel footer, per coerenza.

### 3. Pagina Tisane — 16 ingredienti, tutti cliccabili
Ho aggiunto agli 8 ingredienti esistenti altri 8: **Passiflora, Biancospino,
Liquirizia, Rosa Canina, Ortica, Tarassaco, Malva, Lavanda**.

Ogni ingrediente (tutti e 16, non solo i nuovi) ora è cliccabile e apre una
scheda dedicata con: una piccola illustrazione, cos'è la pianta, le sue
particolarità, l'effetto sul corpo e i problemi che aiuta a risolvere,
dove nasce e come viene coltivata, come viene raccolta ed essiccata prima
di entrare in una tisana. Ho scritto ogni scheda verificando le proprietà
reali di ciascuna pianta.

**Nota sulle immagini**: non potendo scaricare fotografie reali da internet
in questo ambiente, ho creato 16 illustrazioni botaniche originali in stile
minimale (fiore, radice, ombrella o bacca a seconda della pianta), coerenti
con la grafica del sito. Se preferisci foto reali al posto delle
illustrazioni, mandami le foto (anche scattate al telefono, come per le
stanze) e te le monto come ho fatto con quelle — oppure posso lasciarle così,
danno comunque un'identità visiva pulita e riconoscibile.

### 4. Servizi — le due stanze ora sono perfettamente allineate
Ho fissato un'altezza minima per titolo, testo e lista puntata di entrambe
le card, così qualsiasi differenza nella lunghezza del testo non sposta più
la gallery fotografica: le immagini di sinistra e destra ora sono sempre
sulla stessa riga, punto per punto. Ho anche riscritto leggermente il testo
della Stanza 02 per bilanciarne la lunghezza con la Stanza 01.

## Le recensioni Google — come attivarle

Questo pacchetto non tocca la parte recensioni (era già a posto dal
pacchetto precedente). Se non l'hai ancora fatto, ecco di nuovo il percorso
completo, passo passo:

### Passo 1 — Crea un progetto Google Cloud
1. Vai su **https://console.cloud.google.com/**
2. Accedi con l'account Google della parafarmacia
3. In alto, menu progetti → **Nuovo progetto** → chiamalo "Parafarmacia sito" → Crea

### Passo 2 — Abilita la Places API
1. Menu laterale → **API e servizi** → **Libreria**
2. Cerca **"Places API"** (quella classica, non "Places API (New)")
3. Apri la scheda → **Abilita**

### Passo 3 — Attiva la fatturazione
Google la richiede anche restando nella fascia gratuita (200$/mese di
credito incluso — con 1 richiesta al giorno il costo reale resterà €0).
Menu laterale → **Fatturazione** → collega una carta.

### Passo 4 — Crea la chiave API
1. **API e servizi** → **Credenziali** → **Crea credenziali** → **Chiave API**
2. Copiala e conservala
3. Consigliato: sulla chiave appena creata → **Limitazioni API** → seleziona
   solo **"Places API"**, così è utilizzabile solo per quello

### Passo 5 — Trova il Place ID della parafarmacia
1. Vai su **https://developers.google.com/maps/documentation/places/web-service/place-id**
2. Nella mappa di quella pagina cerca "Parafarmacia Erboristeria Viale
   Umberto 1° Reggio Emilia"
3. Clicca sul segnaposto giusto → copia il **Place ID** (tipo `ChIJ...`)

### Passo 6 — Aggiungi i due secret su GitHub
Sul repo `intheboxstudio/parafarmacia-viale-umberto`:
1. **Settings** → **Secrets and variables** → **Actions** → **New repository secret**
2. Crea `GOOGLE_PLACES_API_KEY` → incolla la chiave del Passo 4
3. Crea `GOOGLE_PLACE_ID` → incolla il Place ID del Passo 5
4. `GH_PAT` dovrebbe già esserci (lo usa già il blog agent)

### Passo 7 — Avvia il primo aggiornamento
Su GitHub → tab **Actions** → workflow **"Reviews Agent — aggiornamento
recensioni Google"** → **Run workflow**, per farlo partire subito invece di
aspettare il cron delle 07:30. Dopo 1-2 minuti, aggiorna la home page: le
recensioni compariranno in fondo, con la stellina Google, l'attribuzione
"Recensioni da Google" e il link alla vostra scheda Google Maps.

Se qualche passaggio dà errore, mandami uno screenshot e ti aiuto a risolverlo.
