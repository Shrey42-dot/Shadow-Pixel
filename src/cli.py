# src/cli.py

import argparse
import sys

from stego_utils import (
    hide_secret_in_image,
    reveal_secret_from_image,
)


def main() -> None:
    parser = argparse.ArgumentParser(
    prog="shadow-pixel",
    description=(
        "Shadow-Pixel — Invisible Cryptographic Steganography\n\n"
        "Hide encrypted secrets inside ordinary images using AES-GCM "
        "and LSB pixel encoding."
    ),
    epilog=(
        "Examples:\n"
        "  shadow-pixel hide --image cat.png --out secret.png "
        "--msg \"hello\" --key password\n"
        "  shadow-pixel reveal --image secret.png --key password\n"
    ),
    formatter_class=argparse.RawTextHelpFormatter,
)


    subparsers = parser.add_subparsers(dest="command", required=True)

    # --------------------
    # hide command
    # --------------------
    hide_parser = subparsers.add_parser(
        "hide", help="Hide a secret message inside an image"
    )
    hide_parser.add_argument(
        "--image", required=True, help="Path to input image"
    )
    hide_parser.add_argument(
        "--out", required=True, help="Path to output stego image"
    )
    hide_parser.add_argument(
        "--msg", required=True, help="Secret message to hide"
    )
    hide_parser.add_argument(
        "--key", required=True, help="Encryption password"
    )

    # --------------------
    # reveal command
    # --------------------
    reveal_parser = subparsers.add_parser(
        "reveal", help="Reveal a hidden secret from an image"
    )
    reveal_parser.add_argument(
        "--image", required=True, help="Path to stego image"
    )
    reveal_parser.add_argument(
        "--key", required=True, help="Encryption password"
    )

    args = parser.parse_args()

    try:
        if args.command == "hide":
            hide_secret_in_image(
                args.image,
                args.out,
                args.msg,
                args.key,
            )
            print("[+] Secret successfully hidden")

        elif args.command == "reveal":
            secret = reveal_secret_from_image(
                args.image,
                args.key,
            )
            print("[+] Revealed secret:")
            print(secret)

    except Exception as e:
        print(f"[!] Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
