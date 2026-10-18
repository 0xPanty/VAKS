---
type: pro_upload_prompt
status: ready
created_at: 2026-06-06
truth_boundary: prompt only; not reviewed knowledge; not action basis
---

# Upload To Pro Prompt: Lightweight Sidecar Design

请基于下面这套 VAKS 沙盒测试包，做一次开放式调研和轻量化架构设计：

```text
outputs/review/project-sidecar-seven-candidate-pressure-test-2026-06-05/
```

请优先阅读：

```text
FINAL_REPORT.md
ISSUES_AND_RECOMMENDATIONS.md
checks/pressure-matrix.md
checks/mainline-copy-insertion-check.md
checks/action-facing-escalation.md
checks/retrieval-hygiene-check.md
checks/non-author-confusion-check.md
misa_overlay/MISA.md
misa_overlay/MISA-closeout-manifest-2026-06-05.md
```

背景：

VAKS 当前主线已经落下两条最小原则：

1. `v0.2.13 late-stage action-facing warrant gate`
   - 任何候选点、证据、外部资料一旦要用于 action basis、重要 promotion、架构吸收、决策、风险敏感回答，就不能只列 evidence，必须说明 evidence 为什么在当前 scope / assumption 下支撑 claim，并说明 gaps / risks / residual review。

2. `generic project-scoped sidecar overlay boundary principle`
   - 项目可以在通用知识点之外维护项目作用域的临时复用视角 / 导航提示，但它不改写知识点本体，不是 truth、reviewed knowledge、ADR、action basis 或 truth confidence。若进入行动或正式吸收，仍回到 v0.2.13 warrant gate。

我们刚做了一轮高压沙盒测试：

```text
把七个候选机制完整插入主架构副本
用 Misa / misa-cybernetic-evolution 做第二真实项目样本
跑 lifecycle、retrieval hygiene、authority leakage、non-author confusion、action-facing escalation
```

测试结论简述：

```text
七个候选沙盒可用性高，但主线成熟度低。
全量写入主架构副本后，主线明显变重。
这些机制帮助 Codex 维护项目，但对象模型、字段、snapshot、closeout lifecycle 不适合整套主线化。
```

量化结果：

```text
sandbox usefulness: 2.57 / 3
mainline readiness: 0.71 / 3
leakage risk: 2.43 / 3
maintenance gain: 2.57 / 3
```

现在的问题不是“Project Lens 要不要进主线”，而是：

```text
如何设计一套更轻量、更不污染主线、但保留核心功能的 project-scoped sidecar overlay operating pattern？
```

请你参考外部成熟实践做调研和设计，包括但不限于：

- W3C Web Annotation / annotation body-target separation
- boundary objects
- architecture knowledge management 的 generic knowledge / project-specific artifact split
- ADR / MADR / AWS / Azure 的 design exploration vs decision separation
- lessons learned / experience report / significant-valid-applicable 经验沉淀
- IBIS / gIBIS / design rationale
- software project memory / lightweight issue labels / review manifests
- retrieval hygiene / evidence retrieval vs verification separation
- agent workbench / file-first traceability / human-in-the-loop safety patterns

请重点回答：

1. 在保留功能的前提下，哪些东西可以进一步轻量化？
2. 哪些功能是真必要，哪些只是测试时看起来完整但长期会变重？
3. 是否应该继续使用 `Project Lens` 这个名字？如果不建议，用什么名字更稳？
4. 最小字段应该是什么？哪些字段应该删除、派生、或只在报告里出现？
5. `stance` 是否必要？如果必要，最小状态集是什么？
6. `snapshot` 机制如何改得更轻，避免 best practice / universal ban 泄漏？
7. closeout drain 如何保留，但不做成生命周期状态机？
8. archive / delete+tombstone / carry-forward / supersede 哪些应保留为操作，哪些应删除或合并？
9. `default retrieval precedence` 是否足够？有没有更好的轻量表达？
10. 如何让 Codex/agent 用起来顺手，但不让普通用户感觉多了一套制度？
11. 如何与 v0.2.13 warrant gate 分工，避免 sidecar 变成常驻 mini-assurance-case？
12. 是否有一种“一页纸协议”可以覆盖 80% 功能？

请输出：

## A. 总体判断

这条 project-scoped sidecar 方向是否继续？继续的话，以什么形态继续？

## B. 外部参考压缩

请把外部成熟实践压缩成 5-8 条可借鉴原则，不要只列论文/框架名。

## C. 轻量化设计方案

请给出一版最小可用设计，要求：

```text
保留项目临时视角
保留 kp_ref / 回源能力
保留 stance/outcome 分离
保留 closeout drain
保留 archive/tombstone 的检索卫生
保留 action-facing use 回到 v0.2.13
不把它做成 ADR
不把它做成 truth layer
不改 SCHEMA.md / REVIEW_QUEUE.md / templates
不引入 formal workspace directory
```

## D. 最小字段和最小操作

请明确：

```text
required fields
optional fields
fields to delete
derived/check-only fields
allowed live states
allowed closeout operations
forbidden words / forbidden states
```

## E. 一页纸协议

请写一版可以直接给 Codex/agent 使用的“一页纸操作协议”，越短越好，但必须守住边界。

## F. 是否需要主线改动

请明确回答：

```text
现在是否需要修改 ARCHITECTURE_PRINCIPLES.md？
现在是否需要修改 FUSION_ARCHITECTURE_V0_2_DRAFT.md？
现在是否需要修改 SCHEMA.md？
现在是否需要修改 REVIEW_QUEUE.md？
现在是否需要修改 templates？
```

## G. 风险和反例

请列出最容易让这个轻量方案失败的 5 个反例，并给出对应 guardrail。

## H. 最终建议

请用非常明确的结论说明：

```text
keep sandbox only
mainline minimal wording only
promote a tiny principle
drop the direction
or another recommendation
```

要求：

- 不要默认同意现有设计。
- 不要只做 yes/no 审批。
- 不要把字段表设计得更重。
- 优先找“更少字段、更少状态、更少文件、更少仪式感”的方案。
- 但也不要丢掉这次测试证明有用的功能：项目视角、回源链、清场、防污染、检索卫生、行动闸门。
