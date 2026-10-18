---
record_kind: source_card
type: source
status: source-captured
title: "AI Second Brain Architecture: 7 Folders That Make Your Obsidian Vault Actually Intelligent"
source_id: web-mindstudio-ai-second-brain-obsidian-vault-folder-architecture-2026-06-07
source_uri: mindstudio:blog/ai-second-brain-obsidian-vault-folder-architecture
source_url: https://www.mindstudio.ai/blog/ai-second-brain-obsidian-vault-folder-architecture
source_type: article
author: MindStudio Team
publisher: MindStudio
published_at: 2026-05-07
updated_at:
captured_at: 2026-06-07
captured_by: Codex
extracted_at: 2026-06-07
extracted_by: Codex
extraction_tool: web.open + Invoke-WebRequest metadata check
version_or_commit: "HTML SHA256 A073417D7670D15914294FAE2FD2E0850C3F041A841880C26E2E34128E5AFDCF"
source_status: active
http_status_observed: 200
html_content_length_observed: 96786
raw_location: raw/articles/2026-06-07-mindstudio-ai-second-brain-obsidian-vault-folder-architecture-source.md
raw_text_status: not_retained_full_web_article
processing_mode: article-review
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
review_priority: normal
review_owner: Codex
formalization_status: raw-only
access_boundary: public_web_no_cookies
verification_status: source_page_observed_not_independently_verified
evidence_granularity: excerpt_or_passage
topics:
  - obsidian
  - ai-second-brain
  - folder-architecture
  - llm-wiki
  - codex-automation
  - markdown-agent-memory
projects:
  - verified-action-knowledge-system
source_family: ai-obsidian-wiki-architecture-article
upstream_sources:
  - https://github.com/karpathy/llm-wiki
related_outputs:
  - outputs/review/2026-06-07-mindstudio-ai-second-brain-obsidian-folder-architecture-candidate-distillation.md
  - outputs/review/project_overlays/VAKS/VAKS-mindstudio-ai-second-brain-obsidian-folder-architecture-2026-06-07.md
related_prior_distillation:
  - outputs/review/2026-06-07-agricidaniel-claude-obsidian-candidate-distillation.md
  - outputs/review/project_overlays/VAKS/VAKS-agricidaniel-claude-obsidian-2026-06-07.md
candidate_relation_suggestions:
  - target: "raw-processed-wiki-spine"
    relation_type: refines
    relation_state: candidate
    why_suggested: "The article explains raw intake, processed audit trail, generated wiki, and index/log navigation as a simple vault architecture."
  - target: "agents-md-as-behavior-spec"
    relation_type: refines
    relation_state: candidate
    why_suggested: "The article treats agents.md as the editable behavior surface for AI vault operations."
  - target: "auto-processing-as-risk"
    relation_type: risk_of
    relation_state: candidate
    why_suggested: "The article praises hourly Codex automation and commit/push backup, which must not become VAKS defaults without gates."
tags:
  - raw-article
  - mindstudio
  - obsidian
  - candidate-only
---

# Source: MindStudio AI Second Brain Obsidian Folder Architecture

## 为什么收录

这篇文章是一个 AI + Obsidian second brain 的结构化说明。它把个人 vault 讲成一套很轻的文件系统：

```text
/raw
/raw/processed
/wiki
/journal
/crm
agents.md
index.md
log.md
```

它对 VAKS 有价值，因为它用很直白的方式解释了：

- 原始资料为什么要先进入 intake queue。
- processed 区为什么能当去重和 audit trail。
- wiki 为什么会从资料和问题中生长。
- journal / CRM 为什么是项目化使用层，不是通用真理层。
- `agents.md` 为什么像 agent 的行为 spec。
- `index.md` / `log.md` 为什么是导航和操作审计层。

但它也有明显风险：文章把自动化处理、自动 commit/push、问题生成 wiki、journal/CRM 全放在一个顺滑叙事里。对 VAKS 来说，这些都只能是 candidate/tool/workbench 层参考，不能直接变成 reviewed knowledge 或默认自动化。

## 来源信息

- 作者：MindStudio Team
- 发布方：MindStudio
- 发布时间：2026-05-07
- 原始链接：https://www.mindstudio.ai/blog/ai-second-brain-obsidian-vault-folder-architecture
- 采集时间：2026-06-07
- HTTP 状态：200
- HTML SHA256：`A073417D7670D15914294FAE2FD2E0850C3F041A841880C26E2E34128E5AFDCF`
- 原文全文：未复制保留；本卡只保留 provenance、锚点和候选抽取，避免把网页全文当本地 raw corpus。

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

Source card 只提供 provenance 和可回查锚点。它不提供 adopted decision、reviewed relation、truth confidence 或 action basis。

## Source Anchors

| Anchor | What the article covers | Candidate extraction | Boundary |
|---|---|---|---|
| web lines 38-48 | Title, date, and folder/file architecture summary | The article frames Obsidian as active AI knowledge base when folder structure is explicit | Marketing framing; not verification |
| web lines 54-79 | `/raw` as intake queue, Web Clipper as capture path | Raw intake should stay dumb until processed | VAKS raw is provenance, not library/truth |
| web lines 80-84 | `/raw/processed` as dedupe and audit trail | Processed state helps avoid repeated ingestion and preserve source trail | Moving files is only one possible dedupe mechanism |
| web lines 85-90 | `/wiki` generated pages and question-driven growth | Generated wiki can compound from sources and questions | Generated pages are candidate in VAKS, not reviewed |
| web lines 91-100 | `/journal` grounded reflection from wiki/journal/CRM | Journal is a use-context layer that can surface repeated patterns | Personal reflection is not truth support |
| web lines 101-106 | `/crm` as markdown contact records | Named markdown records can support contextual recall | CRM is sensitive/project/user data, not general knowledge |
| web lines 107-137 | `agents.md` as editable behavior prompt/spec | Behavior rules travel with the vault and are inspectable | Prompt file is not authority or permission |
| web lines 138-141 | `index.md` catalog and `log.md` audit trail | Pointer index + operation log help agent navigation and recovery | Index/log are activation/trace only |
| web lines 144-149 | AI does continuous retrieval work; index as pointer layer | Pointer index resembles agent memory architecture | Continuous automation is not a VAKS default |
| web lines 152-179 | non-obvious decisions: processed is load-bearing, GitHub backup, questions grow wiki | Dedupe, versioning, question-to-note are useful patterns | Auto commit/push and question-generated wiki need gates |
| web lines 182-192 | one-week setup path and scaling story | Start small; add journal/CRM/hourly automation later | Setup recipe is not VAKS implementation plan |
| web lines 207-209 | Karpathy LLM Wiki suggested for deeper wiki module | Source positions itself as a simplified extension of LLM Wiki | Need upstream check before promotion |

## 初步看点

The article is strongest as a plain-language explanation of an AI Obsidian vault:

```text
source intake
-> processed/audit trail
-> generated wiki
-> journal/CRM use contexts
-> agents.md behavior spec
-> index/log navigation and trace
```

The core useful idea for VAKS is not the exact folder names. It is the separation of:

```text
source queue
processed source trail
generated knowledge/workbench
use-context modules
agent behavior manual
navigation index
operation log
```

## 明显疑点

- The title says "7 folders", but the body describes 5 folders plus 3 root files. Treat the count as loose marketing wording, not schema.
- The article references a source implementation and video/demo but does not itself prove the automation quality.
- The article promotes hourly Codex automation and GitHub push as part of the architecture; VAKS must keep commit/push as separate user decisions.
- Web Clipper, journal, CRM, and agent vault access create privacy and source-hygiene questions.
- The article's `/wiki` generated knowledge has no VAKS-style candidate/reviewed/action-basis boundary.

## 可抽取 Candidate Points

- `/raw` as an intentionally dumb queue keeps capture easy and prevents premature authority.
- `/raw/processed` or an equivalent manifest/state marker can serve dedupe and audit-trail needs.
- Generated wiki pages are useful as candidate synthesis and navigation, but they need review gates before action use.
- Journal and CRM are use-context modules, not global knowledge layers.
- `agents.md` works as a project-local behavior spec, similar to VAKS `AGENTS.md` / handoffs / skill manuals.
- `index.md` and `log.md` act as pointer layer and operation trace, not truth.
- Question-driven wiki growth is useful, but the generated answer page must stay candidate-only.
- Automated processing should start manual/explicit and only become scheduled after workflow pressure justifies it.

## 当前处理等级

```text
medium article intake
```

Upgrade to heavy only if a future task tries to use this article to justify:

- changing VAKS source-intake schema;
- enabling scheduled intake;
- enabling auto commit/push;
- treating generated wiki pages as reviewed knowledge;
- adding journal/CRM modules to VAKS core.

## 下一步

Read the candidate distillation and VAKS overlay for borrowing order and avoid tags.
