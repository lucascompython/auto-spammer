import argparse
import json
import shutil
import subprocess
import sys
from time import perf_counter
import os 
import os.path

OS = sys.platform

class Colors():
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"
    RESET = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"

def parse_cli() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--dev", help="Build the project in development mode", action="store_true")
    parser.add_argument("-r", "--release", help="Build the project in release mode", action="store_true")
    parser.add_argument("-u", "--upx", help="Use UPX for extra compression, not recommended on slow PC's", action="store_true")
    parser.add_argument("-t", "--target", help="Specify the target OS", choices=("win32", "linux"), default=OS)

    return parser.parse_args()


def build_go(target: str, upx: bool):
    io_handler_path = os.path.join("src-tauri", "src", "io_handler")
    print(Colors.BLUE + "Building Go code..." + Colors.RESET)
    start = perf_counter()
    cmds = f"go build -v -buildmode=c-shared -o libio.{'a' if target == 'linux' else 'dll'} -ldflags='-w -s' io.go"
    
    if target == "win32" and OS == "linux": # Cross compiling from linux to windows
        extra_args = "GOOS=windows GOARCH=amd64 CGO_ENABLED=1 CC=x86_64-w64-mingw32-gcc CXX=x86_64-w64-mingw32-g++ "
        cmds = extra_args + cmds
    elif target == "linux" and OS == "win32": # Cross compiling from windows to linux
        extra_args = "GOOS=linux GOARCH=amd64 "
        cmds = extra_args + cmds
    subprocess.run(cmds, cwd=io_handler_path, shell=True)
    print(Colors.GREEN + f"Done Building! Took {Colors.BOLD}{perf_counter() - start:.2f}s{Colors.RESET}" + Colors.RESET)
    if upx and target == "linux":
        print(f"{Colors.YELLOW}WARNING:{Colors.RESET} UPX cannot be used on .a files!")
        return
    if upx:
        start = perf_counter()
        print(Colors.BLUE + "Compressing library with UPX..." + Colors.RESET)
        subprocess.run(["upx", "--ultra-brute", f"libio.{'a' if target == 'linux' else 'dll'}" ], cwd=io_handler_path)
        print(Colors.GREEN + f"Done compressing! Took {Colors.BOLD}{perf_counter() - start:.2f}s{Colors.RESET}" + Colors.RESET)


def tauri_config(target: str):
    with open("./src-tauri/tauri.conf.json", "r") as f:
        tauri_config = json.load(f)
    
    external_bin = tauri_config["tauri"]["bundle"]["resources"]
    external_bin.clear()
    match target:
        case "win32":
            external_bin.append("./libio.dll")
        case "linux":
            external_bin.append("./libio.a")

    with open("./src-tauri/tauri.conf.json", "w") as f:
        json.dump(tauri_config, f, indent=4)
    
def build_tauri(target: str, upx: bool, dev: bool):
    print(Colors.BLUE + "Building Tauri..." + Colors.RESET)
    for file in os.listdir("./src-tauri"):
        if file.endswith(".dll") or file.endswith(".a") or file.endswith(".h"):
            os.remove(os.path.join("./src-tauri", file))

    shutil.copyfile(f"./src-tauri/src/io_handler/libio.{'a' if target == 'linux' else 'dll'}", f"./src-tauri/libio.{'a' if target == 'linux' else 'dll'}")
    if dev:
        subprocess.run(["cargo", "tauri", "dev"])
    else:
        start = perf_counter()
        cargo_target = ""
        if target == "linux":
            cargo_target = "x86_64-unknown-linux-gnu"
        elif target == "win32" and OS == "linux":
            cargo_target = "x86_64-pc-windows-gnu"
        elif target == "win32" and OS == "win32":
            cargo_target = "x86_64-pc-windows-msvc"
        subprocess.run(["cargo", "tauri", "build", "--target", cargo_target], cwd="src-tauri")
        print(Colors.GREEN + f"Done Building! Took {perf_counter() - start:.2f}s" + Colors.RESET)
        if upx:
            start = perf_counter()
            print(Colors.BLUE + "Compressing app with UPX..." + Colors.RESET)
            subprocess.run(["upx", "--ultra-brute", f"auto-spammer{'.exe' if target == 'win32' else ''}" ], cwd=f"src-tauri/target/{cargo_target}/release")
            print(Colors.GREEN + f"Done compressing! Took {perf_counter() - start:.2f}s" + Colors.RESET)
    os.remove(f"./src-tauri/libio.{'a' if target == 'linux' else 'dll'}")

def main():
    args = parse_cli()
    if not args.dev and not args.release:
        sys.stderr.write(f"{Colors.RED}ERROR:{Colors.RESET} You must specify a build mode!\n")
        sys.exit(1)

    if args.dev and args.release:
        sys.stderr.write(f"{Colors.RED}ERROR:{Colors.RESET} You cannot specify both development and release mode!\n")
        sys.exit(1)

    if not args.dev: # Build go code only if we are in release mode because of the cross compiling and UPX. 
        #The go code is built in dev mode by tauri
        build_go(args.target, args.upx)

    tauri_config(args.target)

    build_tauri(args.target, args.upx, args.dev)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nExiting...")
        sys.exit(0)
else:
    sys.stderr.write(f"{Colors.RED}ERROR:{Colors.RESET} This file is not meant to be imported!\n")
    sys.exit(1)