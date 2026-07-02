#!/bin/bash
# mata el procés que té PID de l'script pantalla-start.sh
kill -INT $(cat /tmp/ffmpeg.pid)
