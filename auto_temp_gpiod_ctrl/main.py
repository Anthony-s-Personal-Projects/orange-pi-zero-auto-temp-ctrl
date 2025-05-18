from .utils.gpio_control import parse_offset, send_signal
from .utils.temps_monitor import fetch_temps, clear_screen
import threading
import sys
import time
import argparse

def heavy_calc(stop_event: threading.Event):
    """
    Run a CPU‐intensive loop until stop_event is set.
    Simulates a realistic CPU load by performing math operations in a loop.
    """
    while not stop_event.is_set():
        total = 0
        for i in range(1_000_000):
            total += i * i
        # Optionally, short sleep to avoid 100% pegging
        # time.sleep(0.01)

def print_help():
    """
    Print detailed help and configuration instructions for the user.
    """
    help_text = f"""
    auto-temp-gpiod-ctrl: Temperature-based GPIO Control
    ---------------------------------------------------
    This tool monitors system temperatures and controls a GPIO pin based on configurable thresholds.

    Usage:
      python -m auto_temp_gpiod_ctrl.main [OPTIONS]

    Options:
      -i, --interval FLOAT    Seconds between temperature checks and table refresh (default: 5.0)
      --soc-pin PIN           SoC pin spec to control (e.g. H2, PH2) (default: PH2)
      -c, --chip CHIP         GPIO chip device (e.g. gpiochip0 or /dev/gpiochip1) (default: gpiochip1)
      --on-temp FLOAT         Threshold to turn ON GPIO (≥ this temperature, default: 50.0)
      --off-temp FLOAT        Threshold to turn OFF GPIO (≤ this temperature, default: 40.0)
      --test-mode             Enable heavy calculation simulation (for testing only)
      -h, --help              Show this help message and exit

    Example:
      python -m auto_temp_gpiod_ctrl.main --soc-pin PH2 --chip gpiochip1 --on-temp 55 --off-temp 45 --interval 3

    Notes:
      - The GPIO pin will always be set to OFF (0) at startup and shutdown for safety.
      - Use --test-mode to simulate CPU load for testing the control logic.
      - Ensure you have the necessary permissions to access GPIO devices.
    """
    print(help_text)

def main():
    parser = argparse.ArgumentParser(
        description='Run CPU load simulation and temperature‐based GPIO control',
        add_help=False
    )
    parser.add_argument('-i', '--interval', type=float, default=5.0, help='Seconds between temperature checks and table refresh')
    parser.add_argument('--soc-pin', default='PH2', help='SoC pin spec to control (e.g. H2, PH2)')
    parser.add_argument('-c', '--chip', default='gpiochip1', help='GPIO chip device (e.g. gpiochip0 or /dev/gpiochip1)')
    parser.add_argument('--on-temp', type=float, default=50.0, help='Threshold to turn ON GPIO (≥ this temperature)')
    parser.add_argument('--off-temp', type=float, default=40.0, help='Threshold to turn OFF GPIO (≤ this temperature)')
    parser.add_argument('--test-mode', action='store_true', help='Enable heavy calculation simulation (for testing only)')
    parser.add_argument('-h', '--help', action='store_true', help='Show this help message and exit')
    args = parser.parse_args()

    if args.help:
        print_help()
        sys.exit(0)

    try:
        offset = parse_offset(args.soc_pin, 'soc')
    except ValueError as e:
        print(f"Error parsing soc_pin: {e}")
        sys.exit(1)

    stop_event = threading.Event()
    if args.test_mode:
        thread = threading.Thread(
            target=heavy_calc,
            args=(stop_event,),
            daemon=True
        )
        thread.start()
    else:
        thread = None

    # Initialize GPIO state: always set to 0 (OFF) at start
    gpio_state = 0
    send_signal(offset, 0, args.chip)

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
        # On exit, always reset GPIO to 0 (OFF) and release the line
        send_signal(offset, 0, args.chip)
        stop_event.set()
        if thread:
            thread.join()
