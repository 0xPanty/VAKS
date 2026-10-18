---
slice_id: 2026-06-20-p2-110-gptpro-vaks-guard-context-package-sandbox
status: failure_cases_complete
---

# Context Confusion Cases To Block

These are the failures this Pro context package must prevent.

| Case | Bad Interpretation | Correct Interpretation |
| --- | --- | --- |
| FC-01 | p2-109 passed, so the guards are already mainline. | p2-109 passed sandbox-only Product Acceptance. |
| FC-02 | Tool checks can approve reviewed knowledge. | Tool checks can block or warn; they do not approve truth. |
| FC-03 | Retrieval receipt proves support. | Retrieval receipt proves retrieval process, not evidence support. |
| FC-04 | Feedback validator means feedback can update truth if valid. | Feedback never mutates truth directly. |
| FC-05 | Runtime artifact exclusion means deleting user files. | It only classifies/excludes runtime artifacts from knowledge/context selection unless separately approved. |
| FC-06 | VAKS Guard is a new architecture truth layer. | VAKS Guard is a lightweight tool layer under existing architecture boundaries. |
| FC-07 | The Pro review can authorize mainline merge by itself. | Pro can advise; user approval and later mainline-specific review are still required. |

