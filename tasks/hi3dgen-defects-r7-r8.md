# Advisory: reworks findings 7 & 8 (Hi3DGen normal bridge defects)

Date: 2026-07-28. Analysis only — no source edits, no GPU runs. Evidence gathered
by reading `scripts/ai-pipeline/prop_hi3dgen.py`, the hub snapshot
(`~/.cache/torch/hub/hugoycj_StableNormal_main`), the fork
(`C:/tools/Hi3DGen/Hi3DGen`, `vordar-fixes`), torch 2.7.1's `hub.py`, and by
running `scripts/ai-pipeline/check_weights.py` (full re-hash, 45/45 OK).

---

## Defect A — the offline load has never worked (finding 8)

### A1. Root-cause fix

**Cause chain.** `prop_hi3dgen.py:290-297` passes `pretrained=True` to the
local `torch.hub.load`. The kwarg was cargo-culted from the fork's DINOv2 load
(`fork:hi3dgen/pipelines/hi3dgen.py:96`), whose hubconf genuinely accepts it.
StableNormal's hubconf entrypoints are
`StableNormal(local_cache_dir, device, yoso_version, diffusion_version)` and
`StableNormal_turbo(local_cache_dir, device, yoso_version)` — no `pretrained` —
so the local call raises `TypeError` on every run, the bare `except Exception`
swallows it, and the GitHub fallback (`prop_hi3dgen.py:298-305`) runs instead.

**The fix is three deletions plus one pin, not a patch:**

1. **Delete `pretrained=True`** from the local call. Verified against the
   snapshot's `hubconf.py` signatures; the reworks note also reproduced that
   dropping it makes the local branch load.
2. **Delete the entire `try/except` + network fallback.** Yes, the same
   treatment as the fork's deleted DINOv2 fallback applies, and for the same
   reason: the snapshot is a pinned local dependency, so a missing snapshot is
   a setup error that must raise, not a condition to route around. The
   fallback is also an active per-run network touch today: torch 2.7.1's
   `_parse_repo_info` does `urlopen("https://github.com/hugoycj/StableNormal/tree/main/")`
   to resolve the branch on *every* invocation — every "offline" run so far
   has quietly required GitHub connectivity. With the fallback gone,
   `source="local"` makes zero network calls; the offline guarantee becomes
   structural instead of env-guarded. (`HF_HUB_OFFLINE=1` stays — it correctly
   guards the HF-side loads; it never governed `torch.hub`, and after this fix
   nothing in the script uses `torch.hub`'s network path at all.)
3. **Pin the hub snapshot code in `models.sha256`.** The executed code
   (`hubconf.py`, `stablenormal/**/*.py`) is as load-bearing as the weights —
   after a cache eviction, the old fallback would have re-downloaded whatever
   upstream `main` is that day and silently changed every normal map. Add the
   snapshot's `.py` files under a `Hi3DGen/StableNormal-hub/` prefix with a
   matching `PREFIX_ROOTS` entry in `check_weights.py` (the mechanism already
   exists and already spans three roots).
4. Optionally: record the loaded snapshot path in `hi3dgen_manifest.json`
   next to the weight identities. Cheap, and it closes the manifest's current
   silence about which code produced the normal.

### A2. Does this invalidate the A/B measurements? **No.**

What every run actually loaded, established from code + hashes rather than
inference:

- **Weights: the pinned local files, in both branches.** The fallback call
  passes the *same* `local_cache_dir=C:/tools/Hi3DGen/Hi3DGen/weights` and the
  same `yoso_version`/`diffusion_version` kwargs as the local call. hubconf
  builds the weight path purely from `local_cache_dir` and loads it with
  `from_pretrained(<local dir>)` — no HF fetch is possible, and
  `HF_HUB_OFFLINE=1` backstops it. So the yoso / stable-normal weights came
  from the fork's `weights/` directory on every run regardless of which branch
  fired.
- **Code: the pinned snapshot bytes, in both branches.** torch 2.7.1's
  `_get_cache_or_reload` with `force_reload` unset takes the `use_cache` path
  when `hugoycj_StableNormal_main` exists — "Using cache found in …", no
  download, no re-validation. That cache directory is the *same directory* the
  local branch targets. The fallback's only network activity is the
  branch-name probe above; the code it executes is the snapshot.
- **Hashes.** `check_weights.py` just re-verified all 45 `Hi3DGen/…` lines —
  including `yoso-normal-v1-8-1/{unet,vae,controlnet}/…fp16.safetensors` and
  the full `stable-normal-v0-1` set actually loaded by the entrypoints —
  against disk: **45/45 match.** Snapshot code files are dated 2026-07-19,
  untouched since (both studies ran 2026-07-28); no leftover download zip in
  the hub dir.
- **Cross-study corroboration.** The turbo `normal.png` is byte-identical
  between the two studies (`69076427b0fe…`), which is only possible if code
  and weights were stable across the whole campaign.

So the fallback delivered byte-identical code and byte-identical weights to
what the intended offline path would have delivered. **Neither
`ab-conditioning-2026-07-28.md` nor `ab-normal-model-2026-07-28.md` needs a
re-run on defect-A grounds.** (The 768/1024 grid does need a re-run — but for
defect B's reason, as a new measurement, not as a redo of a corrupted one.)

### A3. Is `models.sha256` pinning files nothing loads? **No — the failure recurred inverted.**

Every `Hi3DGen/…` pin resolves to a load-bearing location: the fork `weights/`
entries are loaded via `local_cache_dir` (even through the fallback), the
`Hi3DGen/BiRefNet/…` pins map to the revision-pinned HF snapshot that
`preload_birefnet` loads, and `Hi3DGen/DINOv2/…` maps to the torch-hub
checkpoint the fork's (working) local DINOv2 load consumes. No dead pins.

The earlier defect — pins detached from loads — has recurred **as its mirror
image: a load detached from any pin.** The hub snapshot's *code* is executed
on every run and appears nowhere in `models.sha256`, while its loader carried
a live network path that would replace it silently after a cache eviction.
Same broken guarantee ("the pinned bytes are the loaded bytes"), opposite
route: last time dead pins, this time an unpinned load. Fix item 3 above
closes it; a lesson note should generalize the trigger to "the pin set and
the load set must be proven equal in both directions".

---

## Defect B — what `--normal-resolution` actually does (finding 7)

### B1. End-to-end trace

Confirmed in the snapshot code:

- `hub:hubconf.py` `Predictor.__call__(img, resolution, …)`: PIL-LANCZOS
  resizes the (8-bit) input to `resolution` (multiple-of-64), NEAREST-resizes
  the alpha mask alongside, then calls `self.model(img,
  match_input_resolution=…, **kwargs)` where `kwargs` can only ever contain
  `num_inference_steps`. **`processing_resolution` is never passed.**
- Both `pipeline_yoso_normal.py` (line 159) and `pipeline_stablenormal.py`
  (line 246) default `default_processing_resolution=768` in the constructor;
  `yoso-normal-v1-8-1/model_index.json` contains no override (verified — it
  lists only the component classes). At `__call__` time,
  `processing_resolution=None` → falls back to 768.
- Inside the pipeline: input is antialiased-bilinear downsampled (float
  tensor space) to max-side 768, denoised at 768, and — with
  `match_input_resolution=True` — the *float* prediction is bilinear-upsampled
  back to the pipeline's input size before quantization.

So the two arms are:

| step | `--normal-resolution 768` | `--normal-resolution 1024` |
|---|---|---|
| pre-pipeline | PIL LANCZOS 1024→768, 8-bit | identity |
| pipeline input resample | ~identity (already 768) | float bilinear-AA 1024→768 |
| denoise | 768 | 768 (identical) |
| pipeline output resample | ~identity | float bilinear 768→1024, pre-quantization |
| mask applied at | 768 | 1024 |
| post-pipeline | PIL LANCZOS 768→1024 of the **quantized 8-bit** map (incl. the hard mask edge) | identity |

The finding-7 claim is correct: the denoiser sees 768 px in both arms. The
flag selects **which resample chain wraps the same 768 denoise**. The 768 arm
adds two lossy 8-bit PIL resamples — including a LANCZOS upsample of an
already-quantized map with a hard-masked silhouette, which is exactly the
operation that smears 1–2 px features and rings at edges. The two arms also
hand the denoiser *slightly different conditioning* (LANCZOS-8-bit vs
bilinear-AA-float downsample), so the predictions differ genuinely, not just
by resampling of one field: measured 2.5–2.8° mean angular difference.

**Is that mechanism sufficient for +21.8% faces downstream?** Yes. The
geometry stage's noise floor of ~0.01–0.06% was measured with a
*byte-identical* normal map; it bounds run-to-run drift, not sensitivity to
input perturbation. The turbo-vs-full study supplies the missing curve: mesh
change magnitude tracks angular deviation of the conditioning normal on both
subjects (11–18° mean → −29%…−46% faces on crucero). A real 2.8° conditioning
change producing a +21.8% single-run change on the ornament-dense subject sits
on that curve; the direction matches the visual mechanism (chips resolved in
the 1024-chain map became geometry; the 768-chain "mottled wash" did not).
What n=1 per cell does *not* establish is the repeatability of the 21.8%
magnitude — only that the effect is real and its cause is the resample chain,
not denoising resolution.

### B2. Instrument adjudication

The two "instruments" are two implementations of the same radial-ring
spectrum. The tell is in the numbers: on the resample-free r1024 cells they
**agree** (candelabra 0.00605 vs 0.0060; crucero 0.00146 vs ~0.0019), and they
diverge 20–35× only on the r768 cells — the arm whose map passed through the
extra 8-bit LANCZOS up/down cycle. The instruments differ precisely where the
chain artifacts live.

**Study 1's top-octave argument loses, at two levels:**

1. **Premise.** "The top octave is the band a 768-processed map cannot
   legitimately occupy" — both maps are 768-processed. Above 0.75 of the
   1024-frame Nyquist, *neither* arm can carry legitimate signal; everything
   either instrument measures there is resample artifact (LANCZOS overshoot on
   a quantized map, hard mask-edge ringing, quantization noise). The band
   measures the chain, and the comparison being made is *between chains* — the
   instrument measures the confound, not the signal. Its concrete failure
   mode: **it counts energy, not detail**, and sharp-kernel upsampling of an
   8-bit image injects exactly the band being scored.
2. **Implementation.** The script was not kept, its ordering is contradicted
   by the surviving instrument on the same artifacts, and the agreement
   pattern above suggests it did not measure the shipped 1024-px files for the
   r768 arm (e.g. measured the native-768 grid, where a tiny top octave is
   expected from VAE roll-off — an apples-to-oranges Nyquist). Unreproducible
   + contradicted = discard.

Study 2's ring implementation is the sound one *as a measurement* (one
instrument over all cells, cross-checked by reproducing study 1's angular
numbers to the digit, run on the artifacts the geometry stage actually
consumes) — and its own verdict is that the band is unusable as a detail
metric here, which it correctly declined to use as evidence.

**Single instrument for future normal-map comparisons:** the angular-domain
suite on decoded unit vectors inside the eroded object mask —
mean/p95 angular difference, detail-pixel angular gradient, and the
5×5-median speckle fraction — plus the zoom panels for the human check. That
is `ab-normal-model`'s instrument, already validated. Spectral ring measures
are admissible only between arms with *identical* resample chains, which is
the one situation where nobody needs them.

### B3. Verdict: **1024 stays the default.** No further measurement needed to keep it.

The honest restatement: `--normal-resolution 1024` was adopted for a reason
that is now dead (it does not raise denoising resolution), but the setting is
still right, for a different and firmer reason — **it is the strictly cleaner
chain around the same denoiser**:

- 768 adds two lossy 8-bit PIL resamples and bakes the mask at 768; 1024's
  resampling happens once each way, in float, pre-quantization, with the mask
  applied at output resolution. This is a dominance argument, not a
  measurement: same denoise, same cost, strictly fewer destructive ops.
- Every honest observation agrees: the zoom panels (wires/chips resolved vs
  smeared) match the chain explanation; the coarse-relief check shows 768's
  Laplacian/gradient "wins" were smear amplitude; the crucero geometry gain
  is real in direction (if unestablished in magnitude); cost is nil in both
  time and VRAM.
- 768 has no evidence in its favor anywhere: its only remaining "win" is
  study 2's top-octave number, which B2 identifies as ringing artifact.

Reverting to 768 would reintroduce two lossy resamples to honor a study whose
decisive metric was invalid — the wrong conclusion from the right correction.

**What still must be measured — already queued as finding 7's re-run, and it
is a new experiment, not a defense of the current default:** plumb
`processing_resolution` through (call the pipeline directly or fix
`Predictor.__call__` in the pinned snapshot — the snapshot is ours once fix
A.3 pins it), verify the denoiser's working size from inside the run, then
re-run the 768/1024 grid, same two subjects, same seed, with the angular
instrument and ≥2 repeats per cell on the geometry side (finding 6's noise
protocol). Decision rule for *that* knob: adopt true-1024 denoising only if
it improves detail-pixel angular sharpness without speckle regression and
fits VRAM (~1.8× pixels at the peak stage); if it speckles or spills, the
current default (1024 chain, 768 denoise) already is the optimum of the knob
that actually exists.

**Two report corrections to carry with the fix** (advisory; both are doc
edits, not code): `ab-conditioning-2026-07-28.md`'s "Radial spectrum … is the
decisive evidence" section needs an addendum marking it invalidated by
finding 7, with the adoption rationale replaced by the chain argument; and
`prop_hi3dgen.py:75`'s comment ("resolves fine detail that 768 smears") is
true of the output but implies a resolution mechanism that doesn't exist —
reword when finding 7 lands.
