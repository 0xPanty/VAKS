---
record_kind: candidate_distillation
status: draft
provisional: true
title: "mdvs：VAKS Markdown frontmatter 校验与本地搜索侧车候选"
created_at: "2026-06-14"
created_by: Codex
knowledge_status: candidate
processing_tier: heavy
lifecycle_state: candidate_provisional
overlay_state: none
review_pressure: review_due
source_ref: "raw/repos/2026-06-14-edochi-mdvs-source.md"
derived_from:
  - "raw/repos/2026-06-14-edochi-mdvs-source.md"
  - "raw/repos/_snapshots/2026-06-14-edochi-mdvs-66ff5f3-source.zip"
  - "wiki/summaries/2026-06-14-edochi-mdvs-architecture-review.md"
  - "outputs/review/project_lens_overlays/2026-06-14-edochi-mdvs-vaks-validation-search-overlay.md"
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
  - frontmatter-validation
  - vault-lint
  - local-search
  - agent-post-write-check
possible_project_refs:
  - verified-action-knowledge-system
point_anchor_refs:
  - "raw/repos/2026-06-14-edochi-mdvs-source.md#Inspected Repository Areas"
  - "raw/repos/_snapshots/2026-06-14-edochi-mdvs-66ff5f3-source.zip:README.md"
  - "raw/repos/_snapshots/2026-06-14-edochi-mdvs-66ff5f3-source.zip:book/src/concepts/validation.md"
  - "raw/repos/_snapshots/2026-06-14-edochi-mdvs-66ff5f3-source.zip:book/src/recipes/ci.md"
  - "raw/repos/_snapshots/2026-06-14-edochi-mdvs-66ff5f3-source.zip:crates/mdvs/src/cmd/check/validate.rs"
  - "raw/repos/_snapshots/2026-06-14-edochi-mdvs-66ff5f3-source.zip:crates/mdvs/src/index/backend/search.rs"
borrow_value: strong
borrow_order:
  - "P1: frontmatter/schema drift lint for VAKS Markdown records"
  - "P2: local hybrid search with typed frontmatter filters as activation/cache sidecar"
  - "P3: agent-callable JSON command surface and skill packaging"
avoid:
  - "Do not treat mdvs check pass as reviewed knowledge or action readiness."
  - "Do not treat mdvs search rank/score as evidence support."
  - "Do not let mdvs.toml replace VAKS schema governance or enum registry."
  - "Do not commit `.mdvs/` as truth; it is rebuildable cache."
  - "Do not run auto-update on the formal vault in CI/action contexts."
dev_context_hint:
  default_layer: support_with_required_risk
  core_only_when: "the task is specifically about VAKS metadata lint, agent write validation, or local vault search/cache tooling"
  support_when: "designing validator pipelines, frontmatter contracts, retrieval receipts, or Markdown vault health checks"
  risk_when: "someone proposes valid frontmatter or search rank as truth, evidence support, review pass, or action basis"
  cold_references:
    - "raw/repos/2026-06-14-edochi-mdvs-source.md"
    - "raw/repos/_snapshots/2026-06-14-edochi-mdvs-66ff5f3-source.zip"
tags:
  - candidate
  - provisional
  - mdvs
  - markdown-vault
  - frontmatter-validation
  - local-search
  - candidate-only
---

# 候选蒸馏：mdvs

## 说人话

这个对 VAKS 有帮助，而且是很贴的那种。

但它不是帮我们“判断知识真不真”的工具。它适合做：

```text
Markdown vault 结构校验器
本地搜索/检索缓存
AI agent 写完文件后的字段漂移检查
```

一句话：

```text
mdvs 可以帮 VAKS 防止 Markdown metadata 写烂，也可以帮找东西；但不能替我们审核证据。
```

## 直接评分

| 维度 | 分数 | 判断 |
|---|---:|---|
| 帮 VAKS metadata / frontmatter 质量 | 9/10 | 非常贴，尤其适合 agent 写入后的漂移检查。 |
| 帮 VAKS retrieval / activation | 7/10 | 本地 hybrid search + SQL metadata filter 有用。 |
| 进入 VAKS 核心权威层 | 2/10 | 不应该进权威层，最多做侧车。 |
| 直接生产采用 | 5/10 | 设计好，但项目很新，需 sandbox；Windows 预构建未见。 |
| 设计借鉴价值 | 9/10 | `mdvs.toml` vs `.mdvs/` 的边界特别适合 VAKS。 |

## Candidate Point 1: mdvs is a lint sidecar for Markdown records

VAKS 有大量 Markdown 记录：

```text
raw/repos
raw/articles
raw/videos
outputs/review
outputs/feedback
wiki/claims
wiki/patterns
wiki/decisions
templates
```

这些文件的 frontmatter 很容易漂：

```text
字段拼错
布尔变字符串
required 字段漏掉
candidate / reviewed 状态混乱
path-scoped 字段跑错目录
agent 写出未注册 enum
```

mdvs 的 `check` 正好能作为一层结构检查：

```text
Markdown files
-> mdvs.toml field contract
-> mdvs check --no-update
-> deterministic violations
```

对 VAKS 的正确位置：

```text
lint / maintenance / preflight
```

不是：

```text
review pass
truth check
action readiness
```

## Candidate Point 2: `mdvs.toml` / `.mdvs/` split matches VAKS

mdvs 的设计有一个很好的边界：

```text
mdvs.toml = schema/config, commit to version control
.mdvs/ = search index, gitignore, rebuildable
```

这和 VAKS 完全同频：

```text
Markdown vault = source of truth
derived index/cache = acceleration, not authority
```

VAKS 可以借：

```text
contract file is visible and reviewable
index is rebuildable and disposable
build metadata records model/schema mismatch
search refuses incompatible model/index
```

不能借成：

```text
.mdvs/ is the new truth database
search hit is evidence
schema inference automatically rewrites VAKS schema
```

## Candidate Point 3: path-scoped field rules are useful

mdvs 会根据目录推断字段 allowed / required。

这对 VAKS 很有价值，因为不同目录本来就应该有不同 frontmatter：

| VAKS area | Example field pressure |
|---|---|
| `raw/**` | `knowledge_status: raw`, `action_basis_allowed: false` |
| `outputs/review/*candidate*` | `knowledge_status: candidate`, `promotion_gate` |
| `outputs/feedback/**` | `event_kind`, `review_pressure_effect`, no truth mutation |
| `wiki/claims/**` | reviewed-only fields and evidence links |
| `templates/**` | template markers, no accidental record promotion |

但是 VAKS 不能让自动 inference 直接决定规范。

更合理的做法：

```text
manual VAKS enum registry / templates stay authority
mdvs.toml becomes lint projection / companion contract
```

## Candidate Point 4: agent post-write check is the strongest use

README 里直接提到 LLM agents 维护知识库时可以用 `mdvs check` 防 drift。

这对 VAKS 很关键。

未来 agent 写入候选文件后，可以跑：

```text
mdvs check --no-update --output json
VAKS custom validators
git diff scoped check
sync hash check
```

这能挡住：

```text
字段错拼
unknown enum
status/action_basis 矛盾
目录字段跑偏
required metadata 漏掉
```

它挡不住：

```text
证据不支持结论
引用是假的
candidate 被当 truth
scope 过度外推
行动风险
```

所以它是 P0/P1 validator 的好搭档，不是替代品。

## Candidate Point 5: hybrid search is useful as activation, not support

mdvs search:

```text
semantic vector search
BM25 full-text search
RRF hybrid
SQL --where frontmatter filter
best chunk per file
line ranges
```

这对 VAKS 的检索非常好用，尤其是：

```text
找 candidate-only 材料
按 knowledge_status / project / tags / path filter
准备 context pack
找可能相关 source anchors
排查 metadata drift
```

但边界必须硬：

```text
search result = activation
search score = relevance signal
line range = candidate anchor to inspect
not support
not confidence
not review
not action basis
```

## Candidate Point 6: CI recipe is directly borrowable

mdvs docs 的 CI 建议很成熟：

```text
pin version
run mdvs check --no-update
fail on violations
do not auto-update schema in CI
```

这刚好补 VAKS 的工程纪律。

VAKS 最小借法：

```text
P1 sandbox:
  generate mdvs.toml from a copied vault slice
  manually tighten fields for raw/candidate/overlay/feedback
  run mdvs check --no-update
  compare with VAKS custom validator output
```

不要直接：

```text
mdvs init on formal vault and commit inferred schema blindly
```

## VAKS Fit

| VAKS layer | Fit | Borrow |
|---|---:|---|
| Capture / Provenance | Medium | Validate required raw source metadata. |
| Candidate Distillation | High | Catch candidate frontmatter drift and forbidden field mistakes. |
| Review Queue | Medium | Could preflight review objects structurally. |
| Reviewed Knowledge | Low | Only structural lint, no truth authority. |
| Activation / Dev Context | High | Hybrid search with frontmatter filters. |
| Context Pack | Medium | Finds candidate/context material; context pack still needs receipts. |
| Action Basis | No | mdvs output cannot support action. |
| Feedback | Medium | Validate feedback-event schema shape. |
| Agent Write Boundary | High | Post-write check and deterministic JSON output. |
| Productization | Medium | Local single-binary UX is attractive. |

## Borrow / Avoid

### Borrow

- `mdvs.toml` as visible field-contract sidecar.
- `.mdvs/` as rebuildable search cache.
- `check --no-update` for deterministic CI/lint.
- deterministic JSON output and exit codes.
- path-scoped allowed/required field rules.
- JSON Schema export/import interop.
- hybrid search + typed frontmatter SQL filters.

### Adapt

- Use VAKS enum registry and templates as authority; mdvs contract is generated/maintained projection.
- Keep mdvs search behind retrieval receipts if used for context preparation.
- Pair mdvs with VAKS validators for authority boundaries.
- Run on a sandbox copy first.

### Avoid

- Blind `mdvs init` on the formal vault and accepting inferred schema as truth.
- `check` auto-update in CI/action-facing flows.
- `.mdvs/` committed as source of truth.
- search score/rank as evidence support.
- valid frontmatter as review pass.
- replacing VAKS custom validators with mdvs alone.

## Open Questions

- Can mdvs handle VAKS frontmatter diversity without too many false positives?
- Should VAKS generate `mdvs.toml` from `tools/source_intake_enum_registry.json` and templates, rather than infer it?
- How well does search perform on Chinese-heavy notes and mixed English/Chinese metadata?
- Can it build on Windows from source even without a prebuilt release asset?
- Should it run only on canonical subsets first: `raw/**`, `outputs/review/*candidate*`, `outputs/feedback/**`?

## Routing Hint

Route this source to:

```text
metadata lint
source-intake validators
agent write boundary
retrieval/cache sidecar
operator cockpit / vault health
```

Do not route to:

```text
truth model
reviewed evidence
action readiness
schema authority replacement
```

## Bottom Line

mdvs 对我们很有帮助，但帮助点非常具体：

```text
它让 VAKS 的 Markdown 文件更像“可校验、可查询、可维护”的资料系统。
```

我们的版本必须比它更强的地方：

```text
mdvs validates fields and finds notes.
VAKS validates authority, evidence, review, sufficiency, and action boundaries.
```
