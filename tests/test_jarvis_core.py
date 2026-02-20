from __future__ import annotations

from jarvis_core import resolve_open_target


def test_resolve_open_target_known_aliases():
    assert resolve_open_target("калькулятор") == "calc.exe"
    assert resolve_open_target("notepad") == "notepad.exe"
    assert resolve_open_target("терминал") == "cmd.exe"
    assert resolve_open_target("браузер") == "https://google.com"
    assert resolve_open_target("steam") == "steam"


def test_resolve_open_target_fallback_to_raw_query():
    assert resolve_open_target("msinfo32.exe") == "msinfo32.exe"
