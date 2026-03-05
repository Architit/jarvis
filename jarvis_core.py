from __future__ import annotations

import re
from typing import Dict, Optional


TARGET_MAP: Dict[str, Dict[str, str]] = {
    "core": {"system_id": "LRPT", "subtree_prefix": "LRPT/core", "address": "LRPT/core"},
    "archive": {"system_id": "TRNM", "subtree_prefix": "TRNM/Trianiuma", "address": "Trianiuma"},
    "trianiuma": {"system_id": "TRNM", "subtree_prefix": "TRNM/Trianiuma", "address": "Trianiuma"},
    "chronolog": {"system_id": "LRPT", "subtree_prefix": "LRPT/chronolog", "address": "LRPT/chronolog"},
}

GLOBAL_RECURSIVE_WRITE_PATTERNS = (
    r"\brm\s+-rf\s+LRPT/",
    r"\bcp\s+-r\s+.+\s+LRPT/",
    r"\bmv\s+.+\s+LRPT/",
    r">\s*LRPT/",
    r"\btee\b.+LRPT/",
    r"\bfind\s+LRPT/.*-exec\s+.*(rm|mv|cp)",
)


def resolve_open_target(query: str) -> str:
    q = (query or "").lower().strip()

    if "калькулятор" in q or "calc" in q:
        return "calc.exe"
    if "блокнот" in q or "notepad" in q:
        return "notepad.exe"
    if "cmd" in q or "терминал" in q:
        return "cmd.exe"
    if "браузер" in q or "хром" in q:
        return "https://google.com"
    if "steam" in q:
        return "steam"
    return q


def resolve_orchestration_target(query: str) -> Optional[Dict[str, str]]:
    """Deterministically resolve known organ targets to system_id/subtree_prefix."""
    q = (query or "").lower().strip()
    for key, target in TARGET_MAP.items():
        if key in q:
            return dict(target)
    return None


def is_global_recursive_write(command: str) -> bool:
    """Detect prohibited global recursive write intents against LRPT/."""
    cmd = (command or "").strip()
    if not cmd:
        return False
    for pattern in GLOBAL_RECURSIVE_WRITE_PATTERNS:
        if re.search(pattern, cmd):
            return True
    return False


def enforce_no_global_writes(command: str, explicit_approval: bool = False) -> None:
    """Fail-fast guard: block dangerous writes unless explicit approval is present."""
    if is_global_recursive_write(command) and not explicit_approval:
        raise ValueError(
            "NO_GLOBAL_WRITES: blocked command requires explicit approval"
        )
