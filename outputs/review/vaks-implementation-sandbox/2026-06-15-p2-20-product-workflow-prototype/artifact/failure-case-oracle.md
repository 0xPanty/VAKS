---
record_kind: failure_case_oracle
slice_id: 2026-06-15-p2-20-product-workflow-prototype
status: drafted
truth_boundary: sandbox_failure_oracle_only
---

# Failure Case Oracle

Executable expectations live in `artifact/failure-case-oracle.json`.

Failure case files do not contain expected validity or expected issue codes.
They only describe mutations against `fixtures/valid-product-workflow.json`.

Covered failure classes:

- missing or reordered workflow steps;
- missing workflow questions and non-claims;
- missing required validators;
- wrong P2-19 source screening reference;
- wrong step workflow key or P2-PX mapping;
- production UI, real Bases, sync, runtime, dependency install, MCP write,
  commit, push, outside write, and protected path attempts;
- path traversal and absolute outside path attempts while allowing valid
  absolute paths inside the sandbox;
- authority confusion: reviewed truth write, status as authority, badge as
  promotion, hash as support, export as action basis, navigation as authority,
  dirty state replacing validators;
- copy-level authority claims with authority flags still false;
- same-field negated boundary phrases followed by authority claims;
- malformed scope, truthy malformed scope, and non-object step inputs;
- missing hash and action boundary copy.

Passing this oracle is not Product Acceptance. It only proves the workflow
validator catches the intended bad paths.
