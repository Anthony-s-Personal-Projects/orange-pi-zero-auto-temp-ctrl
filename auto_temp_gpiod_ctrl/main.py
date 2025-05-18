from .gpio_control import parse_offset, send_signal
from .temps_monitor import fetch_temps, clear_screen
import threading
import sys
import time
import argparse

def heavy_calc(stop_event: threading.Event):
    """
    Run a CPU‐intensive loop until stop_event is set.
    """
    while not stop_event.is_set():
        time.sleep(0.1)

def main():
    parser = argparse.ArgumentParser(
        description='Run CPU load simulation and temperature‐based GPIO control'
    )
    parser.add_argument(
        '-i', '--interval',
        type=float,
        default=5.0,
        help='Seconds between temperature checks and table refresh'
    )
    parser.add_argument(
        '--soc-pin',
        default='PH2',
        help='SoC pin spec to control (e.g. H2, PH2)'
    )
    parser.add_argument(
        '-c', '--chip',
        default='gpiochip0',
        help='GPIO chip device (e.g. gpiochip0 or /dev/gpiochip1)'
    )
    parser.add_argument(
        '--on-temp',
        type=float,
        required=True,
        help='Threshold to turn ON GPIO (≥ this temperature)'
    )
    parser.add_argument(
        '--off-temp',
        type=float,
        required=True,
        help='Threshold to turn OFF GPIO (≤ this temperature)'
    )
    args = parser.parse_args()

    try:
        offset = parse_offset(args.soc_pin, 'soc')
    except ValueError as e:
        print(f"Error parsing soc_pin: {e}")
        sys.exit(1)

    stop_event = threading.Event()
    thread = threading.Thread(
        target=heavy_calc,
        args=(stop_event,),
        daemon=True
    )
    thread.start()

    gpio_state = 0
    send_signal(offset, gpio_state, args.chip)

    try:
        while True:
            temps = fetch_temps()
            clear_screen()
            header_keys = list(temps.keys())
            display_keys = [k.replace('_thermal_0', '') for k in header_keys]
            col_width = 10
            header = ' '.join(f"{k:>{col_width}}" for k in display_keys)
            print(header)
            print('-' * len(header))
            print(' '.join(f"{temps[k]:>{col_width}}" for k in header_keys))

            max_temp = max(float(v) for v in temps.values())

            if max_temp >= args.on_temp and gpio_state == 0:
                send_signal(offset, 1, args.chip)
                gpio_state = 1
            elif max_temp <= args.off_temp and gpio_state == 1:
                send_signal(offset, 0, args.chip)
                gpio_state = 0

            time.sleep(args.interval)

    except KeyboardInterrupt:
        print("\nShutting down...")
    finally:
        stop_event.set()
        thread.join()
