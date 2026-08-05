# P3.3 G3 gate — per-class ship gate for S5 survivors (spec, 2026-08-05)

First execution of G3. Classes and candidate pools (from
`docs/reviews/props/dark-iron-class-blocked-2026-08-05.md` §queue):

- **oak_dark**: retablo `target/prop-batch/h3-retablo/cand_1` (v2 PASS
  2.58%), `cand_3` (v2 PASS 1.93%), `cand_2` (v2 ESCALATE 3.14% — judge-
  only: it may win ONLY if the judge explicitly clears its open_dark at
  1:1 on the albedo channel).
- **limestone**: shrine_pillar `target/prop-batch/h4-shrine/cand_203`,
  `cand_501` (both v2 PASS 0.40%/0.26%).

Registry state at gate time: `retablo` + `shrine_pillar` entries present
in assets.json (uncommitted; they ship with the winning installs).

## Gate criteria (pre-registered)

G3's priced deliverable is one shippable prop per class from the S5
chain. The gate is the deliverable plus no-regression — not any defect's
headline band:

1. **Subject/material read** — at gameplay framing (2.3 m) the prop reads
   as its registry subject (dark oak retablo with gilt beading / pale
   limestone shrine pillar with lit candle); materials read physically
   plausible under studio, raking, and ship lighting.
2. **No ghost-class shading at 1:1** — albedo-channel frames show no
   painted contact shadow or view-baked highlight structure at gameplay
   or macro distance. (v2 pre-screen already passed these; the judge's
   1:1 eyeball is the percentile-blindness backstop.)
3. **No-regression vs comparators** — the candidate must not read worse
   than the interleaved photoscan reference frames (`--reference`) in
   surface credibility at matched framing, allowing for material
   difference; and blind-test placement must be at or above the shipped
   generated props' historical band (blind #1: photoscan 8, shipped
   2.5–4) with no "shading painted in" tell named against it.
4. **Candidate selection** — the judge picks one winner per class (or
   fails the class with the defect named and frame-cited).

Axes 1–3 are scored /10 per candidate; a winner needs ≥7 on each axis.
A class with no candidate ≥7/7/7 FAILS and reports, not installs.

## Instruments

- `prop_audit.py --asset <cand_dir path>` — table with rock_face_01
  reference row. By-path mode omits shipped_height_m / blend_coverage /
  hole_frac: quote blend coverage from the cand's blend-cache
  `coverage.json` instead. Judges receive the table; measurement-only.
- `color_cast.py <cand_dir>` — R−B and Lab a*/L* of the shipped atlas.
  Anchors on record: July warm-cast baseline R−B 22.91 / a* 1.436;
  lightning-adopted a* −0.03. A candidate a* far outside the neutral
  band is judge-attention material, not an auto-fail.
- `asset_inspect <final.glb> --lighting studio,raking,ship
  --channel beauty,albedo --distance gameplay,macro --angles 4
  --reference --stats` — the named-frame evidence base. `full` arm is
  NOT used for silhouette judgment (standing caveat).
- Blind set — turntable contact sheets, anonymized letters, mapping
  withheld from the judge (held by orchestrator; worker writes
  `<class>_mapping.json` OUTSIDE the blind dir). Control = rock_face_01
  contact sheet rendered by the SAME turntable bin in the same run if
  the bin accepts a gltf path; otherwise the on-disk
  `target/prop-redesign-after/rock_face_01/contact_sheet.png` with its
  lighting provenance noted to the judge.

## Execution

Stage A (sonnet worker, one per class; implementation only):
1. Per cand: `gen_prop.py --asset <name> --out <batch> --seed <S>
   --skip-concept <recorded concept> --through turntable` — resumes past
   existing stages; runs preprocess (CPU) + bake + turntable (GPU
   seconds). Verify final.glb + final.textures/ + contact_sheet.png.
2. Run color_cast.py and prop_audit.py (by path, with --json) per cand;
   persist outputs under `target/prop-g3/<class>/`.
3. Run asset_inspect per cand → `target/prop-g3/<class>/<cand>/`.
4. Assemble the blind set → `target/prop-g3/blind/<class>/` (letters) +
   mapping json outside it.

Stage B (fresh opus judge, one per class; visual only, NO
recommendations): blind ranking first (before seeing any labeled
material), then axes 1–3 per candidate on named frames + table, then
selection per §criteria. Record → `docs/reviews/props/
g3-<class>-2026-08-05.md`.

Stage C (orchestrator): adjudicate records, install winners
(`install_asset.py`, provenance chain intact, byte-equality vs judged
artifacts, content_lint), commit with registry entries, close G3.
