#!/usr/bin/env bash
# ============================================================================
# init_repo.sh — Setup automatico del repository "parafarmacia-viale-umberto"
# ============================================================================
#
# Cosa fa:
#   1. Verifica che GITHUB_TOKEN sia esportato (con scope `repo`).
#   2. Crea la repo privata su GitHub via API (idempotente: se esiste, prosegue).
#   3. Inizializza il repo Git locale nella cartella corrente.
#   4. Configura il remote e fa il primo push su main.
#
# Uso:
#   1. cd nella cartella che contiene tutti i file del progetto (blog_agent.py,
#      index.html, articles.json, .github/, ecc.)
#   2. export GITHUB_TOKEN=ghp_xxxxxxxxxxxxxxxx
#      (PAT classic con scope `repo`, oppure fine-grained con write su contents
#       e administration:write sull'org/utente)
#   3. ./init_repo.sh
#
# Personalizzabile via env:
#   - GH_USER         (default: intheboxstudio)
#   - REPO_NAME       (default: parafarmacia-viale-umberto)
#   - REPO_VISIBILITY (default: private; "public" per pubblica)
#   - DEFAULT_BRANCH  (default: main)
# ============================================================================

set -euo pipefail

# --- Config -----------------------------------------------------------------

GH_USER="${GH_USER:-intheboxstudio}"
REPO_NAME="${REPO_NAME:-parafarmacia-viale-umberto}"
REPO_VISIBILITY="${REPO_VISIBILITY:-private}"
DEFAULT_BRANCH="${DEFAULT_BRANCH:-main}"
DESCRIPTION="Sito + blog agent della Parafarmacia Erboristeria Viale Umberto 1° (Reggio Emilia)"

# --- Colori -----------------------------------------------------------------

GREEN='\033[0;32m'
YELLOW='\033[0;33m'
RED='\033[0;31m'
NC='\033[0m'

info()  { echo -e "${GREEN}[✓]${NC} $*"; }
warn()  { echo -e "${YELLOW}[!]${NC} $*"; }
fatal() { echo -e "${RED}[✗]${NC} $*" >&2; exit 1; }

# --- Pre-flight checks ------------------------------------------------------

[ -n "${GITHUB_TOKEN:-}" ] || fatal "GITHUB_TOKEN non impostato. Esporta un PAT: export GITHUB_TOKEN=ghp_..."

command -v git >/dev/null || fatal "git non installato."
command -v curl >/dev/null || fatal "curl non installato."
command -v jq >/dev/null || warn "jq non installato — uso parsing rudimentale (consigliato: brew/apt install jq)."

# Test token (whoami)
WHOAMI=$(curl -sS -H "Authorization: Bearer $GITHUB_TOKEN" \
              -H "Accept: application/vnd.github+json" \
              https://api.github.com/user)
if echo "$WHOAMI" | grep -q '"message":'; then
    fatal "Token non valido. Risposta GitHub: $WHOAMI"
fi
LOGIN=$(echo "$WHOAMI" | grep -o '"login": *"[^"]*"' | head -1 | sed 's/.*"\([^"]*\)"$/\1/')
info "Autenticato come: $LOGIN"

# --- Crea repo su GitHub ----------------------------------------------------

REPO_FULL="$GH_USER/$REPO_NAME"
info "Verifico esistenza repo $REPO_FULL..."

STATUS=$(curl -sS -o /tmp/repo_check.json -w "%{http_code}" \
              -H "Authorization: Bearer $GITHUB_TOKEN" \
              -H "Accept: application/vnd.github+json" \
              "https://api.github.com/repos/$REPO_FULL")

if [ "$STATUS" = "200" ]; then
    warn "Repo $REPO_FULL già esistente — salto la creazione."
elif [ "$STATUS" = "404" ]; then
    info "Creo la repo $REPO_FULL ($REPO_VISIBILITY)..."

    # Determina se l'utente è il proprietario (creazione su user) o se è un'org
    if [ "$LOGIN" = "$GH_USER" ]; then
        CREATE_URL="https://api.github.com/user/repos"
    else
        CREATE_URL="https://api.github.com/orgs/$GH_USER/repos"
    fi

    PRIVATE_FLAG="true"
    [ "$REPO_VISIBILITY" = "public" ] && PRIVATE_FLAG="false"

    PAYLOAD=$(cat <<EOF
{
  "name": "$REPO_NAME",
  "description": "$DESCRIPTION",
  "private": $PRIVATE_FLAG,
  "auto_init": false,
  "has_issues": true,
  "has_projects": false,
  "has_wiki": false
}
EOF
)

    CREATE_RESP=$(curl -sS -X POST \
                       -H "Authorization: Bearer $GITHUB_TOKEN" \
                       -H "Accept: application/vnd.github+json" \
                       -d "$PAYLOAD" \
                       "$CREATE_URL")

    if echo "$CREATE_RESP" | grep -q '"full_name"'; then
        info "Repo creata: $REPO_FULL"
    else
        fatal "Creazione fallita. Risposta: $CREATE_RESP"
    fi
else
    fatal "Stato inatteso dalla GitHub API: HTTP $STATUS. Body: $(cat /tmp/repo_check.json)"
fi

# --- Init Git locale --------------------------------------------------------

if [ ! -d ".git" ]; then
    info "Inizializzo repo Git locale..."
    git init -b "$DEFAULT_BRANCH" >/dev/null
else
    info "Repo Git locale già inizializzato."
    # Assicura che il default branch sia quello giusto
    CURRENT_BRANCH=$(git symbolic-ref --short HEAD 2>/dev/null || echo "")
    if [ -n "$CURRENT_BRANCH" ] && [ "$CURRENT_BRANCH" != "$DEFAULT_BRANCH" ]; then
        warn "Branch corrente: $CURRENT_BRANCH (atteso: $DEFAULT_BRANCH). Rinomino..."
        git branch -M "$DEFAULT_BRANCH"
    fi
fi

# --- .gitignore safety net --------------------------------------------------

if [ ! -f ".gitignore" ]; then
    info "Creo .gitignore (manca)..."
    cat > .gitignore <<'EOF'
.env
.venv/
__pycache__/
*.pyc
node_modules/
dist/
.DS_Store
EOF
fi

# Sicurezza: rifiuta di committare .env
if [ -f ".env" ] && ! grep -q "^\.env$" .gitignore; then
    fatal ".env presente ma non in .gitignore — abortisco per evitare leak di secrets."
fi

# --- Configura remote e committa --------------------------------------------

REMOTE_URL="https://x-access-token:$GITHUB_TOKEN@github.com/$REPO_FULL.git"
PUBLIC_URL="https://github.com/$REPO_FULL.git"

if git remote get-url origin >/dev/null 2>&1; then
    info "Remote 'origin' già esistente — aggiorno l'URL."
    git remote set-url origin "$REMOTE_URL"
else
    info "Aggiungo remote 'origin'..."
    git remote add origin "$REMOTE_URL"
fi

# Stage + commit
info "Stage di tutti i file..."
git add -A

if git diff --staged --quiet; then
    warn "Niente da committare (working tree pulito)."
else
    info "Creo il commit iniziale..."
    git -c user.email="parafarmaciavialeumberto@gmail.com" \
        -c user.name="In the BoX Studio" \
        commit -m "init: setup iniziale sito + blog agent

- Sito statico (index.html) della Parafarmacia Erboristeria Viale Umberto 1°
- Blog agent (blog_agent.py) con generazione automatica articoli via Claude
  Sonnet 4.6 e immagini coerenti via Gemini 2.5 Flash Image
- GitHub Actions workflow per pubblicazione quotidiana alle 10:00 IT
- articles.json con articolo di benvenuto" >/dev/null
fi

# --- Push -------------------------------------------------------------------

info "Push su origin/$DEFAULT_BRANCH..."
git push -u origin "$DEFAULT_BRANCH"

# Pulizia URL remote (rimuove il token dall'URL salvato)
git remote set-url origin "$PUBLIC_URL"

info "Done. Repo online: https://github.com/$REPO_FULL"
echo
echo "===================================================================="
echo "PROSSIMI PASSI"
echo "===================================================================="
echo
echo "1. Su GitHub, vai su:"
echo "   https://github.com/$REPO_FULL/settings/secrets/actions"
echo
echo "   Aggiungi i seguenti secrets:"
echo "   - ANTHROPIC_API_KEY       (da console.anthropic.com)"
echo "   - GEMINI_API_KEY          (da aistudio.google.com/apikey)"
echo "   - GH_PAT                  (un PAT con scope 'repo' o fine-grained"
echo "                              con write su 'contents' di questo repo)"
echo "   - BRAVE_SEARCH_API_KEY    (opzionale, da search.brave.com/api)"
echo
echo "2. Verifica il workflow:"
echo "   https://github.com/$REPO_FULL/actions"
echo "   → Click su 'Blog Agent — daily post'"
echo "   → 'Run workflow' (con force_run = true) per test immediato"
echo
echo "3. Collega Railway al repo per servire index.html:"
echo "   railway.app → New Service → Deploy from GitHub repo"
echo "   → Seleziona $REPO_FULL"
echo "===================================================================="
