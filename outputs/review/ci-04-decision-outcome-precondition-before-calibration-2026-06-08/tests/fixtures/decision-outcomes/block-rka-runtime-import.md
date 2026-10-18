---
fixture_id: ci04-block-rka-runtime-import
expected_result: BLOCK_EXPECTED
proposed_import:
  - RKA runtime
  - RKA MCP
  - RKA API server
  - RKA dashboard
  - RKA SQLite database
expected_violation: CI-04 borrows only the decision outcome precondition, not the runtime
---

# BLOCK: RKA Runtime Import

CI-04 is a small Use Ledger hardening rule, not a runtime adoption.

