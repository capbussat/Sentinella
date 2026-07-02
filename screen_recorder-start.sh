#!/bin/bash
# obté ressolució
RES=$(xdpyinfo | awk '/dimensions/{print $2}')
log_date() {
     date +'%Y-%m-%d-%H%M'
}

# inicia captura  amb X11 (no wayland) sobre el fitxer en format mkv (matrioska)
ffmpeg -loglevel error -f x11grab -framerate 10 -video_size "$RES" -i "$DISPLAY" output_$(log_date).mkv &
# guarda el PID d'aquest script per aturar-lo
echo $! > /tmp/ffmpeg.pid
