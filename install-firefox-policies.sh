#!/bin/bash
#!/bin/bash

# ============================================================
#  install_firefox_policies.sh
#  Bloqueja totes les URLs excepte les permeses
# ============================================================

set -e

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

# ============================================================
# Detecta la instal·lació de Firefox (snap o apt)
# ============================================================
if snap list firefox &>/dev/null 2>&1; then
  POLICIES_DIR="/var/snap/firefox/current"
  info "Firefox detectat com a SNAP → $POLICIES_DIR"
else
  POLICIES_DIR="/etc/firefox/policies"
  info "Firefox detectat com a APT/DEB → $POLICIES_DIR"
fi

POLICIES_FILE="$POLICIES_DIR/policies.json"

# ============================================================
# Crea el directori si no existeix
# ============================================================
info "Creant directori $POLICIES_DIR ..."
mkdir -p "$POLICIES_DIR"

# ============================================================
# Escriu el fitxer de policies
# ============================================================
info "Escrivint $POLICIES_FILE ..."

cat > "$POLICIES_FILE" << 'EOF'
{
  "policies": {
    "WebsiteFilter": {
      "Block": ["<all_urls>"],
      "Exceptions": [
        "https://www.institutpedralbes.cat/*",
        "https://institutpedralbes.cat/*",
        "https://campus.institutpedralbes.cat/*",
        "https://accounts.google.com/*",
        "https://accounts.google.es/*",
	"https://accounts.google.de/*"
      ]
    }
  }
}
EOF

# ============================================================
# Verificació
# ============================================================
echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}  Policies instal·lades correctament    ${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
info "Fitxer generat:"
cat "$POLICIES_FILE"
echo ""
info "URLs PERMESES:"
echo "  ✅  https://campus.institutpedralbes.cat"
echo "  ✅  https://accounts.google.com"
echo ""
info "Reinicia Firefox perquè els canvis tinguin efecte."
info "Pots verificar-ho a: about:policies"

