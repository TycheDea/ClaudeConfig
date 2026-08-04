# A6.1 — Settle the MR contract

Measured on the A5b bake-off views (`target/base-bakeoff/`), applying
`prop_texture.py`'s exact zoning maths, masked to the object silhouette by the
depth map each view was conditioned on.

## 1. The band does break on Z-Image

`METAL_VALUE_BAND = (0.24, 0.34)`, smoothstep, `metallic > 0.5` counted as metal:

| Base | mean luma | p10 | p50 | p90 | metal % |
|---|---|---|---|---|---|
| SDXL | 0.325 | 0.101 | 0.261 | 0.733 | **57.9%** |
| Qwen-Image | 0.269 | 0.066 | 0.197 | 0.655 | 67.2% |
| Z-Image | 0.190 | 0.038 | 0.145 | 0.355 | **81.4%** |
| Z-Image (short cue) | 0.206 | 0.028 | 0.145 | 0.441 | **77.9%** |

Sensitivity is ~1.7 points of metal per 0.01 of mean luma. Any constant band is
tuned to one model's brightness distribution.

## 2. But luma *is* bimodal — the premise isn't the problem

Otsu between-class variance ratio (how much of total variance a two-class split
explains — high = two real populations, low = one blob cut arbitrarily):

| Base | Otsu threshold | separability | dark mean | light mean |
|---|---|---|---|---|
| SDXL | 0.490 | 0.751 | 0.233 | 0.753 |
| Qwen-Image | 0.408 | 0.738 | 0.175 | 0.644 |
| Z-Image | 0.396 | 0.592 | 0.152 | 0.646 |
| Z-Image (short cue) | 0.412 | 0.681 | 0.146 | 0.681 |

Two well-separated populations on every base. **The shipped band sits far below
the natural boundary even on SDXL** (midpoint 0.29 vs Otsu 0.490), so it has
been cutting into the dark population all along.

## 3. A self-normalising threshold does not rescue it

Deriving the split from each image's own histogram was the obvious fix — it
would be immune to the brightness shift, and to the style LoRA's shift later.
It fails: dark-class fraction runs 67–92%, and **82% metal on SDXL** is plainly
wrong for a candelabra that is part wax and part stone.

The reason is structural. Luma conflates three things — albedo, shading, and
material — and the dominant split in a dark-fantasy render is lit-vs-shadowed,
not iron-vs-wax. No threshold rule recovers material identity from a channel
that does not carry it. **Rejected on measurement, not on taste.**

## 4. `--mr zoned` has exactly one consumer

`content/models/props/`: `candelabra_shrine` is the only pipeline-generated prop
(`generation_manifest.json`, `metal_fraction: 0.4076`). `rock_07`, `rock_09`,
`rock_face_01` and `dead_quiver_trunk` are Poly Haven library assets that never
went through this stage, and are slated for replacement under the no-libraries
ruling.

So the heuristic was tuned by eye, on one fixture, against no ground truth, and
nothing else has ever exercised it.

## 5. It has now failed the same way twice

Characters already rejected zoning (A4.6): darkest-equals-iron metalised dark
robes and hair, and the fix was `--mr dielectric`. Every prop the art direction
actually calls for — stone, wood, bone, cloth, plaster — contains **no metal at
all**, and renders dark. Zoning would metalise all of them.

This is not a Z-Image regression to retune around. Z-Image only made a
pre-existing defect visible.

## Conclusion

Per-texel material identity is not inferable from basecolor luma. The pipeline
does hold the information — in the subject prompt ("near-black weathered dark
iron, stone base, melted wax candles") — but as **per-prop** knowledge, not
per-texel.

## Ruled (user, 2026-07-20) — retire zoning

`--mr zoned|dielectric` is replaced by two declared constants,
`--metallic` (default 0) and `--roughness` (default 0.8). Deleted:
`METAL_VALUE_BAND`, `METAL_ROUGHNESS`, `DIELECTRIC_ROUGHNESS`,
`DIELECTRIC_MODE_ROUGHNESS`, the `--mr` enum, `--metal-roughness`, the zoning
branch, and the `island` mask's return path out of both basecolor strategies
(it had no other consumer).

The defaults *are* the old character contract, so `gen_character.py` now passes
no MR flags at all. Prop dielectric roughness moves 0.7 → 0.8, unifying props
and characters on one number.

True per-texel capture (a generated material mask) becomes the escalation rung
under A6.3 — mirroring the existing `projection` → `multiview` ladder rather
than adding a new axis.

`candelabra_shrine` is declared metallic: it is predominantly iron, and the
engine has real HDRI-driven IBL (`presentation.rs:68`), so the frame keeps its
reflection. Wax and stone base read wrong until A6.3.
**Reversed 2026-07-21 (`0894d2f`):** the regenerated asset's pale cream candles
broke the "predominantly near-black" premise — bright albedo at metallic 1 reads
as crystal, while game-HDRI side-by-side shows dark iron identical under either
declaration. With one constant per prop, the declaration must favor the bright
material: dielectric (metallic 0, roughness 0.8).

### Consequence: MR is no longer a texture

Two constants do not need a 1024² map. MR now rides the glTF scalar factors,
which the loader already honours (`gltf_import.rs:308`, `store.rs:155`).
Measured on the candelabra: 3 embedded images → 2, GLB 4.01 MB → 3.22 MB.
`content_lint.rs` is unaffected — its MR checks are `if let Some(...)` on the
slot and a byte-budget accumulator, both fine with the slot absent.

A per-texel material mask (A6.3) would bring the texture back.

### Verification

`blender --background --python prop_texture.py -- <glb> <glb> <concept_rgba>
out.glb --metallic 1.0 --roughness 0.45` → exported `metallicFactor 1.0`,
`roughnessFactor 0.45`, no `metallicRoughnessTexture`. Rust suite not run: the
change touches Python, README and this document only — no Rust, no shipped
content.

### Not done

The shipped `candelabra_shrine.glb` still carries its zoned MR texture. Its
source candidate dir no longer exists, so applying the declaration means a full
re-roll — which **A6.4 will do anyway** with Z-Image. Regenerating twice buys
nothing, so the declaration lands at A6.4. *(Scheduling call, flagged.)*
