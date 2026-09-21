# AGENTS.md — contract for AI agents in this repo

This file is the **single** contract for any agent (Codex, Claude Code, Cursor,
Gemini or another). `CLAUDE.md`, `.cursor/rules` and `GEMINI.md` only point
here — never duplicate content into them.

> Adapt this file to your project. Replace anything in `<...>`. Delete what does
> not apply: a contract carrying dead rules teaches that rules are decorative.
>
> **Language:** this ships in English so any team can use it. Translating it into
> your team's language is expected and encouraged — agents follow it equally well
> either way. Keep one language per repo.

## Starting a session

```bash
python scripts/render_state.py
```

- **Exit 0** → read `docs/agent/STATE.md`. That is the project's state.
- **Non-zero exit** → **do not read `STATE.md`**: it has been deleted or is
  stale. Fix the fragments named in the error, or say so. Never work from a
  state that could not be generated.

`STATE.md` and `log/INDEX.md` are **generated and not committed**. Do not edit
them: your change is lost on the next render and nobody ever sees it.

## Hard rules

Numbered so they can be cited in a review ("this breaks rule 4").

1. **Everything lands through a PR.** No agent commits straight to the main
   branch, documentation included. No exceptions for "it is a small change".
2. **No unregistered work.** Before touching code, create a fragment in
   `docs/agent/state/active/` saying what you are about to do and **which files
   you will touch**. Before you start, read the other `active/` fragments so you
   do not collide with another person or agent.
3. **Closing an item means deleting its file** from `state/`, plus a new entry
   in `docs/agent/log/`. Never strike it through or mark it "DONE" in place.
4. **Verify before you claim.** Before saying "done", "fixed" or "passing", run
   the command that proves it and read the real output. If you did not run it,
   do not say it.
5. **Tests with every behaviour change.** Write the test first and watch it
   fail; a test that never failed proves nothing.
6. **Do not widen the scope.** No improving adjacent code, no new dependencies
   without justifying them, no refactoring what is not broken.
7. **Do not skip hooks** (`--no-verify`) and do not force-push. If a hook fails,
   fix the cause.
8. **Volatile facts are never written down.** SHAs, PR numbers, branch lists:
   query them with `git` / `gh` at the moment of use. Written into a `.md` they
   go stale, and somebody decides on a false fact.
9. **No test data left in production.** If you must create some, delete it when
   you are done and verify it is gone.
10. **When in doubt, ask.** A question costs minutes; a wrong assumption found
    after the merge costs days.

## Finishing a session or a PR

In the **same PR** as the change, never in a separate commit:

1. A new entry in `docs/agent/log/YYYY-MM-DD-<slug>.md`, with `summary:` in the
   frontmatter (one sentence: what changed and why it matters).
2. Update `docs/agent/state/`: **delete** the fragment for the item you closed,
   create fragments for whatever is left open. A pending item with no exit
   criterion is one nobody picks up — say what unblocks it.
3. Run `python scripts/render_state.py` again and confirm it exits 0.

**Leave nothing "for after the merge".** Every deferred step stops happening: it
either travels in this PR or it does not exist. If it genuinely cannot be done
now, it goes as a fragment in `pending/` with its exit criterion — never as a
comment on the PR.

## Commands

<!-- Replace with your stack's. These must be the ones CI runs, one per line. -->

```bash
<setup command>            # install dependencies
<test command>             # the suite
<lint command>
<type-check command>
<build command>
```

## How a change flows

```
need → spec/proposal → [GATE 1: a human approves]
     → implementation (tests first)
     → review of your own diff
     → PR → [GATE 2: a human reviews] → merge
     → [GATE 3: a human authorises the deploy]
```

A human crosses the gates, never an agent. **Gate 1 is what pays off most with
several agents in parallel**: without an approved proposal, two agents solve the
same problem in two incompatible directions.

Before asking for Gate 2, review your own diff critically and list the findings
in the PR under `## Self-review`. Confirm each finding by **running it**, not by
reading.

## Working in parallel

- One agent, one branch, one worktree. **A worktree belongs to somebody**: do
  not delete it without confirming its branch is pushed.
- If a subagent of yours touched shared files, **check the diff yourself**
  (`git diff --stat`). A report saying "the tree is clean" is not evidence.
- If the main branch moved, integrate it (`git fetch && git merge origin/<main>`).
  That updates your branch; it does **not** authorise you to push or merge.

## Language

- Code, comments, commits, PRs: **<English>**.
- `docs/agent/` and conversation: **<English>**.

## Commit style

Conventional Commits with a scope: `feat(api): add rate limiting`.
Types: `feat`, `fix`, `chore`, `refactor`, `docs`, `test`, `ci`, `perf`.
