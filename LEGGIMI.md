# Aggiornamenti sito — 1 luglio 2026

## Cosa fare
Copia questi file dentro la tua cartella locale del repo
`C:\Users\Shadow Moon\Desktop\Claude Code\parafarmacia`, sovrascrivendo gli
originali, poi fai il solito commit + push.

File in questo pacchetto:
- `index.html` (sostituisce l'originale)
- `blog_agent.py` (sostituisce l'originale)
- `articles.json` (sostituisce l'originale — ora vuoto, blog azzerato)
- `assets/rooms/stanza-luminosa-1.jpg` … `-4.jpg` (nuovi, da aggiungere)

## Da eliminare manualmente nel tuo repo locale
Cartella `assets/blog/` → elimina tutte le 17 immagini dei vecchi articoli
(erano legate agli articoli ora cancellati). Il nome inizia sempre con la
data, es. `2026-06-30-soffri-di-acne-in-eta-adulta-ecco-cosa-f.jpg`.

## Riepilogo modifiche

1. **Frequenza blog**: il testo "Un articolo nuovo ogni mattina" e il tag
   "Aggiornato ogni giorno · ore 10:00" nella pagina Blog ora dicono
   "il martedì, il giovedì e il sabato mattina" / "Aggiornato mar · gio ·
   sab · ore 10:00" — coerente con lo scheduling già corretto nell'agente
   (che pubblica solo mar/gio/sab).

2. **Stanze in affitto**: rimossi "Circa 14 m²" e "Circa 10 m²" dalle due
   card. Aggiunta una piccola gallery fotografica (4 foto, griglia 2×2,
   quadrate, angoli arrotondati, leggero bilanciamento colore per allinearle
   al resto del sito) sotto la card "Stanza 01 — La stanza luminosa".
   La Stanza 02 resta senza foto (non me ne hai mandate).

3. **Prodotti consigliati nel blog**: `blog_agent.py` ora usa un catalogo
   chiuso invece della vecchia whitelist di 8 marchi:
   - **Algàdemy** → catalogo libero (hanno tutto)
   - **Solime** → SOLO "RELAX (Passiflora, Valeriana e Biancospino)",
     "Colostrum Crema rigenerante pelle", "Colostrum Reflugel"
   - **Esi** → SOLO "Omega3"
   Ho tolto Lovrèn, Naturalsalus, Cetilar, Biokyma, Bromatech dalla
   whitelist: li reintegro quando mi dai i prodotti esatti di ognuno.
   Ho anche aggiunto una validazione automatica (`sanitize_products`) che
   scarta qualsiasi prodotto generato dal modello che non rispetti questo
   elenco alla lettera, così anche in caso di errore del modello non finisce
   online un prodotto non disponibile in negozio.

4. **Blog azzerato**: `articles.json` è tornato a `articles: []`. Le 18
   card vecchie e le loro 17 immagini sono cancellate. Si riparte da zero
   al prossimo run automatico (martedì/giovedì/sabato ore 10:00), con i
   nuovi articoli che useranno solo i prodotti approvati sopra.
