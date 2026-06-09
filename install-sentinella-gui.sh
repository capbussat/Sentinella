#!/bin/bash
# ./install-sentinella-gui.sh

# set -e option instructs bash to immediately exit if any command has a non-zero exit status.
# set -u if variable does not exist causes the program to immediately exit.
# set -x all executed commands are printed to the terminal. 
#  set -o pipefail prevents errors in a pipeline from being masked# 
set -euo pipefail

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

sudo cp senti /usr/local/bin
echo "cp senti /usr/local/bin"

sudo cp sentinella.desktop /usr/share/applications/
echo "cp sentinella.desktop /usr/share/applications/"

sudo mkdir -p /etc/sentinella
echo  "mkdir -p /etc/sentinella"

sudo cp settings.yaml /etc/sentinella 
echo "cp settings.yaml /etc/sentinella"

echo "Fet!"