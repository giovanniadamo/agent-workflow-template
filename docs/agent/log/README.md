# Session history

One entry per session or PR: `YYYY-MM-DD-<slug>.md`, with `summary:` in the
frontmatter. **Immutable**: if something changed, write a new entry — never edit
an old one. That is what lets several branches write here without colliding.

`INDEX.md` is **generated** (`python scripts/render_state.py`) and not committed.
