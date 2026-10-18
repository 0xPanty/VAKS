---
record_kind: source_card
type: source
status: source-captured
title: AgriciDaniel/claude-obsidian
source_id: github-agricidaniel-claude-obsidian-2026-06-07
source_uri: github:AgriciDaniel/claude-obsidian
source_url: https://github.com/AgriciDaniel/claude-obsidian
source_type: repository
platform: github
owner: AgriciDaniel
repo: claude-obsidian
default_branch: main
checked_ref: main
checked_commit: cb93ff6d82f9c35a08bf6010e7fac36dfddc827b
commit_time: 2026-05-28T00:42:42Z
captured_at: 2026-06-07
captured_by: Codex
extracted_at: 2026-06-07
extracted_by: Codex
extraction_tool: git clone --depth 1 + GitHub API + rg inspection
source_status: active
source_metadata:
  full_name: AgriciDaniel/claude-obsidian
  description_observed: "Self-organizing AI second brain for Obsidian + Claude Code."
  stars_observed: 6256
  forks_observed: 727
  updated_at: 2026-06-07T13:18:24Z
  pushed_at: 2026-05-28T00:42:43Z
license_status: MIT
raw_location: raw/repos/2026-06-07-agricidaniel-claude-obsidian-source.md
snapshot_location: raw/repos/_snapshots/AgriciDaniel-claude-obsidian-cb93ff6d82f9c35a08bf6010e7fac36dfddc827b.zip
snapshot_sha256: 2242F21524D29C31FD10584EA12DF306D3D7FFCCAEA415DDF77629C9C032116D
snapshot_bytes: 6801930
processing_mode: repo-review
processing_level: heavy
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
access_boundary: public_no_cookies
verification_status: snapshot_captured_not_executed
evidence_granularity: table_or_code_anchor
topics:
  - obsidian
  - claude-code
  - llm-wiki
  - agent-skills
  - file-first-memory
  - hot-cache
  - hybrid-retrieval
  - multi-writer-locking
  - methodology-router
projects:
  - verified-action-knowledge-system
source_family: ai-obsidian-wiki-implementation-reference
upstream_sources:
  - https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f
  - https://github.com/kepano/obsidian-skills
  - https://www.anthropic.com/news/contextual-retrieval
related_outputs:
  - outputs/review/2026-06-07-agricidaniel-claude-obsidian-candidate-distillation.md
  - wiki/summaries/2026-06-07-agricidaniel-claude-obsidian-architecture-review.md
  - outputs/review/project_overlays/VAKS/VAKS-agricidaniel-claude-obsidian-2026-06-07.md
candidate_relation_suggestions:
  - target: "agent-skills-as-action-surface"
    relation_type: refines
    relation_state: candidate
    why_suggested: "The repository implements a skill catalog and command routing surface for wiki operations."
  - target: "hot-cache-as-activation-state"
    relation_type: refines
    relation_state: candidate
    why_suggested: "The repository uses hot.md, index.md, and log.md as a lightweight recovery and navigation spine."
  - target: "agent-file-write-safety"
    relation_type: refines
    relation_state: candidate
    why_suggested: "The repository adds per-file advisory locks and hook-level auto-commit deferral."
tags:
  - raw-repo
  - github
  - candidate-only
  - source-identity-only
---

# Repository Source: AgriciDaniel/claude-obsidian

## 为什么收录

这个仓库是一个公开的 Claude Code + Obsidian second-brain 实现样本。

它对 VAKS 的价值不在于“照搬一套 AI 笔记系统”，而在于它把几个我们已经讨论过的方向做成了具体工程表面：

- `skills/` 作为可读、可触发的动作模块。
- `wiki/hot.md`、`wiki/index.md`、`wiki/log.md` 作为轻量恢复和导航状态。
- `.raw/` 作为原始来源区，`wiki/` 作为生成知识区。
- `wiki-lock.sh`、hooks、manifest、tests 作为 AI 文件写入的安全边界。
- BM25、contextual prefix、rerank 作为可重建检索缓存。
- methodology mode router 把“怎么归档”从“内容是什么”里拆出来。

本卡只记录来源身份、版本和看过的锚点。项目借鉴判断写在 overlay，不写进 source card。

## 来源信息

- 仓库：https://github.com/AgriciDaniel/claude-obsidian
- 观察分支：`main`
- 观察 commit：`cb93ff6d82f9c35a08bf6010e7fac36dfddc827b`
- commit 时间：`2026-05-28T00:42:42Z`
- GitHub API 观察时间：`2026-06-07`
- 观察到 stars / forks：`6256 / 727`
- license：MIT
- 本地 snapshot：`raw/repos/_snapshots/AgriciDaniel-claude-obsidian-cb93ff6d82f9c35a08bf6010e7fac36dfddc827b.zip`
- snapshot SHA256：`2242F21524D29C31FD10584EA12DF306D3D7FFCCAEA415DDF77629C9C032116D`
- 访问方式：公开 GitHub / Git clone，无 cookies，无私有账号

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

Source card 只提供 provenance 和 source/code anchors。它不提供 reviewed knowledge、truth confidence、架构决定或行动依据。

## Source / Code Anchors

| Anchor | What exists | Why it matters | Boundary |
|---|---|---|---|
| `README.md:20-27` | README 描述 15 个 Claude Code skills、multi-writer safe、methodology modes、hybrid retrieval、Obsidian CLI transport | 说明这个 repo 是实现级组合，不只是文章概念 | README 是自述，不等于运行验证 |
| `README.md:173-208` | 命令面：`/wiki`、`ingest`、`/save`、`/autoresearch`、`/canvas`、`/think`，并 seed `hot.md/index.md/log.md/dashboard.base` | 可以作为“skill action surface”样本 | 命令触发不等于 VAKS 允许自动化 |
| `README.md:287-315` | 跨项目知识库读取顺序：先 `hot.md`，再 `index.md`，再具体页；创建 index/log/hot | 轻量恢复和 token 控制样本 | hot/index 是 activation，不是 truth |
| `README.md:325-350` | 架构图入口：vault flow、multi-writer locking、hybrid retrieval | 说明设计已经落到图和工具层 | 图是解释材料，不是证据支持 |
| `README.md:455-472` | 文件结构列出 15 skills、wiki-cli、wiki-retrieve、wiki-mode 等目录 | skill decomposition 有具体目录锚点 | 目录存在不代表适合直接装进 VAKS |
| `README.md:567-570` | FAQ 解释 per-file advisory locking 和 `hot.md/index.md` 区别 | 直接锚定文件锁与两层缓存设计 | 这是项目语义，不能直接变成 VAKS truth |
| `AGENTS.md:29-38` | skills 触发词表：wiki-ingest、wiki-query、wiki-lint、wiki-fold、save、canvas 等 | agent skill router 的轻量 registry 样本 | 触发词要受本项目显式授权规则限制 |
| `AGENTS.md:43-56` | 定义 vault root、hot cache、raw sources、generated knowledge、manifest 和 agent startup flow | 项目本地 AGENTS 作为运行入口 | 不能把它的 AGENTS 规则全球化 |
| `CLAUDE.md:41-46` | 跨项目读取规则，且提醒不要为一般编码问题读 wiki | 很贴近 VAKS 的 activation gating | 它仍然不区分 reviewed/action basis |
| `CLAUDE.md:67-75` | transport detection、wiki-lock、mode router 的集中说明 | 工具能力选择和写入安全可借鉴 | transport 选择不是权限授权 |
| `CLAUDE.md:77-79` | pre-commit verifier agent，读 staged diff，输出分级 findings | 独立 reviewer pass 是有用工程手段 | reviewer output 不是 evidence review |
| `WIKI.md:143-185` | `.raw/`、`wiki/`、`index.md`、`log.md`、`hot.md` 和 hot cache 更新规则 | 轻量 wiki spine 的详细说明 | 它的 `wiki/` 是 agent-owned，VAKS 的 reviewed 层不能这么开放 |
| `WIKI.md:423-486` | ingest/query/lint 工作流：更新 index/hot/log、lint 输出 report、ask before fix | 工作流可作为 VAKS tool/workbench 参考 | lint/report 不等于 truth mutation |
| `skills/wiki/SKILL.md:29-64` | `.raw/` + `wiki/` + `index/log/hot` 的基础结构 | Karpathy LLM Wiki 的具体技能化版本 | raw 和 generated wiki 都不能替代 VAKS review |
| `skills/wiki-ingest/SKILL.md:50-82` | per-file locks、PostToolUse deferral、manifest delta tracking | AI 多写者安全与重复处理跳过机制 | VAKS 不应默认 auto-commit/auto-ingest |
| `skills/wiki-ingest/SKILL.md:163-178` | single source ingest 需要读完整 source，更新 overview/index/hot/log | 完整 ingestion checklist | VAKS 需要多一层 candidate/review separation |
| `skills/wiki-query/SKILL.md:49-73` | quick/standard/deep 查询分层：hot/index/3-5 pages/deep | 查询深度分层可借鉴 | VAKS 还要按 authority bucket 检索 |
| `skills/wiki-lint/SKILL.md:12-18` | lint 后写 report，ask before auto-fixing，走 transport policy | maintenance report 的实现样本 | lint 只能 observe/report，不能自动修 truth |
| `skills/wiki-lint/SKILL.md:214-230` | 地址缺失等 lint error，但不自动分配地址 | “发现问题”和“修改状态”分开 | 与 VAKS maintenance-manifest 边界同频 |
| `skills/wiki-retrieve/SKILL.md:15-24` | contextual prefix 外发被 `--allow-egress` gate，`--no-llm` 可本地化 | 明确的网络/隐私边界 | 外部 API 不应成为默认路径 |
| `skills/wiki-retrieve/SKILL.md:128-178` | BM25-only、explain mode、quick mode 不触发 retrieval、refresh 手动 | 检索作为可调缓存，而不是强制层 | 检索分数不是 support 或 confidence |
| `scripts/wiki-mode.py:2-18` | mode router 是 single source of truth；缺省 generic；route TYPE NAME | filing policy 可以集中化 | filing mode 不能改变知识 authority |
| `scripts/wiki-mode.py:146-184` | generic/LYT/PARA/Zettelkasten 各自 route path | 归档策略可配置，不硬编码 | 不能把一种方法论变成 VAKS 默认 |
| `hooks/hooks.json:3-17` | SessionStart 读取 `wiki/hot.md`，启动时清 stale locks | hot cache 可以作为恢复入口 | hook 注入上下文不是审阅知识 |
| `hooks/hooks.json:33-50` | PostToolUse auto-commit 避开 locks；Stop 提醒更新 hot cache | AI 写入后自动维护的完整闭环 | VAKS 默认不采用 auto-commit |
| `PRIVACY.md:6-18` | 声明本地 Markdown、本地会话、默认不外发 | 隐私边界有显式文档 | 声明需要结合代码/使用验证 |
| `PRIVACY.md:25-33` | optional egress 表，Anthropic API 和 remote ollama 需要 flag | egress gate 可借鉴 | 不能默认读取私有数据或远程发送 |
| `Makefile:10-25` | test target 覆盖 retrieval、concurrency、mode、contextual 等 | repo 有 hermetic test surface | 本次未运行这些测试 |
| `tests/test_concurrent_write.sh:2-13` | 多写者测试说明锁保护同一文件并发写 | 安全机制有测试锚点 | 测试存在不等于本地已验证 |
| `tests/test_wiki_lock.sh:129-143` | absolute path、`../`、newline、CR path rejection | path safety 有明确测试 | 仅作为参考，不是 VAKS 工具安全结论 |

## 初步看点

- 这是一个“AI 维护 Obsidian wiki”的完整工程样本。
- 最值得看的是 skill decomposition、hot/index/log spine、locks/hooks、methodology router、retrieval consent gate。
- 它的风险也很清楚：generated wiki 可以被误读成 truth；auto-research 和 auto-commit 很容易越界；检索/缓存/仪表盘容易被误当成 authority。

## 明显疑点

- 本次没有运行 repo 测试，也没有安装插件。
- 仓库默认假设 agent 可以写 `wiki/`，这和 VAKS reviewed truth layer 的边界不同。
- `autoresearch` 的默认描述是“output goes directly into the knowledge base”，这对 VAKS 来说必须降级为 raw/candidate。
- hook auto-commit 对共享 repo 或严格审计环境有风险。
- methodology modes 适合做 filing policy，不适合变成全局知识模型。

## 可抽取 Candidate Points

- Agent-facing skills can be treated as explicit action surfaces, with trigger words, workflow scope, and fallback rules.
- A small `hot.md + index.md + log.md` spine can support session recovery and low-cost context activation.
- AI file writes need per-file locks, path validation, and hook gates before any future multi-writer workflow.
- Retrieval should be a derived, refreshable cache with egress consent gates, not a truth source.
- Filing methodology should be a router/configuration layer, not a global architecture decision.
- Lint and verifier agents are useful maintenance and bias-control surfaces, but their output is diagnostic, not truth.

## 当前处理等级

```text
heavy repo intake
```

Reason:

- public GitHub repository;
- implementation-level reference;
- directly relevant to VAKS source intake, skill routing, Obsidian, activation, retrieval, and agent-write safety;
- inspected snapshot and source/code anchors;
- not promoted to reviewed knowledge.

## 下一步

- Read the candidate distillation for reusable points.
- Read the architecture review when designing VAKS workbench, skill runtime, retrieval/cache, or AI write safety.
- Use the project overlay only for active VAKS design context.
- Do not use this source as action basis without a later evidence-aware review.
