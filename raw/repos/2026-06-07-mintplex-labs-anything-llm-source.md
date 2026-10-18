---
type: source
record_kind: source_card
status: source-captured
title: "Mintplex-Labs/anything-llm"
source_id: github-mintplex-labs-anything-llm-2026-06-07
source_uri: https://github.com/Mintplex-Labs/anything-llm
source_url: https://github.com/Mintplex-Labs/anything-llm
source_type: repository
author: Mintplex-Labs
publisher: GitHub
published_at: 2023-06-04
updated_at: 2026-06-06
captured_at: 2026-06-07
captured_by: Codex
version_or_commit: cba598edb57f0850a7cc27f6baf824084ab9f17d
source_status: active
raw_location: raw/repos/2026-06-07-mintplex-labs-anything-llm-source.md
processing_mode: source-intake-routing-github-scout
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
topics:
  - obsidian-workbench
  - source-intake
entities:
  - AnythingLLM
  - ObsidianVault
  - DataConnectors
  - source citations
aliases:
  - Mintplex-Labs/anything-llm
projects:
  - VAKS
source_family: github_repo_workbench_scout
upstream_sources: []
verification_status: source_metadata_checked
tags:
  - github-scout
  - source-intake-routing
---

# 来源记录：Mintplex-Labs/anything-llm

## 为什么收录

为 `source-intake-routing` 工作台调研。AnythingLLM 的价值不是算法，而是“本地/私有知识工作台”的用户体验：workspace、documents、data connectors、Obsidian/GitHub/website/Youtube source routes、citation UI。

这张卡只记录来源，不代表 VAKS 采用 AnythingLLM。

## 来源信息

- 作者/组织：Mintplex-Labs
- 发布方：GitHub
- 原始链接：https://github.com/Mintplex-Labs/anything-llm
- 版本 / commit：`cba598edb57f0850a7cc27f6baf824084ab9f17d`
- commit time：2026-06-05T14:14:35Z
- GitHub pushed_at：2026-06-06T00:16:52Z
- stars captured：61149
- forks captured：6641
- default branch：master
- license：MIT
- source_status：active
- 采集方式：GitHub API metadata + raw file anchor inspection; no clone; no runtime execution.

## Intake Boundary

```yaml
processing_tier: medium
knowledge_status: raw
retrieval_policy:
  policy_kind: source_identity_only
  pack_allowed: drilldown_required
  action_basis_allowed: false
  warning_code: raw_is_provenance_only
promotion_gate: none
action_basis_allowed: false
truth_mutation_allowed: false
```

## Source / Code Anchors

| Anchor | What exists | Why it matters for source-intake-routing | Boundary |
|---|---|---|---|
| `README.md:52` | App ingests documents and provides document pipelines. | Useful product framing for simple workbench intake. | README claim only. |
| `README.md:67-70` | Workspace agents, document types, drag/drop uploads, source citations. | Direct UX inspiration for VAKS front door. | Citation UI is not evidence support. |
| `collector/utils/extensions/ObsidianVault/index.js:11-36` | Obsidian vault path parsing and output folder handling. | Highly relevant to Obsidian-specific source route. | Do not copy folder logic into mainline without review. |
| `collector/utils/extensions/RepoLoader/GithubRepo/RepoLoader/index.js:13-78` | GitHub repo loader and URL validation. | Useful for repo source-intake route hygiene. | Loader output is raw source, not reviewed knowledge. |
| `collector/utils/extensions/WebsiteDepth/index.js:71-90,137` | Website depth loader with HTML parsing. | Shows web-source acquisition route. | Web crawl results need provenance/selector records. |
| `frontend/src/components/Modals/ManageWorkspace/DataConnectors/index.jsx:1-11` | Data connector options include GitHub/GitLab/YouTube/Confluence/Obsidian/Website. | Strong workbench UX reference for source route entrypoints. | UI categories are not ontology. |
| `frontend/src/components/WorkspaceChat/ChatContainer/ChatHistory/Citation/index.jsx:52-113` | Citation/source type icon and source combining. | Useful for context pack display. | Citation display cannot equal action basis. |

## 初步看点

- AnythingLLM 很适合提醒 VAKS：工作台入口应该按 source route 展示，而不是让用户记目录路径。
- ObsidianVault、GitHubRepo、WebsiteDepth、Youtube 等 loader 是很好的“source-intake routing”参考集合。
- Source citation UI 适合借作 context pack display，但要明确 citation/source type 只是回钻入口。

## 明显疑点

- 未 clone、未运行、未验证 UI 交互。
- AnythingLLM 的“workspace/memory/agent”系统若整体吸收会污染 VAKS 边界。
- Citation UI 容易让用户误以为“有引用就有证据支持”。

## 可抽取 Candidate Points

- source-intake-routing 工作台应提供明显 source route：Obsidian、GitHub repo、website、YouTube、document upload。
- context pack UI 应显示 source type 和回钻入口，但必须同时显示 citable status / action_basis_allowed。
- Repo/website/Obsidian loader 只负责 capture/provenance，不负责 truth。

## 当前处理等级

```text
medium
```

升级到 heavy 的条件：

- 准备做 Obsidian front-door 页面或 source route UI 原型。
- 需要比较 AnythingLLM / Dify / RAGFlow 的 connector UX。

## 下一步

进入 `source-intake-routing` GitHub scout candidate distillation。
