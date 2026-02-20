# Test Mirror Matrix — J.A.R.V.I.S (2026-02-17)

## Existing Coverage

- Runtime smoke.
- Query-to-target normalization for known aliases + fallback.
- Governance artifact/header checks.

## Missing High-Value Tests

| Domain | Missing Test | Priority |
|---|---|---|
| Runtime Branches | `open_app_function` shell success/failure with mocked subprocess | P0 |
| Runtime Branches | Win+R fallback branch with mocked `pyautogui/pyperclip` | P0 |
| CLI | `--text` mode loop exit semantics | P1 |
| Resilience | speech recognition timeout/error handling loop behavior | P1 |
| Interop | payload/command bridge tests with ecosystem agents | P2 |

## Mirror Plan

- Mirror-A: P0 runtime branch tests with full mocking.
- Mirror-B: P1 CLI/voice-loop resilience tests.
- Mirror-C: P2 interop contract tests with LAM ecosystem.
