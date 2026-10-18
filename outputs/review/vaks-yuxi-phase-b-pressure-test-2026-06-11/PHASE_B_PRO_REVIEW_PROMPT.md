---
record_kind: sandbox_external_review_prompt
status: candidate
project_id: VAKS
created_at: 2026-06-11
truth_boundary: prompt_not_mainline_adoption
action_basis_allowed: false
---

# Phase B Pro Review Prompt

Copy this prompt to Pro or another review window.

## Prompt

你现在是 VAKS 架构复核员。请只做架构复核，不要替我合并，不要改文件，不要把 sandbox 结果当成主线结论。

我在 VAKS 的 Phase B 沙盒里测试了一个 Yuxi-like 检索适配层。我的目标不是把 Yuxi 整套搬进 VAKS，而是只借它的“解析、chunk、metadata、向量/图谱召回、click-back、retrieval receipt”这一层，让 VAKS 自己继续负责 authority bucket、review、truth、action gate。

请你复核这件事：

```text
Phase B 是否值得做一个最小 documentation-only 主线说明补丁？
如果值得，最小应该动哪些文件？
如果不值得，卡在哪里？
```

## Must-Preserve Boundary

请按这些硬边界评审：

```text
VAKS Markdown/YAML remains source of truth.
Yuxi-like runtime is read-only derived adapter only.
Retrieval score is not evidence support.
Vector similarity is not truth confidence.
Graph edge is not reviewed relation.
Chunk manifest is not reviewed knowledge.
Retrieval receipt is not action basis.
Context-pack candidate is not action approval.
Feedback/retrieval/eval can create activation or review pressure only.
No Skills.
No MCP writes.
No subagents as production evidence.
No formal writeback.
No production readiness claim.
```

## Evidence To Review

请重点看这些文件：

```text
outputs/review/vaks-yuxi-phase-b-pressure-test-2026-06-11/PHASE_B_MAINLINE_READINESS_PACKET.md
outputs/review/vaks-yuxi-phase-b-pressure-test-2026-06-11/PHASE_B_MAINLINE_READINESS_DECISION.md
outputs/review/vaks-yuxi-phase-b-pressure-test-2026-06-11/PHASE_B_MAINLINE_READINESS_CHECK.md
outputs/review/vaks-yuxi-phase-b-pressure-test-2026-06-11/PHASE_B_INTEGRATION_READINESS_PACKAGE.md
outputs/review/vaks-yuxi-phase-b-pressure-test-2026-06-11/PHASE_B_INTEGRATION_READINESS_CHECK.md
outputs/review/vaks-yuxi-phase-b-pressure-test-2026-06-11/PHASE_B_CONTRACT_TEST_DECISION.md
outputs/review/vaks-yuxi-phase-b-pressure-test-2026-06-11/results/phase_b_integration_readiness_check.json
outputs/review/vaks-yuxi-phase-b-pressure-test-2026-06-11/results/phase_b_adapter_contract_test.json
```

如果你需要理解主线文档位置，请只读这些主线文件：

```text
SOURCE_INTAKE.md
IMPLEMENTATION_BLUEPRINT.md
DEV_CONTEXT.md
MEMORY_TIER.md
SCHEMA.md
REVIEW_QUEUE.md
templates/architecture-review-window-prompt.md
```

## Current Quantitative Floor

当前 sandbox 证据如下：

```text
main primary:
  hit@5: 30/30
  hit@10: 30/30
  MRR: 1.0000
  leakage: 0.0000

main full:
  hit@5: 30/30
  hit@10: 30/30
  MRR: 1.0000
  leakage: 0.0000

holdout primary:
  hit@5: 12/15
  hit@10: 13/15
  MRR: 0.7811
  leakage: 0.0000

holdout full:
  hit@5: 13/15
  hit@10: 13/15
  MRR: 0.7591
  leakage: 0.0000

contract validator:
  pass / 0 errors

integration readiness validator:
  pass / 0 errors

mainline-readiness validator:
  pass / 0 errors

core docs:
  dirty lines: 0
```

## Candidate Minimal Touch Set

我目前建议如果要进主线说明，只做 documentation-only，优先考虑：

```text
SOURCE_INTAKE.md
IMPLEMENTATION_BLUEPRINT.md
DEV_CONTEXT.md
MEMORY_TIER.md
```

暂缓，除非你认为必须：

```text
SCHEMA.md
REVIEW_QUEUE.md
templates/architecture-review-window-prompt.md
```

## Candidate Mainline Language To Review

请评审这些候选片段是否足够、是否过度、是否放错位置。

### SOURCE_INTAKE.md

```markdown
#### Phase B Read-Only Retrieval Adapter

VAKS may use a derived retrieval adapter for parser/chunk/metadata/vector-like
or graph-neighborhood recall, but VAKS authority buckets must be applied before
ranking or RRF fusion.

The adapter may emit chunk manifests, retrieval receipts, click-back anchors,
source hashes, chunk hashes, warning codes, and retrieval reasons.

The adapter must not promote raw/candidate/diagnostic/feedback material into
reviewed support, reviewed relation, truth confidence, or action basis.
```

### IMPLEMENTATION_BLUEPRINT.md

```markdown
Phase B query-layer work starts as a read-only derived adapter:

1. build chunk manifest and retrieval receipt artifacts;
2. filter by VAKS authority bucket before ranking;
3. run bucket-local retrieval and rerank;
4. return context-pack candidates with click-back and warnings;
5. require pressure, contract, and readiness gates before any mainline adoption.

Do not attach Skills, MCP writes, subagents, or formal writeback in Phase B.
```

### DEV_CONTEXT.md

```markdown
Retrieval receipts may help assemble a context-pack candidate.

They are not action basis by themselves. A context pack that uses adapter output
must still expose source click-back, authority badge, usage badge, warning code,
and any stale or scope warning before it can be used for action-facing review.
```

### MEMORY_TIER.md

```markdown
Retrieval activation is not truth.

Vector similarity, graph-neighborhood hits, rerank score, repeated retrieval,
and evaluation score may improve activation or review pressure. They must not
increase truth confidence, create reviewed relations, or approve action basis.
```

## Questions To Answer

请按下面格式回答：

```text
1. Verdict:
   APPROVE_MINIMAL_DOC_PATCH / REVISE_BEFORE_PATCH / REJECT_FOR_NOW

2. Short reason:
   用大白话说明为什么。

3. Minimal touch set:
   列出应该改哪些文件，不要泛泛而谈。

4. Must-change wording:
   指出候选片段里必须改的句子。

5. Must-not-change boundary:
   列出不能碰的边界。

6. Open blockers:
   哪些问题必须在主线前解决，哪些可以先作为 sandbox 限制保留。

7. Hidden risk:
   有没有任何路径会让 adapter output 变成 truth / reviewed relation / action basis。

8. Final recommendation:
   下一步应该是：
   - 准备最小 documentation-only patch
   - 继续 sandbox 测试
   - 先跑原版 Yuxi full-stack
   - 或者完全搁置 Phase B
```

## Important Constraint

请不要因为指标好就建议进入主线。只有在边界清楚、插入点清楚、回滚清楚、且不会侵蚀 VAKS truth/review/action gate 的情况下，才可以建议 documentation-only patch。
