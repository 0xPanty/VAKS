# Verifier Portability Dependency Policy

Slice: `2026-06-15-p2-47-sandbox-verifier-portability-dependency-audit-sandbox`

This policy is a static sandbox audit. It does not execute old verifiers, install
dependencies, certify runtime behavior, promote artifacts, or approve action use.

## Blocking Signals

- Syntax error in a verifier script.
- External import outside Python standard library and same-slice modules.
- Network/API import such as `requests`, `httpx`, `socket`, or `urllib`.
- Dependency install, commit, push, network, or background-service token.

## Warning Signals

- `subprocess` import is a warning for human inspection of default path behavior.
- Boundary words such as formal-vault path text, Obsidian sync text, or MCP-write labels are warnings when they appear only as source text.
- Explicit `--rebuild` support is allowed but must be treated as Builder-only.
