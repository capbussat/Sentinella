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

PID="/tmp/ffmpeg.pid"
BIN_DIR="/usr/local/bin/"
VIDEOS_DIR="/var/lib/sentinella/videos/"

if command -v ffmpeg &>/dev/null; then
  info "ffmpeg detectat."
else
  info "cal instal·lar ffmpeg ->"
  apt update -y && apt install ffmpeg -y
fi

cp "screen_recorder-start.sh" "${BIN_DIR}screen_recorder-start.sh"
cp "screen_recorder-stop.sh"  "${BIN_DIR}screen_recorder-stop.sh"
info "Scripts screen_recorder copiats a ${BIN_DIR}"

mkdir -p "${VIDEOS_DIR}"
info "Creat el directori ${VIDEOS_DIR}"
