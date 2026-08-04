---
name: visual-verification
description: Verification is headless; renders are judged by Opus eyes on in-engine gameplay-framing evidence — never by existence checks, metrics alone, or turntables
metadata:
  type: feedback
---

User rulings, consolidated: no GUI launches, no user feel-checks — Opus says whether it is visually acceptable.

**Why:** a character passed every file/size/joint-count assert while rendering fully translucent; five props passed fable-tier turntable review then failed in-game on texel density, IBL material response, and scale beside the player; a soft watercolor material passed every seam/tiling metric — crispness was never scored; launching windowed binaries disrupts the user's machine.

**How to apply:**
- Verify headless: `cargo build`/`cargo test` (bot-client e2e is fine). For visuals, render offscreen (`zone_review`, `asset_inspect`, turntable) — never launch a window, never hold work open for a user feel-check.
- Any image/render deliverable gets an eyeball step on the rendered output in its verification contract; existence/size/count asserts prove nothing.
- The verdict runs on Opus ([[orchestration-model]]); producing the artifact and judging it are separate dispatches. Opus states what is wrong and how wrong — never what to change; the fix plan returns to fable with the verdict as input.
- Ship-clearing evidence is (a) in-engine under the destination zone's lighting, (b) a close-up at gameplay camera distance, (c) a frame with the player model for scale. Turntable sheets compare candidates; they never clear a ship. Run cheap machine gates (texel density vs a reference asset, roughness-vs-raw estimator) before the vision pass.
- Score crispness/micro-detail explicitly — would it read as photographed material at 1 m? — alongside register, relief, and cohesion.
- Procedural primitives are placeholders, labeled as such when shown; the quality bar is real assets ([[aa-art-direction]]).
