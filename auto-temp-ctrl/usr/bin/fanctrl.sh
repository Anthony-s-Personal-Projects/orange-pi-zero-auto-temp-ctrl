#!/bin/bash
set -e

CONFIG_FILE="/etc/auto-temp-ctrl.conf"
trap 'echo "ERROR: Script aborted due to unexpected error."; exit 1' ERR

if [ -f "$CONFIG_FILE" ]; then
    source "$CONFIG_FILE"
else
    echo "Config file not found: $CONFIG_FILE"
    exit 1
fi

start_temp=${start_temp:-50}
stop_temp=${stop_temp:-40}
gpio_pin=${gpio_pin:-15}
interval=${interval:-5}
gpio_cmd=${gpio_cmd:-/usr/local/bin/gpio}

FAN_STATE=0

if ! command -v "$gpio_cmd" &> /dev/null; then
    echo "ERROR: gpio command not found at $gpio_cmd"
    echo "WiringOP is required. Install now? (y/N):"
    read -r answer
    if [[ "$answer" == "y" || "$answer" == "Y" ]]; then
        git clone https://github.com/sunzone93/WiringOP-Zero.git ~/WiringOP-Zero
        cd ~/WiringOP-Zero
        chmod +x ./build
        sudo ./build

        echo "WiringOP installed. Restarting auto-temp-ctrl service..."
        sudo systemctl restart auto-temp-ctrl.service
        exit 0
    else
        echo "WiringOP is required. Please install and restart the service."
        exit 1
    fi
fi

if [ ! -f /sys/class/thermal/thermal_zone0/temp ]; then
    echo "ERROR: CPU temperature sensor not found."
    exit 1
fi

GPIO_PATH="/sys/class/gpio/gpio$gpio_pin"
if [ ! -e "$GPIO_PATH" ]; then
    echo "Exporting GPIO pin $gpio_pin"
    echo "$gpio_pin" > /sys/class/gpio/export
    sleep 1
fi

if [ ! -e "$GPIO_PATH" ]; then
    echo "ERROR: GPIO path $GPIO_PATH could not be created."
    exit 1
fi

cleanup() {
    echo "Exiting... Turning fan OFF"
    "$gpio_cmd" write "$gpio_pin" 0
    exit 0
}
trap cleanup SIGINT SIGTERM

"$gpio_cmd" mode "$gpio_pin" out
"$gpio_cmd" write "$gpio_pin" 0

sleep 5
echo "Starting fan control..."

while true; do
    CPU_TEMP_RAW=$(cat /sys/class/thermal/thermal_zone0/temp)
    CPU_TEMP=$((CPU_TEMP_RAW / 1000))

    echo "CPU Temperature: $CPU_TEMP °C"

    if [ "$CPU_TEMP" -ge "$start_temp" ]; then
        if [ "$FAN_STATE" -eq 0 ]; then
            "$gpio_cmd" write "$gpio_pin" 1
            FAN_STATE=1
            echo "Fan turned ON"
        fi
    elif [ "$CPU_TEMP" -le "$stop_temp" ]; then
        if [ "$FAN_STATE" -eq 1 ]; then
            "$gpio_cmd" write "$gpio_pin" 0
            FAN_STATE=0
            echo "Fan turned OFF"
        fi
    fi

    sleep "$interval"
done
