---
type: summary
status: draft
title: "mdvs architecture review for VAKS validation and search sidecar"
created: "2026-06-14"
library_name: "mdvs"
repo_url: "https://github.com/edochi/mdvs"
source_url: "raw/repos/2026-06-14-edochi-mdvs-source.md"
checked_commit: "66ff5f3cc43e1be7160eacd601ef96de6fa2d6f6"
commit_time: "2026-06-07T22:02:09Z"
source_status: active
reviewed_at: "2026-06-14"
domain: "Markdown validation / local search / vault lint"
related_projects:
  - verified-action-knowledge-system
current_branch: "source-intake validators / retrieval sidecar / agent write boundary"
extracted_patterns:
  - "frontmatter schema inference"
  - "path-scoped validation"
  - "rebuildable local search cache"
  - "agent-callable deterministic CLI"
fusion_decision: adapt-after-sandbox
inspection_confidence: medium
evidence_count: 16
cross_validated_with:
  - "tools/source_intake_enum_registry.json"
  - "tools/validate_source_intake_contract.py"
  - "outputs/review/vaks-architecture-upgrade-plan-2026-06-13.md"
negative_evidence:
  - "No local runtime test was run."
  - "Project is young and small by public adoption metrics."
  - "Windows prebuilt binary not observed in release assets."
  - "Schema inference can overfit current messy files if trusted blindly."
extension_potential: "High as a validation/search sidecar; low as a truth authority."
knowledge_status: candidate
action_basis_allowed: false
truth_mutation_allowed: false
tags:
  - summary
  - architecture-review
  - mdvs
  - validation
  - local-search
  - candidate-only
---

# mdvs 架构评审：VAKS validation/search sidecar 候选

## 一句话判断

mdvs 是 VAKS 目前见过的外部工具里，最贴近“Markdown vault 工程纪律”的一个。

正确吸收方式：

```text
Use mdvs as structure/search sidecar.
Do not let mdvs become truth, review, or action basis.
```

## 它解决什么问题

mdvs 解决的是 Markdown 目录的两个问题：

```text
frontmatter metadata 不一致
本地文件难以按语义 + metadata 组合查询
```

它做了：

```text
schema inference
frontmatter validation
JSON Schema interop
incremental local search index
semantic / BM25 / hybrid search
SQL where filtering on frontmatter
agent-friendly JSON output and exit codes
```

这与 VAKS 的工程短板重合：

```text
agent 写文件后要防 metadata drift
candidate/raw/overlay/feedback 要有结构边界
retrieval/cache 要可重建且不能变成权威
```

## 核心设计

The architecture has two clear layers:

```text
Validation layer:
  scan markdown
  infer/read mdvs.toml
  validate frontmatter
  output deterministic violations

Search layer:
  chunk markdown body
  embed with local Model2Vec model
  store chunks + metadata in LanceDB under .mdvs/
  search by semantic / fulltext / hybrid with SQL filters
```

The key boundary:

```text
mdvs.toml = committed contract
.mdvs/ = derived cache
```

That is exactly the kind of split VAKS wants.

## Source / Code Anchors

| Anchor | What exists | Design extraction | Boundary |
|---|---|---|---|
| `README.md` | mdvs positions itself as in-process validation/search for Markdown documents. | Confirms broad fit. | Not local proof. |
| `README.md` | Obsidian vaults and LLM-agent maintained knowledge bases are named use cases. | Strong active-project relevance. | Use-case claim is not adoption decision. |
| `README.md` | Hybrid search, JSON Schema interop, local single binary, incremental builds, JSON output, deterministic exit codes. | Strong command surface for sandbox. | Search/validation are still diagnostics. |
| `Cargo.toml` | Rust crate `mdvs` v0.8.0, MIT; dependencies include LanceDB, Model2Vec, jsonschema, text-splitter, gray_matter. | Runtime and dependency map. | No local build/test. |
| `Cargo.toml` | dist targets include ARM macOS and Linux x86_64; Windows target commented out. | Windows friction. | Source build may still work but was not tested. |
| `book/src/introduction.md` | Markdown directory as database; `mdvs.toml` committed and `.mdvs/` ignored/rebuildable. | Excellent VAKS boundary pattern. | Database metaphor must be downgraded to cache/sidecar. |
| `book/src/concepts/schema.md` | Types, path patterns, nullability; allowed/required globs inferred from directories. | Useful for path-scoped VAKS record families. | Do not auto-infer VAKS authority schema. |
| `book/src/concepts/validation.md` | Seven violation types and byte-stable sorted output. | Good validator behavior. | Structural pass only. |
| `book/src/commands/check.md` | `check --no-update`, `--jsonschema`, read-only validation, exit codes 0/1/2. | Strong CI/agent preflight candidate. | New fields informational unless policy wraps them. |
| `book/src/commands/build.md` | Build validates before embedding; schema/model changes require force. | Good "lint before cache" discipline. | Build can mutate `.mdvs/`; keep derived. |
| `book/src/commands/search.md` | Query with modes, limit, where, no-update, no-build. | Retrieval receipt candidate. | Rank/score not support. |
| `book/src/recipes/ci.md` | Pin version and use `--no-update` for deterministic CI. | Direct VAKS borrow. | Do not use latest installer in CI. |
| `book/src/recipes/obsidian.md` | Obsidian setup, `.mdvsignore`, Dataview limitation. | Good vault hygiene notes. | Dataview inline fields not scanned. |
| `crates/mdvs/src/cmd/check/validate.rs` | Four-pass validation over frontmatter errors, field values, required fields, sorted collection. | Robust lint internals. | Not benchmarked. |
| `crates/mdvs/src/cmd/build/mod.rs` | Validate, classify, embed, write. | Good pipeline sequencing. | Embedding cache is not authority. |
| `crates/mdvs/src/index/backend/search.rs` | Vector/BM25/hybrid dispatch, SQL field translation, chunk-to-file dedupe. | Good local retrieval reference. | Search is activation only. |
| `.github/workflows/ci.yml` / `audit.yml` | Build/test/clippy/fmt/audit/deny. | Maintenance maturity signal. | Upstream CI is not VAKS validation. |

## 当前支线价值

Current local concern:

```text
source-intake validators
retrieval receipts
agent/plugin write boundary
vault health
```

mdvs supports:

- Source Intake metadata structure lint.
- Candidate/overlay/feedback frontmatter drift detection.
- Agent post-write checks.
- Local activation search with metadata filters.
- Rebuildable retrieval cache discipline.

Risks:

- Inferred schema can normalize existing mess instead of enforcing intended design.
- Search rank can be misread as support.
- Auto-update can silently admit schema drift.
- `.mdvs/` can be mistaken for a database truth source.

## 全貌架构价值

| Architecture Zone | Value / Finding | Adopt? |
|---|---|---|
| Karpathy spine | Strong fit: Markdown remains source-of-truth; index/cache is derived. | adapt |
| Dusk workbench | Could feed vault health and review dashboards. | adapt |
| source ingest | Good frontmatter contract/lint sidecar. | adapt |
| review queue | Can preflight structural fields, not review content. | adapt |
| schema / reviewed knowledge | No truth authority. | reject as authority |
| memory / dev context | Useful filtered search for support/cold references. | adapt |
| feedback | Can validate feedback-event metadata shape. | adapt |
| retrieval / cache | Strong local hybrid search/cache candidate. | adapt |
| API / MCP / agent access | CLI JSON output and deterministic exit codes are agent-friendly. | adapt |
| viewer / workbench | Could power status tables or operator cockpit inputs. | watch |
| publishing | Could lint docs-as-code frontmatter. | watch |
| risk / anti-pattern | Main risk is metadata/search becoming authority. | adopt guardrail |

## 值得提炼的模式

### 1. Visible contract, disposable cache

```text
mdvs.toml committed
.mdvs/ ignored
```

VAKS version:

```text
VAKS templates / enum registry / mdvs.toml projection are visible.
Derived search indexes are rebuildable and disposable.
```

### 2. Validate before embedding

Build runs validation before index work.

VAKS should use this pattern:

```text
frontmatter/enum check
-> VAKS authority-boundary validators
-> derived retrieval/cache build
```

### 3. Deterministic lint for agent writes

The JSON output and exit codes are very suitable for agent pipelines:

```text
0 success
1 violations
2 tool/config error
```

### 4. Metadata-filtered retrieval

Hybrid search + `--where` can reduce retrieval pollution:

```text
search query
where knowledge_status = 'candidate'
where action_basis_allowed = false
where project = 'verified-action-knowledge-system'
```

But it remains retrieval.

## 标签与量化

- domain: Markdown validation / local search
- problem: Markdown vault metadata drift and weak local retrieval
- pattern: validation/search sidecar
- maturity: emerging
- complexity: medium
- problem_fit: 5/5
- reuse_value: 5/5
- implementation_cost: 3/5
- integration_fit: 4/5 as sandbox sidecar
- evidence_strength: 3/5 for design fit, 1/5 for local runtime
- reversibility: 5/5 if `.mdvs/` remains rebuildable cache

## Knowledge Calibration / Point Collision

| Candidate Point | Local Reviewed / Candidate Knowledge | Calibration Output | Review Question |
|---|---|---|---|
| Markdown files can be linted as typed records. | SOURCE_INTAKE already has enum registry and validators. | refines | Should mdvs.toml be generated from VAKS registry/templates or hand-maintained? |
| Local hybrid search can help activation. | Retrieval score/rank is not support. | candidate_relation with risk | Can retrieval receipts mark mdvs hits as activation only? |
| Agent post-write check should be deterministic. | Agent write quarantine forbids direct truth mutation. | supports as process pattern | Should every future write tool run mdvs + VAKS validators? |
| `.mdvs/` is rebuildable cache. | VAKS treats derived indexes/caches as non-authority. | aligns | Can lint prevent `.mdvs/` from entering source/review scope? |

## Support / Challenge Review

What supports it:

- Official docs match VAKS Markdown vault use case directly.
- Source code separates validation and search layers.
- Command interface supports JSON output and deterministic exit codes.
- Local VAKS already has Source Intake enum/validator direction.

What challenges it:

- No local pilot yet.
- Young repo and low adoption metrics.
- No Windows prebuilt observed.
- mdvs validates frontmatter only, not body semantics/evidence.

Challenge severity:

```text
minor for design borrowing
major for immediate dependency adoption
```

Scope limits:

```text
Use as lint/search sidecar candidate.
Do not use as truth/review/action authority.
```

Action readiness:

```text
not_ready
```

## 可拓展性

- 是否适合作为插件/适配层：yes, as CLI sidecar.
- 是否会绑定核心结构：should not; keep VAKS templates and registry as authority.
- 未来替换成本：low if only outputs reports/search receipts.
- 可迁移路径：run on sandbox copy, compare with current validators, then decide whether to generate a VAKS-specific `mdvs.toml`.

## 复杂度和风险

- Medium runtime complexity on Windows because no prebuilt asset was observed.
- Low conceptual complexity.
- Medium false-positive/false-negative risk if inference is trusted blindly.
- High authority-confusion risk if search/lint output is treated as review.

## 不可行点 / 避坑

- Do not replace `tools/source_intake_enum_registry.json`.
- Do not replace VAKS custom validators.
- Do not run auto-update in CI/action mode.
- Do not let inferred fields decide allowed architecture.
- Do not use search scores as support/confidence.
- Do not commit `.mdvs/`.

## 融合判断

- 结论：adapt-after-sandbox.
- 理由：The design fits VAKS strongly, but local runtime and vault-noise behavior must be tested.
- 验证方式：sandbox copy of selected VAKS directories, strict `--no-update`, compare against VAKS validators.

## 直接判断

- Direct use: not yet on formal vault.
- Fork: no.
- Design-only: yes, strong.
- Sandbox: yes, recommended.
- Reject: reject only truth/review/action use.
- Current branch value: strong.
- Whole architecture value: high for validation/cache discipline.
- Risk: search/lint authority confusion.
- Next action: add to architecture plan as validation/search sidecar candidate and run a small sandbox only when requested.

## 后续行动

Possible future sandbox:

```text
P1.5-MDVS: Markdown Validation/Search Sidecar Sandbox
```

It should run on a copied subset first:

```text
raw/repos/*.md
outputs/review/*candidate-distillation.md
outputs/feedback/*.md
templates/*.md
```

and require:

```text
no source mutation
no truth mutation
no action basis
no committed .mdvs/
manual review of inferred mdvs.toml before any reuse
```
