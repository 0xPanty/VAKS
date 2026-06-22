---
type: source
record_kind: source_card
status: source-captured
title: "byarbrough/obsidian-para source review"
source_url: "https://github.com/byarbrough/obsidian-para"
source_type: repo
captured_at: 2026-05-27
captured_by: Codex
raw_location: "temporary clone: %TEMP%/codex-obsidian-para"
review_priority: normal
review_owner: Codex
formalization_status: candidate-generated
topics:
  - PARA
  - Obsidian
  - memory-tier
  - dev-context
  - actionability
projects:
  - verified-action-knowledge-system
source_family: obsidian-vault-template
upstream_sources:
  - "https://fortelabs.co/blog/para/"
  - "https://fortelabs.co/blog/progressive-summarization-a-practical-technique-for-designing-discoverable-notes"
verification_status: single-source
candidate_relation_suggestions:
  - target: "[[2026-05-27-obsidian-para-architecture-review]]"
    type: derived_from
    strength: 5
    confidence: high
    evidence:
      - "[[2026-05-27-obsidian-para-source]]"
    rationale: "This source record anchors the architecture review and extracted patterns."
    created: 2026-05-27
    last_verified: 2026-05-27
tags:
  - source
  - repo
  - obsidian
  - para
  - memory-tier
knowledge_status: raw
processing_tier: light
source_id: "https://github.com/byarbrough/obsidian-para"
why_saved: see_body_or_legacy_record
retrieval_policy:
  policy_kind: source_identity_only
  pack_allowed: drilldown_required
  action_basis_allowed: false
  warning_code: raw_is_provenance_only
promotion_gate: none
action_basis_allowed: false
truth_mutation_allowed: false
---
# 来源记录：byarbrough/obsidian-para

## 为什么收录

用户要求把 `byarbrough/obsidian-para` 作为外部参考库分析，优先判断它能否进入本资料库的大框架设计防线，并专门检查它是否能补强当前正在打磨的 `MEMORY_TIER.md` / `DEV_CONTEXT.md` 初稿。

## 来源信息

- 作者：byarbrough
- 发布方：GitHub
- 原始链接：https://github.com/byarbrough/obsidian-para
- 仓库描述：Template for using Obsidian for P.A.R.A.
- 采集方式：GitHub 页面阅读 + `git clone --depth 1`
- 当前检查 commit：`83da427385df3bbdfee30817a63f464f0016ac3f`
- commit 时间：`2025-10-23T21:57:59-04:00`
- commit message：`Completely ignore .obsidian/`
- release：GitHub 页面显示 latest release 为 `Initial Release`，日期 `2022-01-17`

## Source Code / Vault Template Map

本仓库不是插件或运行时代码库，而是一个最小 Obsidian vault 模板。

文件清单：

```text
.gitignore
.obsidian/app.json
.obsidian/appearance.json
.obsidian/hotkeys.json
.obsidian/templates.json
1. Projects/README.md
2. Areas/README.md
3. Resources/README.md
4. Archive/README.md
README.md
images/obsidian-folder-as-vault.png
images/obsidian-insert-template.png
templates/goal_template.md
templates/resource_template.md
```

关键 blob / size：

```text
README.md                                      8885 bytes
1. Projects/README.md                         1595 bytes
2. Areas/README.md                            2016 bytes
3. Resources/README.md                        1826 bytes
4. Archive/README.md                          1815 bytes
templates/goal_template.md                    89 bytes
templates/resource_template.md                81 bytes
.obsidian/templates.json                      27 bytes
.gitignore                                    14 bytes
```

Obsidian 配置很轻：

```text
.obsidian/templates.json:
  templates folder = templates

.obsidian/appearance.json:
  baseFontSize = 16

.obsidian/app.json and hotkeys.json:
  empty JSON

.gitignore:
  ignores .obsidian/**
```

## 初步看点

1. PARA 的强项不是“知识真实性”，而是“行动性位置”：把资料放到下一次最可能使用的位置。
2. Projects / Areas / Resources / Archive 可以看作一套生命周期状态机，而不是可信知识 schema。
3. 迁移建议中“旧资料先进 Archive，用到时再移动出来”非常贴合冷热记忆：默认 cold，使用行为触发 reactivation。
4. Progressive Summarization 提供了“每次交互压缩一点”的激活后加工思路，但必须保留 raw source，不能让压缩替代证据。
5. PARA 缺少 review gate、truth confidence、source provenance、negative evidence、risk layer；不能直接作为本资料库主骨架。

## 明显疑点

- 仓库主要是模板和说明，代码实现量很小，不能提供复杂自动化实现参考。
- PARA 的 top-level folder taxonomy 如果直接搬入本资料库，会冲突 `raw/`、`wiki/`、`outputs/`、`products/` 的 verified-action 分层。
- “folder where likely needed next” 对个人效率有帮助，但不能替代 `verification_status`、`relations`、`evidence_level`。
- Risk/anti-pattern 在 PARA 中没有独立层；这是我们 `DEV_CONTEXT.md` 需要保留并强化的差异化设计。

## 可抽取 Candidate Points

- Actionability-based placement：资料位置按下一次行动场景决定，而不是按主题纯分类。
- Archive-first migration：旧资料不预先精细整理，先入档案；使用时再激活和重定位。
- Lifecycle transition grammar：Project / Area / Resource / Archive 之间有明确流转。
- Project goal gate：没有目标或时限的内容不应轻易进入 project/current-work 层。
- Progressive summarization on interaction：每次重新接触资料时做轻量压缩和连接，而不是一次性完美整理。
- Primary reference vault：可以先有一个主参考系统，再投射到其他工具，而不是所有系统各自发散。

## 对当前 MEMORY_TIER / DEV_CONTEXT 的直接价值

可吸收：

```text
Archive-first lazy reactivation:
  old material starts cold; actual use creates activation reason.

Where-needed-next rule:
  hot/warm should be scoped by next likely action, not generic importance.

Project gate:
  dev context Core needs goal / task / stop condition, not just relevance.

Lifecycle transition:
  project结束后要扫描可复用材料，写回 warm patterns / resources，再 archive one-off residue.
```

不能吸收为核心：

```text
PARA folders as truth layer
manual file-moving as primary memory mechanism
four folders as universal schema
archive as evidence quality signal
```

## 下一步

- 已创建架构 review：`wiki/summaries/2026-05-27-obsidian-para-architecture-review.md`
- 已提炼模式：`wiki/patterns/actionability-based-memory-routing.md`
- 已提炼模式：`wiki/patterns/archive-first-lazy-reactivation.md`
- 已提炼反模式：`wiki/anti-patterns/para-folder-taxonomy-as-truth-layer.md`
- 已轻量更新 `MEMORY_TIER.md` / `DEV_CONTEXT.md`，作为初稿骨架的 PARA 参考修正。
