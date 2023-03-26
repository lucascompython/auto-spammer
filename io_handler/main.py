import sys
from time import sleep
import multiprocessing

import keyboard.keyboard as keyboard
import mouse.mouse as mouse
import argparse


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="IO Handler")
    parser.add_argument("-b", "--bind", help="Bind a key to string", nargs=2)
    parser.add_argument(
        "-a", "--autoclicker", help="Bind a key to autoclicker", nargs=2
    )
    return parser.parse_args()


def toggle_autoclicker(interval: float, toggle: bool) -> None:
    toggle = not toggle
    while toggle:
        mouse.click()
        sleep(float(interval))


def start_autoclicker(
    interval: float, toggle: bool, proc: multiprocessing.Process | None
) -> None:
    if proc is None:
        proc = multiprocessing.Process(
            target=toggle_autoclicker, args=(interval, toggle)
        )
        proc.start()
    else:
        proc.terminate()
        proc = None


def main() -> None:
    args = parse_args()
    if not args.bind and not args.autoclicker:
        print("No arguments provided. Exiting...")
        sys.exit(0)

    if args.bind:
        key, string = args.bind
        keyboard.add_hotkey(key, keyboard.write, args=(string,))

    if args.autoclicker:
        key, interval = args.autoclicker
        interval = float(interval)
        toggle = False
        proc = None

        keyboard.add_hotkey(key, start_autoclicker, args=(interval, toggle, proc))

    keyboard.wait()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Exiting...")
        sys.exit(0)
else:
    sys.stderr.write("This file is not intended to be imported.")
