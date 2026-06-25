#|/bin/bash
#!/bin/bash

# Obté l'usuari que té sessió gràfica activa
get_active_user() {
    loginctl list-sessions --no-legend | while read session_id uid user seat tty; do
        if loginctl show-session "$session_id" -p Type --value | grep -q "x11\|wayland\|mir"; then
            echo "$user"
            return
        fi
    done
}

USER=$(get_active_user)

if [[ -z "$USER" ]]; then
    echo "No hi ha cap usuari amb sessió gràfica activa"
    exit 1
fi

UID_USER=$(id -u "$USER")
DISPLAY_VAR=$(loginctl show-session \
    $(loginctl list-sessions --no-legend | awk -v u="$USER" '$3==u {print $1}') \
    -p Display --value)

# Fallback si loginctl no retorna el display
if [[ -z "$DISPLAY_VAR" ]]; then
    DISPLAY_VAR=":0"
fi

echo "Usuari actiu: $USER (UID: $UID_USER), Display: $DISPLAY_VAR"

sudo -u "$USER" \
    DISPLAY="$DISPLAY_VAR" \
    XAUTHORITY="/home/$USER/.Xauthority" \
    DBUS_SESSION_BUS_ADDRESS="unix:path=/run/user/$UID_USER/bus" \
    XDG_RUNTIME_DIR="/run/user/$UID_USER" \
    /usr/local/bin/start-chromium.sh  &
