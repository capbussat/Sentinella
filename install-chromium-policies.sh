#!/bin/bash
# install-chromium-policies.sh

if [[ "$EUID" -ne 0 ]]; then
    echo "Error: cal executar com a root (sudo)" >&2
    exit 1
fi
# Instal·la chromium
snap install chromium
# Crea el directori chromium de policies per ubuntu snap
mkdir -p /var/snap/chromium/current/policies/managed

cat > /var/snap/chromium/current/policies/managed/policies.json << 'EOF'
{
  "HomepageLocation": "https://www.institutpedralbes.cat",
  "HomepageIsNewTabPage": false,
  "URLBlocklist": ["*"],
  "URLAllowlist": [
    "institutpedralbes.cat",
    "accounts.google.com",
    "elmeuescriptori.gestioeducativa.gencat.cat",
    "chrome://policy"
  ]
}
EOF
# canvia els permisos
chmod 644  /var/snap/chromium/current/policies/managed/policies.json
snap restart chromium
