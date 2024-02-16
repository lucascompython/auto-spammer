#!/usr/bin/env python3

import argparse
import os
import sys
import subprocess
from time import perf_counter
from shutil import rmtree

OS = sys.platform
if OS == "win32":
    OS = "windows"
VERBOSE = False


class Colors:
    """ANSI color codes."""
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    MAGENTA = "\033[95m"
    CYAN = "\033[96m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
    ITALIC = "\033[3m"
    END = "\033[0m"

    @classmethod
    def warning_message(cls, message: str) -> str:
        return f"{cls.YELLOW}{cls.BOLD}WARNING:{cls.END} {message}"
    
    @classmethod
    def error_message(cls, message: str) -> str:
        return f"{cls.RED}{cls.BOLD}ERROR:{cls.END} {message}"
    
    @classmethod
    def success_message(cls, message: str) -> str:
        return f"{cls.GREEN}{cls.BOLD}Sucess:{cls.END} {message}"
    
    @classmethod
    def info_message(cls, message: str) -> str:
        return f"{cls.BLUE}{cls.BOLD}INFO:{cls.END} {message}"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=f"{Colors.UNDERLINE}Auto-Spammer{Colors.END} build script.")

    parser.add_argument("-d", "--dev", action="store_true", help="Run in development mode.")
    parser.add_argument("-r", "--release", action="store_true", help="Run in release mode.")
    parser.add_argument("-c", "--clean", action="store_true", help="Cleans the build directories and dependencies.")
    parser.add_argument("-v", "--verbose", action="store_true", help="Prints verbose output.")
    parser.add_argument("-u", "--upx", action="store_true", help=Colors.warning_message("WARNING:  Compress the executable using UPX. Might cause false positives in some antivirus software."))
    parser.add_argument("-t", "--target", type=str, help=f"The target platform to build for. Default: {Colors.BOLD + OS + Colors.END} (current OS)", choices=("windows", "linux"), default=OS)
    parser.add_argument("-n", "--nightly", action="store_true", help=Colors.warning_message(f"WARNING:  Build using the {Colors.UNDERLINE} nightly {Colors.END} toolchain for a smaller binary size."))
    parser.add_argument("--run", action="store_true", help="Run the executable after building.")
    parser.add_argument("--native", action="store_true", help=f"Build using the {Colors.ITALIC} 'target-cpu=native' {Colors.END} flag. This will optimize the binary for the current CPU architecture.")
    parser.add_argument("-s", "--smallest", action="store_true", help="Build the smallest possible binary size")

    return parser.parse_args()

def verbose_print(message) -> None:
    if VERBOSE:
        print(message)


def run_command(command: tuple[str], **kwargs) -> None:  
    try:
        if VERBOSE:
            subprocess.run(command, check=True, **kwargs)
        else:
            with open(os.devnull, "w") as devnull:
                subprocess.Popen(command, stdout=devnull, stderr=devnull, **kwargs).wait()

    except subprocess.CalledProcessError as e:
        sys.stderr.write(f"{Colors.error_message(f'{e}')}\n")
        sys.exit(1)



def clean() -> None:
    print(Colors.info_message("Cleaning build directories and dependencies..."))
    if VERBOSE:
        start = perf_counter()

    run_command(("cargo", "clean"), cwd="src-tauri")

    try:
        rmtree("src-frontend/dist")
    except FileNotFoundError:
        pass
    
    try:
        rmtree("src-frontend/node_modules")
    except FileNotFoundError:
        pass
    
    if VERBOSE:
        end = perf_counter()
        print(f"{Colors.success_message(f'Cleaned build directories and dependencies in {end - start:.2f} seconds.')}\n")
        





def check_node_modules() -> None:   
    if not os.path.exists("src-frontend/node_modules"):
        print(Colors.info_message("Installing frontend dependencies..."))
        run_command(("bun", "install"), cwd="src-frontend")
    

def is_mingw_installed() -> bool:
    try:
        subprocess.run(
            ("gcc", "--version"),
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=True,
        )
        return True
    except FileNotFoundError:
        return False
    except subprocess.CalledProcessError:
        return False

def get_target(target: str) -> str:

    if target == "linux":
        return "x86_64-unknown-linux-gnu"
    elif target == "linux" and OS == "windows":
        if is_mingw_installed():
            return "x86_64-unknown-linux-gnu"
        return "x86_64-unknown-linux-musl"

    elif target == "windows" and OS == "linux":
        return "x86_64-pc-windows-gnu"

    elif target == "windows" and OS == "windows":
        if is_mingw_installed():
            return "x86_64-pc-windows-gnu"
        
        return "x86_64-pc-windows-msvc"
    
    else:
        sys.stderr.write(f"{Colors.error_message(f"Invalid target: {target}.")}\n")
        sys.exit(1)

def get_app_name(target: str) -> str:
    app_name = "auto-spammer"
    if target == "windows":
        app_name += ".exe"

    return app_name

def build_release(args: argparse.Namespace) -> None:    
    print(Colors.info_message("Building in release mode..."))
    check_node_modules()

    target = get_target(args.target)

    if args.smallest:
        args.nightly = True
        args.upx = True

    command = ["cargo", "tauri", "build", f"--target {target}"]  
    rustflags = []

    if "msvc" in target:
        rustflags.append("-C target-feature=+crt-static") # Make sure the binary is statically linked
        rustflags.append("-C linker=rust-lld")

    if args.nightly:    
        command.insert(1, "+nightly")
        rustflags.append("-Zlocation-detail=none")

        command.extend([
            "--",
            "-Z",
            "build-std=std,panic_abort",
            "-Z",
            "build-std-features=panic_immediate_abort",
        ])
    
    if args.native:
        rustflags.append("-C target-cpu=native")
    
    run_command(f"RUSTFLAGS='{" ".join(rustflags)}' " + " ".join(command), cwd="src-tauri",  shell=True)

    if args.upx:
        print(Colors.info_message("Compressing executable using UPX..."))

        run_command(
            (
                "upx",
                "--ultra-brute",
                f"src-tauri/target/{target}/release/{get_app_name(args.target)}",
            )
        )

def convert_bytes(num: int | float | str) -> str:
    if isinstance(num, str):
        num = float(num)
    """
    this function will convert bytes to MB.... GB... etc
    """
    for x in ["bytes", "KB", "MB", "GB", "TB"]:
        if num < 1024.0:
            return "%3.1f %s" % (num, x)
        num /= 1024.0
    return f"{num:.1f} PB"

def get_size(target: str) -> str:
    target = get_target(target)
    app_name = get_app_name(target)


    try:
        size = os.path.getsize(f"src-tauri/target/{target}/release/{app_name}")
        return convert_bytes(size)
    except FileNotFoundError:
        print(Colors.warning_message(f"Executable not found at {Colors.UNDERLINE}src-tauri/target/{target}/release/{app_name}{Colors.END}."))
        return "N/A"


def run_app(target: str) -> None:
    if OS != target:
        print(Colors.warning_message(f"Cannot run {target} executable on {OS}."))
        return

    app_path = f"./src-tauri/target/{get_target(target)}/release/{get_app_name(target)}"


    if OS == "linux":
        command = ["/usr/bin/time", "-f", "'%M'", app_path]
    elif OS == "windows":
        #command = ["powershell", "-Command", f"Measure-Command {{ {command} }}"]
        command = [
            "powershell",
            "-ExecutionPolicy",
            "Bypass",
            "-File",
            "get_peak_mem.ps1",
            app_path
        ]
    else:
        sys.stderr.write(f"{Colors.error_message(f"Unsupported OS: {OS}.")}\n")
        sys.exit(1)
    
    print(Colors.info_message(f"Running {app_path}..."))
    proc = subprocess.run(command, capture_output=True)

    if proc.returncode != 0:
        sys.stderr.write(f"{Colors.error_message(f"Error running {app_path}.")}\n")
        sys.exit(1)
    
    if OS == "linux":
        peak_mem = proc.stderr.decode().strip().replace("'", "")
    else:
        peak_mem = proc.stdout.decode().strip()

    peak_mem = convert_bytes(peak_mem + "000" if OS == "linux" else "")

    print(Colors.info_message(f"Peak Memory Usage: {Colors.BOLD}{peak_mem}{Colors.END}"))

def main() -> None:
    args = parse_args()
    global VERBOSE
    VERBOSE = args.verbose

    if args.dev and args.release:
        sys.stderr.write(f"{Colors.error_message('Cannot use both --dev and --release flags at the same time.')}\n")
        sys.exit(1)
    
    if args.clean: 
        clean()


    if args.dev:
        print(Colors.info_message("Building in development mode..."))
        check_node_modules() 
        VERBOSE = True # Always print output in development mode
        run_command(("cargo", "tauri", "dev"), cwd="src-tauri")  
        VERBOSE = args.verbose # Reset verbosity to user's preference

    elif args.release or args.smallest:
        build_release(args)
        print(Colors.info_message(f"{Colors.BOLD}Executable Size: {get_size(args.target)}"))

    if args.run:
        run_app(args.target)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Colors.MAGENTA}Exiting...{Colors.END}")
else:
    sys.stderr.write(f"{Colors.error_message('This script cannot be imported.')}\n")
    sys.exit(1)