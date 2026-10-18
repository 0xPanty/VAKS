---
type: source
status: source-captured
title: "DataChain"
source_id: 2026-06-06-datachain-ai-datachain-source
source_uri: https://github.com/datachain-ai/datachain
source_url: https://github.com/datachain-ai/datachain
source_type: repository
author: datachain-ai
publisher: GitHub
published_at:
updated_at: 2026-06-04
captured_at: 2026-06-06
captured_by: Codex
version_or_commit: a8bd465484e7dcb7501cef18d672a95cf27762c3
commit_time: "2026-06-04 21:46:30 +0700"
commit_subject: "Skill knowledge base: refactor to reuse code in SaaS (#1797)"
source_status: active
license: Apache-2.0
raw_location: raw/repos/2026-06-06-datachain-ai-datachain-source.md
snapshot_location: raw/repos/_snapshots/datachain-ai-datachain-a8bd465484e7dcb7501cef18d672a95cf27762c3.zip
processing_mode: immediate
processing_level: heavy
review_priority: high
review_owner: Codex
formalization_status: candidate-generated
topics:
  - data-context-layer
  - typed-datasets
  - versioned-artifacts
  - agent-knowledge-base
  - compiled-markdown
  - codex-skill
  - mcp
  - lightweight-toolchain
  - retrieval
  - checkpoints
  - delta-processing
projects:
  - verified-action-knowledge-system
source_family:
  - data-context-layer
  - agent-workbench
  - toolchain-contract
  - retrieval-workbench
upstream_sources: []
verification_status: primary-source-captured
candidate_relation_suggestions:
  - target: "[[Activation Tier]]"
    relation_type: refines
    relation_state: candidate
    why_suggested: "Compiled knowledge pages and dataset registry are useful as read-first activation surfaces, not truth."
  - target: "[[Agent memory quarantine]]"
    relation_type: refines
    relation_state: candidate
    why_suggested: "DataChain's Skill/MCP separation and local dc-knowledge read path are useful for read-first agent operation."
  - target: "[[Source Intake]]"
    relation_type: refines
    relation_state: candidate
    why_suggested: "Named, versioned, typed outputs suggest a stricter manifest contract for VAKS source/candidate/query-run artifacts."
  - target: "[[Feedback Ledger]]"
    relation_type: relates_to
    relation_state: candidate
    why_suggested: "Checkpoint, delta, and query lineage patterns may help append-only run records without truth mutation."
tags:
  - datachain
  - typed-datasets
  - versioned-artifacts
  - compiled-knowledge-base
  - obsidian
  - codex-skill
  - mcp-read-layer
  - candidate-only
---

# DataChain Source Record

## 为什么收录

DataChain 是一个 Python 库，目标不是普通 RAG，也不是 Obsidian 插件。它把 S3 / GCS / Azure / local files 里的文件处理结果落成 typed、versioned、queryable datasets，再把这些 datasets 编译成 agent 和人都能读的 `dc-knowledge/` Markdown 知识库。

它对 VAKS 的价值主要在三个地方：

```text
1. 已经做过的处理结果如何被 agent 找到并复用
2. 脚本 / pipeline 产物如何命名、version、记录 lineage、避免 silent overwrite
3. agent 如何先读 compiled knowledge surface，再查 registry，最后才触发昂贵计算
```

边界要写硬：DataChain 自己把 Dataset DB 说成 ground truth；VAKS 不能照搬。对 VAKS 来说，任何 DB / index / compiled view / skill output 都只能是 activation、workbench、receipt 或 candidate layer，不能替代 Markdown reviewed knowledge。

## 来源信息

- Repository: `datachain-ai/datachain`
- URL: https://github.com/datachain-ai/datachain
- Checked commit: `a8bd465484e7dcb7501cef18d672a95cf27762c3`
- Commit time: `2026-06-04 21:46:30 +0700`
- Commit subject: `Skill knowledge base: refactor to reuse code in SaaS (#1797)`
- License: Apache-2.0
- Package status marker: `pyproject.toml` includes `Development Status :: 2 - Pre-Alpha`
- Snapshot: `raw/repos/_snapshots/datachain-ai-datachain-a8bd465484e7dcb7501cef18d672a95cf27762c3.zip`
- Inspected mode: source/docs/code read; no package execution; no network service or MCP server launched.

## 文件 / 代码锚点

| Anchor | What exists | VAKS extraction | Boundary |
|---|---|---|---|
| `README.md:9-17` | DataChain presents Compute Engine, Dataset DB, Knowledge Base, Agent Harness. | Three-layer split maps to VAKS toolchain/cache/workbench/agent surfaces. | Product README claim is not independent evidence of quality. |
| `README.md:142-180` | Every `.save()` registers a dataset with schema, version, lineage, local SQLite `.datachain/db`; Pydantic schema becomes queryable. | VAKS scripts should produce named, typed, versioned artifacts with receipts. | Dataset version is provenance, not truth confidence. |
| `README.md:216-263` | Checkpoints, incremental update, vectors stored with metadata. | Long source intake / index rebuild / embedding jobs need resumability and reusable caches. | Vector distance remains activation / diagnostic only. |
| `README.md:312-326` | Dataset DB is called ground truth; Knowledge Base is derived Markdown in `dc-knowledge/`. | Compiled Markdown for agents is a strong workbench pattern. | VAKS must invert the authority: Markdown reviewed notes remain source of truth; compiled views are derived. |
| `docs/architecture.md:13-19` | Compute Engine, Dataset DB, Knowledge Base; agents read KB first, query DB if summaries are not enough, compute only when nothing higher answers. | Good read-first operating sequence for Codex skill: compiled index -> reviewed/candidate artifacts -> raw/compute. | Do not hide VAKS gates behind an invisible runtime. |
| `docs/concepts/dataset-db.md:7-17` | Dataset DB stores named, versioned datasets as units of reasoning. | Candidate source/candidate/query-run/context-pack artifacts can be treated as named units. | "Settled fact" language is unsafe for VAKS unless reviewed. |
| `docs/concepts/dataset-db.md:35-39` | Store stays current because operations record results by running, not voluntary catalog maintenance. | Useful warning against manual-only maintenance indexes. | Automatic recording can still record bad outputs. |
| `docs/concepts/dataset-db.md:67-126` | Registry/provenance, queryable system of record for datasets; out of scope for Slack/Notion/meeting institutional knowledge. | VAKS can borrow registry and provenance; scope mismatch is explicit. | DataChain is not a full knowledge governance system. |
| `docs/concepts/datasets.md:7-25` | Dataset is named, versioned typed collection; carries complex nested objects. | VAKS artifact manifests should prefer typed fields over loose blobs. | Typed field completeness does not imply evidence support. |
| `docs/concepts/datasets.md:117` | Agents depend on datasets as established facts. | Shows why VAKS needs quarantine and warrant gates before agent reuse. | VAKS cannot let agent-produced data become fact by save alone. |
| `docs/concepts/chain.md:7-30` | Chain is lazy; terminal operations run; results go to staging and only `save()` commits all-or-nothing. | Strong pattern for VAKS lightweight compiler scripts: explicit inputs, staging, atomic publish. | VAKS should not require DataChain runtime just to get the pattern. |
| `docs/concepts/knowledge-base.md:7-29` | Knowledge Base compiles datasets into agent-readable pages with schema, lineage, previews, links; compiled rather than retrieved. | Directly useful for Obsidian workbench and read-first Codex skill. | "Compiled not retrieved" should not become "view equals authority." |
| `docs/concepts/skill-and-mcp.md:7-17` | Skill is local OSS with `dc-knowledge/` + `.datachain/db`; MCP is hosted Studio. | Useful split for VAKS: local read-first skill now; remote write/MCP parked. | MCP write/read authority must stay least-privilege. |
| `docs/concepts/skill-and-mcp.md:27-46` | Skill teaches agent how to introspect KB/DB and when to materialize new datasets; MCP adds teams/ACL/scale. | VAKS Codex skill should encode read order, stop rules, and write boundaries. | Skill cannot self-approve promotion. |
| `src/datachain/skill/core/SKILL.md:32-48` | Dataset reuse is highest priority; read `dc-knowledge/index.md` first; reuse over rebuild; save named datasets. | VAKS skill should read indexes/records before re-extracting or re-running. | Reuse is activation efficiency, not correctness. |
| `src/datachain/skill/core/SKILL.md:75-95` | One stage = one script; expensive compute saves full result, problem-specific filters downstream. | Strong toolchain contract for VAKS source intake, embedding, ASR/OCR, pack generation. | Not every ordinary query needs saved artifacts. |
| `src/datachain/skill/core/SKILL.md:147-183` | CAST quick reference; `dc-knowledge/` owned by knowledge skill, not directly modified. | Separation of mechanics skill vs methodology skill maps well to VAKS Codex skill design. | CAST should not be imported as VAKS schema now. |
| `src/datachain/skill/knowledge/SKILL.md:49-68` | `dc-knowledge/` Markdown is persistent output; JSON intermediate; `CAST.md` owns methodology. | Useful division: durable Markdown output + disposable intermediate receipts. | Intermediate JSON should not become hidden authority. |
| `src/datachain/skill/knowledge/SKILL.md:77-115` | Workflow modes and precondition: read index and CAST before writing pipeline; if existing dataset solves task, do not write a new pipeline. | VAKS skill boot sequence should do read-first + stop-if-supported. | "Existing artifact solves task" still needs v0.2.13 if action-facing. |
| `src/datachain/skill/knowledge/CAST.md:84-108` | CAST layers: Container, Asset, Sense, Task. | Great substrate-vs-task intuition for VAKS derived artifacts. | Do not expand VAKS object model with CAST layers now. |
| `src/datachain/skill/knowledge/CAST.md:903-927` | Critical rules: follow CAST, save named/tagged datasets, C/A/S substrate mandatory, one script per stage, one save per script. | Good operating discipline for script layer. | Too heavy for ordinary VAKS capture. |
| `src/datachain/cli/commands/skill.py:26-45` | Skill installer supports targets including `codex` with `.codex/skills`. | Confirms DataChain treats Codex skill surface as first-class. | VAKS should not install external skill into project by default. |
| `src/datachain/skill/knowledge/scripts/plan.py:53-190` | Plan script checks `dc-knowledge/index.md`, JSON/MD paths, and statuses `new`, `stale`, `ok`. | Useful model for VAKS index/workbench freshness audit. | Freshness status is maintenance signal, not truth status. |
| `docs/guide/delta.md:97-109` | Delta processing has unsafe operations; `delta_unsafe=True` is advanced. | VAKS update-index / query-run refresh should label incremental modes and unsafe aggregation. | Incremental success does not prove full-corpus correctness. |
| `docs/guide/checkpoints.md:202-204` | Checkpoints have limitations: script path matters, some callables always recompute. | VAKS checkpoint/resume must record script path/version and limitations. | Checkpoints are operational, not evidence. |
| `docs/use-cases/agent-anti-patterns.md:46-88` | Anti-patterns include folder-as-dataset, reprocessing, long pipelines without checkpoints. | Good negative examples for VAKS toolchain and agent operation. | DataChain anti-patterns are data-pipeline-specific, adapt cautiously. |
| `docs/use-cases/retroactive-agent-runs.md:48-83` | New model/prompt creates derived dataset; old remains unchanged; compare side-by-side. | Useful for VAKS source extraction re-runs and candidate version diffs. | New model output is not a reviewed replacement. |
| `docs/use-cases/cross-agent-reasoning.md` | Knowledge Base lets agents/humans coordinate through Markdown pages. | Strong support for Obsidian-facing workbench. | Coordination surface is not authority surface. |

## 人话总结

DataChain 的核心不是“搜索更准”，而是：

```text
raw files
-> typed pipeline outputs
-> named versioned datasets
-> queryable registry / lineage
-> compiled markdown knowledge base
-> agent reads existing substrate before doing new work
```

对 VAKS 来说，它最该被吸收成：

```text
raw/source records
-> typed candidate / extraction / query-run / context-pack artifacts
-> compiled Obsidian / Codex read-first indexes
-> action-facing use still returns to reviewed evidence + warrant gate
```

不要吸收成：

```text
Dataset DB becomes truth
compiled index becomes authority
agent save becomes promotion
MCP write becomes default
CAST becomes new VAKS schema
```

## Candidate Points

1. `compiled-kb-as-read-first-surface`

候选结论：VAKS 可以编译一层 agent-readable Markdown/index/workbench，让 Codex 先读“已有源卡、候选蒸馏、review queue、context-pack receipt、decision/action basis 索引”，再决定是否深挖 raw。

边界：compiled surface 是 activation/workbench，不是 reviewed truth。

2. `versioned-operational-artifacts`

候选结论：source extraction、candidate distillation、query-run、context-pack、feedback-event 应该是命名、可复盘、可比较的 artifacts，而不是散落的临时文本。

边界：artifact version 是运行 provenance，不是 truth confidence。

3. `staged-atomic-toolchain-writes`

候选结论：VAKS lightweight scripts 应该有 file-in/file-out、staging、receipt、atomic publish 的习惯，避免 silent overwrite 和半成品污染。

边界：工程成功不等于语义正确。

4. `reuse-before-recompute-agent-rule`

候选结论：Codex skill 应先查已有 source card / distillation / index / review queue，再决定是否重新抓取、重新摘要、重新生成 pack。

边界：复用减少成本和漂移，但行动依据仍需 evidence + warrant。

5. `one-stage-one-script-toolchain`

候选结论：ingest-source、make-candidate、update-index、make-context-pack、record-feedback 等脚本应拆开，不要一个万能 daemon 混合多种语义责任。

边界：拆脚本是可维护性，不是新平台化方向。

6. `expensive-compute-save-full-filter-later`

候选结论：ASR/OCR/embedding/LLM extraction 这类昂贵处理应该先保存足够通用的中间产物，再在 query/task 层过滤，避免为一次任务丢掉可复用信息。

边界：普通轻查询不需要被迫保存所有中间物。

7. `checkpoint-and-delta-as-derived-layer-hygiene`

候选结论：长源处理和索引刷新需要 checkpoint/delta；但对 group_by/merge/diff/aggregate 等全局操作，要明确标注 delta unsafe 或强制全量重建。

边界：delta 成功只说明增量运行完成，不说明全库判断成立。

8. `cast-as-substrate-analogy-not-schema`

候选结论：CAST 的 Container/Asset/Sense/Task 对 VAKS 有启发：先保留可复用 substrate，再做 task-specific pack/result。

边界：不要把 CAST 变成 VAKS 正式对象层。

## Open Review

- 需要后续和 VAKS 当前 compiler/toolchain contract 设计一起对齐。
- 需要区分哪些 artifacts 只在 `outputs/review`，哪些未来可进入 `tools/` 产物规范。
- 若未来真的评估 DataChain runtime，要另开工程试验，不在本次 source distillation 内决定。
