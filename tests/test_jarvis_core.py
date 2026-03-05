from __future__ import annotations

import pytest

from jarvis_core import (
    enforce_no_global_writes,
    is_global_recursive_write,
    resolve_open_target,
    resolve_orchestration_target,
)


def test_resolve_open_target_known_aliases():
    assert resolve_open_target("калькулятор") == "calc.exe"
    assert resolve_open_target("notepad") == "notepad.exe"
    assert resolve_open_target("терминал") == "cmd.exe"
    assert resolve_open_target("браузер") == "https://google.com"
    assert resolve_open_target("steam") == "steam"


def test_resolve_open_target_fallback_to_raw_query():
    assert resolve_open_target("msinfo32.exe") == "msinfo32.exe"


def test_resolve_orchestration_target_known_organs():
    archive = resolve_orchestration_target("update the archive now")
    assert archive is not None
    assert archive["system_id"] == "TRNM"
    assert archive["subtree_prefix"] == "TRNM/Trianiuma"

    core = resolve_orchestration_target("jarvis status of core organ")
    assert core is not None
    assert core["system_id"] == "LRPT"
    assert core["subtree_prefix"] == "LRPT/core"


def test_resolve_orchestration_target_unknown_returns_none():
    assert resolve_orchestration_target("unknown target organ") is None


def test_no_global_writes_guard_blocks_without_approval():
    dangerous = "rm -rf LRPT/core/tmp"
    assert is_global_recursive_write(dangerous) is True
    with pytest.raises(ValueError, match="NO_GLOBAL_WRITES"):
        enforce_no_global_writes(dangerous, explicit_approval=False)


def test_no_global_writes_guard_allows_with_approval_or_safe_command():
    dangerous = "rm -rf LRPT/core/tmp"
    enforce_no_global_writes(dangerous, explicit_approval=True)
    enforce_no_global_writes("echo ok > /tmp/safe.txt", explicit_approval=False)
