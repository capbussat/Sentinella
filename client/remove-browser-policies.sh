#!/bin/bash
# remove:
# - Chromium policies
# - Firefox policies

set -euo pipefail

# --- Constants ---
CHROME_POLICY_DIR="/var/snap/chromium/current/policies/managed"
CHROME_POLICY_FILE="${CHROME_POLICY_DIR}/policies.json"
FIREFOX_POLICY_DIR="/var/snap/firefox/current"
FIREFOX_POLICY_FILE="${FIREFOX_POLICY_DIR}/policies.json"

LOG="/var/log/sentinella.log"


log() {
    echo "[$(date +'%Y-%m-%d %H:%M')] $*" | tee -a "$LOG"
}

# --- Comprovació de permisos: força execució com a root ---
if [[ $EUID -ne 0 ]]; then
  echo -e "${RED}[ERROR]${NC} Cal ser root. Re-executant amb sudo..."
  exec sudo bash "$0" "$@"
fi

rm -f $CHROME_POLICY_FILE
log "removed $CHROME_POLICY_FILE"
rm -f $FIREFOX_POLICY_FILE
log "removed $FIREFOX_POLICY_FILE"

