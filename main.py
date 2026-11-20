#!/usr/bin/env python3
"""news-image-20261119 entrypoint.

Copies the committed front-page image to the make.fun output directory.
Standard library only; deterministic: the same bytes every run.
"""
import hashlib
import os
import shutil
import sys

IMAGE = "entry.png"
OUTPUT_NAME = "entry.png"


def main() -> int:
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "out")
    src = os.path.join(os.path.dirname(os.path.abspath(__file__)), IMAGE)
    if not os.path.isfile(src):
        print(f"error: {src} not found", file=sys.stderr)
        return 1
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, OUTPUT_NAME)
    shutil.copyfile(src, dst)
    with open(dst, "rb") as fh:
        digest = hashlib.sha256(fh.read()).hexdigest()
    print(f"wrote {dst} sha256={digest}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
