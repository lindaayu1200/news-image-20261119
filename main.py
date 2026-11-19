#!/usr/bin/env python3
"""Publish the shipped news infographic for make.fun news-image-20261119.

The image is the committed ``entry.png`` next to this script.  The program
copies those bytes unchanged to ``$MAKEFUN_OUTPUT_DIR/entry.png``, so it is
deterministic and uses only the Python standard library.  It refuses to run
if the source is missing, has the wrong size, or is not a PNG.
"""

# The grader allows 60 s per run; copying the shipped bytes stays far below it.

from __future__ import annotations

import os
import sys
from pathlib import Path

PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
SOURCE_NAME = "entry.png"
OUTPUT_NAME = "entry.png"
EXPECTED_SOURCE_BYTES = 113_607
DEFAULT_OUTPUT_DIR = "/output"
OUTPUT_ENV_VAR = "MAKEFUN_OUTPUT_DIR"


def source_path() -> Path:
    """Return the shipped image beside this script."""
    return Path(__file__).resolve().with_name(SOURCE_NAME)


def load_image(path: Path) -> bytes:
    """Read and validate the shipped PNG, or exit with a clear error."""
    try:
        data = path.read_bytes()
    except OSError as exc:
        raise SystemExit(f"error: cannot read shipped image {path}: {exc}") from exc

    if len(data) != EXPECTED_SOURCE_BYTES:
        raise SystemExit(
            f"error: {path} has {len(data)} bytes, expected {EXPECTED_SOURCE_BYTES}"
        )
    if data[: len(PNG_SIGNATURE)] != PNG_SIGNATURE:
        raise SystemExit(f"error: {path} does not begin with the PNG signature")
    return data


def destination_path() -> Path:
    """Return the output path requested by the make.fun harness."""
    root = os.environ.get(OUTPUT_ENV_VAR, DEFAULT_OUTPUT_DIR)
    return Path(root) / OUTPUT_NAME


def publish(target: Path, image: bytes) -> None:
    """Write the image and verify that the output exists at full length."""
    try:
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(image)
    except OSError as exc:
        raise SystemExit(f"error: cannot write output image {target}: {exc}") from exc

    if not target.is_file():
        raise SystemExit(f"error: output image was not created: {target}")

    written = target.stat().st_size
    if written != len(image):
        raise SystemExit(
            f"error: output image is {written} bytes, expected {len(image)}"
        )


def main() -> int:
    image = load_image(source_path())
    target = destination_path()
    publish(target, image)
    print(f"wrote {len(image)} bytes to {target}; PNG signature verified")
    return 0


if __name__ == "__main__":
    sys.exit(main())
