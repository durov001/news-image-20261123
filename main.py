#!/usr/bin/env python3
"""Entrypoint for the news-image-20261123 make.fun bounty.

The front page for Monday 23 November 2026 was rendered in advance and
ships with this repo as entry.png (1024x1024, cream newspaper front page,
37 stories). This entrypoint only places that file into the output
directory the grader provides. Standard library only, no network access,
fully deterministic: every run writes the same bytes.

The output directory belongs to the grader. We create it if it does not
exist and write into it; we never delete, replace, or clean it.
"""

import os
import sys
from pathlib import Path

IMAGE_NAME = "entry.png"


def locate_image() -> Path:
    """Path of the pre-rendered front page next to this file."""
    return Path(__file__).resolve().parent / IMAGE_NAME


def output_dir() -> Path:
    """Output directory from the environment, defaulting to ./out."""
    return Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "out"))


def main() -> int:
    source = locate_image()
    if not source.is_file():
        print(f"{IMAGE_NAME} is missing next to main.py", file=sys.stderr)
        return 1

    target_dir = output_dir()
    target_dir.mkdir(parents=True, exist_ok=True)
    target = target_dir / IMAGE_NAME

    # Stream the bytes through so the copy is exact, whatever the size.
    with source.open("rb") as reader, target.open("wb") as writer:
        while True:
            chunk = reader.read(65536)
            if not chunk:
                break
            writer.write(chunk)

    print(f"wrote {target} ({target.stat().st_size} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
