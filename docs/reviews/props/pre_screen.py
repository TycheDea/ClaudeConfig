#!/usr/bin/env python3
"""Round-2 pre-screen: island-masked luma p5/p50/p95, p95/p5 ratio, and
fraction of island texels below 45% of median luma, for one glb+albedo pair.
Reuses prop_audit.py's island_mask/luma_of (read-only import, not a copy) so
the metric matches the shipped-prop instrument.

Usage: python pre_screen.py <glb_path> <albedo_image_path> [--label NAME]
"""
import argparse
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts" / "ai-pipeline"))
from prop_audit import island_mask, load_gltf, luma_of  # noqa: E402
from PIL import Image  # noqa: E402


def measure(glb_path, image_path):
    gltf, buffers = load_gltf(Path(glb_path))
    w, h = Image.open(image_path).size
    mask = island_mask(gltf, buffers, w, h)
    luma = luma_of(Path(image_path))
    m = luma[mask]
    p5, p50, p95 = (float(np.percentile(m, q)) for q in (5, 50, 95))
    below45 = float((m < 0.45 * p50).mean())
    return {
        "island_texels": int(mask.sum()), "atlas_w": w, "atlas_h": h,
        "luma_p5": p5, "luma_p50": p50, "luma_p95": p95,
        "p95_over_p5": p95 / p5, "below_45pct_median_frac": below45,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("glb_path")
    ap.add_argument("image_path")
    ap.add_argument("--label", default=None)
    args = ap.parse_args()
    stats = measure(args.glb_path, args.image_path)
    label = args.label or args.image_path
    print(f"{label}: " + ", ".join(f"{k}={v:.4f}" if isinstance(v, float) else f"{k}={v}"
                                    for k, v in stats.items()))


if __name__ == "__main__":
    main()
