---
id: EXAMPLE-active-delete-me
section: active
title: EXAMPLE - what an in-progress item looks like (delete this file)
updated: '2026-01-01'
---

One fragment per item. The `id` matches the filename and the `section` matches
the folder: the generator fails if they do not.

**Reservation —** this is the part that keeps two agents from colliding:

> Working on the invoice parser. Do not touch `src/billing/parser.py` or
> `tests/test_parser.py` while this line is alive.

When the item closes, **this file is deleted** and an entry is written in
`docs/agent/log/`. It is never struck through or marked "DONE".
