#!/bin/bash

# ============================================================
#  install_sentinella.sh
#  Instal·la el servei i el timer systemd de Sentinella
# ============================================================

# set -e option instructs bash to immediately exit if any command has a non-zero exit status.
# set -u if variable does not exist causes the program to immediately exit.
# set -o pipefail prevents errors in a pipeline from being masked#
set -euo pipefail

# --- Constants ---
LOG="/var/log/sentinella.log"
SETTINGS_DIR="/etc/sentinella"
BINARY_DIR="/usr/local/bin"
TMP_FILE="/tmp/sentinella"

log() {
    echo "[$(date +'%Y-%m-%d %H:%M')] $*" | tee -a "$LOG"
}

# --- Colors ---
GREEN="\033[0;32m"
RED="\033[0;31m"
YELLOW="\033[1;33m"
NC="\033[0m" # No Color

info()    { echo -e "${GREEN}[INFO]${NC} $1"; }
warn()    { echo -e "${YELLOW}[WARN]${NC} $1"; }
error()   { echo -e "${RED}[ERROR]${NC} $1"; exit 1; }

# --- Comprovació de permisos: força execució com a root ---
if [[ $EUID -ne 0 ]]; then
  echo -e "${RED}[ERROR]${NC} Cal ser root. Re-executant amb sudo..."
  exec sudo bash "$0" "$@"
fi

# ============================================================
# 1. Crear el script principal (sentinella.sh)
#    → Modifica aquest bloc per afegir la lògica real
# ============================================================
info "Creant $BINARY_DIR/sentinella.sh ..."

mkdir -p $SETTINGS_DIR
cp allow $SETTINGS_DIR/allow
info "Copiant allow a $SETTINGS_DIR/allow ..."
chmod +x sentinella.sh
chmod +x add-chromium-policies.sh
chmod +x add-firefox-policies.sh
chmod +x remove-browser-policies.sh
info "Fent scripts executables."

cp sentinella.sh  $BINARY_DIR/sentinella.sh
info "Copiant sentinella.sh $BINARY_DIR/sentinella.sh ..."

cp add-chromium-policies.sh $BINARY_DIR/add-chromium-policies.sh
info "Copiant add-chromium-policies.sh a $BINARY_DIR/add-chromium-policies.sh ..."

cp add-firefox-policies.sh $BINARY_DIR/add-firefox-policies.sh
info "Copiant add-firefox.sh a $BINARY_DIR/add-firefox-policies.sh ..."

cp remove-browser-policies.sh $BINARY_DIR/remove-browser-policies.sh
info "Copiant remove-browser-policies.sh a $BINARY_DIR/remove-browser-policies.sh ..."

info "Scripts executables copiats."

# ============================================================
# 2. Crear la Service Unit
# ============================================================
info "Creant /etc/systemd/system/sentinella.service ..."

cat > /etc/systemd/system/sentinella.service << 'EOF'
[Unit]
Description=Sentinella Service is running every 30 seconds.

[Service]
Type=oneshot
ExecStart=/usr/local/bin/sentinella.sh
EOF

info "sentinella.service creat."

# ============================================================
# 3. Crear la Timer Unit
# ============================================================
info "Creant /etc/systemd/system/sentinella.timer ..."

cat > /etc/systemd/system/sentinella.timer << 'EOF'
[Unit]
Description=Run sentinella every 30 seconds

[Timer]
OnBootSec=10
OnUnitActiveSec=30s

[Install]
WantedBy=timers.target
EOF

info "sentinella.timer creat."

# ============================================================
# 4. Recarregar systemd i activar el timer
# ============================================================
info "Recarregant systemd daemon..."
systemctl daemon-reload

info "Activant sentinella.timer (s'iniciarà a cada arrencada)..."
systemctl enable sentinella.timer

info "Iniciant sentinella.timer ara mateix..."
systemctl start sentinella.timer

# ============================================================
# 5. Verificació final
# ============================================================
echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}  Instal·lació completada correctament  ${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
info "Estat del timer:"
systemctl status sentinella.timer --no-pager

echo ""
info "Comandes útils:"
echo "  touch $TMP_FILE desactiva internet"
echo "  rm --force $TMP_FILE activa internet"
echo "  systemctl status sentinella.timer   → Estat del timer"
echo "  systemctl status sentinella.service  → Estat del servei"
echo "  journalctl -u sentinella.service -f  → Logs en temps real"
echo "  systemctl stop sentinella.timer      → Aturar el timer"
echo "  systemctl disable sentinella.timer   → Desactivar a l'arrencada"

log "Sentinella instal·lat correctament"
