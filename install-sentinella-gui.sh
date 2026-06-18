#!/bin/bash
# ./install-sentinella-gui.sh

# set -e option instructs bash to immediately exit if any command has a non-zero exit status.
# set -u if variable does not exist causes the program to immediately exit.
# set -x all executed commands are printed to the terminal. 
#  set -o pipefail prevents errors in a pipeline from being masked# 
set -euo pipefail

# --- Constants ---
LOG="/var/log/sentinella.log"

log() {
    echo "[$(date +'%Y-%m-%d %H:%M')] $*" | tee -a "$LOG"
}

# --- Colors ---
GREEN="\033[0;32m"
RED="\033[0;31m"
YELLOW="\033[1;33m"
NC="\033[0m" # No Color

# --- Comprovació de permisos: força execució com a root ---
if [[ $EUID -ne 0 ]]; then
  echo -e "${RED}[ERROR]${NC} Cal ser root. Re-executant amb sudo..."
  exec sudo bash "$0" "$@"
fi

coin() {
    local src="$1"
    local dest="$2"

    #dest inclou el nom del fitxer

    if [ -f "$dest" ]; then
        # Si el dest és més recent o igual, no es copia
        echo "Ja existeix: $dest"
    
        if [ "$src" -ot "$dest" ]; then
            return 0
        fi
    fi

    if cp "$src" "$dest"; then
        echo "Copiat: $src -> $dest"
    else
        echo "Error copiant $src to $dest" >&2
        return 1
    fi
}

log "Copia els de fitxers de Sentinella GUI."
coin sentinella /usr/local/bin/sentinella
coin sentinella.desktop /usr/share/applications/sentinella.desktop
coin assets/images/sentinella.svg /usr/share/icons/hicolor/scalable/apps/sentinella.svg
coin assets/images/sentinella.png /usr/share/icons/hicolor/48x48/apps/sentinella.png
log "Crea el directori de configuració de Sentinella"
sudo mkdir -p /etc/sentinella
log "Copia els fitxers de configuració de Sentinella"
coin hosts /etc/sentinella/hosts
coin settings.yaml /etc/sentinella/settings.yaml

log "Fes sentinella.desktop executable per obrir l'aplicació."
chmod +x /usr/share/applications/sentinella.desktop

log "Sentinella GUI instal·lada correctament"
