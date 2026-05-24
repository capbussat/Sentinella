!/bin/bash
# onsentinella.sh
# ON Sentinella without service or timer

# set -e option instructs bash to immediately exit if any command has a non-zero exit status.
# set -u if variable does not exist causes the program to immediately exit.
# set -x all executed commands are printed to the terminal. 
#  set -o pipefail prevents errors in a pipeline from being masked# 
set -euo pipefail

# Marca com iniciat
SENTINELLA_IS_ON="sentinella_is_on"

# comprovació de allow
ALLOW_FILE=allow

if [[ ! -f "$ALLOW_FILE" ]]; then
    echo "Missing allow file"
    exit 1
fi


ips=()
# Comprova IPs, ha d'estar abans que la consulta de dominis 
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

# actualitza date
log_date() {
     date +'%Y-%m-%d-%H%M'
}


restrict() {
if [ -f "$SENTINELLA_IS_ON" ]; then
    exit 0
fi
    ufw default deny outgoing
    for ip in "${ips[@]}"; do
        ufw allow out to "$ip" port 443 proto tcp
        ufw allow out to "$ip" port 80 proto tcp
    done
    ufw allow 11100/tcp
    ufw allow 11200/tcp
    ufw allow 11300/tcp
    ufw allow 11400/tcp
    ufw allow out proto udp to any port 53
    ufw allow out proto tcp to any port 53
    ufw --force enable
    ufw status verbose
    echo "$(log_date) Enabled UFW rules " 
    touch "${SENTINELLA_IS_ON}"
    echo "$(log_date) Set ${SENTINELLA_IS_ON} " 
}

if [ -f "$SENTINELLA_IS_ON" ]; then
        echo "Ja està establert"
        exit 0
else
        echo "Restringeix internet"
        restrict
        touch "$SENTINELLA_IS_ON"
fi

