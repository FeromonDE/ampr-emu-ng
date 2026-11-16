#!/usr/bin/env python3
"""Keep the diagnostic trace outside mounted game images."""
import argparse
from pathlib import Path
import re

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--check", action="store_true")
args = parser.parse_args()
root = Path(__file__).resolve().parents[1]
source = root / "crates/ampr-sys/src/rt/blackbox.rs"
data = source.read_bytes()
pattern = rb'const PATH: [^\r\n]*= c"(/[^"\r\n]*/ampr_emu_trace\.txt)";'
matches = list(re.finditer(pattern, data))
if len(matches) != 1:
    raise SystemExit("AMPR trace implementation changed; review before building")
target = b"/download/ampr_emu_trace.txt"
path = matches[0].group(1)
if args.check:
    if path != target:
        raise SystemExit(f"Unexpected diagnostic trace path: {path!r}")
else:
    source.write_bytes(data.replace(path, target))
    for name in ["AGENTS.md", "docs/debug-build.md"]:
        doc = root / name
        doc.write_bytes(doc.read_bytes().replace(path, target))
print("Diagnostic trace: /download/ampr_emu_trace.txt")
