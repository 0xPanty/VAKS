---
type: source
status: source-captured
title: "ResearchWiki / AI paper knowledge-base system"
source_id: github:jiawei601/ResearchWiki@3f0705087fdd242514f1179bc53518b87a97f02c
source_uri: https://github.com/jiawei601/ResearchWiki
source_url: https://github.com/jiawei601/ResearchWiki
source_type: repo
author: jiawei601
publisher: GitHub
published_at:
updated_at: 2026-06-03T12:55:47Z
captured_at: 2026-06-07
captured_by: Codex
version_or_commit: 3f0705087fdd242514f1179bc53518b87a97f02c
source_status: active
raw_location: raw/repos/_snapshots/jiawei601-ResearchWiki-3f0705087fdd242514f1179bc53518b87a97f02c.zip
snapshot_sha256: 81C459F54F0FF7116D9510DDAF001368ACB78F712D95B8210C00E07DB2D14EB0
processing_mode: repository_review
processing_level: heavy
processing_tier: heavy
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
formalization_status: raw-only
topics:
  - ai-research-wiki
  - paper-intake
  - zotero-workflow
  - obsidian
  - source-ingest
projects:
  - VAKS
source_family:
  - external-reference
  - repo-reference
upstream_sources: []
verification_status: source-captured
candidate_relation_suggestions:
  - target: "paper-intake-as-candidate-graph"
    relation_type: refines
    relation_state: candidate
    why_suggested: "The repo shows a concrete Zotero/PDF-to-paper/topic/method/claim/gap workflow that may refine VAKS source intake and academic research lanes."
    source_anchor: README.md:65-107
tags:
  - source
  - repo
  - source-intake
  - research-wiki
  - zotero
---

# 来源记录：jiawei601/ResearchWiki

## 为什么收录

用户明确要求蒸馏 `jiawei601/ResearchWiki`。

本记录只保存来源、快照和初步可追踪锚点。它不是采纳结论，不是 reviewed knowledge，不是 action basis。

## 来源信息

- 作者：`jiawei601`
- 发布方：GitHub
- 原始链接：https://github.com/jiawei601/ResearchWiki
- 默认分支：`main`
- 检查 commit：`3f0705087fdd242514f1179bc53518b87a97f02c`
- commit 时间：`2026-06-03T12:47:46Z`
- commit message：`Improve open-source README`
- pushed_at：`2026-06-03T12:55:47Z`
- license：MIT
- GitHub stars / forks at capture：8 / 0
- 快照位置：`raw/repos/_snapshots/jiawei601-ResearchWiki-3f0705087fdd242514f1179bc53518b87a97f02c.zip`
- 快照 SHA256：`81C459F54F0FF7116D9510DDAF001368ACB78F712D95B8210C00E07DB2D14EB0`
- 采集方式：GitHub public API metadata + GitHub zipball snapshot + local file inspection

## Intake Boundary

```yaml
processing_tier: heavy
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

Source records provide provenance and findability. They must not carry adopt/reject verdicts, truth scores, project borrowing conclusions, or action basis.

## Source / Code Anchors

| Anchor | What exists | Why it matters | Boundary |
|---|---|---|---|
| `README.md:36-47` | Repo positioning as local AI paper knowledge base using Codex / LLM Agent, Obsidian, Zotero | Names the problem: scattered PDFs and Zotero records become a maintained Markdown Wiki | Positioning only |
| `README.md:67-79` | Three-layer design: `raw/`, `wiki/`, `memory/ + agents/ + templates/`; paper card is not the endpoint | Core architecture spine | Candidate design reference |
| `README.md:85-95` | Mermaid flow from Zotero collection to import plan, PDF read, paper page, topic/method, claim/gap, synthesis/gap/review, memory/log | Shows the actual loop | Candidate workflow reference |
| `README.md:199-218` | Zotero/PDF ingestion safety boundary and example prompts | Good source-intake boundary | Candidate source-ingest reference |
| `AGENTS.md:18-25` | Raw/wiki/rule layer split and "not only single-paper summary" rule | Confirms README is operational instruction, not just marketing copy | Candidate operation reference |
| `AGENTS.md:121-127` | `import_zotero.md` creates import plan/manifest; single-paper reading goes to `pdf_read_agent.md` | Strong candidate for future Zotero lane | Candidate workflow reference |
| `AGENTS.md:232-246` | Raw safety, source/evidence back-links, uncertainty marking, tag/alias discipline | Strong guardrail pattern | Candidate guardrail reference |
| `AGENTS.md:270` | Graph view value comes from real relations, not link count | Important anti-metric warning | Candidate anti-pattern |
| `agents/import_zotero.md:22-37` | Read only user-specified Zotero collection; no full DB/storage scan; no Zotero mutation | Strong privacy and source-boundary pattern | Candidate source-ingest reference |
| `agents/pdf_read_agent.md:23-33` | Single PDF creates paper page and extracts topic/method/dataset/metric/claim/gap; no cross-paper synthesis | Separation of intake vs synthesis | Candidate processing reference |
| `agents/pdf_read_agent.md:80-83` | Important claims need source support; gaps need evidence or `AI 推断`; no summary-only output | Evidence discipline | Candidate review input |
| `agents/synthesis_agent.md:60-72` | Multi-paper synthesis reads paper/topic/method/claim/gap and marks evidence gaps | Periodic synthesis pattern | Candidate synthesis reference |
| `agents/gap_agent.md:64-90` | Gap extraction from limitations, assumptions, metrics, conflicts; evidence strength and no duplicate gap pages | Good gap discipline | Candidate research-lane reference |
| `agents/lint_agent.md:23-25` | Lint checks duplicate pages, missing claim sources, missing gap evidence strength | Maintenance surface | Candidate lint reference |
| `memory/hard_memory.md:21-32` | Long-term project rules and AI inference boundary | Operational memory pattern | Not truth layer |
| `memory/tag_taxonomy.md:14-18` | Tag canonicalization rules | Useful alias/tag hygiene | Candidate lint reference |
| `memory/term_aliases.md:10-47` | Alias map to prevent duplicate topic/method/claim/gap pages | Duplicate prevention | Candidate lint reference |
| `docs/zotero-workflow.md:5-11` | Collection -> plan/manifest -> check existing -> user chooses -> ingest one at a time; no storage scan or moving PDFs | Concise Zotero workflow | Candidate source-ingest reference |

## 初步看点

- 它把论文入库拆成 `Zotero collection -> import_plan / manifest -> single-paper PDF read -> paper card -> topic/method/claim/gap -> synthesis/review/gap`。
- 它把 `memory/agents/templates` 做成显性规则层，让 agent 不靠聊天历史工作。
- 它强调论文卡片不是终点，真正价值在跨论文的 claim、gap、synthesis、review。
- 它有比普通 Obsidian vault 更清晰的 Zotero 安全边界：只读指定 collection，不扫全库，不改 Zotero 条目和附件。
- 它有轻量但重要的证据纪律：重要判断回链到论文、页码、章节、图表或 claim；AI 推断必须标明。

## 明显疑点

- `wiki/claims/` 在 ResearchWiki 中是可复用判断页面，但没有 VAKS 的 reviewed/action-basis 分离。
- `memory/` 是规则和研究状态，不应被误读成 truth layer。
- Zotero 插件/connector 只是路径说明，仓库本身不是完整运行时。
- Obsidian graph 仍需要人工和规则维护，不能把链接数量当成关系质量。
- 它适合论文研究流，不是通用资料库/行动依据系统。

## 可抽取 Candidate Points

- `zotero_collection_as_source_candidate_lane`
- `paper_card_not_endpoint`
- `paper_topic_method_claim_gap_graph`
- `evidence_marked_gap_and_claim_intake`
- `memory_agents_templates_as_agent_rule_layer`
- `tag_alias_lint_for_duplicate_prevention`
- `graph_links_are_not_relation_quality`

## 当前处理等级

```text
heavy
```

升级为主线设计或 action-facing 支持的条件：

- 必须走 VAKS v0.2.13 / evidence-aware review；
- 必须区分 source identity、candidate orientation、project overlay、reviewed support；
- 必须补齐插件/connector 权限边界与本地 Zotero 读取安全验证；
- 必须证明不会把 ResearchWiki 的 `memory` 或 `wiki/claims` 误升格成 VAKS reviewed truth。

## 下一步

- 已生成候选蒸馏：`outputs/review/2026-06-07-jiawei601-researchwiki-candidate-distillation.md`
- 已生成架构复盘：`wiki/summaries/2026-06-07-jiawei601-researchwiki-architecture-review.md`
- 已生成 VAKS 项目 overlay：`outputs/review/project_overlays/VAKS/VAKS-jiawei601-researchwiki-2026-06-07.md`
