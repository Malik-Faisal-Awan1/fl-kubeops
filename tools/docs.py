#!/usr/bin/env python3
"""Keep README.md, AGENTS.md and docs/sprint-1.md in sync with project.toml and the repo.

Usage:
    python3 tools/docs.py --write   regenerate marked sections; run invariant checks
    python3 tools/docs.py --check   change nothing; fail if docs are stale or a rule is broken

Standard library only (Python 3.11+). Text between
    <!-- BEGIN GENERATED:name -->  and  <!-- END GENERATED:name -->
is owned by this script. Edit project.toml instead of editing that text.
"""
from __future__ import annotations

import argparse
import re
import sys
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# file -> generated blocks it must contain
TARGETS: dict[str, list[str]] = {
    "README.md": ["status", "layout", "toolchain", "commands", "team"],
    "AGENTS.md": ["state", "layout", "decisions", "blocked", "team", "open", "commands"],
    "docs/sprint-1.md": ["header", "scope", "out_of_scope", "tasks", "ac", "unverified"],
}

MARKER = re.compile(
    r"(<!-- BEGIN GENERATED:(?P<name>[a-z_]+) -->)\n(?P<body>.*?)\n?(<!-- END GENERATED:(?P=name) -->)",
    re.DOTALL,
)

DEP_GLOBS = [
    "pyproject.toml", "requirements*.txt", "requirements*.lock",
    "*/pyproject.toml", "*/requirements*.txt", "*/requirements*.lock",
]


# ----------------------------------------------------------------- helpers
def load(root: Path) -> dict:
    with open(root / "project.toml", "rb") as fh:
        return tomllib.load(fh)


def cell(text: str) -> str:
    return str(text).replace("|", "\\|").replace("\n", " ")


def table(headers: list[str], rows: list[list[str]]) -> str:
    out = ["| " + " | ".join(headers) + " |", "| " + " | ".join("---" for _ in headers) + " |"]
    out += ["| " + " | ".join(cell(c) for c in row) + " |" for row in rows]
    return "\n".join(out)


def real_files(root: Path, pattern: str) -> list[Path]:
    return [p for p in root.glob(pattern) if p.is_file() and p.name != ".gitkeep"]


def make_targets(root: Path) -> set[str]:
    mk = root / "Makefile"
    if not mk.is_file():
        return set()
    return set(re.findall(r"(?m)^([A-Za-z0-9_.-]+):", mk.read_text(encoding="utf-8")))


def name_regex(name: str) -> str:
    return "[-_.]+".join(re.escape(part) for part in re.split(r"[-_.]", name))


def dep_files(root: Path) -> list[Path]:
    found: set[Path] = set()
    for pattern in DEP_GLOBS:
        found.update(p for p in root.glob(pattern) if p.is_file())
    return sorted(found)


def strip_comments(text: str) -> str:
    return "\n".join(line for line in text.splitlines() if not line.lstrip().startswith("#"))


# --------------------------------------------------------------- rendering
def render(cfg: dict, root: Path) -> dict[str, str]:
    proj = cfg["project"]
    states = []
    for st in cfg.get("state", []):
        states.append((st, bool(real_files(root, st["glob"]))))
    code_present = [st["label"] for st, ok in states if ok and st.get("kind") == "code"]
    targets = make_targets(root)
    cmds = [c for c in cfg.get("command", []) if c["target"] in targets]

    blocks: dict[str, str] = {}
    blocks["status"] = (
        f"**{proj['sprint']}: {proj['sprint_status']}.** Application code: "
        + (", ".join(code_present) if code_present else "none yet")
        + ". See `docs/sprint-1.md` for tasks."
    )
    blocks["state"] = (
        f"Current sprint: **{proj['sprint']}**, status **{proj['sprint_status']}**.\n\n"
        + table(["Item", "Status"], [[st["label"], "present" if ok else "absent"] for st, ok in states])
        + "\n\nApplication code: "
        + (", ".join(code_present) if code_present else "**none exists yet**")
        + "."
    )
    layout = table(["Path", "Purpose"], [[f"`{p['path']}/`", p["purpose"]] for p in cfg["path"]])
    blocks["layout"] = layout
    blocks["toolchain"] = " · ".join(d["short"] for d in cfg["decision"] if "short" in d)
    if cmds:
        blocks["commands"] = "\n".join(f"- `{c['cmd']}`: {c['purpose']}" for c in cmds)
    else:
        blocks["commands"] = "_No commands exist yet. Do not invent any._"
    blocks["decisions"] = table(["Topic", "Decision"], [[d["topic"], d["value"]] for d in cfg["decision"]])
    blocks["blocked"] = table(
        ["Package", "Blocked until", "Why"],
        [[f"`{b['name']}`", b["until"], b["why"]] for b in cfg.get("blocked", [])],
    )
    people = cfg.get("person", [])
    blocks["team"] = table(["Person", "Role", "Sprint stories"], [[p["name"], p["role"], p["stories"]] for p in people])
    blocks["open"] = "\n".join(f"- {o['text']}" for o in cfg.get("open_item", []))
    blocks["header"] = (
        f"**Status:** {proj['sprint_status']} · **Dates:** {proj['sprint_dates']}\n\n"
        f"**Objective:** {proj['objective']}\n\n**Capacity:** {proj['capacity']}."
    )
    blocks["scope"] = table(
        ["ID", "Item", "Owner", "Points"],
        [[s["id"], s["item"], s["owner"], s["points"]] for s in cfg.get("scope", [])],
    )
    blocks["out_of_scope"] = " · ".join(proj["out_of_scope"])
    blocks["tasks"] = "\n".join(
        f"- [{'x' if t['done'] else ' '}] {i}. {t['title']} ({t['owner']})"
        for i, t in enumerate(cfg.get("task", []), start=1)
    )
    blocks["ac"] = "\n".join(f"- **{a['id']}** {a['text']}" for a in cfg.get("ac", []))
    blocks["unverified"] = "\n".join(f"- {u['text']}" for u in cfg.get("unverified", []))
    return blocks


def apply_blocks(text: str, blocks: dict[str, str], where: str, errors: list[str]) -> str:
    seen: set[str] = set()

    def sub(m: re.Match) -> str:
        name = m.group("name")
        seen.add(name)
        if name not in blocks:
            errors.append(f"{where}: unknown generated block '{name}'")
            return m.group(0)
        return f"{m.group(1)}\n{blocks[name]}\n{m.group(4)}"

    new = MARKER.sub(sub, text)
    for name in TARGETS.get(where, []):
        if name not in seen:
            errors.append(f"{where}: missing block <!-- BEGIN GENERATED:{name} --> ... <!-- END GENERATED:{name} -->")
    return new


# -------------------------------------------------------------- invariants
def invariants(cfg: dict, root: Path) -> list[str]:
    errs: list[str] = []

    declared = {p["path"] for p in cfg["path"]}
    for entry in sorted(root.iterdir()):
        if entry.is_dir() and not entry.name.startswith("."):
            if entry.name not in declared:
                errs.append(f"undeclared top-level folder '{entry.name}/': add it to [[path]] in project.toml or remove it")
    for p in sorted(declared):
        if not (root / p).is_dir():
            errs.append(f"declared path '{p}/' does not exist")

    files = dep_files(root)
    for d in cfg["decision"]:
        for pin in d.get("pins", []):
            name, _, ver = pin.partition("==")
            rx = re.compile(
                r"(?i)(?<![A-Za-z0-9_.-])" + name_regex(name) + r"(?:\[[^\]]*\])?\s*==\s*([0-9][^\s\"',;\]\\]*)"
            )
            for f in files:
                for found in rx.findall(strip_comments(f.read_text(encoding="utf-8", errors="replace"))):
                    if not (found == ver or found.startswith(ver + "+")):
                        errs.append(f"{f.relative_to(root)}: {name}=={found} but project.toml pins {pin}")
    for b in cfg.get("blocked", []):
        rx = re.compile(
            r"(?im)(?<![A-Za-z0-9_.-])" + name_regex(b["name"]) + r"(?:\[[^\]]*\])?\s*(?:==|>=|<=|~=|!=|<|>|;|,|[\"']|$)"
        )
        for f in files:
            if rx.search(strip_comments(f.read_text(encoding="utf-8", errors="replace"))):
                errs.append(
                    f"{f.relative_to(root)}: blocked package '{b['name']}' (blocked until {b['until']}: {b['why']}). "
                    "Remove it, or have a human remove it from [[blocked]] in project.toml"
                )

    wf_dir = root / ".github" / "workflows"
    if wf_dir.is_dir():
        for wf in sorted(list(wf_dir.glob("*.yml")) + list(wf_dir.glob("*.yaml"))):
            text = wf.read_text(encoding="utf-8")
            rel = wf.relative_to(root)
            for m in re.finditer(r"(?m)^\s*-?\s*uses:\s*(\S+)", text):
                ref = m.group(1)
                if ref.startswith("./"):
                    continue
                if not re.search(r"@[0-9a-f]{40}$", ref):
                    errs.append(f"{rel}: action '{ref}' is not pinned to a full 40-char commit SHA")
            if re.search(r"(?m)^\s*runs-on:\s*.*latest", text):
                errs.append(f"{rel}: do not use a '-latest' runner; use ubuntu-24.04")
            if "pull_request_target" in text:
                errs.append(f"{rel}: pull_request_target is forbidden")
            if not re.search(r"(?m)^permissions:", text):
                errs.append(f"{rel}: missing top-level 'permissions:' (use contents: read)")

    for i, t in enumerate(cfg.get("task", []), start=1):
        if t.get("done"):
            for pattern in t.get("evidence", []):
                if not real_files(root, pattern):
                    errs.append(f"task {i} is marked done but evidence '{pattern}' does not exist: {t['title']}")
    return errs


# --------------------------------------------------------------------- run
def run(root: Path, write: bool) -> tuple[list[str], list[str]]:
    """Return (errors, updated_files)."""
    cfg = load(root)
    blocks = render(cfg, root)
    errors: list[str] = []
    updated: list[str] = []
    for rel in TARGETS:
        path = root / rel
        if not path.is_file():
            errors.append(f"{rel}: file is missing")
            continue
        old = path.read_text(encoding="utf-8")
        new = apply_blocks(old, blocks, rel, errors)
        if new != old:
            if write:
                path.write_text(new, encoding="utf-8")
                updated.append(rel)
            else:
                errors.append(f"{rel}: out of date. Run `make docs` (or `python3 tools/docs.py --write`) and commit the result")
    errors += invariants(cfg, root)
    return errors, updated


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    mode = ap.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true")
    mode.add_argument("--check", action="store_true")
    args = ap.parse_args(argv)
    errors, updated = run(ROOT, write=args.write)
    for rel in updated:
        print(f"updated: {rel}")
    for e in errors:
        print(f"ERROR: {e}", file=sys.stderr)
    if errors:
        return 1
    print("docs OK" if args.check else "docs written; all checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
