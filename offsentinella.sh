#!/bin/bash
# offsentinella.sh
# Off sentinella without service or timer
# Works with onsentinella.sh

# set -e option instructs bash to immediately exit if any command has a non-zero exit status.
# set -u if variable does not exist causes the program to immediately exit.
# set -x all executed commands are printed to the terminal. 
#  set -o pipefail prevents errors in a pipeline from being masked# 
set -euo pipefail

# Mmarca com iniciat
SENTINELLA_IS_ON="sentinella_is_on"

# actualitza date
log_date() {
     date +'%Y-%m-%d-%H%M'
}

# --- Comprovació de permisos: força execució com a root ---
if [[ $EUID -ne 0 ]]; then
  echo -e "Cal ser root. Re-executant amb sudo..."
  exec sudo bash "$0" "$@"
fi

echo "Allow internet"
ufw  --force reset
ufw default allow outgoing
ufw --force enable
ufw verbose
rm -f "${SENTINELLA_IS_ON}"
