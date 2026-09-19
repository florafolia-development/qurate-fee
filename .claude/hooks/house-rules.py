#!/usr/bin/env python3
"""House-rule guard. Runs as a Claude Code PostToolUse hook after Edit/Write.

Checks the file that was just written against the rules that are cheap to
check and expensive to get wrong.

Blocking:
  1. Banned brand hex values. The authoritative Qurate palette is Navy
     #2B3D4B, Gold #CA8D05, Cream #D9D2BE, per
     qurate-qvos-skills/skills/qurate-pptx/SKILL.md. Four look-alikes were
     asserted by an earlier source, reached a production deliverable on
     15 August 2026, and are banned outright.
  2. Calibri. Segoe UI is the sole Qurate font, no fallback declared.

Advisory:
  3. Em dashes in Markdown and user-facing copy. House style in every
     register, but two thirds of the existing Markdown in the firm brain
     carries one, so blocking on it would make this guard the first thing
     anyone switched off. It reports and the author decides.

Exit 0 passes. Exit 2 blocks and hands the message back to Claude to fix.
A missing, unreadable or unparseable input is a pass, never a crash: a guard
that falls over on its own plumbing gets switched off, and then it guards
nothing.
"""

from __future__ import annotations

import json
import os
import re
import sys

EM_DASH = chr(0x2014)  # written as a code point so this file obeys the rule

BANNED_HEX = {
    "2D3748": "navy look-alike",
    "D4A843": "gold look-alike",
    "2E3D49": "navy look-alike, present in some legacy issued decks",
    "C19131": "gold look-alike, from the Brand Guidelines printed hex",
}
CORRECT = "Navy #2B3D4B, Gold #CA8D05, Cream #D9D2BE"

# Files whose job is to document the ban, or to record what a legacy artefact
# contains. Matched as a path suffix. A repo adds its own in
# .claude/hooks/house-rules.json next to this script, under "hex_exempt".
# That list is a debt register: every entry is a file still carrying the wrong
# palette, and it should only ever get shorter.
HEX_EXEMPT_SUFFIXES = (
    "skills/qurate-pptx/SKILL.md",
    "skills/qurate-pptx/INSTALL.md",
    "skills/qurate-docx/SKILL.md",
    "skills/qurate-marketcomps-3-assessed-multiple/SKILL.md",
    "shared/brand-spec.md",
    "firm/engineering-operating-standard.md",
    ".claude/hooks/house-rules.py",
    "docs/INCIDENTS.md",
)

EM_DASH_EXTS = {".md", ".mdx", ".txt", ".tsx", ".jsx", ".ts", ".js"}


def repo_exemptions() -> tuple[str, ...]:
    cfg = os.path.join(os.path.dirname(os.path.abspath(__file__)), "house-rules.json")
    try:
        with open(cfg, encoding="utf-8") as fh:
            data = json.load(fh)
    except (OSError, json.JSONDecodeError, ValueError):
        return ()
    got = data.get("hex_exempt")
    return tuple(str(x) for x in got) if isinstance(got, list) else ()


def payload() -> dict:
    try:
        parsed = json.loads(sys.stdin.read() or "{}")
    except (json.JSONDecodeError, ValueError):
        return {}
    return parsed if isinstance(parsed, dict) else {}


def main() -> int:
    data = payload()
    path = (data.get("tool_input") or {}).get("file_path") or ""
    if not path or not os.path.isfile(path):
        return 0
    try:
        with open(path, encoding="utf-8", errors="replace") as fh:
            text = fh.read()
    except OSError:
        return 0

    rel = path.replace(os.sep, "/")
    _, ext = os.path.splitext(rel)
    problems: list[str] = []
    notices: list[str] = []

    exempt = HEX_EXEMPT_SUFFIXES + repo_exemptions()
    if not any(rel.endswith(suffix) for suffix in exempt):
        for bad, why in BANNED_HEX.items():
            if re.search(rf"#?{bad}\b", text, re.IGNORECASE):
                problems.append(
                    f"banned brand hex {bad} ({why}). The palette is {CORRECT}."
                )
        if re.search(r"\bCalibri\b", text):
            problems.append(
                "Calibri. Segoe UI is the sole Qurate font, no fallback declared."
            )

    if ext in EM_DASH_EXTS:
        hits = [n for n, line in enumerate(text.splitlines(), 1) if EM_DASH in line]
        if hits:
            where = ", ".join(f"{rel}:{n}" for n in hits[:5])
            more = f" and {len(hits) - 5} more" if len(hits) > 5 else ""
            notices.append(
                f"em dash at {where}{more}. House style is no em dashes, in any "
                f"register. Replace the ones this change introduced."
            )

    if problems:
        print(f"House rules blocked the write to {rel}:", file=sys.stderr)
        for problem in problems:
            print(f"  - {problem}", file=sys.stderr)
        print("Fix these and write the file again.", file=sys.stderr)
        return 2

    if notices:
        print(
            json.dumps(
                {
                    "hookSpecificOutput": {
                        "hookEventName": "PostToolUse",
                        "additionalContext": "House rules notice: "
                        + "; ".join(notices),
                    }
                }
            )
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())
