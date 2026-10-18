---
case_id: block-zero-success-batch
expected: BLOCK
adapter:
  name: codex-session-directory
  source_type: session_batch
  input_identity: "local:sessions/"
  adapter_status: ok
batch_result:
  imported: 0
  skipped: 3
---

# BLOCK: Zero Success Batch

Batch ingest with zero successful imports must not report ok.
