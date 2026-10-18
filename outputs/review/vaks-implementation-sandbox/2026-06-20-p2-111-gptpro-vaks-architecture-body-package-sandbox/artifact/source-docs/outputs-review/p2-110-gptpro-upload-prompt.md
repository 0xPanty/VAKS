---
slice_id: 2026-06-20-p2-110-gptpro-vaks-guard-context-package-sandbox
status: ready_for_copy_paste
artifact_kind: gptpro_upload_prompt
---

# Copy-Paste Prompt For GPT Pro

You are reviewing the VAKS architecture and the proposed VAKS Guard tool-layer absorption.

Read the attached context brief first:

```text
artifact/gptpro-vaks-guard-context-brief.md
```

Your job is not to approve a merge. Your job is to judge whether the seven guard candidates should be positioned as a lightweight tool layer under the existing architecture.

Hard boundaries:

- Do not treat sandbox success as mainline absorption.
- Do not treat validator pass as reviewer approval.
- Do not treat retrieval as evidence support.
- Do not treat feedback as truth update.
- Do not treat tool checks as truth authority.
- Do not recommend Obsidian vault writes, commit, push, sync, background services, or dependency installation.

Main question:

```text
Are the seven guard candidates best understood as a lightweight read-only VAKS Guard tool layer that executes existing architecture boundaries, rather than a new architecture layer?
```

Please answer in this format:

```text
Verdict:
PASS_TOOL_LAYER_DIRECTION / REVISE_BEFORE_MAINLINE / BLOCK_MAINLINE_ABSORPTION

Main reasoning:

Per-candidate review:
- P0-03 body hash validator:
- P0-04 support boundary validator:
- P0-05 action readiness validator:
- P0-06 feedback validator:
- P0-07 action-boundary failure matrix:
- P1-08 retrieval/operation receipt validator:
- P1-10 runtime artifact exclusion:

Overbuild risks:

Missing guardrails:

Recommended minimal landing shape:

What must not be merged:

Questions for user/Codex:
```

