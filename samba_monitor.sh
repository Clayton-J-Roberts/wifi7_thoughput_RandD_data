#!/bin/bash

INTERFACE=wlp2s0f0   # change to your NIC
SHARE=/srv/samba/shared/

# --- Ask user for folder name ---
read -p "Enter a name for this log session folder: " foldername
today=$(date +%Y-%m-%d)
foldername="${foldername}_${today}"
mkdir -p "$foldername"

# --- Ask user for log file names ---
read -p "Enter a name for the TXT log file (without extension): " txtname
read -p "Enter a name for the CSV log file (without extension): " csvname

TXT_LOG="$foldername/${txtname}.txt"
CSV_LOG="$foldername/${csvname}.csv"

echo "Logs will be saved to:"
echo " - $TXT_LOG"
echo " - $CSV_LOG"
echo "------------------------------------------------------"

# --- Initialize CSV headers ---
echo "Time,File,Event,Delta_MB,File_Mbps,Net_RX_Mbps,Net_TX_Mbps,SSID,Status" > "$CSV_LOG"

declare -A FILE_SIZES FILE_TIMESTAMPS FILE_FINISHED
TOTAL_MB=0
TOTAL_FILES=0
START_TIME=$(date +%s)

# --- Functions ---
get_ssid() {
    local ssid
    ssid=$(iwgetid -r 2>/dev/null)
    [[ -z "$ssid" ]] && ssid="N/A"
    echo "$ssid"
}

log_event() {
    local txt_line="$1"
    local csv_line="$2"
    echo "$txt_line" | tee -a "$TXT_LOG"
    echo "$csv_line" >> "$CSV_LOG"
}

check_finished_files() {
    local current_time=$(date +%s)
    for f in "${!FILE_SIZES[@]}"; do
        if [[ -f "$f" && -z "${FILE_FINISHED[$f]}" ]]; then
            local size=$(stat -c %s "$f" 2>/dev/null || echo 0)
            local prev_size=${FILE_SIZES["$f"]}
            local last_change=${FILE_TIMESTAMPS["$f"]}
            local interval=10
            if   (( size < 50000000 ));  then interval=3
            elif (( size < 500000000 )); then interval=6; fi

            if [[ "$size" -eq "$prev_size" && $((current_time - last_change)) -ge $interval ]]; then
                FILE_FINISHED["$f"]=1
                local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
                local SSID=$(get_ssid)
                ((TOTAL_FILES++))
                log_event \
                    "$timestamp | FILE: $f has finished transferring | SSID: $SSID" \
                    "$timestamp,$f,,0,0,0,0,$SSID,Finished"
            fi
        fi
    done
}

show_summary() {
    END_TIME=$(date +%s)
    DURATION=$((END_TIME - START_TIME))
    AVG_MBPS=0
    if (( DURATION > 0 )); then
        AVG_MBPS=$(printf "%.2f" "$(echo "$TOTAL_MB*8/$DURATION" | bc -l)")
    fi
    echo
    echo "===== Session Summary =====" | tee -a "$TXT_LOG"
    echo "Duration       : ${DURATION} seconds"       | tee -a "$TXT_LOG"
    echo "Files finished : ${TOTAL_FILES}"            | tee -a "$TXT_LOG"
    echo "Total MB moved : $(printf "%.2f" "$TOTAL_MB") MB" | tee -a "$TXT_LOG"
    echo "Avg throughput : ${AVG_MBPS} Mbps"          | tee -a "$TXT_LOG"
    echo "===========================" | tee -a "$TXT_LOG"
}

trap 'echo; echo "Monitoring interrupted."; show_summary; echo "Logs saved in $foldername."; exit 0' SIGINT

# --- Main monitoring loop ---
inotifywait -m --timefmt '%Y-%m-%d %H:%M:%S' --format '%T %w%f %e' "$SHARE" | \
while read -r time filepath event; do

    # Network throughput
    NET=$(ifstat -i "$INTERFACE" 1 1 | awk 'NR==3 {print $1, $2}')
    RX=$(echo $NET | awk '{print $1}')
    TX=$(echo $NET | awk '{print $2}')
    RX_Mbps=$(printf "%.2f" "$(echo "$RX*8/1000" | bc -l)")
    TX_Mbps=$(printf "%.2f" "$(echo "$TX*8/1000" | bc -l)")

    SSID=$(get_ssid)
    now=$(date '+%Y-%m-%d %H:%M:%S')
    delta_mb=""
    mbps_file=""
    status=""

    if [[ -f "$filepath" ]]; then
        size=$(stat -c %s "$filepath" 2>/dev/null || echo 0)
        prev_size=${FILE_SIZES["$filepath"]}
        if [[ -n "$prev_size" ]]; then
            delta=$((size - prev_size))
            if (( delta > 0 )); then
                mbps_file=$(printf "%.2f" "$(echo "$delta*8/1000000" | bc -l)")
                delta_mb=$(printf "%.2f" "$(echo "$delta/1024/1024" | bc -l)")
                TOTAL_MB=$(printf "%.2f" "$(echo "$TOTAL_MB + $delta_mb" | bc -l)")
                status="Transferring"
                log_event \
                    "$now | FILE: $filepath | EVENT: $event | Δsize: ${delta_mb} MB (~${mbps_file} Mbps) | SSID: $SSID" \
                    "$now,$filepath,$event,$delta_mb,$mbps_file,$RX_Mbps,$TX_Mbps,$SSID,$status"
            fi
        fi
        FILE_SIZES["$filepath"]=$size
        FILE_TIMESTAMPS["$filepath"]=$(date +%s)
    fi

    clear
    echo "===== Live Monitor - $now ====="
    echo "NET RX: ${RX_Mbps} Mbps TX: ${TX_Mbps} Mbps | SSID: $SSID"
    for f in "${!FILE_SIZES[@]}"; do
        if [[ -z "${FILE_FINISHED[$f]}" && -f "$f" ]]; then
            size=$(stat -c %s "$f" 2>/dev/null || echo 0)
            prev=${FILE_SIZES["$f"]}
            delta=$((size - prev))
            delta_mb=$(printf "%.2f" "$(echo "$delta/1024/1024" | bc -l)")
            mbps_file=$(printf "%.2f" "$(echo "$delta*8/1000000" | bc -l)")
            echo "FILE: $f | Δsize: ${delta_mb} MB (~${mbps_file} Mbps) | Status: Transferring"
        fi
    done
    echo "-------------------------------"

    check_finished_files
done