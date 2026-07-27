#!/bin/bash
# remove:
# - Chromium policies
# - Firefox policies
# Chrome policies

set -euo pipefail

# --- Constants ---
CHROME_POLICY_DIR="/etc/opt/chrome/policies/managed"
CHROME_POLICY_FILE="${CHROME_POLICY_DIR}/policies.json"
CHROMIUM_POLICY_DIR="/var/snap/chromium/current/policies/managed"
CHROMIUM_POLICY_FILE="${CHROMIUM_POLICY_DIR}/policies.json"

# ============================================================
# Detecta la instal·lació de Firefox (snap o apt)
# ============================================================
if snap list firefox &>/dev/null 2>&1; then
  FIREFOX_POLICY_DIR="/var/snap/firefox/current"
  echo "Firefox detectat com a SNAP → $FIREFOX_POLICY_DIR"
else
  FIREFOX_POLICY_DIR="/etc/firefox/policies"
  echo "Firefox detectat com a APT/DEB → $FIREFOX_POLICY_DIR"
fi

FIREFOX_POLICY_FILE="${FIREFOX_POLICY_DIR}/policies.json"

# just in case ...
FIREFOX_POLICIES="/etc/firefox/policies/policies.json"

LOG="/var/log/sentinella.log"

log() {
    echo "[$(date +'%Y-%m-%d %H:%M')] $*" | tee -a "$LOG"
}

# --- Comprovació de permisos: força execució com a root ---
if [[ $EUID -ne 0 ]]; then
  echo -e "${RED}[ERROR]${NC} Cal ser root. Re-executant amb sudo..."
  exec sudo bash "$0" "$@"
fi

rm -f $CHROMIUM_POLICY_FILE
log "removed $CHROMIUM_POLICY_FILE"
rm -f $CHROME_POLICY_FILE
log "removed $CHROME_POLICY_FILE"
rm -f $FIREFOX_POLICY_FILE
log "removed $FIREFOX_POLICY_FILE"
rm -f $FIREFOX_POLICIES
log "removed $FIREFOX_POLICIES, just in case..."
