import argparse
import json
import os
import os.path
import shutil
import subprocess
import sys
from time import perf_counter

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
    parser = argparse.ArgumentParser(description="Build script for Auto Spammer, only supports Windows and Linux")
    parser.add_argument("-d", "--dev", help="Build the project in development mode", action="store_true")
    parser.add_argument("-r", "--release", help="Build the project in release mode", action="store_true")
    parser.add_argument("-u", "--upx", help="Use UPX for extra compression, not recommended on slow PC's", action="store_true")
    parser.add_argument("-t", "--target", help="Specify the target OS", choices=("win32", "linux", "all"), default=OS)
    parser.add_argument("-c", "--clean", help="Clean the project", action="store_true")
    parser.add_argument("-sg", "--skip-go", help="Skip building the Go code (assuming the library is already in place)", action="store_true")
    parser.add_argument("-st", "--skip-tauri", help="Skip building the Tauri code (only builds go code)", action="store_true")
    parser.add_argument("-n", "--use-nightly", help="UNSTABLE: Use the nightly toolchain for an even smaller App binary size (does not affect the size of library)", action="store_true")

    return parser.parse_args()


def build_go(target: str, upx: bool):
    io_handler_path = os.path.join("src-tauri", "src", "io_handler")
    print(Colors.BLUE + "Building Go code..." + Colors.RESET)
    start = perf_counter()
    cmds = f"go build -v -a -gcflags=all='-l -B -wb=false' -ldflags='-w -s' -buildmode=c-shared -o libio.{'a' if target == 'linux' else 'dll'} io.go"
    
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
    
def build_tauri(target: str, upx: bool, dev: bool, use_nightly: bool):
    print(Colors.BLUE + "Building Tauri..." + Colors.RESET)
    for file in os.listdir("./src-tauri"):
        if file.endswith(".dll") or file.endswith(".a") or file.endswith(".h"):
            os.remove(os.path.join("./src-tauri", file))
    


    shutil.copyfile(f"./src-tauri/src/io_handler/libio.{'a' if target == 'linux' else 'dll'}", f"./src-tauri/libio.{'a' if target == 'linux' else 'dll'}")
    try:
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
            cmds = ["cargo", "tauri", "build", "--target", cargo_target]
            if use_nightly:
                print(Colors.YELLOW + "WARNING: Using nightly toolchain, this may break the build!" + Colors.RESET)
                os.rename("./.rust-toolchain.toml", "./rust-toolchain.toml")
                cmds.extend(["--", "-Z", "build-std=std,panic_abort", "-Z", "build-std-features=panic_immediate_abort"])

            try:
                subprocess.run(cmds, cwd="src-tauri")
                print(Colors.GREEN + f"Done Building! Took {perf_counter() - start:.2f}s" + Colors.RESET)
                if upx:
                    start = perf_counter()
                    print(Colors.BLUE + "Compressing app with UPX..." + Colors.RESET)
                    subprocess.run(["upx", "--ultra-brute", f"auto-spammer{'.exe' if target == 'win32' else ''}" ], cwd=f"src-tauri/target/{cargo_target}/release")
                    print(Colors.GREEN + f"Done compressing! Took {perf_counter() - start:.2f}s" + Colors.RESET)
            finally:
                if use_nightly:
                    os.rename("./rust-toolchain.toml", "./.rust-toolchain.toml")
    finally:
        os.remove(f"./src-tauri/libio.{'a' if target == 'linux' else 'dll'}")



def clean():
    print(Colors.BLUE + "Cleaning..." + Colors.RESET)
    subprocess.run(["cargo", "clean"], cwd="src-tauri")
    for file in os.listdir("./src-tauri"): # Remove all the .dll and .a files form the src-tauri folder
        if file.endswith(".dll") or file.endswith(".a") or file.endswith(".h"):
            os.remove(os.path.join("./src-tauri", file))
    for file in os.listdir("./src-tauri/src/io_handler"): # Remove all the .dll and .a files form the io_handler folder
        if file.endswith(".dll") or file.endswith(".a") or file.endswith(".h") or file.endswith(".upx"):
            os.remove(os.path.join("./src-tauri/src/io_handler", file))
    print(Colors.GREEN + "Done cleaning!" + Colors.RESET)


def main():
    args = parse_cli()
    if not args.dev and not args.release and not args.clean and not args.skip_tauri:
        sys.stderr.write(f"{Colors.RED}ERROR:{Colors.RESET} You must specify a build mode!\n")
        sys.exit(1)

    if args.dev and args.release:
        sys.stderr.write(f"{Colors.RED}ERROR:{Colors.RESET} You cannot specify both development and release mode!\n")
        sys.exit(1)
    
    if args.target == "win32" and OS == "linux" and args.use_nightly:
        sys.stderr.write(f"{Colors.RED}ERROR:{Colors.RESET} You cannot use the nightly std optimization to cross compile from Linux to Windows!\n")

    is_all = False
    if args.target == "all":
        args.target = "linux" 
        is_all = True
    
    if args.target == "linux":
        print(Colors.MAGENTA + Colors.BOLD + "Building for Linux" + Colors.RESET)
    elif args.target == "win32":
        print(Colors.MAGENTA + Colors.BOLD + "Building for Windows" + Colors.RESET)

    if args.dev and args.skip_go:
        print(f"{Colors.YELLOW}WARNING:{Colors.RESET} Skipping go build in dev mode does nothing because the go code is built by rust!")

    if args.clean:
        clean()
        if not args.dev and not args.release: # If we are not building anything, exit
            sys.exit(0)

    if not args.dev and not args.skip_go: # Build go code only if we are in release mode because of the cross compiling and UPX. 
        # The go code is built in dev mode by tauri
        build_go(args.target, args.upx)

    if not args.skip_tauri:
        tauri_config(args.target)

        build_tauri(args.target, args.upx, args.dev, args.use_nightly)
    
    if is_all:
        print(Colors.MAGENTA + Colors.BOLD + "Building for Windows" + Colors.RESET)
        args.target = "win32"
        if not args.dev and not args.skip_go:
            build_go(args.target, args.upx)
        if not args.skip_tauri:
            tauri_config(args.target)
            build_tauri(args.target, args.upx, args.dev, args.use_nightly)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nExiting...")
        sys.exit(0)
else:
    sys.stderr.write(f"{Colors.RED}ERROR:{Colors.RESET} This file is not meant to be imported!\n")
    sys.exit(1)