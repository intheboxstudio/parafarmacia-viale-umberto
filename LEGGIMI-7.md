# Aggiornamento — parte 7

## File in questo pacchetto
```
parafarmacia-updates-7/
├── index.html            (sostituisce l'originale)
└── assets/logo-badge.png (NUOVO — il tuo logo con sfondo bianco)
```

## Comandi
```
cd "C:\Users\Shadow Moon\Desktop\Claude Code\parafarmacia"
git pull origin main --no-rebase
copy /Y "%USERPROFILE%\Desktop\parafarmacia-updates-7\index.html" "index.html"
copy /Y "%USERPROFILE%\Desktop\parafarmacia-updates-7\assets\logo-badge.png" "assets\logo-badge.png"
git add -A
git commit -m "Sostituito logo con la versione a sfondo bianco nel logo nav/footer e nell'avatar Instagram"
git push origin main
```

## Cosa ho fatto
Ho sostituito il logo (foglia bianca su cerchio scuro) con il file che mi
hai mandato (cerchio bianco, bordo nero, foglia disegnata, testo integrato)
nei 2 punti dove appare come badge circolare:

1. **Logo nav/footer** — il cerchietto accanto a "Viale Umberto 1°" in alto
   su ogni pagina e in fondo nel footer
2. **Avatar della pagina Instagram** — il cerchio grande accanto a
   "@parafarmacia.viale.umberto"

Ho tolto lo sfondo scuro che c'era prima dietro il logo (nel tuo file è già
integrato uno sfondo bianco con bordo, quindi non serviva più).

Non ho toccato la foglia decorativa grande sullo sfondo della home page
(quella azzurra/rosa/bianca dietro al cerchio nell'hero): è un elemento
puramente decorativo, diverso dal logo badge, e presumo tu intendessi
questi due punti. Se invece va cambiata anche quella, dimmelo.
