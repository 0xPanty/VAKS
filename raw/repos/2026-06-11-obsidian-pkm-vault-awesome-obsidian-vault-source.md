---
type: source
record_kind: source_card
status: source-captured
title: "Awesome List of Obsidian vaults"
source_id: obsidian-pkm-vault-awesome-obsidian-vault-2026-06-11
source_uri: github:obsidian-pkm-vault/awesome-obsidian-vault
source_url: https://github.com/obsidian-pkm-vault/awesome-obsidian-vault
source_type: repo
author: obsidian-pkm-vault
publisher: GitHub
published_at:
updated_at: 2026-06-11
captured_at: 2026-06-11
captured_by: Codex
version_or_commit: 7f2143823d07698b8873f534831ea6516ae52e3f
source_integrity:
  source_hash: 22ad85f073f27827b00952890c8bcac29d1c40147705067b367f9925c697fede
  snapshot_hash:
  ingest_state: new
adapter_ingest:
  adapter_name: github-raw-readme
  adapter_version: manual-powershell-Invoke-RestMethod
  capture_method: raw README fetch + git ls-remote HEAD
  extraction_trace: "Parsed README table containing 48 vault entries."
  known_limits:
    - "List curation is not independent evidence that each vault is high quality."
    - "The list notes that not all vaults are fully compatible with Obsidian Markdown syntax."
    - "Linked vaults keep their own licenses and must be reviewed separately before reuse."
source_status: active
raw_location: raw/repos/2026-06-11-obsidian-pkm-vault-awesome-obsidian-vault-source.md
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
formalization_status: raw-only
topics:
  - obsidian-vault
  - digital-garden
  - knowledge-base
  - template-gallery
  - source-scouting
projects:
  - verified-action-knowledge-system
source_family: awesome-list
upstream_sources: []
verification_status: unverified
candidate_relation_suggestions: []
tags:
  - source-card
  - github
  - awesome-list
  - obsidian
  - candidate-routing
why_saved: see_body_or_legacy_record
---

# 来源记录：Awesome List of Obsidian vaults

## 为什么收录

用户指定此仓库作为后续 VAKS 蒸馏的候选来源清单，并要求已蒸馏过的库跳过。

这个 source card 只记录清单来源和采集状态。具体 vault 的可借鉴点、优先级和跳过判断放在候选分流文件：

- `outputs/review/2026-06-11-awesome-obsidian-vault-candidate-triage.md`

## 来源信息

- 作者：obsidian-pkm-vault
- 发布方：GitHub
- 原始链接：https://github.com/obsidian-pkm-vault/awesome-obsidian-vault
- Raw README：https://raw.githubusercontent.com/obsidian-pkm-vault/awesome-obsidian-vault/main/README.md
- 版本 / commit：`7f2143823d07698b8873f534831ea6516ae52e3f`
- README SHA256：`22ad85f073f27827b00952890c8bcac29d1c40147705067b367f9925c697fede`
- README table entries：48
- source_status：active
- 采集方式：`git ls-remote` 固定 HEAD，`Invoke-RestMethod` 获取 raw README。

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

## 初步看点

- 这是一个 Obsidian vault / Markdown knowledge base 的横向入口。
- 对 VAKS 有价值的是筛选候选参考库，而不是把列表本身当成质量证明。
- 需要按 VAKS 当前架构层分流：source ingest、review queue、activation、dev context、workbench、publishing、agent boundary、risk。

## 明显疑点

- Awesome list 的收录和星标只说明 curated/popular/polished，不说明适合 VAKS。
- 很多条目是内容库或静态网站，不是知识系统架构参考。
- 有些条目可能不兼容 Obsidian Markdown，不能直接按 vault 模板吸收。
- 每个候选库仍需独立 source/code/template anchors。

## 当前处理等级

```text
medium
```

升级到 heavy 的条件：

- 某个候选库进入 P1 / P2 且要做独立架构 review。
- 某个候选库可能影响 VAKS 检索、工作台、agent boundary、review queue 或 source intake。
- 某个候选库暴露明确反模式，值得写入 risk / anti-pattern 候选。
