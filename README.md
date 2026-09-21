# Template: multi-dev + multi-AI workflow

**English** · [Español](README.es.md)

A skeleton for repos where **several people and several AI agents** (Codex,
Claude Code, Cursor, Gemini) work at the same time without stepping on each
other.

Not a framework, no dependencies. Four convention files and a ~250-line
standard-library script.

## The problem it solves

When the project's state lives in one markdown file that everybody edits, every
branch collides with every other branch. This is not a discipline problem, it is
geometry: everyone writes in the same place in the same file.

Here the state lives in **many small files, one per item**, and the aggregate
view (`docs/agent/STATE.md`) is **generated and never committed**. Two agents
working on different things touch different files, and git merges them on its
own.

## Using it in a new project

**1. Start from the template** — on GitHub, *Use this template*, or:

```bash
git clone https://github.com/giovanniadamo/agent-workflow-template /tmp/tpl
rm -rf /tmp/tpl/.git
cp -r /tmp/tpl/. my-project/
```

**2. Have your agent adapt it.** This prompt is enough:

> This repo ships the multi-agent workflow template. Read `AGENTS.md` and
> `docs/agent/`. Adapt them to this project: fill in
> `docs/agent/state/status.yaml`, replace the commands in `AGENTS.md` with this
> stack's real ones, delete the `EXAMPLE-*` fragments and the example log entry,
> and create the `pending/` fragments for what still has to be done. Then run
> `python scripts/render_state.py` and confirm it exits 0.

**3. Check that the loop closes:**

```bash
python scripts/render_state.py   # must exit 0
cat docs/agent/STATE.md
```

That is it. From then on no agent needs anything handed to it: its tool reads
the contract on its own when it opens the repo.

## Why it works with any tool

`AGENTS.md` is the **only** real content. The rest are one-line pointers:

| File | Read by |
| --- | --- |
| `AGENTS.md` | Codex and several agents |
| `CLAUDE.md` | Claude Code |
| `.cursor/rules` | Cursor |
| `GEMINI.md` | Gemini CLI |

A developer using a different tool **configures nothing**: they clone the repo
and their agent is already under the same contract. When a new tool shows up you
add one more pointer — never a second copy of the rules.

## What is inside

```
AGENTS.md                     the agent contract (the only real content)
CLAUDE.md / GEMINI.md
.cursor/rules                 one-line pointers
.gitattributes                LF: Windows devs + Linux CI
.gitignore                    the generated views are NOT committed

docs/agent/
  state/                      LIVE STATE — one file per item
    status.yaml               project invariants
    active/                   in progress (and file reservations)
    pending/                  queue, each item with its exit criterion
    blocked/                  waiting on a person or on infrastructure
    conventions/              decisions in force
  log/                        IMMUTABLE HISTORY — YYYY-MM-DD-slug.md
  STATE.md                    GENERATED — gitignored, nobody edits it

scripts/render_state.py       the generator (stdlib, nothing to install)
.github/workflows/            the check that makes the convention stick
```

## Three decisions worth keeping

**1. The view is generated and never committed.** Commit it and you bring back
the conflicts this whole design exists to avoid. CI enforces it.

**2. The generator fails closed.** On any error it deletes its outputs and exits
1. The contract says: *if it does not exit 0, do not read `STATE.md`*. A
half-written view read as truth is the most expensive failure mode, because it
looks like good data.

**3. Volatile facts are queried, not stored.** SHAs, PRs and branches are read at
render time. A pointer written by hand goes stale in hours, and somebody makes a
decision with it.

## Closing an item means deleting its file

You do not strike it through or mark it "DONE" leaving the text behind. You
delete the fragment and write an entry in `log/`. This has to be said out loud
because every agent's reflex is to *add*: without the rule, in two months you
have 58 "active" items of which 36 closed weeks ago.

## For your team

Paste this into your project's README:

```markdown
## Working with AI agents
The contract lives in AGENTS.md (your tool reads it on its own).
Before you work:  python scripts/render_state.py  → read docs/agent/STATE.md
When you finish: an entry in docs/agent/log/ + update docs/agent/state/.
Everything lands through a PR. Nobody edits STATE.md: it is generated.
```

## What to add later

The skeleton covers shared state. As the project grows:

- **Specs approved by a human** before implementing. With several agents in
  parallel this is what pays off most: without an approved proposal, two agents
  solve the same problem in two incompatible directions.
- **Reviewing your own diff** before asking for human review.
- **A check for every convention that matters.** Without verification, a
  convention is a suggestion.

## Language

The template ships in English so it is usable by any team. Both the contract and
the fragments are meant to be **translated into your team's language** — the
agents work equally well either way, and `README.es.md` is the Spanish version of
this file.

## License

MIT — use it, copy it and adapt it freely, in your own or your company's
projects.

## Contributing

If you used it and something did not fit your stack, an issue with the concrete
case is worth more than a general suggestion: this skeleton came out of real
failure modes, and that is how it keeps growing.
