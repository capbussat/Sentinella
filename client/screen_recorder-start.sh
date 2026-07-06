#!/bin/bash

VIDEOS_DIR="/var/lib/sentinella/videos/"
# espai que ja ocupen els videos
VIDEO_SIZE=$(du -sh "$VIDEOS_DIR")
# obté ressolució
RES=$(xdpyinfo | awk '/dimensions/{print $2}')
# nom del fitxer
VIDEO_RECORDING="output_$(date +'%Y-%m-%d-%H%M').mkv"
# on es guarda el PID d'aquest script per aturar-lo
TMP_PID="/tmp/ffmpeg.pid"

# quant ocupen els videos
echo "Els videos ja ocupen $VIDEO_SIZE a $VIDEOS_DIR"

# inicia captura  amb X11 (no wayland) sobre el fitxer en format mkv (matrioska)
ffmpeg -loglevel error -f x11grab -framerate 10 -video_size "$RES" -i "$DISPLAY" -vf scale=640:-1 "${VIDEOS_DIR}${VIDEO_RECORDING}" &
echo "Captura iniciada .."
# guarda el PID d'aquest script per aturar-lo
echo $! > "$TMP_PID"
