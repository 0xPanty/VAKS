---
record_kind: source_card
type: source
status: source-captured
title: "trustedsec/Obsidian-Vault-Structure"
source_id: repo-trustedsec-obsidian-vault-structure-2026-06-07
source_uri: github:trustedsec/Obsidian-Vault-Structure
source_url: https://github.com/trustedsec/Obsidian-Vault-Structure
source_type: repository
author: TrustedSec / Sam Link
publisher: GitHub
published_at: 2021-09-08
captured_at: 2026-06-07
captured_by: Codex
extracted_at: 2026-06-07
extracted_by: Codex
extraction_tool: GitHub web/API + raw file inspection
version_or_commit: c408d4914a7bd98f1a5628e0067c84ab4b3a0a1a
commit_date_observed: 2021-09-08T22:34:38Z
source_status: legacy-active
github_stars_observed: 272
github_forks_observed: 55
github_pushed_at_observed: 2023-03-08T04:57:26Z
raw_location: raw/repos/2026-06-07-trustedsec-obsidian-vault-structure-source.md
processing_mode: repo-review
processing_level: medium-light
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
access_boundary: public_github_no_private_credentials
verification_status: repo_metadata_and_selected_files_observed
topics:
  - obsidian
  - team-knowledge-base
  - red-team
  - templater
  - git-sync
  - moc
projects:
  - verified-action-knowledge-system
source_family: team-operational-obsidian-vault-template
upstream_sources:
  - https://www.trustedsec.com/blog/obsidian-taming-a-collective-consciousness
related_outputs:
  - outputs/review/2026-06-07-trustedsec-obsidian-vault-structure-candidate-distillation.md
  - outputs/review/project_overlays/VAKS/VAKS-trustedsec-obsidian-vault-structure-2026-06-07.md
tags:
  - raw-repo
  - trustedsec
  - obsidian
  - team-knowledge
  - candidate-only
---

# Source: trustedsec/Obsidian-Vault-Structure

## 为什么收录

这是一个 2021 年的团队协作 Obsidian vault 模板，配套 TrustedSec 文章解释其红队/渗透测试团队知识管理动机。它对 VAKS 的价值在低摩擦捕获、团队知识共享、模板化 note creation、Git 同步边界和个人/团队区隔离。

## 来源信息

- 仓库：https://github.com/trustedsec/Obsidian-Vault-Structure
- 配套文章：https://www.trustedsec.com/blog/obsidian-taming-a-collective-consciousness
- 检查 commit：`c408d4914a7bd98f1a5628e0067c84ab4b3a0a1a`
- 仓库创建：2021-09-08
- 观察到 stars/forks：272 / 55
- 采集时间：2026-06-07

## Files Observed

```text
000 - Global Index (Start Here!).md
01 - Primary Categories/*
02 - Secondary Categories/02 - Obsidian.md
03 - Content/Obsidian Git.md
03 - Content/Templater.md
04 - Templates/0400 - Gen_Note.md
04 - Templates/04 - Structural Elements/*
```

## Intake Boundary

```yaml
processing_tier: medium
knowledge_status: raw
retrieval_policy:
  policy_kind: source_identity_only
  action_basis_allowed: false
truth_mutation_allowed: false
```

## 初步看点

- Team knowledge capture fails when contribution overhead is high.
- A master template can route new notes by type and destination.
- TTP / Tool / Idea / Documentation note types are useful for operational knowledge.
- Git sync can work for shared vaults, but conflicts and personal data require boundaries.

## 明显疑点

- Legacy source; not AI-native and not VAKS-specific.
- Obsidian Git auto-sync and plugin runtime should not become defaults.
- Security-team vault structure should not be generalized as VAKS schema.
