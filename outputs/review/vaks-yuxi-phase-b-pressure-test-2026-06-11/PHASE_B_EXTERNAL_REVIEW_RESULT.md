---
record_kind: sandbox_external_review_result
status: candidate
project_id: VAKS
created_at: 2026-06-11
truth_boundary: external_review_result_not_mainline_adoption
action_basis_allowed: false
reviewer: subagent_james
---

# Phase B External Review Result

## Reviewer Output

1. Verdict:
   APPROVE_MINIMAL_DOC_PATCH

2. Short reason:
   大白话：值得写一小段主线说明，但只能说明“Phase B 可以作为只读派生检索 adapter 的方向被记录下来”。证据已经有 contract/readiness/mainline-readiness `pass / 0 errors`，core docs 也干净；但这不是生产可用、不是 truth 采纳、不是 runtime 默认开启。证据路径见 `PHASE_B_MAINLINE_READINESS_CHECK.md` 和 `PHASE_B_CONTRACT_TEST_DECISION.md`。

3. Minimal touch set:
   只动这四个：
   - `SOURCE_INTAKE.md`
   - `IMPLEMENTATION_BLUEPRINT.md`
   - `DEV_CONTEXT.md`
   - `MEMORY_TIER.md`

   先不动 `SCHEMA.md`、`REVIEW_QUEUE.md`、`templates/architecture-review-window-prompt.md`。证据包自己也把它们列为 deferred。

4. Must-change wording:
   - `IMPLEMENTATION_BLUEPRINT.md`: “before any mainline adoption”要改成“before any runtime/default/production adoption beyond this documentation note”，否则文档补丁本身会和“mainline adoption”混淆。
   - `DEV_CONTEXT.md`: “before it can be used for action-facing review”要改成“before it can be reviewed for action-facing use”，并补一句：这些 badge/warning 只是前置条件，不足以形成 action basis。
   - `SOURCE_INTAKE.md`: 加明示：`graph_path` / retrieval reason / graph edge 是 recall metadata，不是 reviewed relation，也不是 support。
   - `MEMORY_TIER.md`: “may improve activation or review pressure”要限定为 routing/review_due pressure only；evaluation score、重复召回、similarity 不能自动生成 queue item、confidence、support 或 action readiness。

5. Must-not-change boundary:
   VAKS Markdown/YAML 仍是 source of truth；adapter 只读、派生、可丢弃。Retrieval score 不是 evidence support，vector similarity 不是 truth confidence，graph edge 不是 reviewed relation，chunk manifest 不是 reviewed knowledge，retrieval receipt/context-pack candidate 不是 action basis。仍然禁止 Skills、MCP writes、subagents、formal writeback、production readiness claim。bucket-first 和 no cross-bucket RRF 必须保留。

6. Open blockers:
   主线文档补丁前必须解决：上面几处 wording；补丁保持 documentation-only；明确“不是 runtime/default/prod adoption”；人工接受四文件 touch set。

   可作为 sandbox 限制保留：原版 Yuxi full-stack 未跑、本地 Docker 不可用、holdout 不完美、生产向量库/并发/多用户权限/真实 Obsidian click-through/C-lite 都未验证。这些阻止 runtime 或生产采纳，不阻止最小文档说明。

7. Hidden risk:
   有，但可控。最大风险路径是：adapter receipt 被 DEV_CONTEXT 误读成 action basis；graph_path 被误读成 reviewed relation；evaluation/repeated retrieval 被误读成 confidence；mixed RRF 让 candidate/raw 看起来和 reviewed 同权；Yuxi runtime DB 变成隐藏真值源。现有 integration package 已把错误拓扑列清楚。

8. Final recommendation:
   下一步应该是：准备最小 documentation-only patch，但不要照抄候选片段；先按第 4 点收紧 wording。不要先跑原版 Yuxi full-stack 作为文档补丁前置条件；它应作为后续 runtime/full-stack/production claim 的 blocker。

Reviewer note:

```text
I reviewed read-only, did not edit files, and did not commit.
```
