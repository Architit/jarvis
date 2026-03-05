# GATEWAY ACCESS CONTRACT

## Purpose
Define deterministic access rules for gateway operations in `J.A.R.V.I.S`.

## Rules
1. Gateway actions MUST use explicit target resolution (`system_id` or `subtree_prefix`).
2. Unresolved targets MUST fail fast with `unresolved_target`.
3. Commands that imply global recursive writes across `LRPT/` are blocked by default.
4. Such commands are allowed only with explicit approval context.

## Verification
- `scripts/test_entrypoint.sh --all`
- `tests/test_governance_artifacts.py`
