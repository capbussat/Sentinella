#!/bin/bash
# sentinella.sh
CHECK_FILE=/tmp/sentinella
# Si està aquest fitxer, no cal engegar de nou
CHECK_ON="/tmp/sentinella-on"
LOG="/var/log/sentinella.log"
DATE="$(date +'%Y%m%d_%H%M')"
# comprovació de ip
ALLOW_FILE=/tmp/allow
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
    echo "$DATE Enabled UFW rules " >>  "${LOG}"
    touch "${CHECK_ON}"
    echo "$DATE Set ${CHECK_ON} " >>  "${LOG}"
}

allow() {
    ufw disable
    echo "$DATE Disabled UFW rules " >>  "${LOG}"
    rm -f "${CHECK_ON}"
    echo "$DATE Unset ${CHECK_ON} " >>  "${LOG}"
}
if [[ -f "$CHECK_FILE" ]]; then
    if [ -f "$CHECK_ON" ]; then
        echo "Continua restringint internet"
        exit 0
    fi
        echo "Restringeix internet"
        restrict
        touch "$CHECK_ON"
else
# elimina en producció la línia echo  
      echo "Allow internet"
        allow
        rm -f "$CHECK_ON"
fi
