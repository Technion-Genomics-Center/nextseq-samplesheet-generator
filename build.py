#!/usr/bin/env python3
"""Rebuild index.html from ss_template.html + samplesheet_data.json.

The app ships as one self-contained HTML file, so everything it knows is
injected into the template here:

    /*DATA_PLACEHOLDER*/   samplesheet_data.json       the index plates
    /*APPS_PLACEHOLDER*/   sequencing_defaults.json    read lengths per
                                                       application

sequencing_defaults.json is generated in the atgc-platform repo by
tools/build_sequencing_defaults.py, from the read lengths recorded in the lab
reports on the share. It is committed here because this app is published to
GitHub Pages from its own repository and can read nothing from that one. If it
is missing the app still builds, and the application picker simply stays empty.

Usage:  python build.py
"""
import json
import pathlib
import sys

HERE = pathlib.Path(__file__).parent
TEMPLATE = HERE / "ss_template.html"
DATA = HERE / "samplesheet_data.json"
APPS = HERE / "sequencing_defaults.json"
OUT = HERE / "index.html"
TOKEN = "/*DATA_PLACEHOLDER*/"
APPS_TOKEN = "/*APPS_PLACEHOLDER*/"


def main() -> int:
    tpl = TEMPLATE.read_text(encoding="utf-8")
    if TOKEN not in tpl:
        print(f"ERROR: {TOKEN} not found in {TEMPLATE.name}", file=sys.stderr)
        return 1

    data = json.loads(DATA.read_text(encoding="utf-8"))
    out = tpl.replace(TOKEN, json.dumps(data))

    apps = []
    if APPS.exists():
        apps = json.loads(APPS.read_text(encoding="utf-8")).get("applications", [])
    else:
        print(f"NOTE: {APPS.name} not found — the application picker will be empty",
              file=sys.stderr)
    if APPS_TOKEN not in tpl:
        print(f"ERROR: {APPS_TOKEN} not found in {TEMPLATE.name}", file=sys.stderr)
        return 1
    out = out.replace(APPS_TOKEN, json.dumps(apps))

    OUT.write_text(out, encoding="utf-8")

    plates = len(data.get("plates", {}))
    wells = sum(len(v) for v in data.get("plates", {}).values())
    print(f"Wrote {OUT.name}: {len(out):,} bytes | {plates} plates, "
          f"{wells:,} index pairs, {len(apps)} applications")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
