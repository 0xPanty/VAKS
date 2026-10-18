---
record_kind: project_overlay
status: candidate
knowledge_status: candidate
processing_tier: medium
overlay_state: confirmed
overlay_scope: project_sidecar_only
overlay_storage: confirmed_persistent_project_bucket
retrieval_scope: active_project_only
default_retrieval: false
retrieval_policy:
  policy_kind: project_context_only
  default_scope: project_only
  pack_allowed: activation_only
  action_basis_allowed: false
  warning_code: overlay_not_authority
promotion_gate: v0_2_13_required
action_basis_allowed: false
truth_mutation_allowed: false
project_id: verified-action-knowledge-system
target_ref:
  - raw/videos/2026-06-07-bilibili-self-learning-library-source.md
  - raw/repos/2026-06-07-llk-ll-self-learning-library-source.md
target_selector: "video:BV1cM7C6BEsM + checked_commit:046daf301b361b6cd8de43114b2fdd780adadc0f"
target_hint: "Use as a VAKS local harness / self-growing knowledge-base / selective retrieval reference, not as reviewed knowledge or action basis."
tagging_decision: tagged
tag_level: strong-borrow
tag_level_reason: "High fit with VAKS memory activation, feedback/no-regression, review routing, and candidate/truth boundaries; kept candidate-only because repo is a fresh prototype, paper-specific, and unexecuted locally."
project_borrow_scope:
  - project-local harness entrypoint visible at root
  - correction memory to no-regression guard
  - selective RAG before task/context pack
  - evidence/reasoning/output split
  - conflict/limited/final rule routing
  - workflow governance separated from content rules
  - evidence expansion as lazy gate
project_non_borrow_scope:
  - direct import of paper-writing vault content
  - exact numbered folder names as VAKS mainline schema
  - graph/retrieval/token score as truth confidence
  - generated reports as reviewed evidence
  - automatic truth mutation from feedback or correction
  - global workflow defaults outside the current project
project_reopen_trigger:
  - "VAKS designs or revises project-local AGENTS.md / harness behavior."
  - "VAKS builds Activation Tier -> Context Pack selection."
  - "VAKS turns user corrections into no-regression guards."
  - "VAKS implements conflict / limited / generalized candidate routing."
  - "A future tool output risks being treated as reviewed knowledge or action basis."
confirmation_basis:
  - user explicitly requested video distillation first and repo supplement as one knowledge point
  - Bilibili metadata and local ASR artifacts captured with public/no-cookies path
  - GitHub repository snapshot created at checked commit 046daf301b361b6cd8de43114b2fdd780adadc0f
  - source/docs/scripts read only
  - no runtime execution; no promotion to reviewed knowledge
last_checked_at: 2026-06-07
expires_at: 2026-07-07
borrow_value: strong
borrow_order:
  - "P1: local harness as AI memory and task constraint surface"
  - "P1: correction -> memory -> rule -> no-regression guard"
  - "P1: selective retrieval and lazy evidence expansion"
  - "P1: evidence/reasoning/output layer split"
  - "P1: conflict / limited / final rule routing"
  - "P2: lexical/graph retrieval and token accounting diagnostics"
  - "P3: paper-writing vault demo content"
avoid:
  - "Do not promote this overlay into reviewed knowledge."
  - "Do not split the paired video and repo into two separate VAKS knowledge points."
  - "Do not import the paper-writing vault or generated rules into VAKS."
  - "Do not treat retrieval score, graph score, token-saving output, or generated iteration report as truth support."
tags:
  - VAKS
  - project-overlay
  - self-learning-library
  - strong-borrow
  - P1
  - local-harness
  - self-growing-knowledge-base
  - selective-rag
  - memory-correction-loop
  - no-regression-guard
  - workflow-governance
  - layered-vault
  - evidence-boundary
  - candidate-only
---

# VAKS Project Overlay: Self-Learning Library

## Boundary

This is a project-scoped sidecar.

It does not rewrite the source card, candidate distillation, reviewed note, decision, or pattern.

It can guide the active project, but it cannot act as reviewed knowledge or action basis.

## Target

```yaml
target_ref:
  - raw/videos/2026-06-07-bilibili-self-learning-library-source.md
  - raw/repos/2026-06-07-llk-ll-self-learning-library-source.md
target_selector: video:BV1cM7C6BEsM + checked_commit:046daf301b361b6cd8de43114b2fdd780adadc0f
target_hint: local-harness / self-growing-knowledge-base / selective-rag / no-regression-guard
```

## 标签等级

```yaml
tagging_decision: tagged
tag_level: strong-borrow
borrow_value: strong
borrow_order_primary: P1
```

人话：

```text
有标签。
算 P1。
是 strong-borrow，但不是直接采纳。
```

强的原因：

```text
它正好打中 VAKS 的几个核心问题：
本地记忆怎么激活？
纠错怎么变成下一次检查？
冲突和局部规则怎么不误升？
检索和输出怎么不冒充真理？
```

## Project Borrow Scope

VAKS 当前可以借：

1. **项目本地 harness 入口**：让项目根目录暴露工作规则和执行顺序。
2. **纠错到 no-regression guard**：用户明确纠错后，未来任务结束前要检查是否复发。
3. **选择性检索**：普通任务只激活相关规则；证据扩展走 lazy gate。
4. **证据/推理/输出分层**：输出报告和规则不是证据本身。
5. **冲突/受限/泛化分流**：不要把局部经验直接升成通用规则。
6. **workflow governance 分离**：流程规则控制执行，不污染内容和 reviewed knowledge。

## Project Non-Borrow Scope

VAKS 当前不要借：

- 不要把论文写作 vault 内容导入主库。
- 不要照搬 `10/20/30/40/45/50/60/70` 为 VAKS 主线 schema。
- 不要把 `kb_rag.py` score、graph relation score、token savings 当 truth confidence。
- 不要把 iteration report 当 reviewed evidence。
- 不要让用户纠错直接修改 truth。
- 不要把这个项目的 `AGENTS.md` 规则变成所有项目的全局默认。

## Reopen Trigger

重新打开这条 overlay 的条件：

- VAKS 要设计本地项目 harness。
- VAKS 要设计 Activation Tier 到 Context Pack。
- VAKS 要把显式用户纠错变成 no-regression guard。
- VAKS 要实现 conflict / limited / generalized candidate routing。
- VAKS 要审查“检索结果/报告/评分是否越权成 truth”。

## Confirmation

```yaml
confirmation_basis:
  - user_requested: video first, repo as supplement, one knowledge point
  - video_public_metadata: captured
  - video_transcript_method: local_asr
  - media_retention: deleted
  - checked_commit: 046daf301b361b6cd8de43114b2fdd780adadc0f
  - snapshot_hash_verified: true
  - artifact_paths:
      - raw/videos/2026-06-07-bilibili-self-learning-library-source.md
      - raw/videos/2026-06-07-bilibili-self-learning-library-source/transcript.txt
      - raw/repos/2026-06-07-llk-ll-self-learning-library-source.md
      - outputs/review/2026-06-07-self-learning-library-unified-candidate-distillation.md
      - wiki/summaries/2026-06-07-self-learning-library-architecture-review.md
      - outputs/review/project_overlays/VAKS-self-learning-library-2026-06-07.md
      - raw/repos/_snapshots/LLK-LL-Self-Learning-Library-046daf301b361b6cd8de43114b2fdd780adadc0f.zip
  - runtime_executed: false
last_checked_at: 2026-06-07
expires_at: 2026-07-07
```

## 人话结论

这条对 VAKS 很有帮助。

最应该记住的是：

```text
VAKS 不是把资料越堆越多。
VAKS 要让过去的纠错、证据和边界，在下一次任务开始前被正确激活。
激活不是相信，检索不是证明，输出不是真理。
```

## Forbidden

```text
decision outcome
review verdict
truth confidence
action basis
automatic promotion
global workflow default
```
