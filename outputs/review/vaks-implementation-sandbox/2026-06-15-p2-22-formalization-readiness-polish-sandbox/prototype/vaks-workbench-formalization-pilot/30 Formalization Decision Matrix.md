---
record_kind: sandbox_formalization_decision_matrix
status: sandbox_pilot
truth_boundary: sandbox_only
---

# Formalization Decision Matrix

| Route | Fit | Risk | Boundary | User Approval Required |
| --- | --- | --- | --- | --- |
| `static_html_cockpit` | Best for fast review and browser smoke tests. | Can feel outside native Obsidian if used alone. | inspection surface only | `True` |
| `obsidian_native_markdown_bases` | Best native operator experience after explicit formal-vault approval. | Would write formal vault and possibly .base files, so it is not allowed in this slice. | not executed here | `True` |
| `local_read_only_sidecar` | Best for search, validation, and cockpit refresh without mutating the vault. | Could drift into a runtime service if not tightly scoped. | read-only only | `True` |
| `hybrid_pilot_path` | Best next product route because it keeps Obsidian feel and auditability separate. | Needs a later approved slice to touch the formal vault. | recommended candidate, not approval | `True` |

## Recommendation

Choose `hybrid_pilot_path` for the next approved sandbox, if the user wants to
move closer to a real Obsidian experience:

- native Markdown entry keeps the vault feel;
- static inspector preserves review visibility;
- read-only validator keeps process checks separate from authority;
- no route executes until separately approved.

## Non-Approval

This matrix is not a merge approval, not formal-vault approval, not sync
approval, not commit approval, not push approval, and not promotion approval.
