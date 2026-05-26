---
type: anti_pattern
status: avoid-default
created: 2026-05-26
domain: agent-permissions
failure_mode: broad automatic approval
severity: 5
likelihood: 4
complexity_cost: 4
cross_validated_with:
  - "Claude Code permissions docs"
  - "Yanhua content factory article"
related_projects:
  - 资料库
  - AI短剧
replacement: "默认人工确认；只对低风险、受限目录、可回退任务开放自动批准"
decision: limited-use
---

# 反模式 / 踩坑：生产资料库默认开启 yolo 权限

## 问题描述

文章作者把 Claudian 权限模式设为 yolo，自动批准所有操作，并认为配合 CLAUDE.md 使用顺畅。这个做法对成熟用户可能可行，但不适合当前资料库默认采用。

## 为什么不可行

资料库未来会包含项目资料、设计判断、发布内容、可能还有账号和素材。自动批准所有操作会增加误删、误改、误发布、泄露敏感信息和平台违规风险。

## 失败条件

- 没有 Git 或快照。
- 没有受限工作目录。
- 没有发布前确认。
- 没有 protected files。
- Skills 可以执行浏览器发布、删除、覆盖、上传等高风险动作。

## 标签与量化

- domain: agent-permissions
- failure_mode: unsafe automation
- severity: 5
- likelihood: 4
- complexity_cost: 4
- evidence_strength: 4
- reversibility: 2

## 交叉验证

- 相似失败来源：Claude Code permissions docs 明确 bypassPermissions 会批准到达该步骤的所有操作，Claude 在这种模式下拥有完整系统访问能力。
- 历史项目证据：用户强调 durable handoff、边界、不要混淆执行和审查。
- 支持证据：当前资料库正在建立 source verification 和 negative evidence，默认不应弱化边界。
- 是否可能只是局部失败：是。对低风险目录和成熟 workflow 可局部开放。

## 应该避开什么

- 新系统默认 yolo。
- 发布、删除、移动、覆盖等高风险动作无确认。
- 把 CLAUDE.md 当成权限安全边界。

## 替代方案

```text
低风险读写：可逐步 allow
模板生成/摘要：可半自动
发布/删除/账号动作：必须人工确认
受限目录：raw/wiki/outputs/products 分级权限
Git/snapshot：高风险前必须可回退
```

## 后续是否需要复测

当低风险 Skills 稳定后，可以测试“受限目录 + 自动批准 + Git diff 审查”的局部自动化。

