---
type: pattern
status: active
created: 2026-05-27
updated: 2026-05-27
source_libraries:
  - OpenKB
  - llm-wiki-compiler
related_concepts:
  - "[[source-adapter-ingest-contract]]"
  - "[[2026-05-27-openkb-architecture-review]]"
related_projects:
  - verified-knowledge-system
adoption_status: adopt
tags:
  - pattern/ingest
  - source-state
  - idempotency
evidence_count: 2
confidence: high
negative_evidence:
replaces:
superseded_by:
relations:
  - target: "[[source-adapter-ingest-contract]]"
    type: refines
    strength: 5
    confidence: high
    evidence:
      - "[[source-hash-registry-and-idempotent-ingest]]"
    rationale: "A source adapter should identify content by stable hash before compiling it."
    created: 2026-05-27
    last_verified: 2026-05-27
extension_points:
  - source adapters
  - compile strategies
  - review workflows
---

# 设计模式：Source Hash Registry and Idempotent Ingest

## 一句话定义

入库前先按内容 hash 建 registry；同一份 source 重复出现时跳过或进入 replacement 流程，避免重复编译和重复节点。

## 解决的问题

资料库会不断吸收网页、PDF、repo、会话和手动文件。如果没有内容指纹，会出现：

- 同一资料多次入库。
- 同一 source 生成多个 summary/claim。
- 删除或更新时找不到对应派生产物。
- agent 不知道某份资料是否已经处理过。

OpenKB 用 `.openkb/hashes.json` 保存 SHA-256 -> metadata，并在转换前检查是否已知。

## 适用场景

- raw source 会持续增长。
- 入库动作可能由人、Codex、Misa 或 watcher 多次触发。
- 编译成本高，需要避免重复 LLM 调用。
- 后续需要 remove / replace / recompile。

## 不适用场景

- 一次性临时分析，不落库。
- 同一文件名但内容变化时，只按文件名判断的流程。
- 需要保留同内容不同来源语境的引用时，不能只看 hash，还要记录 origin。

## 反例与避坑

- 失败条件：只按 filename 去重。
- 相似反模式：raw 里同一 PDF 多个副本，wiki 里多个重复 summary。
- 复杂度风险：hash registry 和 formal source record 双写漂移。
- 替代方案：把 hash 字段直接写进 `source` frontmatter，再从 Markdown 派生 registry。

## 来源证据

OpenKB `state.py` 定义 `HashRegistry`，按 SHA-256 记录 metadata；`converter.py` 在复制和转换前检查 hash；`cli.py` 成功编译后才 `registry.add`。

`llm-wiki-compiler` 也有 source state / hash / incremental compile 思路，二者交叉验证。

## 标签与量化

- domain: ingest
- problem: duplicate source and recompile drift
- maturity: proven
- complexity: low
- problem_fit: 5
- reuse_value: 5
- implementation_cost: 2
- integration_fit: 5
- evidence_strength: 5
- reversibility: 5

## 交叉验证

- 相似来源：OpenKB HashRegistry、llm-wiki-compiler source state。
- 历史项目影子：本资料库会保存 repo snapshot、文章、论文，重复采集概率高。
- 支持证据：两个实现都把 source state 当成基础设施。
- 反例：同一内容来自不同上下文时，不能直接丢掉 origin metadata。

## 最小实现方式

先在 source record 里加可选字段：

```yaml
content_hash:
origin_url:
raw_path:
ingest_state: captured | converted | candidate-generated | approved | rejected
compiled_outputs: []
```

再由程序派生：

```text
outputs/state/source-registry.json
```

原则：Markdown source record 是主记录，JSON registry 是加速索引。

## 项目融合建议

进入 `IMPLEMENTATION_BLUEPRINT.md` 的 ingest v0。

不需要一开始做复杂数据库，先用 Markdown + JSON 派生 registry。

## 可拓展性

- 可以通过什么接口/适配层接入：source adapter、candidate compiler、review queue。
- 未来可能被什么替代：SQLite/source table/content-addressed storage。
- 替换或升级成本：低。
- 回退方式：按 raw path 和 source record 人工查重。

## 验证指标

- 同一文件重复 add 是否跳过。
- 内容改变但文件名相同是否能识别。
- source record 是否能追到所有 candidate/formal outputs。
- remove/recompile 是否能找到派生节点。
