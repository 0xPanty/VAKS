---
record_kind: candidate_distillation
status: candidate
provisional: true
knowledge_status: candidate
processing_tier: medium
lifecycle_state: candidate_provisional
overlay_state: none
review_pressure: none
derived_from:
  - raw/repos/2026-06-07-linkwarden-linkwarden-source.md
retrieval_policy:
  policy_kind: orientation_only
  pack_allowed: activation_only
  action_basis_allowed: false
  warning_code: candidate_not_action_basis
promotion_gate: v0_2_13_required
action_basis_allowed: false
truth_mutation_allowed: false
v0_2_13_trigger: no
routing_hint:
  - source-intake
  - source-preservation
  - activation-workbench
  - retrieval-cache
  - source-hygiene
possible_project_refs:
  - verified-action-knowledge-system
point_anchor_refs:
  - snapshot_ref: raw/repos/_snapshots/linkwarden-linkwarden-22723575b04503eb67c9733c63d55179c069903d.zip
    selector_type: source_code
    selector_value: README.md:30-66
  - snapshot_ref: raw/repos/_snapshots/linkwarden-linkwarden-22723575b04503eb67c9733c63d55179c069903d.zip
    selector_type: source_code
    selector_value: apps/worker/lib/archiveHandler.ts:32-229
  - snapshot_ref: raw/repos/_snapshots/linkwarden-linkwarden-22723575b04503eb67c9733c63d55179c069903d.zip
    selector_type: source_code
    selector_value: packages/prisma/schema.prisma:52-218
  - snapshot_ref: raw/repos/_snapshots/linkwarden-linkwarden-22723575b04503eb67c9733c63d55179c069903d.zip
    selector_type: source_code
    selector_value: packages/lib/ssrf.ts:22-251
borrow_value: strong
borrow_order:
  - "P1: link-rot-aware source preservation bundle with explicit unavailable states"
  - "P1: safe arbitrary URL capture guardrails before any preservation worker"
  - "P1: tag-driven source processing policy, but only as routing/control metadata"
  - "P2: derived retrieval cache with access filters and index invalidation"
  - "P2: reader highlights and annotations as review input / use ledger hints"
  - "P3: API/mobile/public-share/collaboration surface for later viewer work"
avoid:
  - "Do not treat AI tags, bookmark tags, search hits, or collection membership as reviewed classification."
  - "Do not treat preserved screenshot/PDF/readability/monolith as evidence support without source-span review."
  - "Do not fork or reuse code directly without AGPL-3.0 and security review."
  - "Do not add a full bookmark product to VAKS core before source-intake needs are proven."
dev_context_hint:
  default_layer: support_with_required_risk
  core_only_when: "approved VAKS task implements web/source capture, URL preservation, source adapter import, or retrieval workbench."
  support_when: "designing source intake, link rot mitigation, tag routing, derived search cache, reader annotation, or source workbench UX."
  risk_when: "arbitrary URL fetching, SSRF, private network access, LLM auto-tag authority confusion, or preserved-copy-as-evidence confusion."
  cold_references:
    - raw/repos/2026-06-07-linkwarden-linkwarden-source.md
    - raw/repos/_snapshots/linkwarden-linkwarden-22723575b04503eb67c9733c63d55179c069903d.zip
tags:
  - candidate
  - provisional
  - linkwarden
  - source-intake
  - source-preservation
  - web-archive
  - bookmark-manager
  - activation-workbench
  - retrieval-cache
  - ssrf-protection
  - ai-tags-are-candidate
  - candidate-only
---

# Linkwarden Candidate Distillation

## Boundary

This note is provisional orientation.

It can help route attention, compare ideas, or suggest project overlays. It is not reviewed knowledge, not a decision, not a formal pattern, and not action basis.

## Source

```yaml
derived_from:
  - raw/repos/2026-06-07-linkwarden-linkwarden-source.md
checked_commit: 22723575b04503eb67c9733c63d55179c069903d
snapshot: raw/repos/_snapshots/linkwarden-linkwarden-22723575b04503eb67c9733c63d55179c069903d.zip
snapshot_sha256: 0E1DD467D1CDC4CF0E31E154605AEDE234EE02A58DD6502C9C23D31A36D63F40
```

## 人话压缩

Linkwarden 对 VAKS 有帮助，但帮助点很窄也很实用：

```text
它不是知识真值系统。
它是“网页资料怎么收、怎么保存副本、怎么标记、怎么检索、怎么避免链接烂掉”的工程样本。
```

VAKS 可以借它三件事：

```text
1. URL 不是资料本身，保存副本和可回钻 artifact 很重要。
2. tag 可以控制处理策略，但 tag 不能变成真值或 reviewed relation。
3. 搜索/索引/cache 是派生层，要能重建、能失效、能受权限过滤。
```

## Candidate Points

### 1. `link-rot-aware-source-preservation-bundle`

候选结论：VAKS 的网页 source intake 不应只保存 URL。对高价值网页，至少应保留可见、可回钻的原文/可读文本/快照/元数据 bundle，并记录哪些格式成功、失败或 unavailable。

锚点：

- `README.md:30-36`
- `README.md:43-66`
- `apps/worker/lib/archiveHandler.ts:117-194`
- `apps/worker/lib/archiveHandler.ts:208-229`
- `apps/worker/lib/preservationScheme/handleReadability.ts:1-57`

对 VAKS 的适配：

- 轻入口仍可只存 URL + source card。
- 强蒸馏 / 高价值来源 / action 相关来源，应保留 repo-visible 或 vault-visible raw artifact。
- preserved artifact 应进入 raw/source 层，不直接变成 reviewed claim。

边界：

```text
URL = provenance
preserved copy = source material
readability text = extracted source text / index material
candidate point = review input
reviewed knowledge = later evidence-aware review
```

### 2. `tag-driven-source-processing-policy`

候选结论：Linkwarden 的 tag 可以带 archiveAsScreenshot / archiveAsPDF / archiveAsReadable / Wayback / aiTag 这类处理策略。VAKS 可以借这个思想，把一些 tag 用作 processing policy 或 routing hint。

锚点：

- `apps/worker/lib/archiveHandler.ts:85-107`
- `packages/prisma/schema.prisma:200-218`

对 VAKS 的适配：

- tag 可以标记 `needs_snapshot`、`public_source`、`private_do_not_fetch`、`candidate_only`、`requires_review`、`external_reference`。
- tag 应该进入 retrieval/routing/workflow，不进入 truth confidence。
- tag-driven policy 必须可解释、可撤销，不做隐形自动晋级。

边界：

```text
tag routes work
tag does not prove truth
tag does not create reviewed relation
tag does not replace source anchor
```

### 3. `safe-arbitrary-url-capture-guardrail`

候选结论：网页采集不是普通 fetch。Linkwarden 对 hostname、IP CIDR、DNS lookup、redirect、Playwright 子请求都做了安全检查。这对 VAKS 未来网页采集是高价值风险样本。

锚点：

- `packages/lib/ssrf.ts:22-58`
- `packages/lib/ssrf.ts:193-251`
- `packages/lib/safeFetch.ts:16-91`
- `apps/worker/lib/protectPageRequests.ts:1-32`
- `apps/worker/lib/archiveHandler.ts:32-41`

对 VAKS 的适配：

- 任何自动 URL capture 都必须先明确 public-only、no private cookies、no local network、no internal IP。
- redirect 后仍要重跑安全检查。
- 浏览器页面内子请求也要拦截。
- 如果未来使用用户浏览器/账号态，需要另开显式授权路径。

边界：

```text
SSRF guardrail != full security proof
public fetch != private browsing
safe URL != reliable source
```

### 4. `derived-retrieval-cache-with-access-filters`

候选结论：Linkwarden 将 link 数据投喂到 Meilisearch，保留 owner/member/public/tag/date 等 filterable attributes，并用 `indexVersion` 控制重建。VAKS 可借这个作为 derived retrieval cache 参考。

锚点：

- `docker-compose.yml:1-23`
- `apps/worker/workers/linkIndexing.ts:23-37`
- `apps/worker/workers/linkIndexing.ts:73-145`
- `apps/web/lib/api/controllers/search/searchLinks.ts:54-153`
- `apps/web/lib/api/searchQueryBuilder.ts:7-104`

对 VAKS 的适配：

- FTS/vector/search index 应是从 Markdown/raw artifacts 派生出来的缓存。
- 检索层必须带 authority bucket、project scope、private/public、candidate/reviewed filter。
- index freshness / indexVersion 是运维字段，不是 truth 字段。

边界：

```text
search result != support
rank != trust
filter match != scope fit
derived cache can be rebuilt from source files
```

### 5. `annotation-as-review-input-not-evidence`

候选结论：Reader highlight / comment / annotation 可以让人对 source span 做操作。VAKS 可以借这个作为 review input 的工作台形态，但不能让高亮本身成为 evidence support。

锚点：

- `README.md:43-44`
- `packages/prisma/schema.prisma:260-272`
- `apps/web/lib/api/controllers/highlights/postOrUpdateHighlight.ts:8-64`

对 VAKS 的适配：

- 用户高亮可以成为 `candidate_extraction_hint`、`review_question`、`support_span_candidate`。
- review 时必须再判断该 span 是否真的支持 point。
- comment 可以记录 reviewer note，但不是自动 review pass。

边界：

```text
highlight = attention marker
comment = reviewer note / candidate clue
evidence support = later reviewed judgment
```

### 6. `ai-tags-are-routing-candidates`

候选结论：Linkwarden 的 auto tag 使用 meta description 或 readable text，再根据 generate / existing / predefined 三种模式给链接打 tag，并限制输出数量。VAKS 可以借这个“AI 只做候选路由”的形状。

锚点：

- `apps/worker/workers/autoTagPreservedLinks.ts:1-70`
- `apps/worker/lib/autoTagLink.ts:69-157`
- `packages/prisma/schema.prisma:52-88`

对 VAKS 的适配：

- AI tag 可以建议 source family / routing hint / project overlay suggestion。
- 对高影响 entity、repo name、version、claim 类型，仍要 key-entity check。
- AI tag 不应成为 reviewed taxonomy 或 relation。

边界：

```text
AI tag = candidate routing
existing tag match = vocabulary constraint
predefined tag = user preference
none of these = truth
```

### 7. `import-export-source-adapter-family`

候选结论：Linkwarden 有 HTML bookmark import、Pocket/Omnivore/Wallabag import、exportData。这提醒 VAKS 的 source adapter 应是一族接口，而不是每种外部来源都硬塞进一个模板。

锚点：

- `apps/web/lib/api/controllers/migration/importFromHTMLFile.ts:8-211`
- `apps/web/lib/api/controllers/migration/exportData.ts:3-30`
- `README.md:54-65`

对 VAKS 的适配：

- Article / repo / paper / video / bookmark / RSS / single-file HTML 可以共用 source adapter contract。
- 导入时保留 source identity、raw artifact、processing tier、candidate distillation。
- export 默认不应把 heavy preserved binaries 混成同一份轻导出。

边界：

```text
imported bookmark != preserved source
exported summary != full source package
adapter success != review success
```

### 8. `collaboration-permission-is-not-review-permission`

候选结论：Linkwarden 的 collection/member/canCreate/canUpdate/canDelete 是协作权限模型。VAKS 可借作 viewer/workbench 权限参考，但它不能替代 reviewer authority。

锚点：

- `README.md:47-50`
- `packages/prisma/schema.prisma:126-164`
- `apps/web/lib/api/verifyUser.ts:14-64`

对 VAKS 的适配：

- 未来多人 VAKS viewer 可区分 read/comment/candidate-write/review-promote。
- 协作编辑权限和 review promotion 权限必须分开。
- Public share 是 output surface，不是 authority surface。

边界：

```text
canUpdate != canReview
public != verified
team collaboration != evidence-aware review
```

## 标签与梯度

```yaml
borrow_value: strong
strong_fit_tags:
  - source-intake
  - source-preservation
  - web-archive
  - link-rot
  - tag-routing
  - source-hygiene
  - derived-retrieval-cache
  - activation-workbench
medium_fit_tags:
  - reader-annotation
  - import-export-adapter
  - collaboration-permission
  - public-share-output
risk_tags:
  - ai-tags-are-candidate
  - preserved-copy-is-not-support
  - search-rank-is-not-trust
  - agpl-direct-reuse-risk
  - arbitrary-url-capture-risk
```

## Open Questions

- VAKS 未来网页 intake 是否需要一条 `web-source` source card runner，类似视频 intake runner？
- 哪些网页 source 应只存 URL，哪些必须保存 raw artifact？
- tag-driven processing policy 应写进 `SOURCE_INTAKE.md`，还是先作为 project overlay / candidate trial？
- 如果要保存网页副本，如何处理版权、登录态、动态页面、隐私和 robots 边界？
- Meilisearch/FTS 是否只作为 derived cache，还是先继续 Markdown + rg + Obsidian search？

## Routing Hint

- Source Intake: strong support, especially link rot and raw artifact retention.
- Activation / Dev Context: medium support, especially collections/tags/dashboard as scoped activation.
- Retrieval cache: medium support, useful when VAKS moves beyond file-first search.
- Feedback / Review workbench: medium support through highlights/annotations.
- Truth layer: no direct value; avoid authority confusion.
- Action basis: not allowed without future reviewed evidence packet.

## Forbidden

```text
project_borrow_scope in this note
decision outcome
formal pattern
action basis
truth confidence
```
