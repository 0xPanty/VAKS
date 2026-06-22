---
type: source
record_kind: source_card
status: source-captured
title: "breferrari/obsidian-mind"
source_id: "github:breferrari/obsidian-mind@9ae6860d01c4bb563dfe972dae89515866f4fbff"
source_uri: "github:breferrari/obsidian-mind@9ae6860d01c4bb563dfe972dae89515866f4fbff"
source_url: "https://github.com/breferrari/obsidian-mind"
source_type: repository
owner: breferrari
repo: obsidian-mind
author: "Brenno Ferrari / GitHub contributors"
publisher: GitHub
created_at_source: "2026-02-28T21:41:41Z"
updated_at_source: "2026-06-11T21:23:27Z"
pushed_at_source: "2026-06-02T00:26:30Z"
captured_at: "2026-06-12T05:31:19+08:00"
captured_by: Codex
version_or_commit: "9ae6860d01c4bb563dfe972dae89515866f4fbff"
release_or_version: "v6.2.1"
commit_time: "2026-06-02T00:26:28Z"
default_branch: main
license: MIT
source_status: active
source_metadata_quality: direct_github_api_plus_git_clone
source_integrity:
  source_hash: "git-commit:9ae6860d01c4bb563dfe972dae89515866f4fbff"
  snapshot_hash: "sha256:84797493e33e30550ba053d069c42543f7945fd7d4e202cfecb46a9c4bfedd82"
  ingest_state: new
snapshot_location: "raw/repos/_snapshots/2026-06-12-breferrari-obsidian-mind-9ae6860d01c4-source.zip"
adapter_ingest:
  adapter_name: git-clone-plus-git-archive
  adapter_version: git
  capture_method: "git clone --depth 1; git archive HEAD"
  extraction_trace:
    - "GitHub API metadata checked with public repo endpoint."
    - "Repository cloned at HEAD commit 9ae6860d01c4bb563dfe972dae89515866f4fbff."
    - "Source snapshot stored as project-visible zip with SHA256 hash."
  known_limits:
    - "No private issues, discussions, CI logs, or maintainer roadmap were inspected."
    - "Runtime was not installed as a VAKS dependency."
github_metadata:
  stars_at_capture: 2953
  forks_at_capture: 367
  open_issues_at_capture: 13
  visibility: public
  archived: false
raw_location: "raw/repos/_snapshots/2026-06-12-breferrari-obsidian-mind-9ae6860d01c4-source.zip"
processing_tier: heavy
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
  - ai-agent-memory
  - obsidian-vault-template
  - lifecycle-hooks
  - qmd
  - mcp
  - codex-cli
  - claude-code
  - gemini-cli
projects:
  - verified-action-knowledge-system
source_family: obsidian-agent-memory-template
upstream_sources:
  - "https://github.com/breferrari/shardmind"
  - "https://github.com/tobi/qmd"
  - "https://github.com/kepano/obsidian-skills"
verification_status: unverified
candidate_relation_suggestions: []
tags:
  - source/repository
  - vaks/candidate
  - agent-memory
  - obsidian
  - qmd
  - mcp
  - project-workbench
why_saved: see_body_or_legacy_record
---

# 来源记录：breferrari/obsidian-mind

## 为什么收录

用户要求对 `breferrari/obsidian-mind` 做“强蒸馏”。该仓库是一个面向 Claude Code / Codex CLI / Gemini CLI 的 Obsidian vault 模板，主张用 vault、hooks、QMD/MCP、命令和子 agent 给 coding agent 提供持久工作记忆。

对 VAKS 来说，它不是 reviewed truth 架构候选，而是一个高信号的操作层/agent workbench/retrieval surface 参考：

- 如何让 agent 每次 session 都拿到轻量上下文，而不是读全库。
- 如何让 hook 做分类、校验和刷新，不直接替代内容判断。
- 如何把 QMD/MCP 作为派生检索层，且由 manifest 统一索引名。
- 如何用 Obsidian Bases 做工作台视图。
- 如何把 agent memory 放在可见 Markdown vault 中，而不是隐藏黑盒。

## 来源信息

- 作者：Brenno Ferrari / GitHub contributors
- 发布方：GitHub
- 首次创建：2026-02-28T21:41:41Z
- 最近 GitHub updated_at：2026-06-11T21:23:27Z
- 最近 pushed_at：2026-06-02T00:26:30Z
- 捕获 commit：`9ae6860d01c4bb563dfe972dae89515866f4fbff`
- commit 时间：2026-06-02T00:26:28Z
- commit subject：`release: update CHANGELOG and manifests for v6.2.1`
- 版本：`v6.2.1`
- 原始链接：https://github.com/breferrari/obsidian-mind
- 快照位置：`raw/repos/_snapshots/2026-06-12-breferrari-obsidian-mind-9ae6860d01c4-source.zip`
- 快照 SHA256：`84797493e33e30550ba053d069c42543f7945fd7d4e202cfecb46a9c4bfedd82`
- stars / forks / open issues at capture：2953 / 367 / 13
- source_status：active
- 采集方式：public GitHub API + `git clone --depth 1` + `git archive`

## Intake Boundary

```yaml
processing_tier: heavy
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

Source records provide provenance and findability. This record does not make any claim true, does not adopt the repository, and does not create action basis.

## 文件/代码锚点矩阵

| Anchor | What exists | Design extraction | Boundary |
|---|---|---|---|
| `README.md:19` | Repository claims persistent memory for AI coding agents. | Source intent: coding-agent work memory, not verified knowledge review. | Treat as project/product claim. |
| `README.md:100-115` | ShardMind install, wizard, sidecar, default clone equivalence. | Packaging/update path for vault templates. | Do not install into VAKS main vault now. |
| `README.md:127-153` | QMD semantic search, MCP tools, manifest-scoped index, fallback to grep/Obsidian CLI. | Derived retrieval surface with visible fallback. | Retrieval is not support or truth. |
| `README.md:171-177` | Procedural code handles hooks; agent owns content; session lifecycle. | Thin automation boundary. | Agent content judgment still needs VAKS review gates. |
| `README.md:179-189` | Five lifecycle hooks. | SessionStart/UserPrompt/PostToolUse/PreCompact/Stop loop. | Lifecycle hints are process aids only. |
| `README.md:194-206` | Token-efficiency tiers. | Lightweight startup + on-demand retrieval. | Needs authority-bucket adaptation for VAKS. |
| `README.md:210-221` | Multi-agent support for Claude Code, Codex CLI, Gemini CLI. | Shared hooks/commands/vault conventions. | Codex skill path note may drift over time. |
| `README.md:287-314` | Performance graph and Bases. | Backlinks as evidence trails; Bases as frontmatter views. | Evidence trail is not evidence support by itself. |
| `ARCHITECTURE.md:13-17` | Three layers: vault, hook pipeline, QMD. | Useful separation of durable Markdown and derived machinery. | VAKS must add reviewed/action boundaries. |
| `ARCHITECTURE.md:56-58` | Procedural code owns environment; agent owns content. | Strong candidate pattern for agent-tool safety. | Does not replace VAKS review. |
| `ARCHITECTURE.md:86-116` | `vault-manifest.json` as source of truth for version, QMD, infra/user content, frontmatter. | Manifest-centered contract reduces drift. | Manifest is operational, not truth authority. |
| `ARCHITECTURE.md:165-169` | Hook behavior details: inject-not-load, classify-not-route, detached QMD refresh, lightweight Stop. | Good minimal automation split. | Still personal-vault assumptions. |
| `ARCHITECTURE.md:173-225` | QMD integration and MCP wrapper. | Typed retrieval contract + named SQLite store. | Must be bucket-aware before VAKS use. |
| `ARCHITECTURE.md:247-278` | Multi-agent config mapping. | Same scripts serve multiple agents. | Event vocabularies are agent-specific and may change. |
| `ARCHITECTURE.md:286-317` | Vault-first memory, `brain/` as durable memory, `~/.claude` as pointer. | Strong inspiration for memory quarantine and visible memory. | VAKS reviewed truth cannot be agent memory. |
| `ARCHITECTURE.md:370-378` | ShardMind additive install and clone-equivalence invariants. | Useful distribution/update idea. | Future packaging only; not current core. |
| `AGENTS.md:9-22` | Hook config table for Claude/Codex/Gemini. | Portable operating manual for agents. | Read as source design, not as VAKS instruction. |
| `CLAUDE.md:14-19` | QMD preference order: MCP tools, CLI, then grep/read. | Clear fallback contract for retrieval. | Need VAKS authority filters before retrieval ranking. |
| `CLAUDE.md:100` | SessionStart injects context and triggers QMD re-index. | Useful session lifecycle idea. | VAKS should not auto-start runtime without approval. |
| `CLAUDE.md:143`, `CLAUDE.md:179` | Required frontmatter and wikilinks. | Simple note hygiene guard. | VAKS needs stronger provenance/review fields for promotion. |
| `CLAUDE.md:280-283` | Brain topics read on demand, prefer QMD. | Low-token topic activation pattern. | Do not load all brain topics as truth. |
| `.claude/scripts/session-start.ts:73-92` | Detached QMD update at session start, scoped by manifest. | Nonblocking derived-index refresh. | Requires clear stale-index warnings for VAKS. |
| `.claude/scripts/classify-message.ts:3-39` | Prompt classification emits hints. | Routing hints without direct write. | Hint is not intent confirmation. |
| `.claude/scripts/lib/signals.ts:1-11` | Multilingual signal definitions. | Data-driven capture routing. | Signal match can false-positive; review before persistence. |
| `.claude/scripts/validate-write.ts:3-58` | Post-write validation warning output. | Hook as lint/check, not rewriter. | VAKS lint must not auto-repair reviewed knowledge. |
| `.claude/scripts/lib/frontmatter.ts:58-79` | Missing frontmatter/tag/date/description/wikilink warnings. | Simple note-health lint. | Too weak for VAKS promotion. |
| `.claude/scripts/qmd-refresh.ts:3-24` | Debounced detached QMD refresh. | Stale retrieval cache mitigation. | Still needs source-hash invalidation for VAKS. |
| `.claude/scripts/qmd-mcp.mjs:7-21`, `.claude/scripts/qmd-mcp.mjs:181` | Cross-platform wrapper and qmd MCP index workaround. | Practical Windows/MCP integration pattern. | Version-specific qmd bug workaround may expire. |
| `.codex/hooks.json:3-43` | Codex hook wiring. | Same TypeScript scripts are reused for Codex. | Depends on current Codex hook surface. |
| `.gemini/settings.json:3-57` | Gemini event-name mapping. | Event adapter layer. | Agent-specific mapping is not universal. |
| `.shardmind/shard-schema.yaml:45-86` | Four setup values and module gating explanation. | Installer UX and optional modules. | Packaging/runtime layer only. |
| `.github/workflows/test.yml` | Node 22/24, Windows/macOS/Linux test matrix, QMD install. | Cross-platform hook contract evidence. | Test pass is diagnostic, not adoption proof. |

## 本次本地检查

在捕获快照上运行了仓库自己的 hook test suite：

```text
cwd: C:\Users\ADMINI~1\AppData\Local\Temp\vaks-obsidian-mind-intake\.claude\scripts
node: v24.11.0
command: npm test
result: 527 passed, 0 failed
```

这只是仓库脚本层自检通过，不代表适合直接并入 VAKS，也不代表任何 README claim 获得 reviewed truth。

## 初步看点

1. `vault-manifest.json` 是一个强中心契约：QMD index、infra/user-content、frontmatter、version fingerprints 都从这里分发。
2. Hook 只做环境与提示：session 注入、消息分类、写后 lint、QMD refresh、compact backup、stop checklist；内容仍交给 agent。
3. QMD/MCP 是可替换的派生检索层，缺失时有 grep/CLI fallback。
4. `brain/` 作为 durable agent memory，`~/.claude` 只做 pointer，这是避免黑盒 memory 的高价值设计。
5. Bases 和 backlinks 让工作/绩效/证据准备可视化，但不做 truth。
6. ShardMind 让 vault template 可安装、可升级、可模块化，但保持 clone 等价。

## 明显疑点

1. README 里的“agent handles the rest”对 VAKS 是危险方向：VAKS 不能让 agent 自动写 reviewed truth。
2. Personal work/performance vault 的证据链不同于 VAKS 的 evidence support；backlink evidence trail 不能直接等于 source-span support。
3. QMD/MCP 检索没有 VAKS authority bucket、source hash、review status 过滤。
4. Slack / people / review-prep 工作流涉及隐私和组织数据，不适合默认吸收。
5. ShardMind/agent hooks 是 runtime 和 installer 层，不能提前进入 VAKS truth core。

## 可抽取 Candidate Points

- Manifest-centered runtime contract can reduce drift across hooks, MCP, installers, and migration tools.
- Lifecycle hooks are useful when they inject context, route hints, validate writes, and refresh caches without owning content judgment.
- QMD/MCP provides a practical typed retrieval surface, but VAKS must apply authority-bucket and source-hash filters before ranking.
- Vault-first agent memory should write to visible project files or candidate/feedback records, not hidden model memory or reviewed truth.
- Obsidian Bases are strong as workbench views over structured Markdown, but views cannot define schema or truth.
- ShardMind's clone-equivalence and sidecar update model is useful for future vault template distribution, not current VAKS core architecture.

## 当前处理等级

```text
heavy candidate-only source intake
```

升级到 reviewed knowledge / pattern / decision 的条件：

- 用户明确要求进入 review/promotion。
- 具体候选点被拆成自足 review candidate。
- 有 source anchors、support/challenge、scope/risk、Evidence Packet。
- VAKS 决定要实现相关 agent hook / workbench / retrieval layer，并做局部试验。

## 下一步

- 读取对应 candidate distillation、architecture review、project overlay。
- 若后续做 VAKS agent-access 或 Obsidian use-surface 原型，可把本 repo 作为 Support / Risk / Cold Reference，而不是 Core。
