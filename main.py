#!/usr/bin/env python3
"""One-Line Office Jokes entry for make.fun.

Writes a single one-line office joke to <MAKEFUN_OUTPUT_DIR>/entry.txt
(default /output/entry.txt). Standard library only, deterministic, no network.

The joke (100 characters):
    Our printer only jams on documents marked urgent, which I now believe
    is its actual job description.
"""

import hashlib
import os
import sys

JOKE = (
    "Our printer only jams on documents marked urgent, "
    "which I now believe is its actual job description."
)

MAX_CHARS = 199


def validate_entry(text):
    """Check the gate: UTF-8 text, 1-199 chars, one line, not only whitespace."""
    if not isinstance(text, str):
        return False, "not text"
    if not text.strip():
        return False, "only whitespace"
    if len(text) != len(text.encode("utf-8").decode("utf-8")):
        return False, "not valid UTF-8 round-trip"
    if not 1 <= len(text) <= MAX_CHARS:
        return False, "length %d outside 1-%d" % (len(text), MAX_CHARS)
    if "\n" in text or "\r" in text:
        return False, "more than one line"
    return True, "ok (%d characters)" % len(text)


def main():
    ok, why = validate_entry(JOKE)
    if not ok:
        print("gate failed: %s" % why, file=sys.stderr)
        return 1

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")

    data = JOKE.encode("utf-8")
    with open(path, "wb") as f:
        f.write(data)

    # Re-read and verify what was written is exactly what was intended.
    with open(path, "rb") as f:
        written = f.read()
    assert written == data, "written bytes differ from intended joke"
    ok, why = validate_entry(written.decode("utf-8"))
    assert ok, "written file failed gate: %s" % why

    print("wrote %s (%d characters)" % (path, len(JOKE)))
    print("sha256: %s" % hashlib.sha256(written).hexdigest())
    return 0


if __name__ == "__main__":
    sys.exit(main())
