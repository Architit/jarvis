from __future__ import annotations


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
