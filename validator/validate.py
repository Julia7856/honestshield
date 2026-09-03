#!/usr/bin/env python3
"""HonestShield honesty.txt validator (reference implementation, v1).

Usage:
    python validate.py examples/messenger.honesty.txt
    python validate.py --url https://example.com
"""
import re
import sys
import urllib.request
from datetime import date

REQUIRED_HEADER = ["App", "Host", "Version", "Contact", "Updated", "Expires"]
KNOWN_SECTIONS = ["DATA", "THIRD-PARTIES", "TRACKERS", "PERMISSIONS",
                  "PROMISES", "SIGNATURE"]
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
KV_RE = re.compile(r"(purpose|retain|shared)=([^;]+)")


class Report:
    def __init__(self):
        self.errors, self.warnings = [], []
        self.header, self.sections = {}, {}

    def error(self, m): self.errors.append(m)
    def warn(self, m): self.warnings.append(m)


def fetch(url):
    if not url.endswith("/.well-known/honesty.txt"):
        url = url.rstrip("/") + "/.well-known/honesty.txt"
    with urllib.request.urlopen(url, timeout=10) as r:
        return r.read().decode("utf-8")


def parse(text, rep):
    section = None
    for n, raw in enumerate(text.splitlines(), 1):
        line = raw.strip()
        if not line:
            continue
        if line.startswith("## "):
            section = line[3:].strip()
            if section not in KNOWN_SECTIONS:
                rep.warn(f"line {n}: unknown section '## {section}'")
            rep.sections.setdefault(section, [])
            continue
        if line.startswith("#"):
            continue
        if section == "TRACKERS" and ":" not in line:
            rep.sections[section].append((line, None, n))
            continue
        if line == "none":
            rep.sections.setdefault(section, []).append(("none", None, n))
            continue
        if ":" not in line:
            rep.error(f"line {n}: expected 'key: value', got '{line}'")
            continue
        key, val = (x.strip() for x in line.split(":", 1))
        if section is None:
            rep.header[key] = val
        else:
            rep.sections[section].append((key, val, n))


def validate(rep):
    for field in REQUIRED_HEADER:
        if field not in rep.header:
            rep.error(f"missing header field '{field}'")

    for f in ("Updated", "Expires"):
        v = rep.header.get(f, "")
        if v and not DATE_RE.match(v):
            rep.error(f"header '{f}' must be YYYY-MM-DD, got '{v}'")
    u, e = rep.header.get("Updated"), rep.header.get("Expires")
    if u and e and DATE_RE.match(u) and DATE_RE.match(e):
        du, de = date.fromisoformat(u), date.fromisoformat(e)
        if de <= du:
            rep.error("Expires must be after Updated")
        elif (de - du).days > 366:
            rep.warn("validity period longer than 1 year")

    for key, val, n in rep.sections.get("DATA", []):
        if val is None:
            continue
        got = dict(KV_RE.findall(val))
        for need in ("purpose", "retain", "shared"):
            if need not in got:
                rep.error(f"line {n}: DATA '{key}' missing '{need}='")

    if "TRACKERS" not in rep.sections:
        rep.warn("no TRACKERS section (declare 'none' or a list)")

    pr = {k for k, v, n in rep.sections.get("PROMISES", [])}
    if "sell-data" not in pr:
        rep.warn("PROMISES: recommend declaring 'sell-data'")

    if "SIGNATURE" not in rep.sections:
        rep.warn("no SIGNATURE section (badge not issued yet)")


def main():
    args = sys.argv[1:]
    rep = Report()
    if args[:1] == ["--url"]:
        text = fetch(args[1])
    elif args:
        with open(args[0], encoding="utf-8") as f:
            text = f.read()
    else:
        print(__doc__)
        return 2
    parse(text, rep)
    validate(rep)

    print("honesty.txt report")
    print(f"  header: {len(rep.header)} fields")
    print(f"  sections: {', '.join(k for k in rep.sections if k) or 'none'}")
    for w in rep.warnings:
        print(f"  WARN  {w}")
    for e in rep.errors:
        print(f"  ERROR {e}")
    if rep.errors:
        print("result: FAIL")
        return 1
    print("result: OK" if not rep.warnings else "result: OK (with warnings)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
