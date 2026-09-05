#!/usr/bin/env python3
"""Validate every SKILL.md in skills/ against the repo authoring standard.

Usage:
  python3 tools/validate_skills.py [--strict]

No third-party dependencies (a minimal YAML front-matter parser is included)
so it runs on a bare CI runner.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = ROOT / "skills"

NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
MAX_NAME = 64
MAX_DESC = 1024
MAX_BODY_LINES = 500

REQUIRED_SECTIONS = [
    "## When to use",
    "## Non-negotiables",
    "## Definition of Done",
]
RECOMMENDED_SECTIONS = ["## Workflow", "## References", "## ملخص عربي"]
KNOWN_KEYS = {
    "name", "description", "version", "license", "category", "tags",
    "allowed-tools", "metadata", "when_to_use", "compatibility",
}


def split_frontmatter(text: str) -> tuple[str, str]:
    if not text.startswith("---"):
        return "", text
    end = text.find("\n---", 3)
    if end == -1:
        return "", text
    return text[3:end], text[end + 4:]


def parse_yaml_ish(raw: str) -> dict:
    """Tiny parser: top-level `key: value`, block scalars (>-, |), inline lists,
    dash lists and one nested mapping level. Enough for skill frontmatter."""
    data: dict = {}
    lines = raw.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        if not line.strip() or line.lstrip().startswith("#") or line.startswith((" ", "\t")):
            i += 1
            continue
        if ":" not in line:
            i += 1
            continue
        key, _, value = line.partition(":")
        key, value = key.strip(), value.strip()
        if value in (">", ">-", "|", "|-"):  # block scalar
            i += 1
            buf = []
            while i < len(lines) and (not lines[i].strip() or lines[i].startswith((" ", "\t"))):
                buf.append(lines[i].strip())
                i += 1
            data[key] = " ".join(b for b in buf if b)
            continue
        if value == "":  # nested block or dash list
            i += 1
            child: dict = {}
            items: list = []
            while i < len(lines) and (not lines[i].strip() or lines[i].startswith((" ", "\t"))):
                sub = lines[i].strip()
                if sub.startswith("- "):
                    items.append(sub[2:].strip())
                elif ":" in sub:
                    k2, _, v2 = sub.partition(":")
                    child[k2.strip()] = v2.strip().strip("\"'")
                i += 1
            data[key] = items if items else child
            continue
        if value.startswith("[") and value.endswith("]"):
            inner = value[1:-1].strip()
            data[key] = [v.strip().strip("\"'") for v in inner.split(",") if v.strip()]
        else:
            data[key] = value.strip("\"'")
        i += 1
    return data


def validate(path: Path, strict: bool) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    rel = path.relative_to(ROOT)
    text = path.read_text(encoding="utf-8")
    raw_fm, body = split_frontmatter(text)

    if not raw_fm:
        return [f"{rel}: missing YAML frontmatter"], warnings
    fm = parse_yaml_ish(raw_fm)

    name = fm.get("name", "")
    folder = path.parent.name
    if not name:
        errors.append(f"{rel}: `name` is required")
    else:
        if not NAME_RE.match(name):
            errors.append(f"{rel}: `name` must be kebab-case (got '{name}')")
        if len(name) > MAX_NAME:
            errors.append(f"{rel}: `name` exceeds {MAX_NAME} chars")
        if name != folder:
            errors.append(f"{rel}: `name` ('{name}') must match folder ('{folder}')")

    desc = fm.get("description", "")
    if not desc:
        errors.append(f"{rel}: `description` is required")
    else:
        if len(desc) > MAX_DESC:
            errors.append(f"{rel}: `description` exceeds {MAX_DESC} chars ({len(desc)})")
        if len(desc) < 60:
            warnings.append(f"{rel}: `description` is short; add trigger keywords")
        if not re.search(r"\buse when\b", desc, re.I):
            warnings.append(f"{rel}: `description` should contain a 'Use when ...' trigger clause")
        if "<" in desc and ">" in desc:
            warnings.append(f"{rel}: `description` should not contain XML-ish tags")

    if "version" in fm and not re.match(r"^\d+\.\d+\.\d+$", str(fm["version"])):
        warnings.append(f"{rel}: `version` should be semver (x.y.z)")

    for key in fm:
        if key not in KNOWN_KEYS:
            warnings.append(f"{rel}: unknown frontmatter key '{key}'")

    body_lines = body.strip().splitlines()
    if len(body_lines) > MAX_BODY_LINES:
        errors.append(f"{rel}: body has {len(body_lines)} lines (max {MAX_BODY_LINES}); move depth to references/")

    for section in REQUIRED_SECTIONS:
        if section.lower() not in body.lower():
            errors.append(f"{rel}: missing required section '{section}'")
    for section in RECOMMENDED_SECTIONS:
        if section.lower() not in body.lower():
            warnings.append(f"{rel}: missing recommended section '{section}'")

    # one-level-deep local references must exist
    for ref in re.findall(r"`(references/[^`]+\.md)`", body):
        if not (path.parent / ref).exists():
            errors.append(f"{rel}: referenced file '{ref}' does not exist")
        if ref.count("/") > 1:
            warnings.append(f"{rel}: reference '{ref}' is deeper than one level")

    return errors, warnings


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--strict", action="store_true", help="treat warnings as failures")
    args = ap.parse_args()

    if not SKILLS_DIR.exists():
        print("no skills/ directory found", file=sys.stderr)
        return 1

    skill_files = sorted(SKILLS_DIR.rglob("SKILL.md"))
    if not skill_files:
        print("no SKILL.md files found", file=sys.stderr)
        return 1

    all_errors: list[str] = []
    all_warnings: list[str] = []
    names: dict[str, Path] = {}

    for f in skill_files:
        errors, warnings = validate(f, args.strict)
        all_errors += errors
        all_warnings += warnings
        n = f.parent.name
        if n in names:
            all_errors.append(f"duplicate skill name '{n}': {f} and {names[n]}")
        names[n] = f

    for w in all_warnings:
        print(f"⚠️  {w}")
    for e in all_errors:
        print(f"❌ {e}")

    print(f"\nChecked {len(skill_files)} skills — {len(all_errors)} errors, {len(all_warnings)} warnings")
    if all_errors or (args.strict and all_warnings):
        return 1
    print("✅ All skills valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
