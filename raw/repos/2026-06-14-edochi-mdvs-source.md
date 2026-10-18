---
type: source
record_kind: source_card
status: source-captured
title: "mdvs - Markdown Validation & Search"
source_id: "repo:edochi/mdvs@66ff5f3cc43e1be7160eacd601ef96de6fa2d6f6"
source_uri: "github:edochi/mdvs@66ff5f3cc43e1be7160eacd601ef96de6fa2d6f6"
source_url: "https://github.com/edochi/mdvs"
source_type: repository
author: "edochi"
publisher: GitHub / crates.io
published_at: "2026-03-15T21:01:30Z"
updated_at: "2026-06-13T17:20:12Z"
captured_at: "2026-06-14"
captured_by: Codex
version_or_commit: "66ff5f3cc43e1be7160eacd601ef96de6fa2d6f6"
observed_version: "0.8.0"
source_integrity:
  source_hash: null
  snapshot_hash: "sha256:D035CE40F596C689ABBE985F57051E7A449B01DF1DAA958E35CAD9842D83BEB8"
  ingest_state: new
adapter_ingest:
  adapter_name: "manual-github-review"
  adapter_version: "2026-06-14"
  capture_method: "GitHub repo page, GitHub API, crates.io API, raw file reads, and commit zip snapshot"
  extraction_trace:
    - "git ls-remote HEAD"
    - "GitHub API repo metadata"
    - "GitHub release metadata"
    - "crates.io crate metadata"
    - "raw.githubusercontent.com README/docs/source inspection"
    - "GitHub commit zip snapshot"
  known_limits:
    - "Repository was inspected but not executed locally."
    - "No VAKS vault pilot was run."
    - "Search quality and schema inference were not benchmarked on the current vault."
    - "Prebuilt release assets inspected via metadata; Windows binary is not advertised in the release target list."
source_status: active
raw_location: "raw/repos/_snapshots/2026-06-14-edochi-mdvs-66ff5f3-source.zip"
processing_tier: heavy
knowledge_status: raw
overlay_state: none
review_pressure: review_due
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
why_saved: "User asked to distill edochi/mdvs and judge whether it helps VAKS."
topics:
  - markdown-validation
  - frontmatter-schema
  - local-search
  - hybrid-search
  - agent-write-check
  - vault-lint
projects:
  - verified-action-knowledge-system
source_family:
  - markdown-vault-tool
  - validation-cli
  - retrieval-cache
upstream_sources:
  - "https://github.com/edochi/mdvs"
  - "https://edochi.github.io/mdvs/"
  - "https://crates.io/crates/mdvs"
verification_status: source_identity_checked
candidate_relation_suggestions:
  - target: "outputs/review/2026-06-14-edochi-mdvs-candidate-distillation.md"
    relation_type: derived_from
    relation_state: candidate
    why_suggested: "Candidate distillation extracts VAKS validation/search-sidecar lessons from this repository."
    suggested_at: "2026-06-14"
tags:
  - source
  - repository
  - candidate-only
  - mdvs
  - markdown-vault
  - validation
  - search
---

# 来源记录：mdvs

## 为什么收录

用户给出：

```text
https://github.com/edochi/mdvs
```

并要求：

```text
这个也蒸馏 看看对我们有没有帮助
```

这个仓库直击 VAKS 的两个工程短板：

```text
1. Markdown frontmatter / source-intake metadata 会随着人工和 agent 写入发生漂移。
2. Markdown vault 需要可重建的本地检索缓存，但缓存不能变成权威来源。
```

## 来源信息

- 作者/组织：edochi
- 仓库：https://github.com/edochi/mdvs
- 文档：https://edochi.github.io/mdvs/
- crates.io：https://crates.io/crates/mdvs
- 语言：Rust
- License：MIT
- 当前上游 HEAD：`66ff5f3cc43e1be7160eacd601ef96de6fa2d6f6`
- commit 时间：`2026-06-07T22:02:09Z`
- commit message：`chore(version): v0.8.0`
- GitHub API metadata：stars `7`，forks `0`，open issues `0`
- crates.io observed version：`0.8.0`
- crates.io created：`2026-03-15T21:01:30Z`
- crates.io updated：`2026-06-07T22:02:11Z`
- latest GitHub release：`v0.8.0`，published `2026-06-07T22:27:58Z`
- release assets observed：macOS ARM and Linux x86_64 archives/installers; no Windows asset in inspected release metadata
- source snapshot：`raw/repos/_snapshots/2026-06-14-edochi-mdvs-66ff5f3-source.zip`
- snapshot SHA256：`D035CE40F596C689ABBE985F57051E7A449B01DF1DAA958E35CAD9842D83BEB8`

## Intake Boundary

```yaml
processing_tier: heavy
knowledge_status: raw
overlay_state: none
review_pressure: review_due
retrieval_policy:
  policy_kind: source_identity_only
  pack_allowed: drilldown_required
  action_basis_allowed: false
  warning_code: raw_is_provenance_only
promotion_gate: none
action_basis_allowed: false
truth_mutation_allowed: false
```

This source card is provenance only. It does not approve mdvs adoption, does not make mdvs search results evidence, and does not change VAKS schema.

## Inspected Repository Areas

| Anchor | What exists | Design extraction | Boundary |
|---|---|---|---|
| `README.md` | Defines mdvs as schema inference, frontmatter validation, and local semantic search for Markdown directories. | Strong match to VAKS Markdown vault lint and retrieval sidecar. | README claims are not local benchmark evidence. |
| `README.md` | Mentions Obsidian vaults, LLM-agent maintained knowledge bases, JSON output, deterministic exit codes. | Direct agent workflow relevance. | Agent-callable does not mean agent-authoritative. |
| `README.md` | Commands: `init`, `check`, `update`, `build`, `search`, `info`, `clean`, `export-jsonschema`, `skill`. | Clear command surface for future sandbox. | Do not run on formal vault without explicit pilot. |
| `Cargo.toml` | Rust workspace; crate version `0.8.0`; MIT; dependencies include LanceDB, Model2Vec, JSON Schema, gray_matter, text-splitter. | Single-binary local tool with validation/search separation. | Dependency/security posture not audited locally. |
| `book/src/introduction.md` | Describes Markdown directory as database, with `mdvs.toml` committed and `.mdvs/` rebuildable. | Strong fit to VAKS: Markdown remains truth, index is cache. | Database metaphor must not become authority metaphor. |
| `book/src/concepts/schema.md` | Directory-aware schema inference: types, allowed paths, required paths, nullability. | Useful for VAKS source-intake frontmatter drift detection. | Inferred schema is a lint input, not schema governance by itself. |
| `book/src/concepts/validation.md` | Seven violation kinds, deterministic output, read-only `check`. | Strong validator candidate for agent post-write checks. | Valid frontmatter does not mean valid knowledge. |
| `book/src/recipes/ci.md` | Recommends pinned version and `mdvs check --no-update` for deterministic CI. | Useful adoption discipline. | CI lint is process evidence only. |
| `book/src/recipes/obsidian.md` | Obsidian setup; `mdvs.toml` committed, `.mdvs/` gitignored, `.mdvsignore` for exclusions. | Strong VAKS operational fit. | Dataview inline fields are not scanned. |
| `book/src/concepts/search.md` and `search-modes.md` | LanceDB storage, BM25, vector, hybrid RRF, SQL `--where`, model mismatch hard error. | Good local retrieval sidecar design. | Search scores/ranks are activation only. |
| `crates/mdvs/src/cmd/check/validate.rs` | Four validation passes and sorted violation collection. | Source-code anchor for deterministic lint. | Not run locally. |
| `crates/mdvs/src/cmd/build/mod.rs` | Build validates before embedding, classifies changes, increments index. | Good pipeline order: lint before index. | Build artifacts must stay derived/rebuildable. |
| `crates/mdvs/src/cmd/search.rs` | Auto-build before search, `--where`, model mismatch handling. | Useful query tool shape. | Auto-build should be disabled in formal CI/action contexts until controlled. |
| `crates/mdvs/src/index/backend/search.rs` | Native vector/fulltext/hybrid search with field translation and best-chunk-per-file dedupe. | Useful retrieval/cache reference. | Retrieval output cannot be support. |
| `crates/mdvs/skills/mdvs/SKILL.md` | Bundled agent skill for commands and boundaries. | Agent tool UX reference. | Skill text does not replace VAKS local manuals. |
| `.github/workflows/ci.yml` and `audit.yml` | Build/test/clippy/fmt plus cargo-audit/cargo-deny. | Project maturity signal and security hygiene. | Passing upstream CI does not validate local VAKS fit. |

## 初步看点

mdvs is a compact tool for turning a Markdown directory into:

```text
validated frontmatter contract
local semantic / full-text / hybrid search index
agent-callable JSON command surface
```

For VAKS, the useful position is:

```text
Markdown vault = source of truth
mdvs.toml = optional lint/schema contract sidecar
.mdvs/ = derived search cache
mdvs check/search output = diagnostic/activation only
```

## 明显疑点

- Very young project and low public adoption signal.
- No Windows prebuilt artifact observed in release metadata.
- Search layer depends on local embedding and LanceDB; not yet tested on the VAKS vault.
- `mdvs init` inference could overfit to current messy files if used without manual tightening.
- `check` auto-update defaults are convenient locally but dangerous for CI unless `--no-update` is used.
- `search` auto-build is convenient but should not be allowed to mutate caches unexpectedly in action-facing flows.

## 可抽取 Candidate Points

1. mdvs is a strong reference for VAKS frontmatter/schema lint, especially agent post-write validation.
2. Its `mdvs.toml` / `.mdvs/` split matches VAKS: committed contract vs rebuildable cache.
3. Directory-aware field constraints could help VAKS keep `raw/`, `outputs/`, `wiki/`, and `templates/` metadata from drifting.
4. Hybrid search with SQL frontmatter filters is useful for activation and context-pack preparation.
5. The key risk is authority confusion: passing mdvs check or ranking high in mdvs search must never imply reviewed truth.

## 当前处理等级

```text
heavy source review, candidate only
```

升级到 sandbox 的条件：

- User asks to evaluate validation/search tools for VAKS.
- A limited copy of the vault is used, not the formal vault directly.
- `mdvs check --no-update` can run without modifying source files or schema unexpectedly.
- `.mdvs/` stays ignored/rebuildable and never becomes truth.

## 下一步

Read:

- `outputs/review/2026-06-14-edochi-mdvs-candidate-distillation.md`
- `wiki/summaries/2026-06-14-edochi-mdvs-architecture-review.md`
- `outputs/review/project_lens_overlays/2026-06-14-edochi-mdvs-vaks-validation-search-overlay.md`
