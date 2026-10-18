---
record_kind: project_overlay
status: candidate
knowledge_status: candidate
processing_tier: medium
overlay_state: confirmed
overlay_scope: project_sidecar_only
overlay_storage: confirmed_persistent_project_bucket
retrieval_scope: active_project_only
default_retrieval: false
retrieval_policy:
  policy_kind: project_context_only
  default_scope: project_only
  pack_allowed: activation_only
  action_basis_allowed: false
  warning_code: overlay_not_authority
promotion_gate: v0_2_13_required
action_basis_allowed: false
truth_mutation_allowed: false
project_id: verified-action-knowledge-system
target_ref: raw/repos/2026-06-07-linkwarden-linkwarden-source.md
target_selector: checked_commit:22723575b04503eb67c9733c63d55179c069903d
target_hint: "Use as a VAKS source-intake and source-preservation reference, not as truth architecture."
tagging_decision: tagged
tag_level: strong-borrow
tag_level_reason: "Strong fit with VAKS source intake, source preservation, URL safety, tag routing, and derived retrieval-cache boundaries; kept candidate-only because runtime/security/licensing review was not performed."
project_borrow_scope:
  - web source preservation bundle for high-value URL sources
  - tag-driven processing policy as candidate routing metadata
  - arbitrary URL safety guardrails before preservation
  - derived retrieval cache with access and authority filters
  - reader highlight / annotation as review input only
project_non_borrow_scope:
  - full bookmark manager product in VAKS core
  - AI tags as reviewed taxonomy or truth labels
  - search rank or collection membership as evidence support
  - public share as publishing approval
  - direct AGPL code reuse without review
project_reopen_trigger:
  - "VAKS starts a web-source intake runner or webpage preservation trial."
  - "VAKS adds a derived retrieval index beyond file-first rg/Obsidian search."
  - "VAKS builds a reader/review annotation workbench."
confirmation_basis:
  - user explicitly requested strong distillation and tagging
  - source card, snapshot, candidate distillation, and architecture review created
  - source/code anchors inspected from checked repository snapshot
  - no runtime execution; no promotion to reviewed knowledge
last_checked_at: 2026-06-07
expires_at: 2026-07-07
borrow_value: strong
borrow_order:
  - "P1: source preservation bundle and unavailable-state tracking"
  - "P1: URL safety guardrails for public web capture"
  - "P1: tag-driven processing policy, strictly candidate/routing only"
  - "P2: derived search/index cache with access filters"
  - "P2: reader highlight and annotation as review input"
  - "P3: collaboration/API/public share as later viewer/workbench reference"
avoid:
  - "Do not make tags, AI tags, search hits, or public collections into reviewed knowledge."
  - "Do not treat preserved page formats as action-ready evidence without later evidence support review."
  - "Do not copy code directly before AGPL/security review."
tags:
  - VAKS
  - project-overlay
  - linkwarden
  - strong-borrow
  - source-intake
  - source-preservation
  - web-archive
  - tag-routing
  - derived-retrieval-cache
  - ssrf-protection
  - activation-workbench
  - ai-tags-are-candidate
  - candidate-only
---

# VAKS Project Overlay：Linkwarden

## Boundary

This is a project-scoped sidecar.

It does not rewrite the source card, candidate distillation, reviewed note, decision, or pattern.

It can guide the active project, but it cannot act as reviewed knowledge or action basis.

## Target

```yaml
target_ref: raw/repos/2026-06-07-linkwarden-linkwarden-source.md
target_selector: checked_commit:22723575b04503eb67c9733c63d55179c069903d
target_hint: source-intake / source-preservation / web-archive / activation-workbench
```

## 标签等级

```yaml
tagging_decision: tagged
tag_level: strong-borrow
borrow_value: strong
borrow_order_primary: P1
```

人话：

```text
有帮助，打 strong-borrow。
它是 P1，但强在 source intake / source preservation / URL safety，不是 truth layer。
```

## Project Borrow Scope

VAKS 当前值得借：

1. **网页资料保存副本**：高价值 URL 不能只留链接，至少要有可回钻 raw/preserved artifact。
2. **保存状态可见**：成功、失败、unavailable、index invalidated 要落在 source/status 层。
3. **tag 作为处理策略**：tag 可以提示是否需要 snapshot、readability、Wayback、AI tag、review_due，但只当 routing。
4. **任意 URL 安全门**：public-only、SSRF、redirect、browser subrequest 都要先有边界。
5. **派生检索缓存**：search/Meili/FTS/vector 都是 derived retrieval cache，必须能被 authority/knowledge_status/project scope 过滤。
6. **高亮/批注**：可作为 review input 或 support-span candidate，不是 evidence support 本身。

## Project Non-Borrow Scope

VAKS 当前不要误借：

- 不要把 VAKS 做成完整 Linkwarden / bookmark SaaS。
- 不要把 AI tags 当成 reviewed taxonomy。
- 不要把 collection/tag/search rank 当成 reviewed relation。
- 不要把 preserved screenshot/PDF/readability 当成自动 action basis。
- 不要默认抓私有网页、登录态内容、会员内容或本地网络。
- 不要直接复用 AGPL-3.0 代码，除非未来做过法律和架构审查。

## Reopen Trigger

重新打开这条 overlay 的条件：

- 用户要做 VAKS 的网页 source intake runner。
- 用户要把外部网页/文章强蒸馏流程从 pasted text 升级为 URL capture。
- VAKS 要做 derived search index 或 viewer/workbench。
- VAKS 需要判断 preserved webpage 是否足够进入 Evidence Packet / action basis。

## Confirmation

```yaml
confirmation_basis:
  - user_requested: "强蒸馏 并且打标签"
  - checked_commit: 22723575b04503eb67c9733c63d55179c069903d
  - artifact_paths:
      - raw/repos/2026-06-07-linkwarden-linkwarden-source.md
      - outputs/review/2026-06-07-linkwarden-linkwarden-candidate-distillation.md
      - wiki/summaries/2026-06-07-linkwarden-linkwarden-architecture-review.md
      - raw/repos/_snapshots/linkwarden-linkwarden-22723575b04503eb67c9733c63d55179c069903d.zip
  - runtime_executed: false
last_checked_at: 2026-06-07
expires_at: 2026-07-07
```

## 人话结论

有帮助，打 `strong-borrow`，但强在 **source intake / source preservation**，不是强在 truth layer。

最值得放在 VAKS 心里的是：

```text
链接会烂，所以重要网页要留副本。
标签可以帮忙分流，但标签不是证据。
检索可以帮忙找到东西，但检索不是审查。
网页抓取要先过安全门。
```

## Forbidden

```text
decision outcome
review verdict
truth confidence
action basis
universal ban
```
