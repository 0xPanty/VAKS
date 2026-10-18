---
slice_id: 2026-06-19-p2-74-original-20-operator-status-surface-sandbox
status: source_map_ready
---

# Source Map

## Input Sources

| Source | Used for | Limit |
|---|---|---|
| p2-71 audit JSON | Original 20 legacy evidence and old strict final-gate count | Audit evidence only |
| p2-72 decision packet JSON | Dry-run changes and user approval boundary | Decision packet only |
| p2-73 sidecar ledger JSON | Product-grade sidecar closeout status | Sidecar evidence only |
| p2-67 strict status package | Frontmatter status parsing for final gate | Parser only |

## Outputs

| Output | Purpose |
|---|---|
| `artifact/original_20_operator_status_surface_contract.json` | Contract and invariants |
| `artifact/build_original_20_operator_status_surface.py` | Rebuilds the status surface |
| `artifact/original_20_operator_status_surface.json` | Machine-readable status surface |
| `artifact/original_20_operator_status_surface.md` | Human-readable operator brief |
| `artifact/original_20_operator_status_surface.html` | Portable cockpit view |
| `artifact/verify_original_20_operator_status_surface.py` | Local verifier and final gate |

## Boundary

This status surface is a sandbox product artifact. It explains state; it does not approve, normalize, merge, promote, review, support evidence, or authorize action.
