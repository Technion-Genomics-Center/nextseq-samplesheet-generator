#!/usr/bin/env python3
"""Rebuild index.html from ss_template.html + samplesheet_data.json.

The app ships as one self-contained HTML file: the index dataset is injected
into the template in place of the /*DATA_PLACEHOLDER*/ token.

Usage:  python build.py
"""
import json
import pathlib
import sys

HERE = pathlib.Path(__file__).parent
TEMPLATE = HERE / "ss_template.html"
DATA = HERE / "samplesheet_data.json"
OUT = HERE / "index.html"
TOKEN = "/*DATA_PLACEHOLDER*/"


def main() -> int:
    tpl = TEMPLATE.read_text(encoding="utf-8")
    if TOKEN not in tpl:
        print(f"ERROR: {TOKEN} not found in {TEMPLATE.name}", file=sys.stderr)
        return 1

    data = json.loads(DATA.read_text(encoding="utf-8"))
    out = tpl.replace(TOKEN, json.dumps(data))
    OUT.write_text(out, encoding="utf-8")

    plates = len(data.get("plates", {}))
    wells = sum(len(v) for v in data.get("plates", {}).values())
    print(f"Wrote {OUT.name}: {len(out):,} bytes | {plates} plates, {wells:,} index pairs")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
