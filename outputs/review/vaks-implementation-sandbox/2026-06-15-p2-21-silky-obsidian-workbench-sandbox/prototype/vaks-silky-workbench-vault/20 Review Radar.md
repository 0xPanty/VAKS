---
record_kind: "vaks_review_radar"
sandbox_only: true
---

# Review Radar

Review due means pressure, not truth mutation. The radar prioritizes:

- missing evidence;
- stale scope;
- negative feedback;
- dirty state;
- anchor mismatch;
- action boundary risk.

Next safe step: open the relevant card, then read its verification, reviewer
report, boundary audit, product acceptance, and next-step file.

- [[Cards/2026-06-15-p0-01-retrieval-receipt-template-sandbox|P0 2026-06-15-p0-01-retrieval-receipt-template-sandbox]] - retrieval has an explicit receipt before anyone treats it as useful context
- [[Cards/2026-06-15-p0-02-operation-receipt-template-sandbox|P0 2026-06-15-p0-02-operation-receipt-template-sandbox]] - operations show what ran, what changed, and what stayed blocked
- [[Cards/2026-06-15-p0-03-body-hash-validator-sandbox|P0 2026-06-15-p0-03-body-hash-validator-sandbox]] - body drift is caught before downstream use
- [[Cards/2026-06-15-p0-04-support-boundary-validator-sandbox|P0 2026-06-15-p0-04-support-boundary-validator-sandbox]] - support claims are separated from provenance and background
- [[Cards/2026-06-15-p0-05-action-readiness-validator-sandbox|P0 2026-06-15-p0-05-action-readiness-validator-sandbox]] - action basis is blocked until readiness checks pass
- [[Cards/2026-06-15-p0-06-feedback-validator-sandbox|P0 2026-06-15-p0-06-feedback-validator-sandbox]] - feedback creates review pressure without mutating truth
- [[Cards/2026-06-15-p0-07-action-boundary-failure-matrix-sandbox|P0 2026-06-15-p0-07-action-boundary-failure-matrix-sandbox]] - known action-boundary failures become visible test cases
- [[Cards/2026-06-15-p1-08-retrieval-operation-receipt-validator-pilot-sandbox|P1 2026-06-15-p1-08-retrieval-operation-receipt-validator-pilot-sandbox]] - retrieval and operation receipts can be validated together
- [[Cards/2026-06-15-p1-09-read-only-query-loop-pilot-sandbox|P1 2026-06-15-p1-09-read-only-query-loop-pilot-sandbox]] - query loops stay read-only and explain their limits
- [[Cards/2026-06-15-p1-10-runtime-artifact-exclusion-test-sandbox|P1 2026-06-15-p1-10-runtime-artifact-exclusion-test-sandbox]] - runtime artifacts are excluded from knowledge surfaces
- [[Cards/2026-06-15-p1-11-semantic-anchor-support-check-sandbox|P1 2026-06-15-p1-11-semantic-anchor-support-check-sandbox]] - semantic anchors are checked before support is claimed
- [[Cards/2026-06-15-p1-5-12-robust-rag-retrieval-sandbox|P1.5 2026-06-15-p1-5-12-robust-rag-retrieval-sandbox]] - robust retrieval ranks context without becoming trust
- [[Cards/2026-06-15-p1-5-13-local-obsidian-graph-retrieval-readonly-mcp-sandbox|P1.5 2026-06-15-p1-5-13-local-obsidian-graph-retrieval-readonly-mcp-sandbox]] - local graph retrieval stays read-only and non-authoritative
- [[Cards/2026-06-15-p1-5-14-raw-intake-parser-router-sandbox|P1.5 2026-06-15-p1-5-14-raw-intake-parser-router-sandbox]] - raw intake routes material without premature interpretation
- [[Cards/2026-06-15-p1-5-15-markdown-validation-search-sidecar-sandbox|P1.5 2026-06-15-p1-5-15-markdown-validation-search-sidecar-sandbox]] - markdown validation and search become a sidecar, not a truth layer
- [[Cards/2026-06-15-p1-5-16-misa-runtime-memory-vaks-bridge-sandbox|P1.5 2026-06-15-p1-5-16-misa-runtime-memory-vaks-bridge-sandbox]] - MISA memory bridge is quarantined from VAKS truth
- [[Cards/2026-06-15-p2-17-use-surface-optimization-pass|P2 2026-06-15-p2-17-use-surface-optimization-pass]] - use surfaces are prioritized around entry, status, and receipts
- [[Cards/2026-06-15-p2-18-bases-cockpit-prototype|P2 2026-06-15-p2-18-bases-cockpit-prototype]] - cockpit prototype gives operator status without authority
- [[Cards/2026-06-15-p2-19-product-experience-screening-sandbox|P2 2026-06-15-p2-19-product-experience-screening-sandbox]] - product candidates are screened before workflow build
- [[Cards/2026-06-15-p2-20-product-workflow-prototype|P2 2026-06-15-p2-20-product-workflow-prototype]] - product workflow shows where to go and where to stop
