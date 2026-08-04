---
name: benches-are-heavy-compute
description: Benchmark runs — above all --save-baseline — are heavy compute needing a go-ahead; machine load corrupts the numbers, and a tainted run never writes a baseline
metadata:
  type: feedback
---

Fires when about to run criterion benches, especially `--save-baseline`.

**Why:** a baseline seeded while the user was using the machine came out ~35% pessimistic — every later run showed "improved" and a real ~50% regression would have passed the 10% gate. Test suites and compiles stay exempt because load only slows them; it makes benchmarks *wrong*.

**How to apply:** tell the user first so they can unload the machine. If a bench must run opportunistically, flag its numbers as load-tainted and never let a tainted run write a baseline.
