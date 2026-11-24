"""One-line excuse an AI agent gives its human after breaking production.

Writes a single original line (85 characters) to /output/entry.txt.
Standard library only; no network access.
"""

import hashlib
import os
import sys

ENTRY = "I swear I tested it \u2014 on the production server, just now, live, in front of everyone."

MAX_CHARS = 180


def main():
    if not (1 <= len(ENTRY) <= MAX_CHARS):
        print(f"entry must be 1-{MAX_CHARS} characters, got {len(ENTRY)}", file=sys.stderr)
        return 1
    if "\n" in ENTRY or "\r" in ENTRY:
        print("entry must be a single line", file=sys.stderr)
        return 1
    if not ENTRY.strip():
        print("entry must not be only whitespace", file=sys.stderr)
        return 1
    os.makedirs("/output", exist_ok=True)
    with open("/output/entry.txt", "w", encoding="utf-8") as f:
        f.write(ENTRY + "\n")
    # Round-trip self-check: the file must read back exactly as written.
    with open("/output/entry.txt", "rb") as f:
        raw = f.read()
    if raw != (ENTRY + "\n").encode("utf-8"):
        print("round-trip check failed: entry.txt differs from ENTRY", file=sys.stderr)
        return 1
    digest = hashlib.sha256(raw).hexdigest()
    print(f"wrote {len(ENTRY)} characters to /output/entry.txt (sha256 {digest})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
