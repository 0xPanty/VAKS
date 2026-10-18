---
type: source
status: source-captured
title: "Agent Learning Hub"
source_id: 2026-06-06-datawhalechina-agent-learning-hub-source
source_uri: https://datawhalechina.github.io/Agent-Learning-Hub/
source_url: https://datawhalechina.github.io/Agent-Learning-Hub/
repo_url: https://github.com/datawhalechina/Agent-Learning-Hub
source_type: repository_documentation
author: "陈思州 / jjyaoao"
publisher: "Datawhale / GitHub Pages"
published_at:
updated_at: 2026-06-05
captured_at: 2026-06-06
captured_by: Codex
version_or_commit: d7967513ace303618ac2e37732468f6e127e4de1
commit_time: "2026-06-05 18:25:15 +1000"
commit_subject: "Update DeerFlow project status"
source_status: active
license: MIT
raw_location: raw/repos/2026-06-06-datawhalechina-agent-learning-hub-source.md
snapshot_location: raw/repos/_snapshots/datawhalechina-Agent-Learning-Hub-d7967513ace303618ac2e37732468f6e127e4de1.zip
snapshot_sha256: 8FA4BFE8D9FEA4854AEE1C09959777F9D5D318AC9856142D0CE3D921390593C5
processing_mode: immediate
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
review_priority: high
review_owner: Codex
formalization_status: candidate-generated
topics:
  - agent-learning-roadmap
  - agent-harness
  - skills
  - mcp-a2a-acp
  - evaluation-safety
  - personal-agent
  - hermes-openclaw
  - misa-vaks-integration
projects:
  - verified-action-knowledge-system
  - misa
source_family:
  - agent-runtime
  - agent-gateway
  - skill-packaging
  - evaluation
  - source-intake
upstream_sources: []
verification_status: primary-source-captured
candidate_relation_suggestions:
  - target: "[[Agent Gateway]]"
    relation_type: refines
    relation_state: candidate
    why_suggested: "The roadmap separates minimal loops, modern harnesses, permission gates, session stores, context compaction, and trace."
  - target: "[[Skill Packaging]]"
    relation_type: refines
    relation_state: candidate
    why_suggested: "The Skills stage treats skills as reusable process packages with steps, acceptance criteria, scripts, templates, and smoke tests."
  - target: "[[Evidence Sufficiency Gate]]"
    relation_type: risk_of
    relation_state: candidate
    why_suggested: "The resource hub is a learning map and link curation surface, not evidence that a design is true or action-ready."
  - target: "[[Feedback Ledger]]"
    relation_type: refines
    relation_state: candidate
    why_suggested: "The evaluation stage emphasizes fixed tasks, traces, failures, cost, latency, and regression checks."
tags:
  - agent-learning-hub
  - datawhale
  - hermes
  - openclaw
  - skills
  - mcp
  - candidate-only
---

# Agent Learning Hub Source Record

## 为什么收录

这个源不是一个 agent runtime，也不是我们要 fork 的项目。它是一个面向学习和工程路线的 agent 资料中心：把 agent 学习拆成从最小工具循环、RAG/记忆、现代 harness、multi-agent、Skills/MCP/A2A/ACP、browser/computer use、评估与安全、真实项目交付的分阶段路线。

对 VAKS / MISA 最有价值的不是“它列了很多链接”，而是它提供了一把接入前的成熟度尺子：

```text
先能解释为什么需要 agent
再做最小 observe-think-act loop
再把 memory / tools / permission / trace / session / compaction 分开
再把 capability 包成 skill
最后才谈 always-on personal agent / Hermes / OpenClaw 式接入
```

边界也要写硬：

```text
Agent Learning Hub 是学习路线和资源导航
不是 VAKS 的 reviewed knowledge
不是 MISA 接入方案本身
不是某个框架的事实证明
不是 action basis
```

## 来源信息

- Site: https://datawhalechina.github.io/Agent-Learning-Hub/
- Repository: https://github.com/datawhalechina/Agent-Learning-Hub
- Checked branch: `main`
- Checked commit: `d7967513ace303618ac2e37732468f6e127e4de1`
- Commit time: `2026-06-05 18:25:15 +1000`
- Commit subject: `Update DeerFlow project status`
- Commit author: `jjyaoao <jjyaoao@126.com>`
- License: MIT
- Files in checked tree: 5
- Snapshot: `raw/repos/_snapshots/datawhalechina-Agent-Learning-Hub-d7967513ace303618ac2e37732468f6e127e4de1.zip`
- Snapshot SHA256: `8FA4BFE8D9FEA4854AEE1C09959777F9D5D318AC9856142D0CE3D921390593C5`
- Inspected mode: docs/static site read; no runtime to install; no external resource links deep-read; no framework code executed.

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

This source record is provenance and findability only. It does not create reviewed patterns, truth confidence, relation strength, or action basis.

## 文件 / 内容锚点

| Anchor | What exists | 初步看点 | Boundary |
|---|---|---|---|
| `README.md:3-5` | README says this is a roadmap and curated todo/source list. | README-first learning hub; the repo's primary artifact is the guide itself. | A curated roadmap is not independent evidence. |
| `README.md:11-16` | Different entry routes for beginners, LLM app builders, project builders, and resource seekers. | Useful routing model: one source can expose multiple use paths without changing truth status. | Routing is activation only. |
| `README.md:18-30` | Current priorities: coding agents, agent harnesses, OpenClaw/Hermes personal agents, Skills/MCP/A2A/ACP, eval/safety. | Strong relevance to MISA and future agent gateway work. | Priority list can drift quickly. |
| `README.md:34-42` | Stage 0: distinguish agent, chatbot, workflow, multi-agent; explain when not to use an agent. | Good intent-confirmation gate before adding agent complexity. | Deciding "agent or not" is design triage, not truth review. |
| `README.md:44-59` | Stage 1: minimal loop, structured JSON, tool functions, max steps, timeout, error handling. | Minimal runnable loop before harness or protocol complexity. | Toy loop is not production readiness. |
| `README.md:61-90` | Stage 2: RAG, memory, tools, failure modes, source-backed answers. | Separates short context, session memory, and long-term memory. | Memory is not reviewed knowledge. |
| `README.md:92-113` | Stage 3: modern harness: directory, loop, tool registry, permission gate, session store, compaction, trace. | Direct checklist for MISA-to-VAKS integration hardening. | Checklist is not implementation proof. |
| `README.md:115-131` | Stage 4: multi-agent coordination with supervisor/graph, roles, schemas, stopping rules. | Useful warning against role-chat pileups. | Multi-agent is optional; single agent may be better. |
| `README.md:133-156` | Stage 5: Skills/protocols/capability packaging, SKILL.md, scripts/templates, acceptance criteria, smoke tests. | High value for future VAKS/MISA skill pack. | Skill packages are process knowledge, not truth mutation. |
| `README.md:158-173` | Stage 6: browser/computer-use agents; public web, action logs, screenshots, DOM, safety. | Useful for future web agent boundary. | Browser action trace is process evidence, not support evidence. |
| `README.md:175-192` | Stage 7: fixed eval set, traces, cost, latency, tool count, human confirmation, injection/data exfiltration risks. | Good operational eval gate before more agents. | Eval pass is diagnostic, not action-basis authority. |
| `README.md:194-218` | Stage 8 and Project Ladder, from calculator agent to personal agent and production harness. | Concrete staircase for not jumping straight to "MISA reads the vault". | Ladder level is maturity hint, not adoption verdict. |
| `README.md:222-240` | Official resources: Anthropic, Claude Code, OpenAI Agents SDK, Gemini, Google ADK, MCP. | Curated source-first orientation. | External links were not deep-read in this intake. |
| `README.md:242-254` | Project map by learning purpose: personal agents, harness runtime, deep research/RAG, browser/multimodal. | Good taxonomy for deciding what kind of agent reference a source is. | Taxonomy is not VAKS schema. |
| `README.md:256-264` | Definitions for Skills, MCP, A2A, ACP, skill quality. | Useful protocol separation for MISA integration vocabulary. | These definitions are learning guide summaries, not standards text. |
| `README.md:266-282` | Modern systems table includes OpenClaw, Hermes, CyberClaw, DeerFlow, LangGraph. | Direct project-neighborhood map. | Resource status must be verified before any adoption. |
| `README.md:284-292` | CrewAI, AutoGen, LangChain agents treated as optional/legacy/older style. | Helpful anti-overinvestment warning. | Do not turn ranking into universal ban. |
| `README.md:294-312` | Papers list: ReAct, Toolformer, Reflexion, SWE-agent, harness/security papers, etc. | Good reading queue seed for agent gateway/eval/safety. | Paper titles listed here are not reviewed by this source card. |
| `README.md:349-366` | Claude Code study path: docs, papers, hello-agents, OpenClaw/Hermes comparison, permissions/hooks/MCP. | Useful for Codex/Hermes-style agent analysis path. | Not a substitute for current official docs/source review. |
| `README.md:368-377` | Learning principles: build first, prefer small reliable agents, strict schemas, evals before more agents, trace important runs, human-in-loop for risky actions. | Strong alignment with VAKS lazy gates and agent-memory quarantine. | Principles are candidate guidance only. |
| `CONTRIBUTING.md:1-41` | Contribution quality bar: official docs/blogs, papers, runnable repos; avoid ads, private/paywalled/scraped content and link dumps. | Useful source-intake quality bar for external reference scouting. | Contributor policy is not evidence review. |
| `index.html:634-640` | Static site stores progress in localStorage. | Lightweight learning workbench, no backend truth store. | UI progress is personal state only. |
| `index.html:880-917` | Search and stage progress rendering. | The guide doubles as a navigable checklist. | Progress checkbox is not review state. |

## 源的实际形态

Checked tree only contains:

```text
.gitignore
CONTRIBUTING.md
index.html
LICENSE
README.md
```

This means the source is best treated as:

```text
curated roadmap + static checklist UI
```

not:

```text
agent framework
runtime implementation
protocol implementation
evaluation harness implementation
```

## 初步看点

1. **先分清 agent 需不需要**：Stage 0 要求先解释为什么 agent 比 workflow/script/chatbot 更合适，这很适合做 MISA 接入 VAKS 的第一道 intent gate。
2. **先做小 loop，再谈系统**：Stage 1 的最小 agent loop 可以变成未来接入前的 smoke-test 基线。
3. **harness 是组件清单，不是玄学**：tool registry、permission gate、session store、context compaction、trace 都被拆成可检查对象。
4. **Skills 是过程包装**：SKILL.md、scripts/templates、acceptance criteria、smoke test 这一组，很适合 VAKS / MISA 之间做可复用操作包。
5. **协议不要混成一坨**：MCP、A2A、ACP 各自连接不同对象；MISA 接入 VAKS 前应先判断需要 data/tool、agent-agent，还是 host-app boundary。
6. **eval 在扩 agent 前面**：固定任务、失败分类、成本、延迟、工具次数、trace、dangerous tool confirmation，都能给未来 MISA-VAKS connector 做验收线。
7. **personal agent 要走网关**：OpenClaw/Hermes/CyberClaw 这组资源说明 always-on agent 更像 gateway + memory + skill + permission 的组合，不是让 agent 随便读写资料库。

## 明显疑点

1. 这是高质量路线图，但不是 peer-reviewed evidence，也不是 runtime benchmark。
2. README 里很多外部链接没有在本次逐条深读；它们只能作为后续 source queue，不是已吸收知识。
3. "current priority" 和项目状态会快速漂移；未来如果要用某个项目，必须重新抓当前 commit / docs。
4. 它把一些旧框架降为 optional/legacy，这是学习路线判断，不应变成 VAKS 的永久禁用规则。
5. localStorage progress 是学习者 UI 状态，不应被误读为 review queue / knowledge status。

## 可抽取 Candidate Points

- `agent-roadmap-as-integration-gate`
- `workflow-before-agent-intent-check`
- `minimal-tool-loop-before-harness`
- `retrieval-memory-source-boundary`
- `harness-anatomy-checklist`
- `personal-agent-connector-map`
- `skills-as-reusable-process-not-truth`
- `protocol-separation-mcp-a2a-acp`
- `eval-before-more-agents`
- `multi-agent-coordination-not-magic`
- `project-ladder-for-misa-vaks`
- `curated-resource-quality-bar`

## 当前处理等级

```text
heavy docs/static-site read, candidate-only extraction
```

升级为 reviewed pattern / decision 的条件：

- 选 1-2 个具体机制，和官方 docs 或项目源码交叉验证。
- 在 MISA / VAKS 上做最小 trial，例如 read-only context_request -> context_pack_response。
- 明确 artifacts 写入层级：raw source / candidate distillation / project overlay / feedback event / reviewed decision。
- 通过用户确认后，才考虑写 `wiki/patterns` 或 `wiki/decisions`。

## 下一步

- 已写入候选蒸馏：`outputs/review/2026-06-06-datawhalechina-agent-learning-hub-candidate-distillation.md`
- 已写入 MISA 项目侧 overlay：`outputs/review/project_overlays/MISA-agent-learning-hub-integration-overlay-2026-06-06.md`
- 已写入 architecture review：`wiki/summaries/2026-06-06-datawhalechina-agent-learning-hub-architecture-review.md`
- 暂不写 `wiki/patterns` / `wiki/decisions`，因为还没有 reviewed adoption。
