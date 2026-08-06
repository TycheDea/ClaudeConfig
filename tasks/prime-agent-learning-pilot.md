# Prime Agent learning-loop pilot — QUEUED 2026-08-06

## User direction

Pause the current texture A/B loop and evaluate setting up Prime Agent instead
of Pi dev so the repeated asset/model-quality campaign can retain learning
across iterations. The exact product identity is still ambiguous; next session
must first confirm whether this means Prime Intellect's PRIME Agent.

This is an architecture/setup fork, not permission to install immediately.
Prime must demonstrate persistent learning from trajectories, rewards, and
replay; merely changing agent harnesses does not improve asset quality.

## Goal

Establish whether Prime can run Vordar's long asset-quality loop with durable,
measurable improvement across episodes while preserving the existing licensing,
visual-judgment, provenance, and one-heavy-GPU-job gates.

Observable success requires all of:

1. An isolated episode uses a frozen real Vordar asset task and cannot write to
   shipping paths.
2. Inputs, tool calls, artifacts, metrics, judge outcomes, reward, and failure
   causes are persisted in a replayable trajectory.
3. A later matched episode demonstrably uses retained learning and improves the
   priced outcome rather than only its own proxy.
4. The comparison reports artifact quality, failure rate, wall/GPU time, token
   cost, licensing state, and operational complexity against Pi as the control.
5. Independent Sol visual judgment remains separate from frame production;
   metrics pre-screen but do not ship visuals.

## Execution model

Finding before change, serial gates, exact-path commits, Pi retained as the
control until Prime wins the matched pilot.

1. **Sol analysis — product and feasibility audit.** Identify the exact Prime
   Agent project/version and authoritative source; inspect license and complete
   runtime/weight dependency closure; determine what actually learns, where
   trajectories/rewards persist, multimodal and visual-evaluation support,
   Windows/WSL/Linux requirements, GPU/VRAM needs, costs, and integration
   boundaries with Vordar. Compare replacement, sidecar-worker, and no-adoption
   outcomes independently. No install, download, web-derived license rewrite,
   or user-global changes.
2. **Sol planning — matched pilot protocol.** Freeze one real task, artifact
   inputs, reward channels, red proofs, independent visual gate, sandbox write
   boundary, control arm, success/failure thresholds, expected wall/GPU time,
   and rollback. The protocol must prove learning across episodes rather than a
   one-off stronger model.
3. **User checkpoint.** Present outcome/confidence as /10 values and concrete
   setup/download/GPU/token costs. Ask before installation, user-global config,
   credentials, or any heavy run not already approved.
4. **Bounded setup change.** Only after approval: Luna performs exact mechanical
   acquisition; Terra or Sol hard-implement handles integration according to
   sensitivity; security/license and reproducibility gates run before access to
   project tools.
5. **Matched pilot and verdict.** Serialize heavy jobs, keep Pi as control,
   preserve every ruling-cited artifact, use a separate Sol visual judge, and
   adopt Prime only on a measured quality win with no licensing or provenance
   regression.

## Do not touch or decide

- Do not replace or disable Pi before the matched verdict.
- Do not install/download Prime, alter user-global configuration, provide
  credentials, change license verdicts, or run training/GPU jobs during the
  audit.
- Do not let Prime train on or emit shipping assets until the sandbox,
  provenance, and license gates pass.
- Do not treat self-reported reward, a single successful episode, or faster wall
  time as evidence of retained learning.
- Exclude `reference/` unless the user explicitly asks to study it.

## Resume state from the interrupted texture loop

- Game commit `185af6b` cleanly fixes separate export/final provenance and
  installs the approved retablo candidate. Retablo source, installed bytes, and
  manifest SHA are `e3d331f1b4bc60f5b1c1ab2222c30ea7b5570fce677a9871521d2821dae8aecb`.
- Queue item 1 was recorded complete in ClaudeConfig commit `f20b192`.
- Texture A/B queue item 2 is **HELD for this Prime decision**.
- The attempted zero-GPU P1b closeout under
  `target/texgen-ab/p1b-closeout/` is invalid, not decision evidence. Its
  reproducer used ordinal canvas slots and swapped the second/third source
  views for all six cart/votive candidates, causing authentic mean calibration
  MAD 8.58–20.28/255 against a required ≤0.5/255. Its corruption proof only
  changed unused copied bytes and is also invalid.
- If the texture loop resumes under either harness, its exact next technical
  step is a bounded correction of that target-local reproducer: derive
  generated-image/view mapping from each generate record and blend key, verify
  producer and consumer hashes, require one-to-one mapping, red-proof by
  deliberately swapping the same pair through the real validator, and stop
  unless all six authentic means calibrate ≤0.5/255. No production edit is
  currently justified.
- Retablo apse placement remains behind texture queue item 2 by the user's
  recorded ordering.

## Known unrelated game-tree dirt to preserve

- `docs/observability/phoenix.md`
- `tools/pi-phoenix/package-lock.json`
- `tools/pi-phoenix/package.json`
- `tools/pi-phoenix/src/startup.ts`
- `tools/pi-phoenix/test/startup.test.ts`
