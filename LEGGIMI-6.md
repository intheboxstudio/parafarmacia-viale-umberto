# Aggiornamento — parte 6

## File in questo pacchetto
```
parafarmacia-updates-6/
└── index.html    (sostituisce l'originale)
```

## Comandi
```
cd "C:\Users\Shadow Moon\Desktop\Claude Code\parafarmacia"
git pull origin main --no-rebase
copy /Y "%USERPROFILE%\Desktop\parafarmacia-updates-6\index.html" "index.html"
git add -A
git commit -m "Fix: spaziatura lettere Dottoressa Emy allineata visivamente a Parafarmacia Erboristeria"
git push origin main
```

## Cosa ho corretto
Il font e la dimensione erano già identici (stessa identica regola CSS per
entrambe le righe). La differenza che notavi era un effetto ottico: la
stessa spaziatura fissa tra le lettere, su una parola molto più corta
("Dottoressa Emy", 14 caratteri) rispetto all'altra ("Parafarmacia ·
Erboristeria", 27 caratteri), si vede proporzionalmente più larga.

Ho ridotto la spaziatura solo sulla riga "Dottoressa Emy" (da 0.22em a
0.10em) così le due righe ora risultano visivamente equilibrate, sia nella
testata del sito che nel footer.
