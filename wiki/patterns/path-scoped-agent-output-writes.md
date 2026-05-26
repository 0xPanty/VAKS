---
type: pattern
status: active
created: 2026-05-27
updated: 2026-05-27
source_libraries:
  - OpenKB
related_concepts:
  - "[[agent-tool-access-tiering]]"
  - "[[2026-05-27-openkb-architecture-review]]"
related_projects:
  - verified-knowledge-system
adoption_status: adopt
tags:
  - pattern/agent-access
  - path-safety
  - reviewed-write
evidence_count: 2
confidence: high
negative_evidence:
replaces:
superseded_by:
relations:
  - target: "[[agent-tool-access-tiering]]"
    type: refines
    strength: 5
    confidence: high
    evidence:
      - "[[path-scoped-agent-output-writes]]"
    rationale: "OpenKB provides a concrete implementation of read-wide/write-narrow agent tooling."
    created: 2026-05-27
    last_verified: 2026-05-27
extension_points:
  - agent access tiers
  - output adapters
  - review workflows
---

# 设计模式：Path-Scoped Agent Output Writes

## 一句话定义

Agent 可以广泛读取知识库，但写入必须限制在候选区、输出区或目标 artifact 目录，不能直接改 formal truth layer。

## 解决的问题

Agent 写权限太大时，会出现：

- 误改正式知识节点。
- prompt injection 诱导修改。
- 输出 artifact 和 truth layer 混在一起。
- 回滚困难。

OpenKB 的做法是：

```text
query agent: read wiki
chat write tool: only wiki/explorations/** and output/**
skill agent: only target skill root
```

这和我们的权限层完全一致。

## 适用场景

- 给 Misa/gbrain/Hermes/Codex 暴露资料库。
- 允许 agent 生成 query result、skill、report、review candidate。
- 不允许 agent 自己批准 formal node。

## 不适用场景

- 需要人类手动维护的纯 Markdown 库。
- agent 不具备本地文件访问能力。
- 系统已经有更强的事务/审批层。

## 反例与避坑

- 失败条件：工具只靠 prompt 约束，不做路径解析和 allowlist。
- 相似反模式：agent 直接写 `wiki/claims` 或 `wiki/decisions`。
- 复杂度风险：路径规则太细导致可用性下降。
- 替代方案：所有 agent 输出都进 `outputs/review/`。

## 来源证据

OpenKB 的 `agent/tools.py` 对读写路径做 resolve + is_relative_to 检查；写入只允许 `wiki/explorations/**` 和 `output/**`。Skill 写工具在 `skill/tools.py` 中限制到 skill root。

## 标签与量化

- domain: agent safety
- problem: untrusted writes
- maturity: proven
- complexity: low
- problem_fit: 5
- reuse_value: 5
- implementation_cost: 2
- integration_fit: 5
- evidence_strength: 5
- reversibility: 5

## 交叉验证

- 相似来源：OpenKB、llm-wiki-compiler MCP read-only resources、obsidian-second-brain write validator。
- 历史项目影子：Misa 需要读取资料库和提出候选，但不能直接改 verified truth。
- 支持证据：多个 agentic vault 方案都需要 write boundary。
- 反例：纯 CLI 本人操作可以直接编辑，但 agent 不应默认同权。

## 最小实现方式

定义路径权限：

```yaml
agent_access:
  read:
    - raw/**
    - wiki/**
    - outputs/**
  write:
    - outputs/review/**
    - outputs/qa/**
    - products/drafts/**
  forbidden_write:
    - wiki/claims/**
    - wiki/patterns/**
    - wiki/decisions/**
```

formal nodes 只能通过 review/approve 工具写入。

## 项目融合建议

立即吸收为 `AGENT_ACCESS.md` 的核心规则。

## 可拓展性

- 可以通过什么接口/适配层接入：agent access tiers、MCP tools、CLI tools。
- 未来可能被什么替代：capability token、transactional review API。
- 替换或升级成本：低。
- 回退方式：agent 只读，用户/Codex 手动写入。

## 验证指标

- 尝试 path traversal 是否被拒绝。
- agent 是否无法写 formal wiki。
- candidate/output 是否能正常写入。
- review approve 是否是唯一 formal write path。
