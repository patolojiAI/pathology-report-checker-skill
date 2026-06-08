#!/usr/bin/env python3
"""Build the distributable ``.skill`` archive for the pathology-report-checker skill.

A ``.skill`` file is just a zip of the skill folder, structured so it imports
cleanly via **Claude.ai -> Settings -> Capabilities -> Skills -> Upload skill**
(or the Claude desktop app). Inside the zip everything lives under a single
top-level ``pathology-report-checker/`` directory with ``SKILL.md`` at its root,
which is what Claude expects.

Only the runtime payload ships. Everything listed in ``.skillignore`` (README,
LICENSE, dev tooling, the GitHub Pages site under ``docs/``, build output, etc.)
is excluded, so the uploaded skill carries just what Claude needs:

    SKILL.md
    references/...
    examples/...

The matcher implements the small subset of ``.gitignore`` syntax actually used
in ``.skillignore``: blank lines and ``#`` comments are skipped, a trailing
``/`` is treated as a directory, ``*.ext`` globs match by basename, and a bare
name matches any path component (so ``.dev`` hides the whole ``.dev/`` tree).

Usage::

    python3 .dev/scripts/build_skill.py
        # -> dist/pathology-report-checker.skill

The script is idempotent: it overwrites any existing archive.

Release (run after the branch is merged and the repo is public)::

    python3 .dev/scripts/build_skill.py
    gh release create v1.3.0 dist/pathology-report-checker.skill \
        --title "v1.3.0" --notes "..."

The README download link points at ``releases/latest/download/<name>.skill``,
so it resolves to the newest release automatically and never needs updating.
"""

from __future__ import annotations

import fnmatch
import sys
import zipfile
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
SKILL_NAME = "pathology-report-checker"
# The skill content lives in its own folder (canonical plugin layout); the .skill
# bundle is built from there so the zip's top-level dir stays ``pathology-report-checker/``.
SKILL_SRC = REPO / "skills" / SKILL_NAME
DIST_DIR = REPO / "dist"
SKILLIGNORE = REPO / ".skillignore"

# Always excluded, even if .skillignore is missing or edited.
# (.skillignore is a build-control file with no runtime value inside the skill.)
ALWAYS_IGNORE = [".git", "dist", "__pycache__", ".DS_Store", ".skillignore"]


def load_ignore_patterns() -> list[str]:
    """Read .skillignore into a flat list of patterns (dir slashes stripped)."""
    patterns: list[str] = list(ALWAYS_IGNORE)
    if SKILLIGNORE.is_file():
        for raw in SKILLIGNORE.read_text(encoding="utf-8").splitlines():
            line = raw.strip()
            if not line or line.startswith("#"):
                continue
            patterns.append(line.rstrip("/"))
    return patterns


def is_ignored(rel: Path, patterns: list[str]) -> bool:
    """True if the repo-relative path matches any .skillignore pattern."""
    rel_str = rel.as_posix()
    for pat in patterns:
        # Whole-path or path-prefix match (handles "docs", "references/_old", ...)
        if (
            fnmatch.fnmatch(rel_str, pat)
            or fnmatch.fnmatch(rel_str, f"{pat}/*")
            or fnmatch.fnmatch(rel_str, f"*/{pat}/*")
        ):
            return True
        # Basename / single-component match (handles "*.pyc", ".dev", "LICENSE")
        for part in rel.parts:
            if fnmatch.fnmatch(part, pat):
                return True
    return False


def collect_payload(patterns: list[str]) -> list[Path]:
    """All skill files that should ship inside the .skill, sorted."""
    payload: list[Path] = []
    for path in sorted(SKILL_SRC.rglob("*")):
        if not path.is_file():
            continue
        rel = path.relative_to(SKILL_SRC)
        if is_ignored(rel, patterns):
            continue
        payload.append(path)
    return payload


def build() -> int:
    patterns = load_ignore_patterns()
    payload = collect_payload(patterns)

    if not any(p.name == "SKILL.md" and p.parent == SKILL_SRC for p in payload):
        print("error: SKILL.md not found in payload — refusing to build", file=sys.stderr)
        return 1

    DIST_DIR.mkdir(parents=True, exist_ok=True)
    out_path = DIST_DIR / f"{SKILL_NAME}.skill"
    if out_path.exists():
        out_path.unlink()

    with zipfile.ZipFile(out_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for path in payload:
            arcname = (Path(SKILL_NAME) / path.relative_to(SKILL_SRC)).as_posix()
            zf.write(path, arcname)

    size_kb = out_path.stat().st_size / 1024
    print(f"  ✓ {out_path.name}  ({len(payload)} files, {size_kb:.1f} KB)")
    print(f"  → {out_path.relative_to(REPO)}")
    print()
    print("  Payload:")
    for path in payload:
        print(f"      {path.relative_to(REPO).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(build())
