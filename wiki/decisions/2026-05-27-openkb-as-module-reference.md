---
type: decision
status: active
created: 2026-05-27
updated: 2026-05-27
decision: "OpenKB 作为模块级实现参考纳入，不作为主架构或 truth schema。"
related_projects:
  - verified-knowledge-system
based_on:
  - "[[2026-05-27-openkb-source]]"
  - "[[2026-05-27-openkb-architecture-review]]"
  - "[[ARCHITECTURE_PRINCIPLES]]"
  - "[[SCHEMA]]"
patterns:
  - "[[wiki-foundation-generator-surface-separation]]"
  - "[[long-document-tree-index-source-adapter]]"
  - "[[knowledge-to-agent-skill-factory]]"
  - "[[path-scoped-agent-output-writes]]"
  - "[[ghost-wikilink-whitelist-before-write]]"
  - "[[source-hash-registry-and-idempotent-ingest]]"
  - "[[url-source-ingest-normalization]]"
  - "[[removal-cleanup-with-registry-commit-point]]"
  - "[[artifact-trigger-and-body-alignment-eval]]"
  - "[[skill-artifact-iteration-workspace-rollback]]"
outcome: adopted
evidence_strength: high
verification_status: active
evidence_level: synthetic
confidence: high
last_verified: 2026-05-27
next_review: 2026-06-03
negative_evidence:
  - "[[auto-compiled-concept-wiki-as-verified-truth-layer]]"
replaces:
relations:
  - target: "[[2026-05-27-quality-bar-extensible-verified-action-knowledge-system]]"
    type: supports
    strength: 4
    confidence: high
    evidence:
      - "[[2026-05-27-openkb-as-module-reference]]"
    rationale: "OpenKB adds implementation modules for long-doc ingest and skill output while preserving the higher-level verified action architecture."
    created: 2026-05-27
    last_verified: 2026-05-27
migration_path: "Map OpenKB ideas into source adapters, output adapters, lint rule packs, and agent access tiers."
rollback_path: "If OpenKB modules prove too heavy, keep the Markdown contracts and use manual source windows/context packs."
---

# 决策记录：OpenKB 作为模块级参考纳入

## 决策

采用 OpenKB 作为模块级实现参考，但不采用它作为主架构，也不采用它的 generic concept wiki schema 作为 truth layer。

本资料库吸收：

```text
long document tree source adapter
wiki foundation / generator surface separation
knowledge-to-agent skill factory
path-scoped agent writes
ghost wikilink whitelist
source hash registry / idempotent ingest
URL source ingest normalization
remove cleanup with registry commit point
skill trigger/body alignment eval
skill artifact iteration workspace / rollback
```

本资料库不吸收：

```text
direct concept auto-rewrite as verified truth
summary/concept/exploration as core node schema
watch auto-compile into formal wiki
query answer as decision record
```

## 背景

用户要求继续提炼 `VectifyAI/OpenKB`。该库与我们当前主线非常接近：它也是 Karpathy LLM Wiki 风格，但多了 PageIndex 长文档处理和 Skill Factory。

因此它不是无关插件，也不是直接替代品，而是一个强实现参考。

## 依据

- OpenKB README 明确 raw -> wiki -> query/chat/skill 的工作流。
- 源码显示它有可复用的 source adapter、compiler、query agent、lint、skill factory、validator/evaluator/workspace、hash registry 和 retryable remove lifecycle。
- 本资料库已经通过 `ARCHITECTURE_PRINCIPLES.md` 确认：外部设计是输入，不是主架构裁决者。
- 本资料库核心节点已经定为 source / summary / claim / pattern / anti-pattern / decision / qa / implementation-note。

## 量化判断

- problem_fit: 5
- reuse_value: 5
- implementation_cost: 4
- integration_fit: 4
- evidence_strength: 4
- reversibility: 4

## 交叉验证

- 相似库/产品/论文：Karpathy LLM Wiki、llm-wiki-compiler、OpenKB、PageIndex、Codex/Claude skills。
- 历史项目证据：用户需要 Misa/Hermes 读取可信资料库，未来可能需要把稳定知识编译成可复用 agent 能力。
- 支持证据：OpenKB 已把 long-doc ingest、query/chat、skill output 做成 CLI。
- 反例或失败边界：OpenKB 直接更新 concept pages，缺少本资料库要求的 review gate 和 actionability。

## 备选方案

1. 直接采用 OpenKB。  
   结论：拒绝。它的 schema 不够 verified/action-oriented。

2. 完全不采用。  
   结论：拒绝。它的 PageIndex 和 Skill Factory 思路很有价值。

3. 作为模块参考吸收。  
   结论：采用。

## 可拓展性与迁移

- 是否绑定特定工具/库：不绑定。PageIndex 可以替换成其他 long-doc adapter。
- 后续新方案如何接入：只要输出 source windows、candidate nodes、lint report、context pack 或 skill candidate，就可以替换。
- 迁移路径：先在设计文档中吸收 contract，再在 implementation blueprint 中决定是否接入 OpenKB/PageIndex。
- 回退路径：保留 raw source 和 Markdown verified nodes，禁用 OpenKB runtime。

## 为什么这样选

OpenKB 很强，但强在 runtime 和 output layer，不强在 verified truth schema。

我们要的是更大的系统：

```text
OpenKB compiler/generator mechanics
+ verified truth layer
+ review queue
+ action basis
+ relation strength
+ feedback timeline
```

## 风险

- 被 OpenKB 的现成 CLI 诱惑，过早跳到 runtime。
- Skill Factory 很吸引人，但可能在 context pack / review queue 未稳定前分散注意。
- PageIndex 引入外部依赖和成本。
- watch 自动编译可能绕过 review。

## 避坑与反模式

- 相关反模式：[[auto-compiled-concept-wiki-as-verified-truth-layer]]
- 不采用哪些做法：不让 `concepts/` 替代 `claim/pattern/decision`。
- 失败边界：OpenKB 输出只能进 candidate/review/output，不能直接进 formal truth。
- 回退方案：Markdown-only source windows + manual review。

## 验证方式

后续如果接入 OpenKB 思路，验证标准是：

1. 长 PDF 是否能产出可追溯 source windows。
2. compiler 输出是否能进入 review queue，而不是直接写 truth。
3. Skill candidate 是否能引用 verified nodes 和 known gaps。
4. agent 写权限是否被路径限制。
5. ghost links 是否能被 lint 捕获。

## 复盘

2026-05-27：完成 README + source-level 第一轮提炼。结论是“模块级纳入，不做主架构替代”。
