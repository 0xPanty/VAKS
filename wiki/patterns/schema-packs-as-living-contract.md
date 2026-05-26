---
type: pattern
status: draft
created: 2026-05-26
source_libraries:
  - garrytan/gbrain
related_concepts:
  - schema-md-as-ai-wiki-contract
related_projects:
  - verified-knowledge-system
adoption_status: watch
tags:
  - schema
  - contract
  - versioning
evidence_count: 1
confidence: medium
negative_evidence:
  - copying-full-second-brain-runtime-before-schema-stabilizes
replaces:
superseded_by:
extension_points:
  - SCHEMA.md
  - future-schema-pack
---

# 设计模式：Schema packs as living contract

## 一句话定义

把页面类型、路径规则、关系类型、可抽取字段、路由规则做成可版本化契约，让 AI 和代码按同一套规则写入和检索。

## 解决的问题

当资料库类型变多时，硬编码目录和字段会碎。schema pack 让“什么算合法知识节点”成为可审查、可演化的文件。

## 适用场景

- 多类型知识节点：source、claim、pattern、anti-pattern、decision、project、output。
- 未来要让 AI 自动创建/修改节点。
- 检索缓存需要按 schema version 隔离，避免旧规则污染新结果。

## 不适用场景

- 当前最早期 schema 还没稳定时，不应该直接做动态 pack engine。
- 只有几十条笔记的小库。

## 反例与避坑

- 失败条件：让 LLM 自动改 schema，导致契约漂移。
- 相似反模式：每个模板字段都随手变，没有统一枚举。
- 复杂度风险：为了 schema pack 过早写 runtime、migration、validator。
- 替代方案：第一阶段只写人类可读的 `SCHEMA.md`。

## 来源证据

- gbrain `docs/architecture/schema-packs.md` 设计 active pack、pack version、page types、link types、expert routing。
- gbrain `src/core/schema-pack/base/gbrain-base.yaml` 把 page types、link types、frontmatter link rules、filing rules 写成 manifest。
- gbrain 搜索缓存和 schema pack 版本绑定，防止不同 schema 下的结果污染。

## 标签与量化

- domain: schema-governance
- problem: evolution-contract
- maturity: emerging
- complexity: high
- problem_fit: 4
- reuse_value: 5
- implementation_cost: 4
- integration_fit: 4
- evidence_strength: 4
- reversibility: 3

## 交叉验证

- 相似来源：Orange Book 的 `SCHEMA.md as AI wiki contract`。
- 支持证据：当前主线缺口第一项就是统一 `SCHEMA.md`。
- 反例：gbrain 的完整 schema pack runtime 当前对我们过重。

## 最小实现方式

先做：

```text
SCHEMA.md
  - node_types
  - required_fields
  - enum_values
  - relation_types
  - promotion_flow
  - health_checks
```

后做：

```text
schema-pack-v1.yaml
validator
cache/version hash
```

## 项目融合建议

理念立即采用，runtime 暂缓。

## 验证指标

- 新增笔记能按 `SCHEMA.md` 自动检查字段。
- 关系类型和状态枚举不再散落在聊天里。
- 后续脚本能从 schema 生成 Bases 视图或 health check。

