#!/bin/bash
#!/bin/bash

# ============================================================
#  install-pantalla.sh
# ============================================================

set -euo pipefail

# --- Colors ---
GREEN="\033[0;32m"
RED="\033[0;31m"
NC="\033[0m"

info()  { echo -e "${GREEN}[INFO]${NC} $1"; }
error() { echo -e "${RED}[ERROR]${NC} $1"; exit 1; }

# --- Força execució com a root ---
if [[ $EUID -ne 0 ]]; then
  echo -e "${RED}[ERROR]${NC} Cal ser root. Re-executant amb sudo..."
  exec sudo bash "$0" "$@"
fi

if command -v ffmpeg &>/dev/null; then
  info "ffmpeg detectat."
else
  info "cal instal·lar ffmpeg ->"
  apt update -y && apt install ffmpeg -y
fi

PID="/tmp/ffmpeg.pid"
BIN_DIR="/usr/local/bin/"

cp "screen_recorder-start.sh" "${BIN_DIR}pantalla-start.sh"
cp "screen_recorder.sh" "${BIN_DIR}pantalla-stop.sh"

info "Scripts pantalla-start.sh i pantalla-stop.sh copiats a ${BIN_DIR}"
