# Aggiornamenti sito — parte 4 (correzioni)

## File in questo pacchetto
```
parafarmacia-updates-4/
├── index.html       (sostituisce l'originale)
└── blog_agent.py    (sostituisce l'originale)
```

## Comandi
```
cd "C:\Users\Shadow Moon\Desktop\Claude Code\parafarmacia"
git pull origin main --no-rebase
copy /Y "%USERPROFILE%\Desktop\parafarmacia-updates-4\index.html" "index.html"
copy /Y "%USERPROFILE%\Desktop\parafarmacia-updates-4\blog_agent.py" "blog_agent.py"
git add -A
git commit -m "Fix: allineamento esatto stanze, evita foto duplicate tra articoli blog"
git push origin main
```

## Cosa ho corretto

### 1. Stanze non allineate
Il fix precedente (altezza minima) non bastava: se il testo di una card
andava a capo più volte di quanto previsto, superava comunque il minimo e
sfalsava tutto. Ora ho messo un'altezza **fissa** (non minima) sia sul
paragrafo che sulla lista puntata di entrambe le card: qualsiasi cosa
succeda al testo, quello spazio resta identico nelle due colonne, quindi le
gallery fotografiche partono sempre dalla stessa riga esatta. Su mobile
(quando le stanze si impilano una sotto l'altra) ho tolto l'altezza fissa,
perché lì l'allineamento non serve e altrimenti si sprecherebbe spazio.

### 2. Due articoli del blog con la stessa foto
Causa: l'agente cercava una foto su Unsplash e sceglieva sempre "la più
popolare" tra i primi risultati. Se due articoli diversi generano parole
chiave simili (es. entrambi su stress/ansia), Unsplash restituisce risultati
simili, e la foto più popolare finiva per essere scelta due volte.

Ho corretto `blog_agent.py` così: prima di cercare una nuova immagine,
l'agente ora guarda quali foto ha già usato negli ultimi 30 articoli (le
tiene in memoria dentro `articles.json`, in un nuovo campo `imageSourceId`)
ed esclude quelle dalla scelta. Se la foto più popolare è già stata usata di
recente, passa alla successiva. Da ora in poi due articoli non avranno più
la stessa foto di copertina.

**Nota**: questa correzione vale per i prossimi articoli. I due articoli già
pubblicati con la foto uguale restano così — non ho un modo per generarne
una nuova diversa per un articolo già pubblicato senza rilanciare l'agente
su quello specifico articolo, e comunque usciranno naturalmente dal blog
quando verranno superati dai nuovi articoli (il blog ne tiene solo gli
ultimi N). Se preferisci sistemarli subito dimmelo e vediamo come fare.
