---
type: pattern
status: active
created: 2026-05-27
updated: 2026-05-27
source_libraries:
  - OpenKB
related_concepts:
  - "[[static-wiki-health-lint-before-auto-rewrite]]"
  - "[[2026-05-27-openkb-architecture-review]]"
related_projects:
  - verified-knowledge-system
adoption_status: adopt
tags:
  - pattern/lint
  - wikilinks
  - write-validator
evidence_count: 1
confidence: high
negative_evidence:
replaces:
superseded_by:
relations:
  - target: "[[static-wiki-health-lint-before-auto-rewrite]]"
    type: refines
    strength: 4
    confidence: high
    evidence:
      - "[[ghost-wikilink-whitelist-before-write]]"
    rationale: "Ghost wikilink filtering is a concrete write-time lint rule for LLM-generated Markdown."
    created: 2026-05-27
    last_verified: 2026-05-27
extension_points:
  - lint rule packs
  - compile strategies
  - review workflows
---

# 设计模式：Ghost Wikilink Whitelist Before Write

## 一句话定义

LLM 写入 Markdown 前，先给它合法 wikilink 白名单；写入前再程序化清洗不存在的链接，防止知识图谱出现幻觉边。

## 解决的问题

LLM 很容易生成看似合理但不存在的 `[[wikilinks]]`。

这些 ghost links 会污染：

- Obsidian 图谱。
- context pack ranking。
- review 导航。
- future graph health。

OpenKB 的做法是：

```text
list existing targets
add planned targets from current compile
give whitelist to LLM
strip unresolved wikilinks before write
```

## 适用场景

- LLM 生成 summary、claim、pattern、concept、decision。
- 需要 Obsidian wikilinks。
- 图谱关系会影响后续 agent 上下文加载。

## 不适用场景

- 纯文本草稿，不需要图谱。
- 刻意记录 missing target 的 review candidate。
- 使用显式 `relations` 而不是 wikilinks 的关系。

## 反例与避坑

- 失败条件：清洗时误删用户手写但尚未创建的计划链接。
- 相似反模式：把 LLM 幻觉链接当成关系证据。
- 复杂度风险：fuzzy normalization 误合并不同节点。
- 替代方案：unknown links 进入 lint warning，不自动删除。

## 来源证据

OpenKB `compiler.py` 有 known target whitelist；`lint.py` 有 `strip_ghost_wikilinks`，能保留合法目标、规范 fuzzy match、把无效链接降级为普通文本。

## 标签与量化

- domain: lint / graph hygiene
- problem: hallucinated links
- maturity: proven
- complexity: low
- problem_fit: 5
- reuse_value: 5
- implementation_cost: 2
- integration_fit: 5
- evidence_strength: 4
- reversibility: 4

## 交叉验证

- 相似来源：OpenKB、llm-wiki-compiler static lint、Obsidian graph hygiene。
- 历史项目影子：本资料库已经把 relations 作为核心字段，wikilinks 不能乱。
- 支持证据：OpenKB 源码把 ghost link 清洗作为编译路径的一部分。
- 反例：有些新节点还未创建，提前链接可能是合理计划。

## 最小实现方式

在 candidate compile 后运行：

```text
known_targets = all wiki md nodes
planned_targets = candidates in same batch
for every [[target]]:
  if target in known_targets or planned_targets: keep
  else: mark lint warning or convert to plain text
```

v0.1 不建议静默删除，优先写入 lint report。

## 项目融合建议

立即吸收为 `LINT_RULES.md` 的规则。

## 可拓展性

- 可以通过什么接口/适配层接入：lint rule pack、compile strategy、review workflow。
- 未来可能被什么替代：formal node registry、graph database constraint。
- 替换或升级成本：低。
- 回退方式：Obsidian broken-link scan + manual fix。

## 验证指标

- LLM 生成不存在链接时能被发现。
- 合法链接不被误删。
- planned candidate links 能被允许或标记为 pending。
- context pack 不使用 broken link 做 ranking。
