---
record_kind: failure_case_oracle
slice_id: 2026-06-15-p2-19-product-experience-screening-sandbox
status: drafted
truth_boundary: sandbox_failure_oracle_only
---

# Failure Case Oracle

The executable oracle is `artifact/failure-case-oracle.json`.

Failure case files do not contain expected validity or expected issue codes.
They only describe mutations against `fixtures/valid-product-experience-screening.json`.
`artifact/verify_product_experience_screening.py` applies the mutation and then
compares validator output against the independent oracle.

Covered failure classes:

- missing or unknown P2-PX candidates;
- duplicate ranks and invalid decisions;
- missing screening fields: validators, source inspiration, boundary warning,
  minimal wireflow, P2-20 handoff role, P2-20 handoff;
- incomplete P2-20 handoff lists that do not exactly match keep / park / reject
  decisions;
- placeholder or unknown required validator names;
- product scope escapes: real UI, real Bases, sync, runtime, dependencies, MCP
  write tools, commit, push, outside writes, protected paths;
- authority confusion: missing authority flag, non-boolean authority flag,
  total-switch-only authority flags, reviewed truth writes, review approval,
  action readiness, activity as confidence, hash as support, badge as promotion,
  navigation as authority, mobile full review;
- forbidden imports: admin dashboard before validators, AI summary as evidence
  support, SQLite as reviewed truth source, consumer onboarding that hides
  boundaries;
- missing non-claims.

Passing this oracle is not Product Acceptance. It only proves the sandbox
validator catches the intended bad paths.
