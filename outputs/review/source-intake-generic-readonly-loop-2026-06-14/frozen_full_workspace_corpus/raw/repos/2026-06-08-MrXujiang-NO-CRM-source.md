---
type: source
record_kind: source_card
status: source-captured
title: "MrXujiang/NO-CRM"
source_id: github-MrXujiang-NO-CRM
source_uri: https://github.com/MrXujiang/NO-CRM
source_url: https://github.com/MrXujiang/NO-CRM
source_type: repository
version_or_commit: 373750dee5b8ddf79b1e38c07e5914e8fad99aef
checked_commit: 373750dee5b8ddf79b1e38c07e5914e8fad99aef
commit_time: "2026-01-08T09:09:40+08:00"
captured_at: "2026-06-08 05:30:00 +08:00"
captured_by: Codex
raw_location: raw/repos/2026-06-08-MrXujiang-NO-CRM-source.md
snapshot_location: raw/repos/_snapshots/2026-06-08-MrXujiang-NO-CRM-373750d-anchor-bundle.zip
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
access_boundary: public
source_status: active
topics:
  - crm
  - enterprise-workbench
  - rbac
  - workflow
  - forms
  - vue
  - nestjs
projects:
  - verified-action-knowledge-system
source_family: xujiang-flowmix-enterprise-app-ecosystem
upstream_sources: []
verification_status: primary-source-captured
candidate_relation_suggestions: []
tags:
  - raw-repo
  - github
  - candidate-only
why_saved: see_body_or_legacy_record
---

# 仓库资料：MrXujiang/NO-CRM

## 为什么收录

用户指出这个仓库可能是小红书视频里讲的开源库。检查后，当前判断是：`MrXujiang/NO-CRM` 不是视频里展示的 AI 知识库源码，而是一个轻量 CRM 系统。它的 README 里另列了 “AI知识库平台：https://ai.flowmix.cn”，这只能说明作者产品线附近存在 AI 知识库产品，不能把 NO-CRM 和视频合并成同一个知识点。

本卡只保留为独立 repo source card：它可作为 CRM / 企业应用壳的低强度参考，但不和小红书 AI 知识库视频合并蒸馏。仓库本身还存在明显 source hygiene 风险，不能作为高强度实现参考。

## Source Status

```text
Repository: MrXujiang/NO-CRM
URL: https://github.com/MrXujiang/NO-CRM
Description: NO-CRM，一款Vue3 实现的全栈CRM系统
Checked commit: 373750dee5b8ddf79b1e38c07e5914e8fad99aef
Commit time: 2026-01-08T09:09:40+08:00
Stars at capture: 131
Forks at capture: 41
Default branch: main
```

## Capture Boundary

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

Repository source records provide provenance, anchors, and candidate extraction
input. They do not create reviewed architecture decisions or action basis.

## 获取方式与快照

本次没有保存全量仓库快照，而是保存轻量 anchor bundle：

```text
raw/repos/_snapshots/2026-06-08-MrXujiang-NO-CRM-373750d-anchor-bundle.zip
```

原因：

```text
GitHub zip 下载失败一次；随后 shallow clone 能取到对象，但 checkout 在 Windows 上因仓库内跟踪的 node_modules / dist 长路径失败。
仓库 HEAD 约 58,731 个文件，其中绝大多数是 backend/node_modules、backend/dist、frontend/dist 等依赖或生成物。
因此本次只保留 README、文件列表和少量可读 anchor 文件，避免把巨量生成/依赖内容当成源码证据。
```

## Files / Code Anchors

| Anchor | What exists | Design extraction | Boundary |
|---|---|---|---|
| `readme.md` | 项目定位为轻量级 CRM，列出 Vue 3 / NestJS / TDesign / RBAC / workflow / form / AI assistant / JSON storage | 证明 NO-CRM 是 CRM 企业应用壳，不是 AI 知识库仓库 | README 是项目自述，不等于实现质量证据 |
| `readme.md` 合作产品 | 列出协同 AI 文档、H5 零代码平台、AI 知识库平台、pxcharts 多维表格 | 说明作者产品线附近有 AI 知识库线索 | 不能证明 NO-CRM 就是视频源码，也不能合并成同一个知识点 |
| `.server.js` | 静态文件服务 + API proxy + SPA fallback | 说明这是可部署演示应用壳 | 不是 VAKS 适配层参考 |
| `backend/dist/app.module.js` | 模块包括 permissions、roles、departments、users、auth、customers、leads、activities、tasks、statistics、upload、contracts、products、orders、recommendation、forms、workflows | 企业应用模块组合比较完整，可作 workbench breadth 参考 | dist 编译产物，不是源代码设计文档 |
| `backend/dist/auth/permissions.guard.js` | 基于 `RequirePermissions` metadata、user/admin、roleId、permissionIds 做权限判断 | RBAC / permission guard 可作 Agent Access / workbench 权限启发 | 不能直接移植；需看源码、测试和真实策略 |
| `backend/dist/common/json-storage.service.js` | JSON 文件读写、CRUD、分页式存储服务 | 适合 demo / prototype 的低门槛数据层 | 不适合 VAKS reviewed truth 或长期可靠数据源 |
| `backend/dist/workflows/workflows.service.js` | workflow definition、start/end node、发布版本等 | 工作流 / 编排入口与企业操作面相关 | 不是证据审查流程 |
| `backend/dist/forms/forms.service.js` | 表单草稿、发布、分享 URL、提交计数、owner/admin 检查 | 表单和收集入口可启发 capture/workbench | 不是知识 intake schema |
| `backend/data/*.json` | roles、permissions、workflow-definitions、forms 等为空数组 | 仓库内演示数据最小化 | 空数据不能证明真实权限模型成熟 |

## 人话判断

这不是视频里的 AI 知识库开源库。更准确说法是：

```text
视频 = AI 知识库产品展示。
NO-CRM = 轻量 CRM / 企业应用壳开源仓库。
两者不是同一个项目，不合并成一个知识点。
本卡只记录 NO-CRM 自身，外加“已排除它是视频源码”的判断。
```

## 可抽取 Candidate Points

- 企业知识产品最终需要一个企业应用壳：登录、组织、角色、权限、表单、工作流、看板、任务和集成入口。
- NO-CRM 的 RBAC / workflow / forms 对 VAKS 的 Agent Access、Use Ledger、capture form、operator workbench 有启发价值。
- JSON 文件存储适合开箱 demo，不适合 VAKS 的 reviewed truth 或 action-basis 长期存储。
- 仓库把大量依赖 / 编译产物纳入版本库，是 source hygiene 风险；这种 repo 不能作为高置信代码参考。
- README 的合作产品列表只能辅助排查关系，不能把两个项目合并成同一源码来源或同一知识点。

## 可借鉴

- 企业级 workbench 的模块广度：用户、部门、角色、权限、任务、合同、订单、统计、表单、工作流。
- RBAC permission guard 对未来 Agent Access / 操作权限层的启发。
- 表单和工作流作为 capture / action / feedback 入口。
- 演示环境和开箱即用的产品包装思路。

## 不能直接借鉴

- 不能把 NO-CRM 的 CRM 业务模型搬进 VAKS core。
- 不能把 JSON 文件存储作为 VAKS truth store。
- 不能把 dist / node_modules 版本库结构当成好实践。
- 不能把 README 中的 AI assistant / recommendation 当作 AI 知识库实现证据。
- 不能把测试账号、默认管理员账号或 demo 配置当成生产安全模式。

## 风险和不确定

- 当前 HEAD 缺少清晰的 `backend/src` / `frontend/src` 源码树；大量文件是依赖或生成物。
- 只做了 anchor bundle，而非完整源码快照。
- README 与实际仓库文件结构之间有不一致：README 展示源码开发结构，HEAD 更像生产发布包。
- 与小红书视频不是同一项目；如果要研究视频里的 AI 知识库，应另找对应产品官网、文档或仓库。

## VAKS 归位

```text
Capture:
  表单、上传、任务入口可作为未来 workbench 输入面参考。

Understand:
  AI assistant / recommendation 只可作为候选产品能力，不可作为理解质量证据。

Review:
  RBAC / workflow 是操作权限和流程，不是 evidence-aware review。

Connect:
  CRM 实体关系不适合进入 VAKS core；组织 / 用户 / 权限关系可作为 workbench 边界参考。

Activation / Context Pack:
  企业应用 shell 可承载 context pack 和 operator cockpit。

Decision / Action:
  该仓库不能作为 VAKS action basis；只能做 design-only 参考。

Use Ledger / Feedback:
  表单、任务、工作流可启发 feedback-event / action follow-up 入口。
```

## 融合判断

- Direct use: no
- Fork: no
- Design-only: yes
- Current branch value: medium-low
- Whole architecture value: medium
- Evidence strength: low-medium
- Reuse value: medium
- Risk: repo source hygiene and generated/dependency bloat
- Next action: 不和视频合并；如后续需要，只作为独立 CRM / 企业应用壳参考，或另找真正的 AI 知识库来源
