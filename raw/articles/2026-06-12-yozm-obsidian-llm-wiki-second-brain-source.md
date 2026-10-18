---
type: source
record_kind: source_card
status: source-captured
title: "나만의 세컨 브레인: 옵시디언 기반 LLM 위키 구축기"
title_zh: "我的第二大脑：基于 Obsidian 的 LLM Wiki 构建记"
source_id: 2026-06-12-yozm-obsidian-llm-wiki-second-brain
source_uri: "https://yozm.wishket.com/magazine/detail/3792/"
source_url: "https://yozm.wishket.com/magazine/detail/3792/"
source_type: article
author: "곰씨네 IT 블로그"
publisher: "요즘IT / Wishket"
published_at: "2026-06-11"
published_at_note: "Inferred from site label '1일 전' captured on 2026-06-12; exact timestamp not independently verified."
updated_at:
captured_at: 2026-06-12
captured_by: Codex
version_or_commit:
source_integrity:
  source_hash: 7F6A46484184196EAD61A06FF64A1C56A77C86885F4B6D9BB6B79C71F18617A8
  snapshot_hash: not_retained
  ingest_state: new
adapter_ingest:
  adapter_name: codex_web_article_capture
  adapter_version:
  capture_method: browser text extraction plus Invoke-WebRequest HTML hash; no full-text article copy retained because source has an explicit copyright notice.
  extraction_trace:
    - "https://yozm.wishket.com/magazine/detail/3792/"
    - "raw/articles/2026-06-12-yozm-obsidian-llm-wiki-second-brain-source/capture-notes.md"
  known_limits:
    - "No full article text or HTML snapshot is retained in this repo."
    - "Published date is inferred from the site's relative label at capture time."
    - "Korean source was distilled through reading and paraphrase; machine-readable full-text anchors are not stored locally."
    - "Tool/product details such as Claude Code hooks, Obsidian plugins, Working Copy, and GitHub token setup were not verified against official docs in this intake."
source_status: active_public_web_page_at_capture
raw_location: raw/articles/2026-06-12-yozm-obsidian-llm-wiki-second-brain-source/capture-notes.md
processing_mode: explicit_distillation
processing_level: medium
processing_tier: medium
knowledge_status: raw
overlay_state: project_sidecar_created
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
  - obsidian
  - llm-wiki
  - second-brain
  - claude-code
  - github-private-repo
  - source-intake
  - lint
  - query
  - sensitive-data
projects:
  - verified-action-knowledge-system
source_family:
  - article
  - personal-llm-wiki-case-study
  - obsidian-workflow
upstream_sources:
  - "Andrej Karpathy LLM Wiki idea"
verification_status: source-read-not-independently-verified
candidate_relation_suggestions:
  - target: "outputs/review/2026-06-12-yozm-obsidian-llm-wiki-second-brain-candidate-distillation.md"
    relation_type: derived_from
    relation_state: candidate
    why_suggested: "The article describes an Obsidian + GitHub + Claude Code LLM Wiki workflow that can inform VAKS source intake, operator commands, context entry, and safety boundaries."
    source_anchor: "raw/articles/2026-06-12-yozm-obsidian-llm-wiki-second-brain-source/capture-notes.md"
    evidence_support:
      span_supports_target: "paraphrase_only"
      evidence_role: "orientation"
      reviewer_note: "Use the public source URL for drilldown; local notes are not reviewed evidence."
    suggested_at: 2026-06-12
tags:
  - source-card
  - raw
  - article
  - obsidian
  - llm-wiki
  - claude-code
  - candidate-only
---

# 来源记录：Yozm Obsidian LLM Wiki Second Brain

## 为什么收录

这篇文章是一个个人 LLM Wiki 案例：作者把 Obsidian、GitHub Private Repo、Claude Code / CLI 和若干 Obsidian 工作流组合成自己的第二大脑。

它对 VAKS 的价值不在于证明某个架构正确，而在于给出了一组很具体的操作形状：

```text
multi-source capture
-> raw folder / wiki ingest
-> root operating manual
-> query over personal context
-> recurring lint
-> security and collaboration limitations
```

这些形状和 VAKS 的 Capture / Understand / Review / Connect / Act and Learn 很接近，但必须保持候选层和权威边界。

## 来源信息

- 作者：곰씨네 IT 블로그
- 发布方：요즘IT / Wishket
- 发布时间：2026-06-11（按 2026-06-12 捕获时页面显示 `1일 전` 推断）
- 更新时间：未验证
- 原始链接：https://yozm.wishket.com/magazine/detail/3792/
- 原始位置：公开网页
- retained local notes: `raw/articles/2026-06-12-yozm-obsidian-llm-wiki-second-brain-source/capture-notes.md`
- full HTML SHA256 at capture: `7F6A46484184196EAD61A06FF64A1C56A77C86885F4B6D9BB6B79C71F18617A8`
- source_status: active_public_web_page_at_capture
- 采集方式：浏览器正文读取 + HTML 哈希；不保留全文转载或 HTML 副本

## Intake Boundary

```yaml
processing_tier: medium
knowledge_status: raw
overlay_state: project_sidecar_created
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

Source record 只负责来源身份和可追溯性。它不能作为事实支持、行动依据、采用决定、工具版本证明或安全保证。

## 初步看点

- 作者的问题起点是多 AI 工具、多信息渠道带来的上下文重复解释和上下文不一致。
- 工具组合是 Obsidian 作为文件化 wiki / vault，GitHub Private Repo 作为备份和同步，Claude Code / CLI 作为 wiki 整理与问答工具。
- 核心运行面包括 root `CLAUDE.md`、SessionStart Hook、Obsidian 相关技能、`/ingest`、`/query`、`/lint`。
- 作者明确提到敏感信息、图片/OCR ingest 不准确、GitHub 私有仓库安全、个人/团队 wiki 难以统一等限制。
- 对 VAKS 来说，最值得借的是 operator command shape 和 lint/recovery/entry-manual 形状；最该避开的是全量个人数据直接进 AI、AI 直接改可信知识、full-vault query 默认化。

## 明显疑点

- 文章是个人经验分享，不是规范、论文、工具官方文档或可复现仓库。
- 文中的 Claude Code、Obsidian 插件、Working Copy、GitHub token 细节没有在本次 intake 中查官方文档。
- 页面只提供相对发布时间，本地记录中的发布日期是按捕获日期推断。
- 作者说的“一切上下文进 wiki”对 VAKS 来说会触发隐私、权限、source hygiene、authority bucket 混淆风险。
- `/query` 如果把整个 wiki 当作同一权威上下文，会和 VAKS 的 raw / candidate / overlay / reviewed 分层冲突。

## 可抽取 Candidate Points

- `context-fatigue-needs-durable-context`: AI 工具越多，越需要可复用的个人/项目上下文，而不是每次重新解释。
- `llm-wiki-operator-triad`: LLM Wiki 的最小操作面可以拆成 ingest、query、lint。
- `root-operating-manual-entrypoint`: root `CLAUDE.md` / AGENTS / handoff 类文件可以稳定新会话的操作边界。
- `session-start-context-injection-risk`: session hook 能改善一致性，也可能把过期或错误规则强制注入。
- `sensitive-data-quarantine-before-ingest`: 私密数据进库前需要隔离、扫描、人工复核，而不能只靠正则。
- `full-vault-query-authority-risk`: 全库问答有价值，但必须展示 raw / candidate / reviewed / overlay 权威桶。
- `lint-as-maintenance-not-truth`: 自动 lint 适合发现坏链、孤儿页、敏感信息和矛盾压力，但不能直接变成修复或真值更新。
- `personal-team-wiki-boundary`: 个人 wiki 和团队 wiki 的上下文共享存在天然边界，不能假装一个 SSOT 覆盖所有作用域。

## 当前处理等级

```text
medium
```

升级到 heavy 的条件：

- 用户要求把 `/ingest`、`/query`、`/lint` 或 SessionStart 类机制落成 VAKS 工具/脚本。
- 需要把 Obsidian + GitHub / Working Copy 作为正式同步方案比较对象。
- 该材料被用于 action basis、mainline 架构修改、自动化执行、或隐私/安全决策。

## 下一步

- 已写候选蒸馏：`outputs/review/2026-06-12-yozm-obsidian-llm-wiki-second-brain-candidate-distillation.md`
- 已写 VAKS 项目 overlay：`outputs/review/project_lens_overlays/2026-06-12-yozm-obsidian-llm-wiki-second-brain-overlay.md`
- 不创建 reviewed claim / pattern / decision。
