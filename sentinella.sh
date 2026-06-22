#!/bin/bash
# sentinella.sh
# place the CHECK_INTERNET on each pupil to start internet restrictions. You can made this with Sentinella GUI. See senti.py 
# Install ./install-sentinella.sh on pupils computer
# Requires running ssh server on pupils computers accessible with ssh keys

# --- Comprovació: cal executar com a root ---
if [ "$EUID" -ne 0 ]; then
  die "Executa aquest script com a root: sudo bash $0"
fi

# remove this file to stop internet restrictions.
CHECK_INTERNET=/tmp/sentinella_internet
CHECK_BROWSER=/tmp/sentinella_browser

# Si està aquest fitxer, no cal engegar de nou
CHECK_ON="/tmp/sentinella-on"
CHECK_OFF="/tmp/sentinella-off"
CHECK_BROWSER_ON="/tmp/sentinella-browser-on"
CHECK_BROWSER_OFF="/tmp/sentinella-browser-off"

# log
LOG="/var/log/sentinella.log"

# actualitza date
log_date() {
     date +'%Y-%m-%d-%H%M'
}

# comprovació de ip
ALLOW_FILE=/etc/sentinella/allow

ips=()
# Comprova IPs
is_ipv4() {
    [[ "$1" =~ ^([0-9]{1,3}\.){3}[0-9]{1,3}$ ]]
}

while IFS= read -r domini; do
    # Salta línies buides i comentaris
    [[ -z "$domini" || "$domini" == \#* ]] && continue

    while IFS= read -r ip; do
        is_ipv4 "$ip" && ips+=("$ip")
    done < <(dig +short "$domini")
done < "$ALLOW_FILE"

# bucle ufw allow
ufw_allow_list(){
for ip in "${ips[@]}"; do
    ufw allow out to "$ip" port 443 proto tcp
    ufw allow out to "$ip" port 80 proto tcp
done
}

restrict() {
if [ -f "$CHECK_ON" ]; then
    exit 0
fi
    ufw default deny outgoing
    ufw_allow_list
    ufw allow proto icmp
    ufw allow 11100/tcp
    ufw allow 11200/tcp
    ufw allow 11300/tcp
    ufw allow 11400/tcp
    ufw allow out proto udp to any port 53
    ufw allow out proto tcp to any port 53
    ufw enable
    ufw status verbose
    touch "${CHECK_ON}"
    echo "$(log_date) Enabled UFW rules" >> "${LOG}"
    echo "$(log_date) Set ${CHECK_ON}" >> "${LOG}"
}

allow() {
echo "Allow internet"
echo "Permet internet"
ufw  --force reset
ufw default allow outgoing
# veyon
    ufw allow 11100/tcp
    ufw allow 11200/tcp
    ufw allow 11300/tcp
    ufw allow 11400/tcp
#services
    ufw allow to any port 22 proto tcp
    ufw allow to any port 53
# final
    ufw --force enable
    ufw status verbose
    rm -f "${SENTINELLA_IS_ON}"
    echo "Sentinella is OFF"
    rm -f "${CHECK_ON}"
    touch "${CHECK_OFF}"
    echo "$(log_date) Disabled UFW rules" >> "${LOG}"
}


if [[ -f "$CHECK_INTERNET" ]]; then
    if [[ ! -f "$CHECK_ON" ]]; then
        echo "Restringint internet"
        restrict
        rm -f "$CHECK_OFF"
        touch "$CHECK_ON"
    else
        echo "Continua restringint internet"
    fi
else
    if [[ ! -f "$CHECK_OFF" ]]; then
        echo "Permet internet"
        allow
        rm -f "$CHECK_ON"
        touch "$CHECK_OFF"
    else
        echo "Continua permetent internet"
    fi
fi

if [[ -f "$CHECK_BROWSER" ]]; then
    if [[ ! -f "$CHECK_BROWSER_ON" ]]; then
        echo "Inicia el navegador"
        /usr/local/bin/start-chromium.sh
        rm -f "$CHECK_BROWSER_OFF"
        touch "$CHECK_BROWSER_ON"
    else 
        echo "Continua actiu el navegador"
    fi
else
# elimina en producció la línia echo
    if [[ ! -f "$CHECK_BROWSER_OFF" ]]; then
        echo "Apaga el navegador"
        rm -f "$CHECK_BROWSER_ON"
        touch "$CHECK_BROWSER_OFF"
    else 
        echo "No engeguis el navegador"
    fi
fi
