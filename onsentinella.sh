!/bin/bash
# onsentinella.sh
# ON Sentinella without service or timer

# set -e option instructs bash to immediately exit if any command has a non-zero exit status.
# set -u if variable does not exist causes the program to immediately exit.
# set -x all executed commands are printed to the terminal. 
#  set -o pipefail prevents errors in a pipeline from being masked# 
set -euo pipefail

# --- Comprovació de permisos: força execució com a root ---
if [[ $EUID -ne 0 ]]; then
  echo -e "Cal ser root. Re-executant amb sudo..."
  exec sudo bash "$0" "$@"
fi

# Marca com iniciat
SENTINELLA_IS_ON="sentinella_is_on"

# comprova que el fitxer allow existeix
ALLOW_FILE=allow

if [[ ! -f "$ALLOW_FILE" ]]; then
    echo "Falta el fitxer allow"
    exit 1
fi

# Comprova IPs
is_ipv4() {
    local ip=$1
    [[ $ip =~ ^([0-9]{1,3}\.){3}[0-9]{1,3}$ ]] || return 1

    IFS='.' read -r a b c d <<< "$ip"

    for octet in $a $b $c $d; do
        ((octet >= 0 && octet <= 255)) || return 1
    done
}

while IFS= read -r domini; do
    # Salta línies buides i comentaris
    [[ -z "$domini" || "$domini" == \#* ]] && continue

    while IFS= read -r ip; do
        is_ipv4 "$ip" && ips+=("$ip")
    done < <(dig +short "$domini")
done < "$ALLOW_FILE"

# Actualitza date
log_date() {
     date +'%Y-%m-%d-%H%M'
}

restrict() {
if [ -f "$SENTINELLA_IS_ON" ]; then
    exit 0
fi
# internet
    ufw default deny outgoing
# allow ips
    for ip in "${ips[@]}"; do
        ufw allow out to "$ip" port 443 proto tcp
        ufw allow out to "$ip" port 80 proto tcp
    done
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
    ufw verbose
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

