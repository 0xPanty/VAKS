---
type: source
record_kind: source_card
status: source-captured
title: "odysseus-dev/odysseus"
source_id: github-odysseus-dev-odysseus
source_uri: https://github.com/odysseus-dev/odysseus
source_url: https://github.com/odysseus-dev/odysseus
source_type: repository
owner: odysseus-dev
repo: odysseus
author: odysseus-dev
publisher: GitHub
published_at: 2026-05-31T14:05:51Z
updated_at: 2026-08-23T18:12:34Z
captured_at: 2026-08-24T02:13:39+08:00
captured_by: Codex
checked_branch: dev
version_or_commit: b4d12932a953b3cdfc745b3525c7ecd5dffd8b3c
commit_time: 2026-08-20T11:06:22Z
main_head_observed: cf4e240ad1622da6a904f496b19d656a2b9c6393
source_status: active
raw_location: https://github.com/odysseus-dev/odysseus/tree/b4d12932a953b3cdfc745b3525c7ecd5dffd8b3c
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
why_saved: "User explicitly requested standard distillation of the public odysseus-dev/odysseus repository."
adapter_ingest:
  adapter_name: github-api-and-shallow-git
  adapter_version: "GitHub REST API + git"
  capture_method: "Official GitHub metadata plus a temporary depth-1 clone of dev, pinned to commit b4d12932; static inspection only."
  extraction_trace: "README, setup, migration, security/threat, license/acknowledgments, architecture inventory, agent tool-gate/approval code, and memory extraction code were inspected."
  known_limits:
    - "No repository code, test, benchmark, dependency installation, service, or live runtime was executed."
    - "No repository snapshot or archive was retained because this was standard/medium intake."
    - "The default dev branch is fast-moving; all code anchors are commit-pinned."
    - "GitHub counts are volatile discovery metadata, not source quality or verification."
    - "Security documents and architecture inventory show possible drift relative to current code; unresolved runtime behavior was not inferred from prose alone."
github_metadata_observed:
  captured_at: 2026-08-24T02:13:39+08:00
  repository_id: 1255180606
  provider_object_id: R_kgDOStCJPg
  default_branch: dev
  stars: 86052
  forks: 602
  subscribers: 467
  open_issues_and_pull_requests: 1107
  releases_observed: 0
  tags_observed: 0
  license_spdx_detected: AGPL-3.0
  note: "README declares AGPL-3.0-or-later; counts and provider metadata are observation-time only."
topics:
  - self-hosted-ai-workspace
  - agent-runtime
  - tool-capability-gates
  - prompt-injection-hardening
  - exact-action-approval
  - agent-memory
  - source-migration
  - local-model-workflows
projects:
  - verified-action-knowledge-system
source_family:
  - repository
  - ai-workspace
  - privileged-agent-runtime
verification_status: statically-inspected-unexecuted
source_annotation_refs:
  - annotation_id: odysseus-exact-action-binding-payload
    path: outputs/review/source_annotations/2026-08-24-odysseus-dev-odysseus/odysseus-exact-action-binding-payload.md
    anchor_status: exact_verified
  - annotation_id: odysseus-external-context-effect-gate
    path: outputs/review/source_annotations/2026-08-24-odysseus-dev-odysseus/odysseus-external-context-effect-gate.md
    anchor_status: exact_verified
  - annotation_id: odysseus-auto-memory-direct-write-risk
    path: outputs/review/source_annotations/2026-08-24-odysseus-dev-odysseus/odysseus-auto-memory-direct-write-risk.md
    anchor_status: exact_verified
candidate_relation_suggestions: []
tags:
  - repo-intake
  - candidate-only
  - agent-runtime
  - security-boundary
---

# 来源记录：odysseus-dev/odysseus

## 为什么收录

用户明确要求对 `https://github.com/odysseus-dev/odysseus` 执行标准“蒸馏”。

该仓库将聊天、Agent、本地/云模型、工具、MCP、深度研究、文档、邮件、笔记、任务、日历和图像工作流整合为一个自托管 AI 工作台。本记录仅保存来源身份、静态检查边界和可回访的候选看点；不代表仓库已通过安全验证、被 VAKS 采纳，或可作为行动依据。

## 来源信息

- 官方仓库：https://github.com/odysseus-dev/odysseus
- 检查分支：`dev`（默认、快速演进）
- 检查 commit：`b4d12932a953b3cdfc745b3525c7ecd5dffd8b3c`
- commit 时间：`2026-08-20T11:06:22Z`
- 同时观测的 `main` HEAD：`cf4e240ad1622da6a904f496b19d656a2b9c6393`
- GitHub created_at：`2026-05-31T14:05:51Z`
- GitHub pushed_at：`2026-08-20T17:39:01Z`
- 源状态：`active`，但属于快速变动、尚无 GitHub tag/release 的阶段
- 许可证：README 声明 `AGPL-3.0-or-later`；GitHub 检测为 `AGPL-3.0`
- 采集方式：官方 GitHub API + 临时 shallow clone + commit-pinned 静态检查
- 原始锚点：https://github.com/odysseus-dev/odysseus/tree/b4d12932a953b3cdfc745b3525c7ecd5dffd8b3c
- 仓库快照：未保留（标准/medium 边界）

GitHub 热度、issue/PR 数量和 CI 标记只是观测时元数据。它们不是安全性、稳定性、真实性或采纳价值的证明。

## Intake Boundary

```yaml
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
```

## 静态检查范围

| 区域 | 主要锚点 | 检查目的 |
|---|---|---|
| 定位与功能面 | `README.md:5-50` | 确认它是一体化自托管 AI 工作台，而不是专用知识权威系统。 |
| 运行架构 | `docs/setup.md:728-744`, `app.py`, `docker-compose.yml` | 确认 FastAPI + 原生前端 + SQLite/JSON/ChromaDB + SearXNG/ntfy 的组合。 |
| Agent 编排 | `src/agent_loop.py` | 确认模型路由、上下文、工具选择、多轮执行和审批在一个大型编排模块中会合。 |
| 外部内容隔离 | `src/prompt_security.py:8-99`, `src/tool_capabilities.py:553-674` | 确认 untrusted wrapper、server-owned 运行状态和 effect gate 的静态形状。 |
| 精确动作审批 | `src/tool_approvals.py:89-470`, `src/agent_loop.py:5680-5767` | 确认服务端绑定字段、摘要、TTL、一次性 claim 和 UI 展示副本。 |
| Agent 迁移 | `docs/agent-migration.md:1-26`, `docs/agent-migration.md:166-194` | 确认 archive document 与 reviewable memory candidate 的文档契约。 |
| 自动记忆路径 | `services/memory/memory_extractor.py:448-471` | 定位自动抽取后直接写入并可 pin identity 的风险路径。 |
| 安全与稳定性自述 | `SECURITY.md`, `THREAT_MODEL.md`, `ROADMAP.md`, `CONTRIBUTING.md` | 记录私网/管理台信任边界、无 shell/filesystem sandbox、未完成审计项和 dev/main 分支差异。 |
| 许可与来源归因 | `LICENSE`, `ACKNOWLEDGMENTS.md` | 确认顶层 copyleft 声明及内嵌/改编上游项目声明。 |

## 初步看点

- 它的产品架构是“单一自托管工作台 + 特权 Agent 工具面 + 多模型/本地服务适配”。
- 最有可回访价值的源码形状是：外部内容标为不可信，运行状态记录影响，高影响工具进入另行用户授权。
- 工具能力被归类为读取、写入、执行、网络、外部副作用、管理变更和破坏性效果；未知工具默认 fail high。
- `agent-migration.v1` 文档将长期原始资料与待审核的短记忆候选分开，但当前自动记忆抽取代码仍存在直接持久化路径，两者不能被当作同一条全局边界。
- 官方已包含安全政策、威胁模型、CI/CodeQL/供应链工作流和大量测试文件；本次没有复现它们，因此不生成运行时验证结论。

## 明显疑点

- `dev` 是默认且快速演进的分支；`main` 被称为较 curated，但捕获时两者已分叉，且没有 GitHub tag/release。
- `THREAT_MODEL.md` 明示它面向信任用户和私有网络，并承认无 shell/filesystem sandbox 和无网络出口限制。
- 部分 Python 依赖、容器镜像和启动时工具不是 digest-pinned，默认构建可能随时间漂移。
- 安全文档和架构盘点存在与当前代码不同步的迹象；文档中的 known gap 是检查路由，不能在未做运行时/调用链审计时自动视为已解决或已证实仍存在。
- 顶层许可是 AGPL；研究机制与复制/改编代码是两件事，后者需另行做许可兼容评估。
- 仓库很新且 GitHub 热度很高；这些信号不能替代 commit、评审、隔离和可复现证据。

## 可抽取 Candidate Points

1. 将“外部内容已影响当前运行”作为 server-owned 完整性状态，再按工具 effect 决定是否需要另行授权。
2. 工具可见性/检索和实际执行权应分离；模型选中工具不等于获得权限。
3. 用户审批可以绑定为精确的 owner/session/run/tool/content/workspace/document/effect 载荷，并采用 TTL、一次性 claim 和服务端摘要。
4. Agent 迁移应先进入中立 manifest，长文/会话作为可追溯 archive，短事实只作为待审核 memory candidates。
5. 任何“自动抽取后直接写 memory”的路径都需要与候选/审核/项目作用域边界分开处理。

## Source Annotation Sidecars

```yaml
source_annotation_refs:
  - annotation_id: odysseus-exact-action-binding-payload
    path: outputs/review/source_annotations/2026-08-24-odysseus-dev-odysseus/odysseus-exact-action-binding-payload.md
    anchor_status: exact_verified
  - annotation_id: odysseus-external-context-effect-gate
    path: outputs/review/source_annotations/2026-08-24-odysseus-dev-odysseus/odysseus-external-context-effect-gate.md
    anchor_status: exact_verified
  - annotation_id: odysseus-auto-memory-direct-write-risk
    path: outputs/review/source_annotations/2026-08-24-odysseus-dev-odysseus/odysseus-auto-memory-direct-write-risk.md
    anchor_status: exact_verified
```

## 当前处理等级

```yaml
processing_tier: medium
heavy_recommended: true
```

推荐以后在用户明确说“强蒸馏”时，再做 commit-pinned 的跨模块调用链、`dev`/`main` 差异、授权作用域、记忆写入路径、威胁模型漂移和安全证据完整评审。本次不会自动升级。

## 本次未执行

- 任何仓库测试或 benchmark。
- 任何依赖安装。
- `docker compose up`、应用启动、模型服务、网页操作或实际工具调用。
- 仓库快照、架构评审、Project Overlay、pattern、decision、index 或 handoff 产物。

## 下一步

- 候选级定位见 `outputs/review/2026-08-24-odysseus-dev-odysseus-candidate-distillation.md`。
- 将三个 annotation 仅作为源码定位器与后续评审输入，不得当作 evidence support。

