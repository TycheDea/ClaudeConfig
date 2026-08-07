#!/usr/bin/env python3
"""Evidence behind triage.md: how the showcase candidates behave under the two
possible black-point controls.

`percentile` is what vfx_post exposes today; `level` is an absolute subtraction
in 0-255 units, which vfx_post has no way to express. Both are followed by the
same clip + centering + border gate vfx_post runs, so the pass counts are the
gate's own verdicts, not a proxy.

    python scripts/ai-pipeline/assets/vfx/showcase/void_floor_sweep.py
"""
import collections
import sys
from pathlib import Path

import numpy as np

SCRIPTS = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(SCRIPTS))
from vfx_post import (black_point_normalize, border_edges, center_mask,  # noqa: E402
                      extract_mask, quantize)

PACK = Path(__file__).resolve().parent
EDGES = ("top", "bottom", "left", "right")


def gates_pass(q):
    """vfx_post's own sequence: clip gate, then centering, then border gate."""
    if max(int(border_edges(q, 2)[e].max()) for e in EDGES) >= 2:
        return False
    centered, _, _ = center_mask(q)
    return max(int(border_edges(centered, 2)[e].max()) for e in EDGES) < 2


def main():
    paths = sorted(p for d in PACK.iterdir() if d.is_dir() and not d.name.startswith("_")
                   for p in d.glob("*.png"))
    masks = {p: extract_mask(p) for p in paths}
    slots = sorted({p.parent.name for p in paths})
    print(f"{len(paths)} candidates over {len(slots)} slots\n")

    print("percentile black point (vfx_post --black-point):")
    for pct in (0.5, 50, 90, 95, 97, 98, 99):
        per = collections.Counter()
        values = []
        for p, m in masks.items():
            normalized, bp = black_point_normalize(m, pct)
            values.append(bp * 255.0)
            if gates_pass(quantize(normalized)):
                per[p.parent.name] += 1
        print(f"  p{pct:<5} pass {sum(per.values()):3d}/{len(paths)}  "
              f"subtracted level {min(values):5.1f}-{max(values):5.1f}/255  "
              f"empty slots {sum(1 for s in slots if not per[s])}")

    print("\nabsolute black level (no vfx_post equivalent):")
    for lvl in (4, 6, 8, 10, 12):
        bp = lvl / 255.0
        per = collections.Counter()
        kept = []
        for p, m in masks.items():
            q = quantize(np.clip((m - bp) / (1.0 - bp), 0.0, 1.0))
            if gates_pass(q):
                per[p.parent.name] += 1
            reference = quantize(m)
            kept.append(float((q > 32).sum()) / max(1.0, float((reference > 32).sum())))
        print(f"  {lvl:2d}/255 pass {sum(per.values()):3d}/{len(paths)}  "
              f"midtone kept {np.mean(kept):.2f}  "
              f"empty slots {sum(1 for s in slots if not per[s])}")


if __name__ == "__main__":
    main()
