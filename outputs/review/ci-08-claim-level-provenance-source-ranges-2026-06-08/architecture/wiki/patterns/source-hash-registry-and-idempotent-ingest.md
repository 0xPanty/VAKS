---
type: pattern
status: active
created: 2026-05-27
updated: 2026-06-08
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

入库前先给 source 内容算 SHA-256；Markdown source record 是主记录，hash registry 只是可重建的加速索引，用来判断“跳过、保留新来源、进入替换候选、还是标记孤儿/待审”。

## 解决的问题

资料库会不断吸收网页、PDF、repo、会话和手动文件。如果没有内容指纹，会出现：

- 同一资料多次入库。
- 同一 source 生成多个 summary/claim。
- 删除或更新时找不到对应派生产物。
- agent 不知道某份资料是否已经处理过。

OpenKB 用 `.openkb/hashes.json` 保存 SHA-256 -> metadata，并在转换前检查是否已知。VAKS 借鉴这个机制，但不把 registry 当成 truth store。

## 适用场景

- raw source 会持续增长。
- 入库动作可能由人、Codex、Misa 或 watcher 多次触发。
- 编译成本高，需要避免重复 LLM 调用。
- 后续需要 remove / replace / recompile。

## 不适用场景

- 一次性临时分析，不落库。
- 同一文件名但内容变化时，只按文件名判断的流程。
- 需要保留同内容不同来源语境的引用时，不能只看 hash，还要记录 origin。
- 需要判断“source 是否可靠”或“claim 是否为真”的场景；hash 只能证明内容是否相同，不能证明内容正确。

## 反例与避坑

- 失败条件：只按 filename 去重。
- 相似反模式：raw 里同一 PDF 多个副本，wiki 里多个重复 summary。
- 复杂度风险：hash registry 和 formal source record 双写漂移。
- 替代方案：把 hash 字段直接写进 `source` frontmatter，再从 Markdown 派生 registry。
- 高风险误用：同一 hash 的不同 origin 被静默丢弃。
- 高风险误用：同一 origin 的新 hash 直接覆盖旧 source record，而不是创建 replacement/recompile 候选。
- 高风险误用：source 被删除后连带删除已被 evidence packet 或 reviewed node 引用的记录。

## 来源证据

OpenKB `state.py` 定义 `HashRegistry`，按 SHA-256 记录 metadata；`converter.py` 在复制和转换前检查 hash；`cli.py` 成功编译后才 `registry.add`。

本次 promotion packet 使用的本地代码锚点：

- `raw/repos/_snapshots/openkb-main-2026-05-27.zip`
- `OpenKB-main/openkb/state.py:8-25`
- `OpenKB-main/openkb/state.py:39-42`
- `OpenKB-main/openkb/state.py:80-87`
- `OpenKB-main/openkb/converter.py:36-61`
- `OpenKB-main/openkb/cli.py:348-361`

`llm-wiki-compiler` 也有 source state / hash / incremental compile 思路，二者交叉验证。

## VAKS 融合边界

这是一层 source 生命周期卫生规则，不是新的真理层。

- source hash 不增加 truth confidence。
- source hash 不算 evidence support。
- source hash 不创建 reviewed relation。
- source hash 不允许绕过 review queue 写入正式 wiki。
- source hash 不允许把 Obsidian 同步当成审批或入库完成。
- JSON registry / state file 必须能从 Markdown source records 重建。

## 入库判定表

| 情况 | 判定 | 允许动作 | 禁止动作 |
|---|---|---|---|
| 同一 origin + 同一 hash | `idempotent_skip` | 跳过重复 compile，记录已见过 | 再生成一份 candidate 或 wiki node |
| 不同 origin + 同一 hash | `preserve_new_origin` | 保留新 origin / source record，registry 指向同 hash 多来源 | 只因 hash 相同就丢弃新 provenance |
| 同一 origin + 新 hash | `replacement_candidate` | 标记 source_changed，进入 replacement / recompile candidate | 静默覆盖旧 source record 或旧 evidence |
| raw path 缺失但被引用 | `orphan_review_due` | 标记孤儿和 review_due，保留引用链 | 静默删除 evidence packet、reviewed node 或 compiled output |
| compile 失败 | `no_registry_commit` | 保留失败日志或 candidate lint violation | 先登记 registry 再假装已处理 |

## Registry Commit Point

OpenKB 的关键细节不是“有 hash”，而是成功后才登记。VAKS 的等价规则：

```text
capture / conversion / candidate creation 成功
-> source record 写入或更新完成
-> registry 派生或刷新
```

失败流程不能提前把 hash 记成 processed，否则下一次会被误判为已入库。

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
hash_algorithm: sha256
origin_url:
origin_label:
raw_path:
source_record_path:
previous_content_hash:
source_changed: unknown | yes | no
ingest_state: captured | converted | candidate-generated | approved | rejected | orphaned
ingest_decision: new_source | idempotent_skip | preserve_new_origin | replacement_candidate | orphan_review_due
compiled_outputs: []
referenced_by:
review_due_reason:
```

再由程序派生：

```text
outputs/state/source-registry.json
```

原则：Markdown source record 是主记录，JSON registry 是加速索引；如果二者冲突，以 Markdown source record 为准，registry 需要重建。

Derived registry 的最小形状：

```yaml
sha256:<hash>:
  source_records: []
  origins: []
  current_versions: []
  compiled_outputs: []
  last_derived_at:
```

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
- 同一 hash 的不同 origin 是否被保留。
- source 缺失时是否标记 orphan/review_due，而不是删除证据链。
- registry 是否能从 Markdown source records 重建。
