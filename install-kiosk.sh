#!/bin/bash
KIOSK_URL="https://campus.institutpedralbes.cat"
KIOSK_USER="kiosk"
KIOSK_PASSWORD="kiosk"

echo "- Crea un usuari kiosk"
echo "- Bloqueja-li el terminal"
echo "- Elimina grups perillosos"
echo "- Instal·la Openbox"
echo "- Crea la sessió kiosk"
echo "- Configura l'autostart d'Openbox"
# Atura el script si qualsevol comanda falla
set -e

# --- Comprovació: cal executar com a root ---
if [ "$EUID" -ne 0 ]; then
  die "Executa aquest script com a root: sudo bash $0"
fi

# Crea l'usuari kiosk
if id "$KIOSK_USER" &>/dev/null; then
  echo "L'usuari '$KIOSK_USER' ja existeix. S'omet la creació de l'usuari."
else
  adduser --disabled-password --gecos "" "$KIOSK_USER"
  passwd "$KIOSK_PASSWORD"
  echo "- Crea un usuari kiosk Fet!"
fi

# Shell lock:
chsh -s /usr/bin/false "$KIOSK_USER"
echo "- Bloqueja-li el terminal Fet!"

#  Elimina grups perillosos
for grp in sudo adm plugdev cdrom dialout; do
  if groups "$KIOSK_USER" | grep -qw "$grp"; then
    deluser "$KIOSK_USER" "$grp" 
  else
    echo "L'usuari no pertany al grup '$grp'. S'omiteix."
  fi
done
echo "- Elimina grups perillosos Fet!"


# Substituïu el GNOME completament per a l'usuari del quiosc amb un WM mínim com 
# Openbox no té dreceres de teclat, ni escriptori, ni panell:

sudo apt install openbox
echo "- Instal·la Openbox Fet!"

# Sessió kiosk 
cat > /usr/share/xsessions/kiosk.desktop <<EOF
[Desktop Entry]
Name=Kiosk
Exec=/usr/bin/openbox-session
Type=Application
EOF
echo "- Crea la sessió kiosk Fet!"

# Llança Firefox en mode quiosc. El bucle el reinicia si es tanca.
OPENBOX_CFG_DIR="/home/$KIOSK_USER/.config/openbox"
mkdir -p "$OPENBOX_CFG_DIR"

cat > "$OPENBOX_CFG_DIR/autostart" <<EOF

# firefox --kiosk "$KIOSK_URL" &
chromium \
    --no-first-run \
    --disable \
    --disable-translate \
    --disable-infobars \
    --disable-suggestions-service \
    --disable-save-password-bubble \
    --start-maximized \
    --kiosk "$KIOSK_URL" &


EOF
echo "- Configura l'autostart d'Openbox Fet!"

cat > "$OPENBOX_CFG_DIR/rc.xml" <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<openbox_config xmlns="http://openbox.org/3.4/rc">
  <keyboard>
    <!-- Ctrl+Alt+Supr: tanca la sessió i torna al display manager -->
    <keybind key="C-A-Delete">
      <action name="Execute">
        <command>loginctl terminate-session \$XDG_SESSION_ID</command>
      </action>
    </keybind>
  </keyboard>
</openbox_config>
EOF
echo "Drecera per tancar CTRL +ALT + SUPR Fet!"
