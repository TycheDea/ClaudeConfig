# Street cobble install — DDS re-check verdict (2026-08-05)

Closes the required follow-up from `ground-regions-2026-08-01.md`: cand_1
(ambientCG PavingStones150, CC0) was approved from PNG-path renders with a
mandatory re-confirmation of the mid-distance read after the real DDS/BC bake.

Shipped in main repo commit `abb9619` — `content/textures/ground/street_cobble/`
(regraded albedo + normal + roughness, DDS sidecars), `zones.ron` street region
retargeted, CREDITS row added. The east zone's separate `worn_cobble` use is
intentionally unchanged. Lint (content_lint, 22 tests) green.

## Moss regrade (decided call, executed)

Local hue-only shift on the green-dominant mask, feathered, V untouched.
Script: `regrade_moss.py` alongside this record (metric script behind the
decision-bearing numbers).

- Moss-region (28,362 px) mean green-excess: 0.0489 → −0.0002
- Moss-region p95: 0.1255 → 0.0039; max: 0.1569 → 0.0510
- Green-dominant pixels: 28,362 → 1,900 (feathered fringe, no hard cutout)
- Mean |V drift|: 0.000000

Metric-provenance note: the earlier round's "+0.0275 whole-image p95" figure
does not reproduce on the source albedo under the stated formula
(g = (G−max(R,B))/255); moss is 0.68% of pixels, so a whole-image p95 cannot
see it (measures −0.0196 before AND after — a vacuous gate). The moss-region
statistics above are the honest gate and were used instead.

## Judge verdict (fresh Opus judge, installed-DDS frames vs approved PNG-path set)

Ground truth: installed `zone_review` 32-frame set vs the previously approved
PNG-path set at identical cameras (`target/ground-cobble-ab/cand_1/`).

1. **DDS/BC damage — 10/10.** Joint-grain luminance correlation r = 0.983–0.999
   at matched crops, RMS diff 0.6–1.1/255, grain energy 100.3–103.8% of the
   PNG path. Dark-joint network fully connected at ~15 px setts (`mid_gate`);
   only the ~4 px deepest plaza band degrades to dots — mip/Nyquist, identical
   in the uncompressed path.
2. **Moss/hue — 9/10.** True green 0.0008% of street pixels (vs 0.218%
   pre-regrade, 270× reduction, no clusters). Street hue medians 27–37°,
   S med 0.10–0.23, V med 0.35–0.39 — inside the warm window. Only breach:
   S≤0.35 ceiling on ~10% of nearest-foreground `close_crucero` pixels — rust
   grit at H≈31°, V 0.325 (warm, darker than stone; not moss).
3. **Scale/joints — 9/10.** No tile-scale super-structure or seam lines at the
   7 m period in low-pass reveal; high-pass skew negative in every crop
   (−0.08 to −0.46) — dark-weighted joints, no inverted bright joints.
4. **Value ladder — 8/10.** `wide.png` unusable (fog whiteout, p1–p99 span
   0.082); read from `mid_north_row`: street lit Y 0.351 between terracotta
   roofs 0.300 and plaster 0.488 / terrain 0.480 — no outlier.

**VERDICT: PASS — shipped.**

Observations recorded, not defects: (a) street is the only yellow-side hue
(H≈33° vs terrain ≈6°, roofs ≈13°) — reads slightly cool/olive against pink
earth by simultaneous contrast while measuring inside the warm window;
(b) `mid_street.png` and `wide.png` are heavily hazed (S med 0.050 vs 0.155 at
`mid_gate`) and are weak judging frames independent of this material.
