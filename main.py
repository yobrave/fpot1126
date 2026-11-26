"""Houseplant fortune courier: read the pot's line, gate it, deliver it."""
import json
import os
import sys
from pathlib import Path

CAP = 120
SLUG = "u-golden-heron-44-fortune-in-a-pot-ded981e9"


def load_line():
    anchor = Path(__file__).resolve().parent
    return (anchor / "entry.txt").read_text(encoding="utf-8").rstrip("\n")


def gate(text):
    if not text.strip():
        return "blank"
    if len(text) > CAP:
        return "too-long"
    return "ok"


def deliver(text, where):
    where.mkdir(parents=True, exist_ok=True)
    out = where / "entry.txt"
    out.write_text(text + "\n", encoding="utf-8", newline="\n")
    return out


def main_flow():
    line = load_line()
    status = gate(line)
    report = {"status": status, "length": len(line), "slug": SLUG}
    if status != "ok":
        print(json.dumps(report))
        sys.exit(2)
    zone = os.environ.get("MAKEFUN_OUTPUT_DIR") or "out"
    landed = deliver(line, Path(zone))
    report["landed"] = str(landed)
    print("RESULT", status, json.dumps(report))


if __name__ == "__main__":
    main_flow()
