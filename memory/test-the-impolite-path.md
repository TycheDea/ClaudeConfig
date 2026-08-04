---
name: test-the-impolite-path
description: Client-lifecycle features are tested on the impolite path — abrupt death, instant relaunch, double login — and every request path needs an observable outcome
metadata:
  type: project
---

Fires when testing any client-lifecycle feature.

**Why:** the first persistence ship ignored a Login for a name already online; live play bricked immediately — the closing client lost the QUIC close-frame race, the server kept the stale session, the relaunched client waited forever on a fire-and-forget Login. The e2e bots only ever disconnected gracefully, so the tests modeled the polite path; real clients crash and relaunch fast.

**How to apply:** test abrupt death (no close frame), instant relaunch, and double login. A fire-and-forget request must never meet "silently do nothing" — every request path gets an outcome the client can observe or a policy that makes waiting safe; takeover (newest connection wins) is the standard session-identity answer. Any "dev-grade, revisit later" shortcut on the connect path will be hit on day one.
