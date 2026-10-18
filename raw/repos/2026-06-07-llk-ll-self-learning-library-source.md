---
type: source
status: source-captured
title: "Self-Learning Library"
source_id: 2026-06-07-llk-ll-self-learning-library-source
source_uri: https://github.com/LLK-LL/Self-Learning-Library
source_url: https://github.com/LLK-LL/Self-Learning-Library
source_type: repository
author: LLK-LL
publisher: GitHub
published_at: 2026-06-05T02:39:56Z
updated_at: 2026-06-06T13:52:42Z
captured_at: 2026-06-07
captured_by: Codex
version_or_commit: 046daf301b361b6cd8de43114b2fdd780adadc0f
commit_time: "2026-06-05T11:24:44+08:00"
commit_subject: "Document token-saving RAG defaults"
default_branch: main
source_status: active
license:
dynamic_metadata_checked_at: 2026-06-07T03:40:21+08:00
dynamic_metadata:
  stars: 3
  forks: 0
  open_issues: 0
  language: Python
raw_location: raw/repos/2026-06-07-llk-ll-self-learning-library-source.md
snapshot_location: raw/repos/_snapshots/LLK-LL-Self-Learning-Library-046daf301b361b6cd8de43114b2fdd780adadc0f.zip
snapshot_sha256: 05747D966B74207977D4A36AF24B19C28DCFDEABAE725AC91689DA5287FEDC1D
processing_mode: immediate
processing_level: medium
processing_tier: medium
knowledge_status: raw
overlay_state: none
review_pressure: none
retrieval_policy:
  policy_kind: source_identity_only
  pack_allowed: drilldown_required
  action_basis_allowed: false
  warning_code: raw_is_provenance_only
promotion_gate: none
action_basis_allowed: false
truth_mutation_allowed: false
review_priority: high
review_owner: Codex
formalization_status: candidate-generated
topics:
  - local-harness
  - self-growing-knowledge-base
  - selective-rag
  - no-regression-guard
  - layered-vault
  - ai-memory
  - workflow-governance
projects:
  - verified-action-knowledge-system
source_family:
  - self-learning-library
  - local-agent-memory
  - harness-workflow
  - candidate-only
upstream_sources:
  - bilibili:BV1cM7C6BEsM
verification_status: primary-source-captured
candidate_relation_suggestions:
  - target: "[[Activation Tier]]"
    relation_type: refines
    relation_state: candidate
    why_suggested: "The repo retrieves only relevant rules before a task instead of loading the whole vault."
  - target: "[[Feedback Ledger]]"
    relation_type: refines
    relation_state: candidate
    why_suggested: "The repo records corrections and process lessons into a local memory loop."
  - target: "[[Evidence-Aware Review]]"
    relation_type: refines
    relation_state: candidate
    why_suggested: "The iteration script separates evidence, reasoning, and output layers and only lets evidence-layer notes contribute support."
  - target: "[[derived-relatedness-as-truth-signal]]"
    relation_type: risk_of
    relation_state: candidate
    why_suggested: "Its lexical/graph retrieval and generated rule reports could be mistaken for truth if imported without VAKS boundaries."
tags:
  - repo-source
  - self-learning-library
  - local-harness
  - self-growing-knowledge-base
  - selective-rag
  - no-regression-guard
  - layered-vault
  - workflow-governance
  - candidate-only
---

# Self-Learning Library Source Record

## 为什么收录

`LLK-LL/Self-Learning-Library` 是视频 `BV1cM7C6BEsM` 对应的开源仓库。用户明确要求视频逻辑和仓库实现作为同一个知识点处理，所以本卡只负责 repository provenance、snapshot 和代码锚点；统一蒸馏见：

```text
outputs/review/2026-06-07-self-learning-library-unified-candidate-distillation.md
```

人话判断：

```text
这不是普通 Obsidian 模板。
它是一个本地 AI harness 原型：先检索相关规则，再执行任务，再用纠错/证据/冲突/泛化层迭代。
```

## 来源信息

- Repository: `LLK-LL/Self-Learning-Library`
- URL: https://github.com/LLK-LL/Self-Learning-Library
- Checked branch: `main`
- Checked commit: `046daf301b361b6cd8de43114b2fdd780adadc0f`
- Commit time: `2026-06-05T11:24:44+08:00`
- Commit subject: `Document token-saving RAG defaults`
- Observed metadata during intake: stars `3`, forks `0`, open issues `0`, language `Python`, license `null`
- Snapshot: `raw/repos/_snapshots/LLK-LL-Self-Learning-Library-046daf301b361b6cd8de43114b2fdd780adadc0f.zip`
- Snapshot SHA256: `05747D966B74207977D4A36AF24B19C28DCFDEABAE725AC91689DA5287FEDC1D`
- Inspected mode: source/docs/scripts read; no package install; no harness execution.

## Intake Boundary

```yaml
processing_tier: medium
knowledge_status: raw
overlay_state: none
review_pressure: none
retrieval_policy:
  policy_kind: source_identity_only
  pack_allowed: drilldown_required
  action_basis_allowed: false
  warning_code: raw_is_provenance_only
promotion_gate: none
action_basis_allowed: false
truth_mutation_allowed: false
```

This source record is provenance and findability only. It does not create reviewed patterns, truth confidence, relation strength, or action basis.

## 文件 / 代码锚点

| Anchor | What exists | 初步看点 | Boundary |
|---|---|---|---|
| `README.md:1-22` | Defines the project as a local self-learning knowledge-base harness for Codex-style AI work. | Good framing: not a normal note folder, but an operating workflow around reusable knowledge. | README framing is project claim, not independent validation. |
| `README.md:24-31` | Separates evidence layer, reasoning layer, and output layer. | Matches VAKS boundary thinking. | Layer names are not VAKS truth schema. |
| `README.md:36-60` | Workflow diagram from user task to local RAG, checklist, no-regression guard, collection, iteration. | Strong candidate for local harness workflow. | Needs adaptation; do not import as global default. |
| `README.md:127-133` | Default lightweight RAG call and workflow-only retrieval path. | Useful selective retrieval reference. | Token-saving report itself showed no saving in one sample; mechanism, not metric, is valuable. |
| `PROJECT_HARNESS_WORKFLOW.md:1-26` | Project-local mandatory workflow and triggered functions. | Harness visibility at project root is a strong operational pattern. | Must remain project-local, not global. |
| `PROJECT_HARNESS_WORKFLOW.md:55-64` | Retrieves `45`, `40`, `50`, `60`, `30`; expands evidence only when needed; excludes `70` from normal task context. | Very relevant to VAKS Activation Tier and context-pack discipline. | Folder order is source-specific. |
| `PROJECT_HARNESS_WORKFLOW.md:71-84` | Source priority and scope for conflicting rules. | Good conflict/scope handling model. | Source priority values are paper-writing-specific. |
| `PROJECT_HARNESS_WORKFLOW.md:86-107` | No-regression guard and manuscript-body purity guard. | Shows correction memory becoming execution guardrails. | Manuscript rules are not reusable VAKS content. |
| `PROJECT_HARNESS_WORKFLOW.md:123-136` | Script reuse guard before creating helpers. | Useful process governance pattern. | Specific commands belong to that project. |
| `PROJECT_HARNESS_WORKFLOW.md:138-153` | Collection routes concrete changes to `10`, reusable memories to `20`, stable rules to `30`, then iteration. | Strong correction-to-rule loop reference. | Direct folder names should not be copied unchanged. |
| `tools/kb_rag.py:268-296` | Lexical score plus layer boosts for supervision, final rules, conflicts, limited rules, writing rules. | Simple local retrieval with priority shaping. | Score is routing only, not truth. |
| `tools/kb_rag.py:333-378` | Lexical or graph-expanded search result with outgoing/incoming links. | Candidate context expansion sample. | Graph expansion does not create reviewed relation. |
| `tools/kb_rag.py:482-525` | Baseline vs selected retrieval token accounting. | Useful instrumentation idea. | Token estimate is rough diagnostic only. |
| `tools/kb_rag.py:533-605` | Evidence expansion gate, workflow route, selected notes. | Good lazy evidence expansion pattern. | Evidence expansion still returns context, not support. |
| `tools/paper_iteration.py:389-408` | Attaches graph support from evidence-layer memory nodes. | Strong boundary: support comes from evidence notes. | It is source-local implementation, not VAKS review authority. |
| `tools/paper_iteration.py:1425-1444` | Final vs limited rule promotion based on evidence support and conflicts. | Useful candidate for VAKS promotion gating intuition. | Thresholds are local/prototype. |
| `tools/paper_iteration.py:1873-1878` | Writes iteration reports and states evidence rule. | Aligns with output layer as audit/report, not truth. | Generated reports remain output layer. |
| `paper_writing_obsidian_vault/70_Iterative_Thinking/layered_graph_overview.md` | Layer flow and counts; only Evidence Graph contributes to support scores. | Good visual check for layer boundaries. | Example vault content is paper-specific. |

## 仓库边界

可借的是 harness 机制，不是仓库内容：

```text
borrow:
  - local harness at project root
  - selective retrieval before work
  - correction -> memory -> rule -> conflict/limited/final routing
  - no-regression guard
  - evidence/reasoning/output layer split

do_not_borrow_directly:
  - paper-writing vault content
  - exact folder names
  - generated rules as VAKS rules
  - lexical/graph score as truth confidence
  - full automation as mainline VAKS runtime
```
