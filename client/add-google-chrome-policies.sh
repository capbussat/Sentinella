#!/bin/bash
# add-google-chromem-policies.sh
# Instal·la Chrome via paquets deb de Google

set -euo pipefail 

# --- Constants ---
POLICY_DIR="/etc/opt/chrome/policies/managed"
POLICY_FILE="${POLICY_DIR}/policies.json"
LOG="/var/log/sentinella.log"

# --- Colors ---
GREEN="\033[0;32m"
RED="\033[0;31m"
YELLOW="\033[1;33m"
NC="\033[0m" # No Color

log() {
    echo "[$(date +'%Y-%m-%d %H:%M')] $*" | tee -a "$LOG"
}

die() {
    echo "Error: $*" >&2
    exit 1
}

# --- Comprovació de permisos: força execució com a root ---
if [[ $EUID -ne 0 ]]; then
  echo -e "${RED}[ERROR]${NC} Cal ser root. Re-executant amb sudo..."
  exec sudo bash "$0" "$@"
fi

# Instal·la Google Chrome
if ! google-chrome --version &>/dev/null; then
    wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
    sudo apt install ./google-chrome-stable_current_amd64.deb
else
    echo "Chrome ja instal·lat"
fi

# Crea el directori chromium de policies per ubuntu snap
mkdir -p "$POLICY_DIR" || die "No s'ha pogut crear $POLICY_DIR"

# --- Escriu les policies (només si han canviat) ---
POLICY_NEW=$(cat << 'EOF'
{
  "HomepageLocation": "https://www.institutpedralbes.cat",
  "HomepageIsNewTabPage": false,
  "URLBlocklist": ["*"],
  "URLAllowlist": [
    "institutpedralbes.cat",
    "accounts.google.com",
    "elmeuescriptori.gestioeducativa.gencat.cat",
    "chrome://policy"
  ]
}
EOF
)

POLICY_CURRENT=$(cat "$POLICY_FILE" 2>/dev/null || echo "")

if [[ "$POLICY_NEW" == "$POLICY_CURRENT" ]]; then
    log "Policies ja actualitzades, no cal reiniciar Chromium"
else
    echo "$POLICY_NEW" > "$POLICY_FILE"
    # canvia els permisos
    chmod 644 "$POLICY_FILE"
    log "Policies escrites a $POLICY_FILE"

    # Reinicia chromium només si estava engegat
    if $(pgrep -x google-chrome >/dev/null); then
	pkill -TERM -x google-chrome ||  log " no s'ha pogut aturar Google Chrome"
        google-chrome || log "Avís: no s'ha pogut iniciar Chrome"
        log "Chrome reiniciat"
    else
        log "Chrome no estava engegat, no cal reiniciar"
    fi
fi

# --- Verificació final ---
log "--- Polítiques actives ---"
cat "$POLICY_FILE" | tee -a "$LOG"

log "Instal·lació completada correctament"
