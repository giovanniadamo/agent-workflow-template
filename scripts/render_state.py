#!/usr/bin/env python3
"""Render docs/agent/STATE.md and docs/agent/log/INDEX.md from versioned fragments.

The generated views are NOT tracked in git: they are rebuilt on demand, so no
two branches ever edit the same file. The sources are the small fragments under
docs/agent/state/ (one file per item) and the immutable entries under
docs/agent/log/.

Fail-closed: on any error both outputs are deleted and the process exits 1.
Consumers may read them only after exit 0.

Volatile facts (branch SHAs, open PRs) are never stored — they are queried here
and injected, or reported as `no disponible`.

    python scripts/render_state.py
    python scripts/render_state.py --check   # validate only, write nothing

Standard library only, on purpose: it must run on any machine that can run the
project, with no install step.
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from dataclasses import dataclass
from datetime import date
from pathlib import Path

SECTIONS: tuple[str, ...] = ("active", "pending", "blocked", "conventions")

SECTION_HEADINGS: dict[str, str] = {
    "active": "En curso",
    "pending": "Pendientes",
    "blocked": "Bloqueado (espera a una persona o a infraestructura)",
    "conventions": "Convenciones vigentes",
}

# A fragment's frontmatter is a deliberately tiny YAML subset: `key: value`,
# one per line, optionally quoted. Parsing it here instead of depending on
# PyYAML keeps this script installable-free. Anything richer is a smell: a
# fragment is a note, not a data structure.
_FRONTMATTER_RE = re.compile(r"\A---\r?\n(.*?)\r?\n---\r?\n?(.*)\Z", re.DOTALL)
_KEY_RE = re.compile(r"^([A-Za-z_][A-Za-z0-9_]*):\s*(.*)$")
_ISO_DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def _say(message: str, *, err: bool = False) -> None:
    """Print without ever crashing on the console's encoding.

    A Windows console defaults to a legacy codepage, so an arrow or an accent
    in a status line raises UnicodeEncodeError and takes the whole run with it
    — on the very first command a new contributor types. The FILES this script
    writes are always UTF-8; only what reaches the terminal is degraded.
    """
    stream = sys.stderr if err else sys.stdout
    encoding = getattr(stream, "encoding", None) or "ascii"
    print(message.encode(encoding, "replace").decode(encoding), file=stream)


class RenderError(Exception):
    """Every problem found, reported at once — fixing them one round-trip at a
    time is the slowest possible way to learn the contract."""

    def __init__(self, problems: list[str]) -> None:
        super().__init__("\n".join(problems))
        self.problems = problems


@dataclass(frozen=True)
class Fragment:
    ident: str
    section: str
    title: str
    updated: date
    body: str
    path: Path


@dataclass(frozen=True)
class LogEntry:
    slug: str
    day: date
    summary: str
    path: Path


def _split_frontmatter(path: Path) -> tuple[dict[str, str], str]:
    raw = path.read_text(encoding="utf-8")
    match = _FRONTMATTER_RE.match(raw)
    if match is None:
        raise RenderError([f"{path}: falta el frontmatter (--- ... ---) al inicio"])
    front: dict[str, str] = {}
    for line in match.group(1).splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        key_match = _KEY_RE.match(line.strip())
        if key_match is None:
            raise RenderError([f"{path}: línea de frontmatter inválida: {line!r}"])
        value = key_match.group(2).strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
            value = value[1:-1]
        front[key_match.group(1)] = value
    return front, match.group(2).strip()


def _parse_fragment(path: Path, section: str) -> Fragment:
    front, body = _split_frontmatter(path)
    problems: list[str] = []

    ident = front.get("id", "")
    if not ident:
        problems.append(f"{path}: falta `id`")
    elif ident != path.stem:
        problems.append(f"{path}: `id` ({ident}) debe coincidir con el nombre del archivo ({path.stem})")

    declared = front.get("section", "")
    if declared != section:
        problems.append(f"{path}: `section` ({declared or 'ausente'}) debe ser `{section}`, como su carpeta")

    title = front.get("title", "")
    if not title:
        problems.append(f"{path}: falta `title`")

    updated_raw = front.get("updated", "")
    updated: date | None = None
    if not _ISO_DATE_RE.match(updated_raw):
        problems.append(f"{path}: `updated` debe ser una fecha ISO (YYYY-MM-DD), no {updated_raw!r}")
    else:
        try:
            updated = date.fromisoformat(updated_raw)
        except ValueError:
            problems.append(f"{path}: `updated` no es una fecha real: {updated_raw!r}")

    if not body:
        problems.append(f"{path}: el cuerpo está vacío — un ítem sin cuerpo no le sirve a nadie")

    if problems or updated is None:
        raise RenderError(problems)
    return Fragment(ident=ident, section=section, title=title, updated=updated, body=body, path=path)


def _load_fragments(root: Path) -> list[Fragment]:
    fragments: list[Fragment] = []
    problems: list[str] = []
    seen: dict[str, Path] = {}
    for section in SECTIONS:
        directory = root / "docs" / "agent" / "state" / section
        if not directory.is_dir():
            problems.append(f"falta la carpeta {directory}")
            continue
        for path in sorted(directory.glob("*.md")):
            try:
                fragment = _parse_fragment(path, section)
            except RenderError as exc:
                problems.extend(exc.problems)
                continue
            if fragment.ident in seen:
                problems.append(f"{path}: `id` duplicado, ya usado por {seen[fragment.ident]}")
                continue
            seen[fragment.ident] = path
            fragments.append(fragment)
    if problems:
        raise RenderError(problems)
    return fragments


def _load_log(root: Path) -> list[LogEntry]:
    directory = root / "docs" / "agent" / "log"
    entries: list[LogEntry] = []
    problems: list[str] = []
    for path in sorted(directory.glob("*.md")):
        if path.name in {"INDEX.md", "README.md"}:
            continue
        front, _ = _split_frontmatter(path)
        summary = front.get("summary", "")
        if not summary:
            problems.append(f"{path}: falta `summary` en el frontmatter")
        stamp = path.name[:10]
        if not _ISO_DATE_RE.match(stamp):
            problems.append(f"{path}: el nombre debe empezar con YYYY-MM-DD")
            continue
        entries.append(
            LogEntry(slug=path.stem, day=date.fromisoformat(stamp), summary=summary, path=path)
        )
    if problems:
        raise RenderError(problems)
    entries.sort(key=lambda entry: (entry.day, entry.slug), reverse=True)
    return entries


def _load_status(root: Path) -> dict[str, str]:
    path = root / "docs" / "agent" / "state" / "status.yaml"
    if not path.is_file():
        raise RenderError([f"falta {path}"])
    status: dict[str, str] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        match = _KEY_RE.match(line.strip())
        if match is None:
            raise RenderError([f"{path}: línea inválida: {line!r}"])
        value = match.group(2).strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
            value = value[1:-1]
        status[match.group(1)] = value
    return status


def _run(argv: list[str], cwd: Path) -> str | None:
    """Best-effort shell-out. `None` means the fact is unavailable right now —
    never a stale value, which is the whole point of not storing these."""
    try:
        result = subprocess.run(argv, cwd=cwd, capture_output=True, text=True, timeout=20)
    except (OSError, subprocess.SubprocessError):
        return None
    if result.returncode != 0:
        return None
    return result.stdout.strip() or None


def _live_facts(root: Path) -> list[str]:
    lines: list[str] = []
    head = _run(["git", "rev-parse", "--short", "HEAD"], root)
    branch = _run(["git", "rev-parse", "--abbrev-ref", "HEAD"], root)
    if head and branch:
        lines.append(f"- **Checkout:** `{branch}` en `{head}`")
    else:
        lines.append("- **Checkout:** no disponible")

    prs = _run(
        ["gh", "pr", "list", "--state", "open", "--limit", "20",
         "--json", "number,title,headRefName",
         "--template", "{{range .}}  - #{{.number}} {{.title}} (`{{.headRefName}}`)\n{{end}}"],
        root,
    )
    if prs:
        lines.append("- **PRs abiertos:**")
        lines.extend(prs.splitlines())
    else:
        lines.append("- **PRs abiertos:** no disponible (¿`gh` sin auth?)")
    return lines


def _render_state(status: dict[str, str], fragments: list[Fragment], log: list[LogEntry], root: Path) -> str:
    lines = [
        f"# {status.get('project', 'Proyecto')} — estado",
        "",
        "GENERADO. No editar: los cambios se pierden en el próximo render.",
        "Se regenera con `python scripts/render_state.py`.",
        "Las fuentes son `docs/agent/state/` (un archivo por ítem) y `docs/agent/log/`.",
        "",
        "## Contexto",
        "",
    ]
    for key, value in status.items():
        if key == "project":
            continue
        lines.append(f"- **{key}:** {value}")
    lines.extend(_live_facts(root))

    if log:
        lines.extend(["", "## Últimas sesiones", ""])
        for entry in log[:10]:
            lines.append(f"- **{entry.day.isoformat()}** — [{entry.slug}](log/{entry.slug}.md): {entry.summary}")

    for section in SECTIONS:
        items = [fragment for fragment in fragments if fragment.section == section]
        items.sort(key=lambda item: (-item.updated.toordinal(), item.ident))
        lines.extend(["", f"## {SECTION_HEADINGS[section]}", ""])
        if not items:
            lines.append("_Nada._")
            continue
        for item in items:
            lines.append(f"### {item.title}")
            lines.append("")
            lines.append(f"_Actualizado {item.updated.isoformat()} · `{item.path.name}`_")
            lines.append("")
            lines.append(item.body)
            lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def _render_log_index(log: list[LogEntry]) -> str:
    lines = [
        "# Historial de sesiones",
        "",
        "GENERADO. No editar. Las entradas son inmutables: si algo cambió, entrada nueva.",
        "",
        "| Fecha | Entrada | Resumen |",
        "| --- | --- | --- |",
    ]
    for entry in log:
        summary = entry.summary.replace("|", "\\|")
        lines.append(f"| {entry.day.isoformat()} | [{entry.slug}]({entry.slug}.md) | {summary} |")
    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="validar sin escribir")
    args = parser.parse_args()

    root = Path(__file__).resolve().parent.parent
    state_out = root / "docs" / "agent" / "STATE.md"
    index_out = root / "docs" / "agent" / "log" / "INDEX.md"

    # Console messages stay ASCII-only: a Windows console defaults to a legacy
    # codepage and a stray arrow or accent crashes the run with
    # UnicodeEncodeError. The FILES are UTF-8; only what we print is limited.
    def fail(problems: list[str]) -> int:
        # Fail closed: a half-written view read as truth is worse than none.
        # This runs for validation errors AND for anything unexpected, so the
        # outputs can never survive a non-zero exit.
        for path in (state_out, index_out):
            path.unlink(missing_ok=True)
        _say("render_state: FAILED - do not read STATE.md or log/INDEX.md", err=True)
        for problem in problems:
            _say(f"  - {problem}", err=True)
        return 1

    try:
        status = _load_status(root)
        fragments = _load_fragments(root)
        log = _load_log(root)

        if args.check:
            _say(f"render_state: OK ({len(fragments)} fragments, {len(log)} log entries)")
            return 0

        state_out.write_text(
            _render_state(status, fragments, log, root), encoding="utf-8", newline="\n"
        )
        index_out.write_text(_render_log_index(log), encoding="utf-8", newline="\n")
    except RenderError as exc:
        return fail(exc.problems)
    except Exception as exc:  # noqa: BLE001 - last line of the fail-closed guarantee
        return fail([f"unexpected error: {type(exc).__name__}: {exc}"])

    _say(f"render_state: OK -> docs/agent/STATE.md ({len(fragments)} items, {len(log)} sessions)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
