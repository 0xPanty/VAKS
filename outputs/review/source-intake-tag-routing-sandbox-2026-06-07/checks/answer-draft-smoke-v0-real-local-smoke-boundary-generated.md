---
record_kind: answer_draft_smoke_candidate
status: candidate
created_at: 2026-06-07T19:30:00+08:00
topic_id: source-intake-routing
truth_boundary: answer_draft_smoke_not_truth
action_basis_allowed: false
truth_mutation_allowed: false
source_skeleton_ref: outputs/review/source-intake-tag-routing-sandbox-2026-06-07/checks/answer-draft-skeleton-v0-real-local-smoke-boundary-generated.md
---

# Answer Draft Smoke v0: real local smoke boundary

## Gate

```yaml
draft_smoke_state: pass_ready_human_readable_real_local
draft_answer_emitted: true
source_refs_policy: claim_evidence_map_only
claims_used: ["rl1", "rl2", "rl3", "rl4", "rl5"]
action_basis_allowed: false
truth_mutation_allowed: false
forbidden_use: ["truth", "reviewed_relation", "action_basis", "agent_action"]
```

## Draft Answer

- [claim_refs: rl1] 这条 smoke lint 的 ready 判断不是自己重新验真，而是假定 skeleton 的 readiness 标签由上游 evidence support check 负责。
- [claim_refs: rl2] 它真正检查的是草稿形状和引用句柄存在：每条答案线要能绑到 skeleton 里已有的 claim_id。
- [claim_refs: rl3] 语义支撑、citation faithfulness、coverage 和 omission 都不在 smoke lint 这一层里解决。
- [claim_refs: rl4] 所以错配 ref 和漏掉某些 claim 的用例是 expected-pass known limitation，而不是这层要硬抓的错误。
- [claim_refs: rl5] 但空 claim_refs、blocked 段落式答案、围栏标题后藏答案这些 shape 问题，应该被 smoke lint 抓住。

## Boundary Banner

```text
This is a real-local answer-draft smoke output only.
It is not action basis, not reviewed knowledge, and not citation-faithfulness checked.
Claim refs are trace handles, not proof of semantic support.
```
