---
type: candidate_pattern
status: active
pattern_id: graph-and-ontology-as-candidate-context
created_at: 2026-06-05
truth_boundary: candidate pattern only; not reviewed knowledge
source_family_ids:
  - sf-graph-ontology
  - sf-rag-engineering
project_fit_refs:
  - outputs/review/project_borrowing_ledgers/VAKS.md
---

# Graph and Ontology as Candidate Context

## One-Line Pattern

本体、知识图谱、实体关系、community summary、ontology object model 可以帮助组织上下文和候选关系，但不能自动成为 reviewed relation。

## Problem Addressed

图谱和本体看起来很正式，容易让人误以为图上的边就是可信关系。GraphRAG 生成的 entity/relationship/community report 也容易被误读成知识图谱真理层。

## Mechanism

- 图谱/ontology 先作为 candidate context。
- auto-extracted relation 进入 candidate_relation。
- 强关系必须经过 evidence-aware review。
- CQ / intermediate representation / evaluation ledger 可作为 review 输入。

## Applicability

- ontology design。
- GraphRAG / LightRAG。
- multi-agent semantic layer。
- VAKS optional point graph fragments / relation review。

## Non-Goals and Trade-Offs

- 不引入完整 ontology stack。
- 不让 graph rank 成为 trust。
- 不让 community report 成为 truth。
- 普通 capture 不展开图谱。

## Derived From Sources

- `raw/videos/2026-06-04-bilibili-ontology-methodology-knowledge-graph-source.md`
- `raw/papers/2026-06-04-methontology-source.md`
- `raw/videos/2026-06-04-bilibili-palantir-ontology-multi-agent-source.md`
- `raw/videos/2026-06-04-bilibili-raglab-17-rag-visual-canvas-source.md`
- `raw/videos/2026-06-04-bilibili-obsidian-exam-knowledge-graph-source.md`

## Aliases or Near-Duplicates

- graph context not graph truth
- ontology as review aid
- auto relation as candidate relation
- semantic layer as activation layer

## Risk of Overreach

- 图越漂亮越像 truth。
- 本体设计拖慢日常 capture。
- 自动关系被项目误用于 action basis。

## Project Fit Refs

- VAKS: `watch`; useful only as candidate context/review aid.

