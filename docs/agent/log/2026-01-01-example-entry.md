---
date: 2026-01-01
summary: Example log entry - show what changed, what you verified and what is still open. Delete this file when you start your project.
---

# 2026-01-01 - Example entry

Log entries are **immutable**: if something changed, write a new one. That is
why they never conflict, even with several branches writing at once.

The `summary:` in the frontmatter is what shows up in the generated index, so it
has to say something: what changed and why it matters, not "various progress".

## What to write

An entry speaks to someone who was not there. What pays off:

- **The defect or the need**, with the data that proves it.
- **The decision and why**, including the alternatives you discarded.
- **The verification**: the command and its real output, not "it works".
- **What is still open**, with its exit criterion.

## What not to write

Anything `git` already answers: the list of touched files, the diff, who
committed. That is queried; the log is for what is not in the code.
