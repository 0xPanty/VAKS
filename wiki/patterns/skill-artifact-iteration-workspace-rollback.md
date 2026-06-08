---
type: pattern
status: active
created: 2026-05-27
updated: 2026-05-27
source_libraries:
  - OpenKB
related_concepts:
  - "[[knowledge-to-agent-skill-factory]]"
  - "[[artifact-trigger-and-body-alignment-eval]]"
related_projects:
  - verified-knowledge-system
adoption_status: adopt
tags:
  - pattern/output-adapter
  - rollback
  - iteration
evidence_count: 1
confidence: high
negative_evidence:
replaces:
superseded_by:
relations:
  - target: "[[knowledge-to-agent-skill-factory]]"
    type: refines
    strength: 4
    confidence: high
    evidence:
      - "[[skill-artifact-iteration-workspace-rollback]]"
    rationale: "Generated agent skills need history and rollback because later iterations can regress."
    created: 2026-05-27
    last_verified: 2026-05-27
extension_points:
  - output adapters
  - feedback adapters
---

# 设计模式：Skill Artifact Iteration Workspace and Rollback

## 一句话定义

生成的 skill/artifact 每次覆盖前先保存旧版本，记录结构 diff，并允许回滚；生成物也需要版本历史。

## 解决的问题

LLM 生成的 artifact 会迭代，而且新版本不一定更好。

如果没有历史：

- 好版本被覆盖。
- eval 退步后无法恢复。
- 用户/agent 在 chat 中的微调丢失。
- 不知道 description、references、scripts 变了什么。

OpenKB 的做法是：

```text
output/skills/<name>/
output/skills/<name>-workspace/iteration-N/
diff.md
rollback --to N
```

回滚本身也是 mutation，所以回滚前也保存当前版本，保证不丢工作。

## 适用场景

- skill、context pack template、workflow pack、agent prompt pack 会多次生成。
- 有 eval/validation，可能发现新版本回退。
- 用户会在 chat 里继续编辑 artifact。

## 不适用场景

- 一次性报告。
- 已经用 git 管理整个 artifact 目录且每次提交。
- artifact 很大，复制成本高。

## 反例与避坑

- 失败条件：覆盖旧 artifact 前不保存。
- 相似反模式：LLM 生成物没有版本概念。
- 复杂度风险：workspace 目录无限膨胀。
- 替代方案：Git branch/commit 管理 artifacts。

## 来源证据

OpenKB `skill/workspace.py` 在覆盖 skill 前保存 iteration，提供 list/restore，并生成 diff：description 变化、references/scripts 增删、SKILL.md 行数变化。

## 标签与量化

- domain: output lifecycle
- problem: generated artifact regression
- maturity: emerging
- complexity: low
- problem_fit: 4
- reuse_value: 4
- implementation_cost: 2
- integration_fit: 4
- evidence_strength: 4
- reversibility: 5

## 交叉验证

- 相似来源：OpenKB skill workspace、Git history、review queue candidate archive。
- 历史项目影子：Misa/Codex skills 后续一定会被反复调整。
- 支持证据：OpenKB 把 history/rollback 做成一等 CLI。
- 反例：formal truth node 不能靠 artifact rollback 替代 decision supersede。

## 最小实现方式

对所有 generator output 使用：

```text
outputs/generated/<type>/<name>/
outputs/generated/<type>/<name>-workspace/iteration-N/
outputs/generated/<type>/<name>-workspace/iteration-N/diff.md
```

或先用 git 记录，再在 artifact metadata 中写：

```yaml
artifact_version:
previous_version:
eval_status:
rollback_to:
```

## 项目融合建议

作为 output adapter 的通用生命周期规则。不要进入 core SCHEMA，但应进入 `IMPLEMENTATION_BLUEPRINT.md`。

## 可拓展性

- 可以通过什么接口/适配层接入：output adapter、feedback adapter。
- 未来可能被什么替代：Git-native artifact versioning。
- 替换或升级成本：低。
- 回退方式：从 workspace 或 git 恢复。

## 验证指标

- 覆盖前是否保存旧版本。
- rollback 是否不丢当前版本。
- diff 是否能说明关键变化。
- eval 退步时是否能恢复上一版。
