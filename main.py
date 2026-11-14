#!/usr/bin/env python3
"""Deliver the round-3 front page for news-image-01.

The image (entry.png, next to this script) is a code-drawn newspaper
front page: 32 stories first reported Friday 13 November 2026, six
continents, one page, rendered by render.py in this repository so every
character is exactly the verified text. This program only delivers it:
it checks the file is a real PNG within the 1 MiB limit, copies it to
$MAKEFUN_OUTPUT_DIR/entry.png (default /output/entry.png), and confirms
the copy is byte-identical to the source so repeated runs are
deterministic.
"""

import os
import shutil
import struct
import sys
from pathlib import Path

MAX_BYTES = 1_048_576
MAX_SIDE = 1024
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"


def problem_with(blob: bytes) -> str | None:
    if len(blob) > MAX_BYTES:
        return f"entry.png is {len(blob)} bytes, over the 1 MiB limit"
    if not blob.startswith(PNG_MAGIC):
        return "entry.png does not start with the PNG magic bytes"
    if len(blob) < 33 or blob[12:16] != b"IHDR":
        return "entry.png has no IHDR chunk"
    width, height = struct.unpack(">II", blob[16:24])
    if width > MAX_SIDE or height > MAX_SIDE:
        return f"entry.png is {width}x{height}, over the 1024x1024 limit"
    return None


def main() -> int:
    here = Path(__file__).resolve().parent
    src = here / "entry.png"
    dest_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    dest = dest_dir / "entry.png"

    blob = src.read_bytes()
    bad = problem_with(blob)
    if bad is not None:
        print(bad, file=sys.stderr)
        return 1

    dest_dir.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(src, dest)

    if dest.read_bytes() != blob:
        print("copied entry.png differs from the bundled image", file=sys.stderr)
        return 1
    print(f"wrote {dest} ({len(blob)} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
