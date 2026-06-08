---
type: pattern
status: active
created: 2026-05-27
updated: 2026-05-27
source_libraries:
  - OpenKB
related_concepts:
  - "[[source-hash-registry-and-idempotent-ingest]]"
  - "[[ghost-wikilink-whitelist-before-write]]"
related_projects:
  - verified-knowledge-system
adoption_status: adopt
tags:
  - pattern/lifecycle
  - source-removal
  - rollback
evidence_count: 1
confidence: high
negative_evidence:
replaces:
superseded_by:
relations:
  - target: "[[source-hash-registry-and-idempotent-ingest]]"
    type: refines
    strength: 4
    confidence: high
    evidence:
      - "[[removal-cleanup-with-registry-commit-point]]"
    rationale: "Source removal should use registry state as the final commit point so failures remain retryable."
    created: 2026-05-27
    last_verified: 2026-05-27
extension_points:
  - review workflows
  - lint rule packs
  - source adapters
---

# 设计模式：Removal Cleanup With Registry Commit Point

## 一句话定义

删除 source 时，先清理可重试的派生产物和外部状态，最后再更新 registry；registry 更新是提交点，失败前保留状态以便重试。

## 解决的问题

知识库不是只会 add，也会 remove / replace。

如果删除流程不严谨，会出现：

- raw 删除了，但 summary/concept/claim 还在。
- index 还指向不存在文件。
- 外部索引仍保留旧 doc。
- registry 先删了，后续失败时找不到 doc_id，无法重试。

OpenKB 的删除流程值得借鉴：先 dry-run 列出动作，确认后删除 summary/source/images，更新 concept sources，更新 index，清理 dangling wikilinks，清 PageIndex state，最后才 remove registry hash。

## 适用场景

- source 被误入库。
- source 有新版，需要替换。
- 某个来源被判定低质量或失效。
- 外部索引/派生文件需要同步清理。

## 不适用场景

- verified decision 已经依赖该 source，需要先做影响分析。
- 法务/审计要求不能物理删除，只能标记 deprecated。
- raw source 必须长期保留。

## 反例与避坑

- 失败条件：先删 registry，再清派生产物。
- 相似反模式：删除 raw 后留下 broken graph。
- 复杂度风险：自动删除 formal truth 可能破坏历史。
- 替代方案：v0.1 先标记 `deprecated/rejected`，不物理删除 formal nodes。

## 来源证据

OpenKB `cli.py remove` 有 `--dry-run`、`--keep-raw`、`--keep-empty-concepts`、确认提示；删除中明确把 registry write 作为 commit point，PageIndex cleanup 失败时保留 registry entry 供重试。

## 标签与量化

- domain: lifecycle
- problem: safe source removal
- maturity: emerging
- complexity: medium
- problem_fit: 4
- reuse_value: 4
- implementation_cost: 3
- integration_fit: 4
- evidence_strength: 4
- reversibility: 4

## 交叉验证

- 相似来源：OpenKB remove pipeline、llm-wiki-compiler source state lifecycle。
- 历史项目影子：资料库后续一定会替换错误资料或过期资料。
- 支持证据：OpenKB 源码把删除流程写得比 add 更谨慎。
- 反例：verified system 不能无脑删 formal node，更多时候应该标记 superseded。

## 最小实现方式

v0.1 不做物理删除自动化，先做状态化：

```yaml
status: deprecated | rejected | superseded
superseded_by:
deprecation_reason:
affected_nodes:
```

实现删除工具时，顺序必须是：

```text
plan/dry-run
owner confirm
mark affected nodes
clean derived indexes
clean external adapter state
update registry commit point last
append log
```

## 项目融合建议

中期吸收为 source lifecycle 工具。

短期只写进 `IMPLEMENTATION_BLUEPRINT.md` 和 `LINT_RULES.md`：检查 deprecated source 是否仍被 active decision 使用。

## 可拓展性

- 可以通过什么接口/适配层接入：source registry、lint rule、review workflow。
- 未来可能被什么替代：transaction log / migration runner。
- 替换或升级成本：中等。
- 回退方式：保留 raw 和 source record，手动修复 index。

## 验证指标

- dry-run 是否列出所有影响。
- 失败后是否能重跑。
- active decision 是否不会静默失去 source。
- 外部索引是否不会保留旧 doc。
