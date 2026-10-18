---
type: source
status: source-captured
title: "METHONTOLOGY: From Ontological Art Towards Ontological Engineering"
source_id: 2026-06-04-methontology-source
source_uri: https://cdn.aaai.org/Symposia/Spring/1997/SS-97-06/SS97-06-005.pdf
source_url: https://cdn.aaai.org/Symposia/Spring/1997/SS-97-06/SS97-06-005.pdf
source_type: paper
author: "Mariano Fernandez-Lopez; Asuncion Gomez-Perez; Natalia Juristo"
publisher: "AAAI Spring Symposium Series"
published_at: 1997
updated_at:
captured_at: 2026-06-04
captured_by: Codex
version_or_commit: "AAAI Technical Report SS-97-06, pp. 33-40"
source_status: legacy
raw_location: raw/papers/2026-06-04-methontology-source.md
processing_mode: immediate
processing_level: heavy
review_priority: normal
review_owner: Codex
formalization_status: candidate-generated
topics:
  - ontology-engineering
  - methontology
  - competency-questions
  - schema-design
  - evaluation
  - documentation
  - reviewed-relations
projects:
  - verified-action-knowledge-system
source_family: ontology-engineering-methodology
upstream_sources: []
verification_status: primary-source-captured
candidate_relation_suggestions: []
tags:
  - source
  - paper
  - architecture-reference
  - candidate-only
---

# METHONTOLOGY: From Ontological Art Towards Ontological Engineering

## 为什么收录

这篇论文是视频 `本体论04-方法论成熟与知识图谱爆发` 中 METHONTOLOGY 部分背后的原始锚点之一。

它对 VAKS 有价值，不是因为我们要照搬重型本体工程，而是因为它把“知识结构怎么从手艺活变成工程活”拆成了可检查的活动、生命周期、中间产物、评估和文档。

对 VAKS 最重要的一句话是：

```text
知识结构不是先画图或先写关系。
先说明目的、范围、用户、使用场景和形式化程度；
再采集知识、概念化、复用、实现、评估、文档化、维护。
```

## 来源信息

- 论文：METHONTOLOGY: From Ontological Art Towards Ontological Engineering
- 作者：Mariano Fernandez-Lopez, Asuncion Gomez-Perez, Natalia Juristo
- 发布方：AAAI Spring Symposium Series
- 技术报告：SS-97-06
- 年份：1997
- PDF：https://cdn.aaai.org/Symposia/Spring/1997/SS-97-06/SS97-06-005.pdf
- AAAI 页面：https://aaai.org/papers/0005-ss97-06-005-methontology-from-ontological-art-towards-ontological-engineering/
- UPM 仓库页：https://oa.upm.es/5484/
- 处理边界：primary source captured；candidate extraction only；不进入 reviewed knowledge。

## 当前采用边界

本资料库不照搬：

```text
full ontology engineering
OWL / Ontolingua / Prolog / frame language runtime
formal reasoner as current core
meta-ontology reuse pipeline
ontology server / translation layer
```

当前只把它作为 VAKS 的工程纪律参考：

```text
requirements before schema
competency questions as design checks
evolving prototype instead of waterfall schema
intermediate representations as review surfaces
evaluation and documentation as quality ledger
reuse only after compatibility check
```

## 人话总览

这篇论文的核心问题是：很多 ontology 已经被做出来了，但怎么做、按什么步骤做、如何评估、如何文档化，都没有足够标准化。因此本体开发还像“手艺活”，没有完全变成工程。

作者提出三层东西：

1. 本体开发过程：应该做哪些活动。
2. 本体生命周期：这些活动大致如何随时间推进。
3. METHONTOLOGY：从零构建本体时，每个阶段该用什么技术、产出什么文档。

它最像一套“知识结构工程化作业规程”。它不是在证明某个具体本体为真，也不是在讲知识图谱规模，而是在说明：如果你想让一个概念/关系系统能被复用、维护、评估和共享，不能只靠最后的代码或图结构，必须保留需求说明、知识采集记录、概念模型、集成记录、评估记录和持续文档。

## 论文结构完整提炼

### Abstract / Introduction

论文目标不是把本体艺术完全变成工程，也不是穷举所有本体研究，而是帮助从零构建 ontology 的人理解：

```text
做哪些活动
按什么生命周期推进
每个阶段使用什么技术
每个阶段产出什么
```

作者指出，当时本体构建缺少标准化活动、生命周期、方法论、设计准则、技术和工具，因此容易停留在 craft。

对 VAKS 的意义：

```text
资料库的 schema / relation / review rule 也不能只靠“感觉合理”。
它需要目的、范围、评估方式和可维护文档。
```

### Section 2: Ontology Development Process

这一节列的是“应该做哪些活动”，但不规定执行顺序。

活动包括：

```text
planification:
  规划任务、时间、资源、人、软件、硬件。

specification:
  明确为什么建、给谁用、用途和范围。

knowledge acquisition:
  从专家、书籍、手册、表格、图、已有 ontology 获取知识。

conceptualization:
  把采集到的知识组织成概念模型。

formalization:
  把概念模型转成形式化或半形式化表示。

integration:
  复用和整合已有 ontology，避免重复造轮子。

implementation:
  用形式化语言或工具实现。

evaluation:
  技术判断、检查错误、不完整、不一致、冗余。

documentation:
  记录整个过程，支持共享和复用。

maintenance:
  后续修改、加入、删除定义。
```

对 VAKS 的意义：

```text
raw capture 不必一次走完这些活动。
但当某个 schema / relation / action-basis 变重要时，VAKS 可以把这些活动当成 lazy gate 展开。
```

### Section 3: Ontology Life Cycle

这一节回答“活动怎么推进”。论文把本体生命周期分成：

```text
specification
-> conceptualization
-> formalization
-> integration
-> implementation
-> maintenance
```

同时有三类贯穿性活动：

```text
knowledge acquisition
evaluation
documentation
```

论文比较了瀑布、增量和 evolving prototype，认为 evolving prototype 更适合 ontology，因为定义会随着需求、错误和遗漏不断调整。

对 VAKS 的意义：

```text
VAKS schema 不应一开始就一次性冻结。
但它也不能随意改。
更合适的是：
candidate rule -> local trial / review -> documented change -> handoff/index sync。
```

### Section 4.1: Specification

这一节规定 specification 至少要写：

```text
purpose:
  目的、用途、使用场景、终端用户。

level_of_formality:
  高度非正式、半非正式、半正式、严格正式。

scope:
  术语集合、特征、粒度。
```

论文还提到 specification 可用自然语言、中间表示，或 competency questions 组织。

它强调好的 specification 至少要检查：

```text
concision:
  术语相关，没有重复或无关术语。

partial completeness:
  术语覆盖、粒度和停止边界合理。

consistency:
  术语及含义在领域内说得通。
```

对 VAKS 的意义：

```text
这直接支持 requirements_before_schema。
先说明为什么要这个字段/关系/层，而不是先扩 schema。
```

### Section 4.2: Knowledge Acquisition

知识采集是独立活动，但会和 specification、conceptualization 同时发生。

来源包括：

```text
experts
books
handbooks
figures
tables
other ontologies
```

技术包括：

```text
brainstorming
unstructured interviews
structured interviews
formal text analysis
informal text analysis
knowledge acquisition tools
```

论文强调：如果目的还不清楚，可以先通过头脑风暴、访谈、检查类似 ontology 得到第一版术语表；再通过文本分析和专家访谈修订术语及含义。

对 VAKS 的意义：

```text
source intake 不是直接提结论。
它先得到候选术语、候选关系、候选问题、候选范围。
```

### Section 4.3: Conceptualization

这一节是论文最像“可落地模板”的地方。作者要求先建立 Glossary of Terms。

Glossary of Terms 包括：

```text
concepts
instances
verbs
properties
their meanings
```

然后把术语分成概念和动词两条线。

概念侧中间表示包括：

```text
data dictionary
tables of instance attributes
tables of class attributes
tables of constants
tables of instances
attributes classification trees
```

动词/动作侧中间表示包括：

```text
verbs dictionary
tables of conditions
tables of formulas
tables of rules
```

论文说这些中间表示能让最终用户不用看源码，也能判断 ontology 是否对某个应用有用、范围是否完整、是否可复用和可共享。

对 VAKS 的意义：

```text
VAKS 可以借这个思想：
把 candidate points、candidate relation suggestions、scope notes、risk notes、review questions 做成可读 review surface。
不要只把关系藏在 YAML 或图里。
```

### Section 4.4: Integration

这一节讲复用已有 ontology。

步骤大意：

```text
1. 检查可用 meta-ontologies，选择和本 conceptualization 匹配的基础术语体系。
2. 检查 ontology libraries 中是否已有语义和实现都兼容的定义。
3. 如果 meta-ontology 不同，需要检查是否有 translator 能转换到目标语言。
4. 如果需要的术语缺失，要向维护者说明为什么需要加入、加入有什么收益。
5. 产出 integration document，记录复用术语来自哪里、在原 ontology 里叫什么、定义参数是什么。
```

对 VAKS 的意义：

```text
外部资料/外部框架/插件能力可以借，但不能直接成为本库权威。
任何复用都要记录来源、适配、范围、缺口和翻译/映射风险。
```

### Section 4.5: Implementation

论文说 implementation 是把 ontology 编码进形式化语言或环境，例如 CLASSIC、BACK、LOOM、Ontolingua、Prolog、C++ 等。

一个 ontology development environment 至少应该提供：

```text
lexical / syntactic analyzer
translator
editor
browser
searcher
evaluator
automatic maintainer
```

对 VAKS 的意义：

```text
这些是未来工具层参考，不是当前必须实现。
当前 VAKS 的工程优先级仍然是 Markdown source of truth、review gate、handoff/index 可恢复。
```

### Section 4.6: Evaluation

论文把 evaluation 定义为：以一个 frame of reference 为参照，对 ontology、软件环境和文档做技术判断。这里的参照就是 requirements specification document。

它区分：

```text
verification:
  检查 ontology / software / documentation 相对于参照是否正确。

validation:
  检查 ontology / environment / documentation 是否对应它应该表示的系统。
```

Evaluation document 应记录：

```text
如何评估
使用了什么技术
每个活动发现了什么错误
评估使用了哪些知识来源
```

对 VAKS 的意义：

```text
这和 maintenance manifest / evidence packet / review-candidate 很贴近。
评估不是 truth，本身是 review input 和质量 ledger。
```

### Section 4.7: Documentation

论文指出 ontology 文档经常缺失，形成循环：

```text
没有文档指南 -> 很少有人写文档
很少有人写文档 -> 很难形成方法论
没有方法论 -> 更没有文档指南
```

METHONTOLOGY 试图打破这个循环：文档不是最后补，而是贯穿全过程。

每阶段文档：

```text
after specification:
  requirements specification document

after knowledge acquisition:
  knowledge acquisition document

after conceptualization:
  conceptual model document with intermediate representations

after formalization:
  formalization document

after integration:
  integration document

after implementation:
  implementation document

during evaluation:
  evaluation document
```

对 VAKS 的意义：

```text
这直接支持“文件为准、对话为辅”。
重要架构判断、source intake、review、同步、cleanup 都要留下 durable artifact。
```

### Section 5: Conclusion

论文总结三点：

```text
1. 识别 ontology development process 中需要做的活动。
2. 认为 evolving prototype 更适合 ontology lifecycle。
3. 定义 METHONTOLOGY：活动、技术和每个活动后的 deliverables。
```

它还强调复用已有 ontology。

对 VAKS 的意义：

```text
VAKS 可以借“活动 + 技术 + deliverable”的思想，
但不能把 deliverable 的存在当成 reviewed truth。
```

## 反漏提取检查

```text
pain point:
  - 本体开发缺少标准化活动、生命周期和文档，容易停留在专家手艺活。
  - 没有 requirements 和 evaluation，概念/关系结构会变成漂亮但不可评估的图。

workflow:
  - plan -> specify -> acquire knowledge -> conceptualize -> formalize -> integrate -> implement -> evaluate -> document -> maintain。
  - 生命周期不是一次性瀑布，而是 evolving prototype。
  - knowledge acquisition、evaluation、documentation 贯穿大多数阶段。

tools / plugins:
  - METHONTOLOGY
  - Ontolingua
  - CLASSIC / BACK / LOOM / Prolog / C++
  - ontology libraries / meta-ontologies
  - evaluators / translators / editors / browsers / searchers

information structure:
  - requirements specification document
  - glossary of terms
  - concept classification tree
  - verbs diagram
  - data dictionary
  - instance attributes / class attributes
  - constants / instances
  - conditions / formulas / rules
  - integration document
  - evaluation document

judgment mechanism:
  - specification 用 purpose / formality / scope 约束。
  - specification 用 concision / partial completeness / consistency 检查。
  - evaluation 以 requirements specification 为参照。
  - verification / validation 分开。

user experience:
  - 对最终用户有价值的是中间表示和文档，因为用户不应该必须读源码才能判断 ontology 是否有用。
  - 对 VAKS 用户同理：review surface 应该可读，不应只给 YAML 或图。

automation boundary:
  - 工具可以做语法检查、翻译、搜索、评估、维护辅助。
  - 但论文不是自动判真系统；工具输出仍要受 requirements / evaluation 约束。

risk:
  - 论文是 1997 年的本体工程方法论，技术栈很旧。
  - 它假设目标是构建 formal ontology；VAKS 当前不是 formal ontology runtime。
  - 如果照搬，会让普通 capture 过重。

fit for us:
  - 借 requirements-before-schema。
  - 借 competency questions / actual questions 作为设计测试。
  - 借 intermediate representations 作为 review surface。
  - 借 evaluation document 作为 quality ledger。
  - 借 evolving prototype 作为 schema 演化纪律。

challenge to us:
  - VAKS 当前 schema / relation / context-pack 设计如果没有能力问题，可能会变成自洽但无用。
  - 如果只追求图谱可视化，没有 requirements/evaluation/documentation，VAKS 会退化成图数据库或双链系统。
```

## 可抽取 Candidate Points

1. `requirements_before_schema`

候选结论：重要 schema、relation enum 或 review gate 改动前，应先写目的、使用者、使用场景、形式化程度和范围。

VAKS 价值：防止为了“看起来完整”而扩 schema。

风险：如果用于普通 capture，会增加摩擦。

2. `competency_questions_as_design_tests`

候选结论：能力问题可作为 VAKS 设计检查：这个 source card / review queue / context pack / action basis 能回答哪些实际问题？

VAKS 价值：把 schema 争论拉回到真实使用问题。

风险：CQ 不能变成自动评测权威；它只是设计检查和 review input。

3. `evolving_schema_not_waterfall_schema`

候选结论：VAKS schema 应允许演化，但演化需要 documented change、review gate、handoff 和 index sync。

VAKS 价值：避免一开始冻结过重结构，也避免随手改核心规则。

4. `intermediate_representations_as_review_surface`

候选结论：Glossary、classification tree、attribute table、rule table 这类中间表示可作为 review surface。

VAKS 价值：让候选关系、范围、风险、规则可读，而不是只藏在图或 YAML 中。

5. `evaluation_document_as_quality_ledger`

候选结论：评估过程应记录技术、错误、阶段和知识来源；评估文档是质量 ledger，不是 truth confidence。

VAKS 价值：补强 maintenance manifest / review-candidate 的解释。

6. `reuse_requires_integration_document`

候选结论：复用外部定义/框架/插件能力时，应记录来源、定义名、参数、适配和转换风险。

VAKS 价值：支持“外部能力可以借，权威不能借”。

7. `documentation_is_part_of_knowledge_work`

候选结论：文档不是最后补；重要知识工程每阶段都要留下 durable artifact。

VAKS 价值：支持文件为准、handoff、ledger、source card。

8. `evaluation_reference_frame_required`

候选结论：评估必须相对于一个 frame of reference；没有 requirements 的评估会变成主观好坏。

VAKS 价值：支持 action basis / context pack 在评估前声明用途和范围。

## 可借鉴

- 用 requirements specification 的思想约束重要 schema / relation 改动。
- 用 competency questions 检查 VAKS 是否真的能支持行动和 review。
- 用 evolving prototype 做 schema 演化模型，但把 review gate 加在演化写回前。
- 用 intermediate representations 做 reviewer-readable surface。
- 用 evaluation document 思想补强 maintenance manifest 和 review-candidate。
- 用 integration document 思想约束外部 ontology / KG / plugin / framework 借鉴。

## 不能直接借鉴

- 不直接上 full METHONTOLOGY 作为普通 source intake 流程。
- 不要求所有普通资料都写 glossary / classification tree / rule table。
- 不把 ontology evaluation 结果当 truth confidence。
- 不把 formal ontology / reasoner 作为 VAKS 当前核心 runtime。
- 不把 1997 年工具栈当现代实现建议。
- 不把本论文对 ontology 的方法论直接替代 VAKS 的 source -> candidate -> review -> action loop。

## 和视频的差异

视频已经讲到：

```text
METHONTOLOGY 是生命周期管理方法论。
本体工程不能只靠专家手工。
CQ 很重要。
本体和知识图谱要区分。
```

论文比视频多出来的东西：

```text
1. 更明确的 ontology development process 活动清单。
2. 生命周期比较：waterfall / incremental / evolving prototype。
3. specification 的最小内容：purpose / formality / scope。
4. specification 的质量检查：concision / partial completeness / consistency。
5. conceptualization 的中间表示清单。
6. integration document 的复用记录要求。
7. evaluation document 应记录技术、错误、阶段、来源。
8. documentation 是贯穿活动，不是最后补。
```

所以视频适合当导读，论文适合当 VAKS 后续 review 的 source anchor。

## VAKS 归位

```text
Capture:
  这篇论文是 paper source；当前卡片是 heavy source digest，但仍是 candidate-generated。

Understand:
  本卡逐节摘要、反漏提取和 candidate points 是 candidate comprehension。

Review:
  若要吸收进 `SOURCE_INTAKE.md` / `SCHEMA.md` / `REVIEW_QUEUE.md`，需要后续 evidence-aware review。

Connect:
  可提示与 requirements、competency questions、evaluation ledger、candidate relation boundary 的候选关系。
  不能直接创建 reviewed relation。

Activation / Context Pack:
  可作为未来讨论 schema design、relation review surface、maintenance manifest 的背景材料。

Decision / Action:
  当前不构成 action basis；不能据此决定引入 ontology runtime。

Use Ledger / Feedback:
  可记录为用户对 ontology / knowledge graph / schema discipline 的研究兴趣，不改变 truth confidence。
```

## Source Anchors

```yaml
source_anchor_matrix:
  - section: Abstract / Introduction
    anchor_note: "Paper frames ontology development as needing activities, life cycle, techniques, and methodology, not only craft."
    used_for:
      - requirements_before_schema
      - documentation_is_part_of_knowledge_work
  - section: Section 2 Ontology Development Process
    anchor_note: "Lists plan, specify, acquire knowledge, conceptualize, formalize, integrate, implement, evaluate, document, maintain."
    used_for:
      - evolving_schema_not_waterfall_schema
  - section: Section 3 Ontology Life Cycle
    anchor_note: "Compares waterfall, incremental, and evolving prototype; chooses evolving prototype for ontology evolution."
    used_for:
      - evolving_schema_not_waterfall_schema
  - section: Section 4.1 Specification
    anchor_note: "Specification includes purpose, formality, and scope; may use competency questions."
    used_for:
      - requirements_before_schema
      - competency_questions_as_design_tests
  - section: Section 4.3 Conceptualization
    anchor_note: "Conceptual model uses glossary, attribute tables, constants, rules, conditions, and other intermediate representations."
    used_for:
      - intermediate_representations_as_review_surface
  - section: Section 4.4 Integration
    anchor_note: "Reuse requires checking meta-ontology compatibility and producing an integration document."
    used_for:
      - reuse_requires_integration_document
  - section: Section 4.6 Evaluation
    anchor_note: "Evaluation records how the ontology was evaluated, techniques, errors, and knowledge sources."
    used_for:
      - evaluation_document_as_quality_ledger
  - section: Section 4.7 Documentation
    anchor_note: "Documentation is an activity throughout the whole development process."
    used_for:
      - documentation_is_part_of_knowledge_work
```

## 明显疑点 / 需要进一步核验

- 论文年代较早，现代 ontology engineering、semantic web、KG 和 LLM 语境已经变化。
- METHONTOLOGY 是从零构建 formal ontology 的方法，不等同于 VAKS 的 Markdown-first verified action system。
- 论文里的工具/语言清单具有历史性，不应作为今天的技术选型依据。
- 若要正式吸收 CQ 或 evaluation document，需要和当前 `SOURCE_INTAKE.md`、`REVIEW_QUEUE.md`、`SCHEMA.md` 对照，避免普通 capture 变重。
- 如果要把本论文作为 reviewed pattern 的 support，至少需要再核验 2003 Ontological Engineering 书、Uschold & Gruninger 1996、以及现代 ontology/KG 工程来源。

## 当前处理等级

```text
processing_level: heavy
formalization_status: candidate-generated
verification_status: primary-source-captured
```

解释：

```text
heavy 表示本卡做了完整论文提炼。
candidate-generated 表示这些提炼还没有进入 reviewed knowledge。
primary-source-captured 表示已读原始 PDF，而不是只依赖视频口述。
```

## 是否建议进入 REVIEW_QUEUE

建议进入，但只进入三个窄问题，不要把整篇论文打包晋级：

1. `competency_questions_as_design_tests`

是否把 CQ 写成 VAKS 的 schema / context pack / action basis 设计检查？

2. `intermediate_representations_as_review_surface`

是否把 candidate relation、scope、risk、rule、coverage 做成 reviewer-readable intermediate representations？

3. `evaluation_document_as_quality_ledger`

是否把 evaluation document 思想吸收到 maintenance manifest / review-candidate / handoff closeout？

## 下一步

- 若用户确认，可以从本卡蒸馏一份 `outputs/review/2026-06-04-methontology-vaks-candidate-distillation.md`。
- 若进入正式 review，先只审 CQ、intermediate representations、evaluation/documentation 三点。
- 暂不修改 `SCHEMA.md`、`SOURCE_INTAKE.md`、`REVIEW_QUEUE.md` 或任何 reviewed knowledge。
