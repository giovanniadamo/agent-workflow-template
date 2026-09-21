---
id: EXAMPLE-pending-delete-me
section: pending
title: EXAMPLE - what a pending item looks like (delete this file)
updated: '2026-01-01'
---

A pending item is written for someone who was not in the conversation. Two
things make it useful:

- **Evidence inside, not by reference.** "See PR #42" works today and is junk in
  three weeks. The measured number, the exact error, the command that reproduces
  it: that survives.
- **What unblocks it.** A pending item with no exit criterion is one nobody
  picks up.

A real example: *"The endpoint takes 4.2 s at p95 (measured with `ab -n 200`).
Suspicion: N+1 in `list_orders`. Unblocks on: deciding whether we paginate or
cache."*
