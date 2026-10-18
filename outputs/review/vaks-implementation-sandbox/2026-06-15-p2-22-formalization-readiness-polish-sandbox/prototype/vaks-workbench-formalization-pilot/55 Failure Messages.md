---
record_kind: sandbox_failure_messages
status: sandbox_pilot
truth_boundary: sandbox_only
---

# Failure Messages

## Human-Readable Blocks

| Machine Code Family | Plain Reason | Safe Alternative |
| --- | --- | --- |
| forbidden_operation | The proposed config tries to do something outside this sandbox. | Remove the operation or request separate user approval. |
| missing_boundary_phrase | The pack no longer says what it is not allowed to mean. | Restore the Boundary Rail and rerun validation. |
| authority_confusing_label | The wording sounds like approval, truth, support, or action readiness. | Rename the surface as navigation, triage, receipt, or review input. |
| journey_too_deep | The flow is no longer a usable product path. | Shorten to the smallest safe route and keep a stop condition. |
| missing_surface | A product-critical surface is absent. | Add the missing page and connect it from Pilot Home. |
| invalid_write_scope | The config points outside the approved sandbox path. | Scope writes back to this slice only. |
| wrong_source_slice | The pack is no longer based on the accepted source slice. | Point back to P2-21 or create a new approved source-map. |

## Boundary

A block reason is diagnostic. It is not a truth judgment, evidence support,
reviewer approval, Product Acceptance, mainline readiness, or permission to act.
