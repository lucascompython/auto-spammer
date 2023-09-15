#!/usr/bin/env python3
import argparse
import os
import subprocess
import sys
from shutil import rmtree
from time import perf_counter

OS = sys.platform
if OS == "win32":
    OS = "win"


class Colors:
    RED: str = "\033[91m"
    GREEN: str = "\033[92m"
    YELLOW: str = "\033[93m"
    BLUE: str = "\033[94m"
    PURPLE: str = "\033[95m"
    CYAN: str = "\033[96m"
    WHITE: str = "\033[97m"
    BOLD: str = "\033[1m"
    UNDERLINE: str = "\033[4m"
    ITALIC: str = "\033[3m"
    END: str = "\033[0m"

    @classmethod
    def warning_message(cls, message: str) -> None:
        print(f"{cls.YELLOW}WARNING:{cls.END} {message}")

    @classmethod
    def info_message(cls, message: str) -> None:
        print(f"{cls.BLUE}INFO:{cls.END} {message}")

    @classmethod
    def success_message(cls, message: str) -> None:
        print(f"{cls.GREEN}SUCCESS:{cls.END} {message}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=f"Build script for {Colors.UNDERLINE}Auto Spammer{Colors.END}."
    )

    parser.add_argument(
        "-d", "--dev", action="store_true", help="Run in development mode."
    )
    parser.add_argument(
        "-r", "--release", action="store_true", help="Build in release mode."
    )
    parser.add_argument(
        "-c",
        "--clean",
        action="store_true",
        help=f"Clean the {Colors.UNDERLINE}build{Colors.END} directory, {Colors.UNDERLINE}node_modules{Colors.END} and {Colors.UNDERLINE}dist{Colors.END} directory.",
    )
    parser.add_argument(
        "-u",
        "--upx",
        action="store_true",
        help=f"{Colors.YELLOW}UNSTABLE:{Colors.END} Compress the executable with {Colors.UNDERLINE}UPX{Colors.END}. Might flag the app as virus.",
    )
    parser.add_argument(
        "-t",
        "--target",
        type=str,
        help=f"The target platform to build for. Default: Current OS ({Colors.BOLD + OS + Colors.END}).",
        choices=("win", "linux"),
        default=OS,
    )
    parser.add_argument(
        "-n",
        "--nightly",
        action="store_true",
        help=f"{Colors.YELLOW}UNSTABLE:{Colors.END} Use the {Colors.UNDERLINE}nightly{Colors.END} toolchain for a smaller binary size.",
    )
    parser.add_argument(
        "-ru",
        "--run",
        action="store_true",
        help="Run the program. If building will run after compiling.",
    )
    parser.add_argument(
        "-m",
        "--mold",
        action="store_true",
        help=f"Use {Colors.BOLD}MOLD{Colors.END} linker only for {Colors.UNDERLINE}Linux{Colors.END}.",
    )
    parser.add_argument(
        "-na",
        "--native",
        action="store_true",
        help=f"Use the {Colors.ITALIC}'target-cpu=native'{Colors.END} RUSTFLAG.",
    )
    parser.add_argument(
        "-front",
        nargs="*",
        help=f"Run commands in {Colors.UNDERLINE}src-frontend{Colors.END}.",
    )
    parser.add_argument(
        "-back",
        nargs="*",
        help=f"Run commands in {Colors.UNDERLINE}src-tauri{Colors.END}.",
    )
    smallest = parser.add_mutually_exclusive_group()
    smallest.add_argument(
        "-s",
        "--smallest",
        action="store_true",
        help=f"Build the smallest binary possible. {Colors.UNDERLINE}UPX{Colors.END} and {Colors.UNDERLINE}nightly{Colors.END} are enabled.",
    )
    return parser.parse_args()


def error_message(message: str, exit: bool = False) -> None:
    sys.stderr.write(f"{Colors.RED}ERROR:{Colors.END} {message}\n")
    if exit:
        sys.exit(1)


def check_node_modules() -> None:
    if not os.path.isdir("src-frontend/node_modules"):
        Colors.info_message("Installing frontend dependencies...")
        subprocess.run(["pnpm" + ".cmd" * (OS == "win"), "install"], cwd="src-frontend")


def build_tauri(target: str, mode: str, nightly: bool) -> None:
    if mode == "dev":
        Colors.info_message("Building in development mode...")
        subprocess.run(["cargo", "tauri", "dev"], cwd="src-tauri")
    elif mode == "release":
        start = perf_counter()
        Colors.info_message("Building in release mode...")
        args = ["cargo", "tauri", "build", "--target", target]
        if nightly:
            args.extend(
                [
                    "--",
                    "-Z",
                    "build-std=std,panic_abort",
                    "-Z",
                    "build-std-features=panic_immediate_abort",
                ]
            )
        tauri = subprocess.run(args, cwd="src-tauri")
        if tauri.returncode != 0:
            error_message(
                f"Tauri failed to build after {Colors.BOLD}{perf_counter() - start:.2f}{Colors.END} seconds.",
            )
        else:
            Colors.success_message(
                f"Built in {Colors.BOLD}{perf_counter() - start:.2f}{Colors.END} seconds!"
            )
    else:
        error_message("Invalid build mode.", True)


def clean() -> None:
    Colors.info_message("Cleaning...")
    start = perf_counter()
    subprocess.run(["cargo", "clean"], cwd="src-tauri")
    try:
        rmtree("src-frontend/dist")
    except FileNotFoundError:
        Colors.info_message(
            f"{Colors.BOLD}dist{Colors.END} directory not found. {Colors.UNDERLINE}Skipping...{Colors.END}"
        )
    try:
        rmtree("src-frontend/node_modules")
    except FileNotFoundError:
        Colors.info_message(
            f"{Colors.BOLD}node_modules{Colors.END} directory not found. {Colors.UNDERLINE}Skipping...{Colors.END}"
        )

    Colors.success_message(
        f"Cleaned in {Colors.BOLD}{perf_counter() - start:.2f}{Colors.END} seconds!"
    )


def upx(target: str) -> None:
    Colors.warning_message("Using UPX may flag your executable as a virus.")
    Colors.info_message("Compressing executable with UPX...")
    start = perf_counter()
    u = subprocess.run(
        [
            "upx",
            "--ultra-brute",
            f"src-tauri/target/{target}/release/autospammer"
            + ".exe" * ("windows" in target),
        ],
    )
    if u.returncode != 0:
        error_message(
            f"Compression failed after {Colors.BOLD}{perf_counter() - start:.2f}{Colors.END} seconds.",
        )
    else:
        Colors.success_message(
            f"Compression complete in {Colors.BOLD}{perf_counter() - start:.2f}{Colors.END} seconds!"
        )


def config_toml(target: str, mold: bool = False, native: bool = False) -> None:
    os.mkdir("src-tauri/.cargo")
    with open("src-tauri/.cargo/config.toml", "w") as f:
        f.write(f"[target.{target}]\n")

        if mold and native:
            f.write(
                "linker = 'clang'\nrustflags = ['-C', 'target-cpu=native', '-C', 'link-arg=-fuse-ld=/usr/bin/mold']"
            )
        if mold and not native:
            f.write(
                "linker = 'clang'\nrustflags = ['-C', 'link-arg=-fuse-ld=/usr/bin/mold']"
            )
        if native and not mold:
            f.write("rustflags = ['-C', 'target-cpu=native']")


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


def get_size(mode: str, target: str) -> None:
    try:
        size = os.path.getsize(
            f"src-tauri/target/{target + '/release' if mode == 'release' else 'debug'}/autospammer"
            + (".exe" if "win" in target else "")
        )
        print(
            f"\n{Colors.BOLD}Executable size:{Colors.END} {Colors.CYAN + convert_bytes(size) + Colors.END}"
        )
    except FileNotFoundError:
        Colors.warning_message("Cannot get executable size.")


def run(target: str) -> None:
    args = [
        f"./src-tauri/target/{target}/release/autospammer" + ".exe" * ("win" in target)
    ]
    fail = False
    if OS == "linux":
        # check if /usr/bin/time exists
        if not os.path.isfile("/usr/bin/time"):
            fail = True
            Colors.warning_message(
                "GNU time command not found. Cannot get memory usage."
            )
        else:
            args = [
                "/usr/bin/time",
                "-f",
                '"%M"',
                *args,
            ]  # uses the GNU time command to get memory usage
    elif OS == "win":  # Windows sucks, and I hope it dies.
        args = [
            "powershell",
            "-ExecutionPolicy",
            "Bypass",
            "-File",
            "./get_peak_mem.ps1",
            *args,
        ]

    p = subprocess.run(args, capture_output=True)
    if p.returncode != 0:
        error_message("Failed to run executable.", True)

    if OS == "linux" and not fail:
        mem = (
            p.stderr.decode().strip().replace('"', "")
        )  # returns the memory usage in KB
        mem = convert_bytes(mem + "000")
        print(
            f"{Colors.BOLD}Peak memory usage:{Colors.END} {Colors.CYAN}{mem}{Colors.END}"
        )
    elif OS == "win" and not fail:
        mem = p.stdout.decode().strip().replace('"', "")
        mem = convert_bytes(mem)
        print(
            f"{Colors.BOLD}Peak memory usage:{Colors.END} {Colors.CYAN}~{mem}{Colors.END}"
        )  # Most of the times no accurate at all.


def main(args: argparse.Namespace) -> None:
    if args.front:
        subprocess.run(
            args.front,
            cwd="src-frontend",
        )
        return
    if args.back:
        subprocess.run(args.back, cwd="src-tauri")
        return

    if args.smallest:
        args.release = True
        args.upx = True
        args.nightly = True

    if args.clean:
        clean()

    target = args.target
    if target == "linux":
        target = "x86_64-unknown-linux-gnu"
    elif target == "win" and OS == "linux":
        target = "x86_64-pc-windows-gnu"
    elif target == "win" and OS == "win":
        target = "x86_64-pc-windows-msvc"

    if args.dev:
        mode = "dev"
    elif args.release:
        mode = "release"

    if not args.dev and not args.release:
        if args.clean:  # if we're cleaning and don't specify a build mode, we're done
            return

        if args.upx:
            upx(target)
            get_size("release", target)
            return

        if args.run:
            get_size("release", target)
            run(target)
            return
        error_message("You must specify either --dev or --release.", True)

    if args.dev and args.release:
        error_message("You cannot specify both --dev and --release.", True)

    if args.nightly:
        Colors.warning_message(
            "Using the nightly toolchain is unstable and may cause issues."
        )

    if args.native:
        Colors.warning_message(
            "Using the 'target-cpu=native' RUSTFLAG may cause issues on other machines."
        )

    check_node_modules()
    try:
        if args.nightly:
            os.rename("src-tauri/.rust-toolchain.toml", "src-tauri/rust-toolchain.toml")

        if args.mold or args.native:
            if args.mold and target != "x86_64-unknown-linux-gnu":
                Colors.warning_message(
                    f"{Colors.BOLD}Mold{Colors.END} is only available on Linux. {Colors.UNDERLINE}Skipping...{Colors.END}"
                )
                config_toml(target, False, args.native)
            else:
                config_toml(target, args.mold, args.native)

        build_tauri(target, mode, args.nightly)
    finally:
        if args.nightly:  # to not use nightly for the next build
            os.rename("src-tauri/rust-toolchain.toml", "src-tauri/.rust-toolchain.toml")

        if args.mold or args.native:
            rmtree("src-tauri/.cargo")

    if args.upx:
        if args.dev:
            Colors.warning_message(
                f"Cannot {Colors.UNDERLINE}compress{Colors.END} in development mode."
            )
        else:
            upx(target)

    get_size(mode, target)

    if args.run:
        if args.release:
            Colors.info_message("Running...")
            try:
                run(target)
            except FileNotFoundError:
                error_message("Executable not found.", True)
            Colors.info_message("Exiting...")
        else:
            Colors.warning_message(
                f"Cannot {Colors.UNDERLINE}run{Colors.END} in development mode."
            )


if __name__ == "__main__":
    try:
        args = parse_args()
        main(args)
    except KeyboardInterrupt:
        print(f"\n{Colors.PURPLE}Program interrupted by user. Quitting..{Colors.END}\n")
else:
    error_message(
        f"{Colors.BOLD}{__name__}{Colors.END} is not the main module.\n", True
    )
