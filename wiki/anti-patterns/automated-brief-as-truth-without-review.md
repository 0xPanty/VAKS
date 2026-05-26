---
type: anti-pattern
status: active
created: 2026-05-27
updated: 2026-05-27
domain: verified-knowledge-system
failure_mode: "Treating automated daily/weekly briefs as verified truth without review."
severity: 4
likelihood: 4
complexity_cost: 3
cross_validated_with:
  - "[[direct-compile-to-truth-layer-without-review]]"
  - "[[automatic-agentic-vault-rewrite-before-schema-stability]]"
related_projects:
  - verified-knowledge-system
replacement:
  - review-gated daily brief
  - weekly synthesis as candidate generator
relations:
  - target: "[[daily-brief-as-knowledge-return-loop]]"
    type: risk_of
    strength: 4
    confidence: medium
    evidence:
      - "[[automated-brief-as-truth-without-review]]"
    rationale: "Daily briefs are useful only if treated as review outputs, not formal truth."
    created: 2026-05-27
    last_verified: 2026-05-27
decision: avoid
---

# 反模式 / 踩坑：把自动 Brief 当成已验证真相

## 问题描述

Daily brief 和 weekly synthesis 很有用，但它们是 agent 生成的二级综合。

如果直接把 brief 里的连接、模式、问题或 one action 当成 verified truth，就会绕过本资料库的 review gate。

## 为什么不可行

自动 brief 可能：

- 引用未验证 capture。
- 过度解释用户近期兴趣。
- 把巧合当模式。
- 把 question 包装成 action。
- 漏掉负面证据。

## 失败条件

- brief 写入 `wiki/claims` 或 `wiki/decisions`。
- 用户/Misa 直接按 brief 行动。
- brief 不区分 verified/unverified。
- brief 没有 sources、confidence、gaps。

## 标签与量化

- domain: feedback automation
- failure_mode: generated synthesis treated as truth
- severity: 4
- likelihood: 4
- complexity_cost: 3
- evidence_strength: 3
- reversibility: 4

## 交叉验证

- 相似失败来源：[[direct-compile-to-truth-layer-without-review]]、[[automatic-agentic-vault-rewrite-before-schema-stability]]
- 历史项目证据：本资料库已明确 automation 先报问题，不直接裁决。
- 支持证据：用户粘贴文章强调自动 brief，但没有 verified truth layer。
- 是否可能只是局部失败：是。普通个人 vault 可以接受更松自动化；本资料库不能。

## 应该避开什么

不要让：

```text
daily brief
weekly synthesis
Claude-generated pattern
N8N scheduled output
```

直接进入 formal truth。

## 替代方案

正确路径：

```text
daily/weekly output
-> outputs/review
-> candidate claim/pattern/decision
-> lint/review
-> formal node
```

## 后续是否需要复测

需要。等 `REVIEW_QUEUE.md` 和 `LINT_RULES.md` 写完后，复查 daily/weekly brief 应该落在哪个目录、需要哪些字段。
