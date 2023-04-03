import subprocess
import os
import sys
import argparse
import json
from time import perf_counter

OS = sys.platform

def parse_cli() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--dev", help="Build the project in development mode", action="store_true")
    parser.add_argument("-r", "--release", help="Build the project in release mode", action="store_true")
    parser.add_argument("-u", "--upx", help="Use UPX for extra compression, not recommended on slow PC's", action="store_true")
    parser.add_argument("-t", "--target", help="Specify the target OS", choices=("win32", "linux"), default=OS)

    return parser.parse_args()


def build_go(target: str, upx: bool, dev: bool):
    print("Building Go code...")
    start = perf_counter()
    cmds = ["go", "build", "-buildmode=c-shared", "-o", f"libio.{'a' if target == 'linux' else 'dll'}", "-ldflags", "'-w", "-s'", "io.go"]
    shell = False 
    if target == "win32" and OS == "linux":
        extra_args = ["GOOS=windows", "GOARCH=amd64", "CGO_ENABLED=1", "CC=x86_64-w64-mingw32-gcc", "CXX=x86_64-w64-mingw32-g++"]

        cmds = extra_args + cmds
        shell = True
        cmds = " ".join(cmds)
    subprocess.run(cmds, cwd="io_handler", shell=shell)
    print(f"Done Building! Took {perf_counter() - start:.2f}s")
    if upx and target == "linux":
        sys.stderr.write("ERROR: UPX cannot be used on .a files!")
        sys.exit(1)
    if upx and dev:
        sys.stderr.write("ERROR: UPX cannot be used in development mode!")
        sys.exit(1)
    if upx:
        start = perf_counter()
        print("Compressing with UPX...")
        subprocess.run(["upx", "--ultra-brute", f"libio.{'a' if target == 'linux' else 'dll'}" ], cwd="io_handler")
        print(f"Done compressing! Took {perf_counter() - start:.2f}s")




def main():
    args = parse_cli()
    if not args.dev and not args.release:
        sys.stderr.write("ERROR: You must specify a build mode!")
        sys.exit(1)
    
    if args.dev and args.release:
        sys.stderr.write("ERROR: You cannot specify both development and release mode!")
        sys.exit(1)

    build_go(args.target, args.upx, args.dev)

    with open("./src-tauri/tauri.conf.json", "r") as f:
        tauri_config = json.load(f)
    
    external_bin = tauri_config["tauri"]["bundle"]["externalBin"]
    external_bin.clear()
    match args.target:
        case "win32":
            external_bin.append("io_handler/libio.dll")
        case "linux":
            external_bin.append("io_handler/libio.a")

    with open("./src-tauri/tauri.conf.json", "w") as f:
        json.dump(tauri_config, f, indent=4)
    
    print("Building Tauri...")
    if args.dev:
        subprocess.run(["tauri", "build", "--dev"], cwd="src-tauri")
    else:
        start = perf_counter()
        target = ""
        if target == "linux":
            target = "x86_64-pc-windows-gnu"
        elif target == "win32" and OS == "linux":
            target = "x86_64-pc-windows-gnu"
        elif target == "win32" and OS == "win32":
            target = "x86_64-pc-windows-msvc"

        subprocess.run(["cargo", "tauri", "build", "--target", target], cwd="src-tauri")
        print(f"Done Building! Took {perf_counter() - start:.2f}s")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nExiting...")
        sys.exit(0)
else:
    sys.stderr.write("ERROR: This file is not meant to be imported!")
    sys.exit(1)