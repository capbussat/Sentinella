#!/usr/bin/env bash
#
# monitor-finestres.sh — Monitoritza obertura/tancament de finestres a GNOME
# Mètode: polling amb wmctrl, comparant l'estat cada N segons.
#
# Dependència: wmctrl
#   sudo apt install wmctrl
#
# Requereix sessió X11 (comprova amb: echo $XDG_SESSION_TYPE)

set -euo pipefail

LOGFILE="${SENTINELLA_LOG:-/var/log/sentinella/window-watch.log}"
INTERVAL="${SENTINELLA_INTERVAL:-2}"   # segons entre comprovacions

mkdir -p "$(dirname "$LOGFILE")"

log() {
    printf '%s [%s] %s\n' "$(date '+%Y-%m-%d %H:%M:%S')" "$1" "$2" >> "$LOGFILE"
}

# Comprova dependència
if ! command -v wmctrl &>/dev/null; then
    echo "ERROR: wmctrl no està instal·lat. Fes: sudo apt install wmctrl" >&2
    exit 1
fi

declare -A finestres_actuals   # id -> "classe títol"

# Llegeix l'estat actual de finestres (id, classe, títol)
obtenir_finestres() {
    wmctrl -lx 2>/dev/null | awk '{
        id=$1; classe=$3;
        $1=$2=$3=$4="";
        sub(/^ +/, "");
        print id "|" classe "|" $0
    }'
}

log "INICI" "Sentinella de finestres engegada (interval=${INTERVAL}s)"

# Estat inicial: registrem com a "OBERTA" totes les finestres existents
while IFS='|' read -r id classe titol; do
    [[ -z "$id" ]] && continue
    finestres_actuals["$id"]="$classe|$titol"
    log "OBERTA" "App=${classe} Titol=${titol} ID=${id}"
done < <(obtenir_finestres)

# Bucle de monitoratge
while true; do
    sleep "$INTERVAL"

    declare -A noves
    while IFS='|' read -r id classe titol; do
        [[ -z "$id" ]] && continue
        noves["$id"]="$classe|$titol"

        # Finestra nova -> no existia abans
        if [[ -z "${finestres_actuals[$id]+x}" ]]; then
            log "OBERTA" "App=${classe} Titol=${titol} ID=${id}"
        fi
    done < <(obtenir_finestres)

    # Finestres que han desaparegut -> tancades
    for id in "${!finestres_actuals[@]}"; do
        if [[ -z "${noves[$id]+x}" ]]; then
            IFS='|' read -r classe titol <<< "${finestres_actuals[$id]}"
            log "TANCADA" "App=${classe} Titol=${titol} ID=${id}"
        fi
    done

    finestres_actuals=()
    for id in "${!noves[@]}"; do
        finestres_actuals["$id"]="${noves[$id]}"
    done
done
