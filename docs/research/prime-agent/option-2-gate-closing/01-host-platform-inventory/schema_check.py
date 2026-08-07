#!/usr/bin/env python3
"""Validate the retained G1 host-inventory schema."""

from __future__ import annotations

import json
import sys
from pathlib import Path

REQUIRED_PATHS = (
    "host.windows.build",
    "wsl.state",
    "wsl.external_guest_termination_capability",
    "storage.project_volume.free_bytes",
    "storage.candidate_guest_storage_volume.free_bytes",
    "pi.executable_identity",
    "gpu.host_adapters",
    "gpu.management_visibility",
    "gpu.wsl_guest_visibility",
)


def lookup(document: object, dotted_path: str) -> object:
    current = document
    for component in dotted_path.split("."):
        if not isinstance(current, dict) or component not in current:
            raise KeyError(dotted_path)
        current = current[component]
    return current


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: schema_check.py PATH", file=sys.stderr)
        return 2

    source = Path(sys.argv[1])
    try:
        document = json.loads(source.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        print(f"SCHEMA FAIL: invalid JSON: {error}")
        return 1

    missing: list[str] = []
    for dotted_path in REQUIRED_PATHS:
        try:
            lookup(document, dotted_path)
        except KeyError:
            missing.append(dotted_path)

    if missing:
        print("SCHEMA FAIL: missing required fields: " + ", ".join(missing))
        return 1

    print("SCHEMA PASS: all required fields present")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
