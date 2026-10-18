---
fixture_id: ci06-block-suggested-action-auto-exec
expected_result: BLOCK_EXPECTED
context_pack:
  version: 1
  prompt: Suggested action should run.
  suggested_actions:
    - command: llmwiki compile
      reason: Refresh context.
  auto_execute_suggested_actions: true
expected_violation: suggested_actions are suggestions, not automatic actions
---

# BLOCK: Suggested Action Auto-Exec

Suggested actions are prompts for a human or agent controller, not execution.

