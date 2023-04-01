import subprocess
import sys
import argparse

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='Builds the go version of the io_handler.')
    parser.add_argument("-r", "--run", help="Builds the go version of the io_handler and runs it.", action="store_true")
    parser.add_argument("-b", "--build", help="Builds the go version of the io_handler.", action="store_true")
    return parser.parse_args()


def main():
    args = parse_args()

    if args.run:
        subprocess.run(['go', 'run', 'main.go'])
        return

    if args.build:
        subprocess.run(['go', 'build', 'main.go'])    
        return



if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(0)
else:
    sys.stderr.write('This script is not meant to be imported.')
    sys.exit(1)

