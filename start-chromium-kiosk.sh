#!/bin/bash
# Substitute the prefrred starting domain on last line
chromium \
    --no-first-run \
    --disable \
    --disable-translate \
    --disable-infobars \
    --disable-suggestions-service \
    --disable-save-password-bubble \
    --start-maximized \
    --kiosk "https://campus.institutpedralbes.cat"
