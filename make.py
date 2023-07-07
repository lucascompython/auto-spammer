# /usr/bin/env python3
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
        help=f"Compress the executable with {Colors.UNDERLINE}UPX{Colors.END}.",
    )
    parser.add_argument(
        "-t",
        "--target",
        type=str,
        help="The target platform to build for.",
        choices=("win", "linux", "all"),
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
        help="Run the program after building if possible.",
    )
    parser.add_argument(
        "-m",
        "--mold",
        action="store_true",
        help=f"Use {Colors.BOLD}MOLD{Colors.END} linker only for {Colors.BOLD}Linux{Colors.END}.",
    )
    parser.add_argument(
        "-na",
        "--native",
        action="store_true",
        help=f"Use the {Colors.ITALIC}'target-cpu=native'{Colors.END} RUSTFLAG.",
    )
    parser.add_argument(
        "pnpm",
        nargs="*",
        help=f"Run {Colors.BOLD}pnpm{Colors.END} commands in {Colors.UNDERLINE}src-frontend{Colors.END}.",
    )
    parser.add_argument(
        "cargo",
        nargs="*",
        help=f"Run {Colors.BOLD}cargo{Colors.END} commands in {Colors.UNDERLINE}src-tauri{Colors.END}.",
    )

    return parser.parse_args()


def error_message(message: str, exit: bool = False) -> None:
    sys.stderr.write(f"{Colors.RED}Error:{Colors.END} {message}\n")
    if exit:
        sys.exit(1)


def warning_message(message: str) -> None:
    print(f"{Colors.YELLOW}Warning:{Colors.END} {message}")


def info_message(message: str) -> None:
    print(f"{Colors.BLUE}Info:{Colors.END} {message}")


def success_message(message: str) -> None:
    print(f"{Colors.GREEN}Success:{Colors.END} {message}")


def check_node_modules() -> None:
    if not os.path.isdir("src-frontend/node_modules"):
        info_message("Installing frontend dependencies...")
        subprocess.run(["pnpm" + ".cmd" * (OS == "win"), "install"], cwd="src-frontend")


def build_tauri(target: str, mode: str, nightly: bool) -> None:
    if mode == "dev":
        info_message("Building in development mode...")
        subprocess.run(["cargo", "tauri", "dev"], cwd="src-tauri")
    elif mode == "release":
        start = perf_counter()
        info_message("Building in release mode...")
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
        subprocess.run(args, cwd="src-tauri")
        success_message(f"Built in {perf_counter() - start:.2f} seconds.")
    else:
        error_message("Invalid build mode.", True)


def clean() -> None:
    info_message("Cleaning...")
    subprocess.run(["cargo", "clean"], cwd="src-tauri")
    try:
        rmtree("src-frontend/dist")
    except FileNotFoundError:
        info_message(
            f"{Colors.BOLD}dist{Colors.END} directory not found. {Colors.UNDERLINE}Skipping...{Colors.END}"
        )
    try:
        rmtree("src-frontend/node_modules")
    except FileNotFoundError:
        info_message(
            f"{Colors.BOLD}node_modules{Colors.END} directory not found. {Colors.UNDERLINE}Skipping...{Colors.END}"
        )

    info_message("Cleaned.")


def upx(target: str) -> None:
    warning_message("Using UPX may flag your executable as a virus.")
    info_message("Compressing executable with UPX...")
    subprocess.run(
        [
            "upx",
            "--ultra-brute",
            f"src-tauri/target/{target}/release/autospammer"
            + ".exe" * ("windows" in target),
        ]
    )
    info_message("Compression complete.")


def config_toml(target: str, mold: bool = False, native: bool = False) -> None:
    os.mkdir("src-tauri/.cargo")
    with open("src-tauri/.cargo/config.toml", "w") as f:
        f.write(f"[target.{target}]\n")

        if mold and native:
            f.write(
                "linker = 'clang'\nrustflags = ['-C', 'target-cpu=native', '-C', 'link-arg=-fuse-ld=/usr/bin/mold' ]"
            )
        if mold and not native:
            f.write(
                "linker = 'clang'\nrustflags = ['-C', 'link-arg=-fuse-ld=/usr/bin/mold' ]"
            )
        if native and not mold:
            f.write("rustflags = ['-C', 'target-cpu=native']")


def main(args: argparse.Namespace):
    if args.pnpm:
        subprocess.run(
            ["pnpm" + ".cmd" * (OS == "win"), *args.pnpm], cwd="src-frontend"
        )
        return
    if args.cargo:
        subprocess.run(["cargo", *args.cargo], cwd="src-tauri")
        return

    if args.clean:
        clean()

    if not args.dev and not args.release:
        if args.clean:  # if we're cleaning and don't specify a build mode, we're done
            return
        error_message("You must specify either --dev or --release.", True)

    if args.dev and args.release:
        error_message("You cannot specify both --dev and --release.", True)

    if args.nightly:
        warning_message("Using the nightly toolchain is unstable and may cause issues.")

    if args.native:
        warning_message(
            "Using the 'target-cpu=native' RUSTFLAG may cause issues on other machines."
        )

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

    check_node_modules()
    try:
        if args.nightly:
            os.rename("src-tauri/.rust-toolchain.toml", "src-tauri/rust-toolchain.toml")

        if args.mold or args.native:
            if args.mold and target != "x86_64-unknown-linux-gnu":
                warning_message(
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

    if args.run:
        if args.release:
            info_message("Running...")
            try:
                subprocess.run(
                    [
                        f"./src-tauri/target/{target}/release/autospammer"
                        + (".exe" if OS == "win" else "")
                    ]
                )
            except FileNotFoundError:
                error_message("Executable not found.", True)
            info_message("Exiting...")
        else:
            warning_message(
                f"Cannot {Colors.UNDERLINE}run{Colors.END} in development mode."
            )

    if args.upx:
        if args.dev:
            warning_message(
                f"Cannot {Colors.UNDERLINE}compress{Colors.END} in development mode."
            )
        else:
            upx(target)


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
