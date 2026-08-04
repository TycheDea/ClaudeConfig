# Hi3DGen geometry non-determinism at fixed seed — analysis

**Defect.** Three seed-5 runs, same concept image: 541220 / 541286 / 541242 vertices.
Runs 2 and 3 came from byte-identical code, so run-to-run non-determinism is proven by that pair
(run 1's delta may also contain a code diff — only 2 vs 3 is clean evidence).
`normal.png` sha256 is bit-identical across all three: divergence is entirely downstream of normal prediction.

**Shape of the signal.** The spread is ~66 vertices out of 541k (~0.012%). That is the signature of a
*small float jitter flipping a handful of marching-cubes level crossings*, not of a divergent occupancy
volume. If the sparse-structure stage produced even one different voxel, `coords.shape[0]` would change and
the SLAT noise `torch.randn(coords.shape[0], 8)` (hi3dgen.py:347-350) would re-index against every voxel —
the meshes would differ grossly, not by 0.01%. So the occupancy coords are almost certainly bit-identical
across runs and the jitter enters in the SLAT stage or the mesh decoder.

**RNG discipline is clean (verified by reading, not suspected).**
`staged_run` (prop_hi3dgen.py:131-146) runs `get_cond` *before* `torch.manual_seed(seed)`; between the seed
and the two `torch.randn` draws nothing consumes RNG (`.to(device)` moves and the Euler sampler are RNG-free;
flow_euler.py has no random op after the initial noise). Both `randn` calls generate on the **CPU** generator
and then `.to(device)` (hi3dgen.py:295, 347), so the initial noise tensors are bit-identical given identical
coords. The "something eats the global RNG" hypothesis is refuted statically.

All four models load as fp16 (`weights/trellis-normal-v0-1/ckpts/*_fp16.safetensors`;
`SLatFlowModel.dtype = torch.float16`), which widens the relative jitter of any reordered accumulation.

---

## 1. Ranked root-cause hypotheses

### H1 — `scatter_reduce('mean')` inside the SLAT flow model's down-sampling (primary)
- Code: `hi3dgen/modules/sparse/spatial.py:60-66` (`SparseDownsample.forward`), instantiated at
  `hi3dgen/models/structured_latent_flow.py:71` and run in every `SparseResBlock3d(downsample=True)`.
- CUDA `torch.scatter_reduce` is documented nondeterministic (atomicAdd; accumulation order varies with
  thread scheduling). It runs on fp16 features, **inside the sampled loop**: 1 downsample per model call
  × 2 calls/step (CFG pos+neg) × 6 SLAT steps = 12 nondeterministic reductions, each feeding the next step.
  Euler iteration compounds the jitter; the decoder then turns a ~1e-3-relative latent perturbation into a
  few flipped SDF signs near the level set. Matches the observed magnitude exactly.
- Note the SS flow model (`sparse_structure_flow.py`) is a *dense* DiT with a dense conv decoder — no scatter
  ops — consistent with the occupancy stage being stable.

### H2 — scatter ops in the mesh-extraction path (secondary, same class)
- `cubes_to_verts`: `torch.scatter_reduce(..., reduce='mean')` on CUDA, fp32, once per run
  (`hi3dgen/representations/mesh/utils_cube.py:48-60`). Directly perturbs the SDF/deform values handed to
  marching cubes — the shortest possible path from atomics to vertex-count changes.
- `MeshExtractResult.comput_v_normals`: three `scatter_add_` calls (`cube2mesh.py:84-90`) — nondeterministic
  but affects **normals only**, not vertex/face counts; cannot explain the defect alone but pollutes byte-level
  mesh comparison.
- Marching cubes itself runs on CPU (`cube2mesh.py:139-150`) and skimage + trimesh are deterministic given
  identical input; they only amplify, never originate.

### H3 — cuBLAS GEMM reduction-order variance (workspace-dependent split-k)
- Every `nn.Linear`/attention projection goes through cuBLAS on fp16. Some cuBLAS algorithms use atomics /
  split-k whose selection depends on available workspace; free-VRAM differs run to run (allocator state, other
  processes). This is exactly what `CUBLAS_WORKSPACE_CONFIG=:4096:8` pins.
- This is also the only real mechanism by which the **per-stage CPU↔GPU movement** could matter: `.to()` is
  bit-preserving on parameters and `empty_cache()` changes no values, but the changed allocator/fragmentation
  state can shift cuBLAS heuristics. Movement is otherwise exonerated — runs 2 and 3 both used the staged
  code and still differed from each other, so movement is not the discriminator; fold it into H3.

### H4 — spconv `native` SubMConv3d (used in SLAT flow resblocks and the mesh decoder's SparseSubdivide blocks)
- `conv_spconv.py:37-42` pins `ConvAlgo.Native` — the right choice: spconv's `implicit_gemm` is the
  documented-nondeterministic algo. Native builds index pairs via a GPU hash table (ordering varies), but per
  kernel-offset each output row receives at most one contribution, offsets are looped sequentially, and GEMM
  is row-independent — so the pair-order permutation should cancel bitwise. Plausibly deterministic; unverified.

### H5 — xformers `memory_efficient_attention` forward
- `modules/sparse/attention/full_attn.py:213-222` (BlockDiagonalMask) and the dense twin in
  `modules/attention/full_attn.py:132-137`. xformers documents nondeterminism in **backward** (atomics for
  dK/dV); the forward cutlass/flash kernels use no atomics and are run-to-run deterministic on fixed
  hardware/version in practice. Low probability, and the SS stage's apparent stability (also xformers-based)
  is weak evidence in its favor.

### Refuted / negligible
- RNG consumption between seed and sampling — refuted by code reading (above).
- `argwhere`, `torch.unique(dim=0)` (sort-based), `SparseUpsample` (pure gather), index_put with unique
  indices in `get_dense_attrs` — all deterministic.
- The stride≠1 argsort path in `conv_spconv.py:54-61` only fires for batch>1; batch is 1 here.

---

## 2. Discriminating experiments (for later GPU time; ~40 s/run; ranked by info/minute)

### E1 — stage-boundary hashes (run first; 2 runs ≈ 2 min, localizes everything)
Instrument `staged_run` to sha256 the raw bytes of: `cond['cond']`, `z_s` (needs a small hook or hashing
`coords` + the decoder input), `coords`, `slat.feats`, and inside `SparseFeatures2Mesh.__call__` the
`sdf_d`/`deform_d` tensors and the MC output vertex array. (Hash via `t.cpu().numpy().tobytes()`.)
Two runs; find the **first divergent hash**:
- `cond` differs → conditioning/DINOv2 (would re-rank H5 up).
- `coords` differs → SS stage after all (H3/H5 in the dense DiT); expect gross downstream divergence.
- `coords` equal, `slat.feats` differ → **H1/H3/H4 in the SLAT sampler** (expected outcome).
- `slat` equal, `sdf_d` differ → **H2 / mesh decoder** (spconv subdivide blocks or `cubes_to_verts`).
- everything equal but verts differ → CPU side (would contradict analysis; re-examine skimage/trimesh).

### E2 — in-process double execution (1 run, discriminates atomics vs workspace)
In one process, call the divergent stage **twice on the identical input** (e.g. `decode_slat(slat)` twice, or
the SLAT flow model twice on a fixed `x_t`) and compare hashes.
- Differs in-process → atomics-class nondeterminism (H1/H2): scheduling variance, not memory state.
- Identical in-process but different across processes → workspace/heuristic variance (H3).

### E3 — deterministic-mode probe (1 run to enumerate, +2 runs to confirm)
Set `CUBLAS_WORKSPACE_CONFIG=:4096:8` and `torch.use_deterministic_algorithms(True, warn_only=True)`;
log warnings. One run prints every op PyTorch knows has no deterministic path that the pipeline actually hits.
Then flip `warn_only=False` (expect possible `RuntimeError` naming the op — that error is itself the answer)
and, if it survives, do 2 runs and compare E1 hashes: match ⇒ the whole fix is the two flags.

### E4 — targeted swaps (2 runs each; only where E1 points)
- Mesh decoder implicated → run `SparseFeatures2Mesh` scatter path on CPU (construct with `device="cpu"`) —
  if hashes stabilize, H2 confirmed.
- Attention implicated → `ATTN_BACKEND=sdpa` (fork supports it, `modules/attention/__init__.py:39`).
- spconv implicated → no algo alternative that's deterministic (`implicit_gemm` is worse); confirm via E2
  isolation on a single SubM conv.

### E5 — noise-floor calibration (10 runs ≈ 7 min GPU; needs a go-ahead per project rule 8)
Ten seed-5 runs; per pair: vertex-count delta, symmetric Chamfer distance (100k surface samples) and
Hausdorff, normalized by bbox diagonal. This is the "measure once" input for §4 regardless of which fix lands.

---

## 3. Fix options and their real cost

**F1 — `CUBLAS_WORKSPACE_CONFIG=":4096:8"` env var in prop_hi3dgen.py (do unconditionally).**
Cost: ~a few MB workspace per stream, negligible perf. No downside; closes H3 permanently.

**F2 — `torch.use_deterministic_algorithms(True)` + `torch.backends.cudnn.deterministic=True`,
`benchmark=False`.**
- Covers torch-native ops only. Ops with a deterministic CUDA fallback (scatter_add, index_add, index_put)
  silently switch to it; ops without one **raise** — E3 tells us which, before committing.
- `scatter_reduce(reduce='mean')` is the open question: recent torch versions route sum/mean through the
  deterministic scatter_add path, but if 2.7.1 raises on it, F3 below is the answer — do not wrap the call in
  a mode-toggle special case.
- Throughput cost: expected <10% here (runtime is GEMM/attention dominated and those kernels mostly don't
  change); measure once against the 40 s baseline.
- Explicit limits: this flag does **not** govern xformers or spconv. It cannot make the stack deterministic
  by itself if either of those is a source — it can only prove/fix the torch-native part.

**F3 — deterministic rewrite of the two `scatter_reduce('mean')` sites (if E1/E3 implicate them and F2
raises).** In `SparseDownsample.forward` and `cubes_to_verts`: replace with `index_add_` for the sum plus a
`bincount` for counts, divide for the mean (`index_add_` has a deterministic CUDA implementation under F2),
or a sort-then-segment reduction. Small, local, in the fork's `vordar-fixes` branch; per-op slowdown only,
called 12×/run (H1 site) and 1×/run (H2 site). Also rewrite/accept `comput_v_normals`' `scatter_add_`
(deterministic under F2 automatically).

**What can and cannot be made bit-reproducible.**
- *Achievable*: bit-identical runs **on this machine, with this frozen stack** (torch 2.7.1+cu128,
  xformers 0.0.31.post1, spconv 2.3.8, same driver, RTX 3080 Ti) — F1+F2(+F3) very likely gets there, because
  the forward-only pipeline's remaining kernels (xformers forward, spconv Native, cuDNN with deterministic
  flag) are believed order-stable; E1 hashes over ~5 consecutive runs are the proof.
- *Not achievable, ever*: bit-identity across GPU architectures, driver/CUDA versions, or library upgrades —
  kernel selection and reduction tiling legitimately change. The manifest already records the full version
  set; bit-repro claims must be scoped to a recorded manifest, and a stack upgrade re-runs the E1 5-run check.
- *Residual risk*: if E2 shows xformers or spconv forward diverging in-process, there is no determinism knob
  for them — the options become backend swap (`sdpa` for attention) or accepting §4's envelope.

---

## 4. Recommendation: what "bounded" should mean

Do F1 immediately, run E1+E2 (three-ish runs) to localize, then F2/F3 as indicated. If a residual
non-torch source survives, or the F2 perf tax proves ugly, fall back to a **calibrated noise envelope**:

- **Calibrate once** with E5 (10 fixed-seed runs): record max pairwise symmetric Chamfer and Hausdorff
  (bbox-diagonal-normalized) and vertex-count spread. Expected order: Chamfer ~1e-4–1e-3 of diag,
  count spread ≲0.05%.
- **Envelope** = 2× the max observed pairwise Chamfer, plus the count-spread tripwire. Store the numbers and
  the measuring script's invocation in this file (or docs/) — it is measured once per recorded stack, not per
  experiment; re-measure only when the manifest's version block or GPU changes.
- **A/B rule**: a pipeline change is a real effect only if its metric delta exceeds the envelope; "no
  regression" means "within envelope", never "bit-equal". Vertex count alone is not an A/B metric — it is
  only the cheap tripwire.
- The three existing runs already suggest the envelope is tiny (0.012% count spread); bounded determinism is
  almost certainly sufficient for every A/B comparison this pipeline does, so full bit-repro (F2/F3) is worth
  taking only if E3 shows it's nearly free.
