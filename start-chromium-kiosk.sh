#!/bin/bash
# Substitute the prefrerred starting domain on last line
# Install ./install-chromium-policies.sh.sh on pupils computers
# Requires running ssh server on pupils computers accessible with ssh keys

DISPLAY=:0 nohup chromium \
    --no-first-run \
    --disable \
    --disable-translate \
    --disable-infobars \
    --disable-suggestions-service \
    --disable-save-password-bubble \
    --start-maximized \
    --kiosk "https://campus.institutpedralbes.cat"
