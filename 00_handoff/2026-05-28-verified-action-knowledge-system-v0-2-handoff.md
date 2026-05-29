# 2026-05-28 handoff：Verified Action Knowledge System v0.2

## 工作目录

```text
C:\Users\Administrator\Documents\资料库
```

## 当前最新架构基线

本 handoff 接续 commit：

```text
7d344d3 Document fusion architecture v0.2 and review synthesis
c3dec34 Update v0.2 handoff and recovery indexes
```

这次更新后的核心判断：

```text
Karpathy-simple outside.
Dusk-style workbench nearby.
Reviewed-action core inside.
Optional retrieval, synthesis, publishing, and agent tooling around it.
```

说人话：

```text
日常入口要简单。
项目工作台要顺手。
真正决定长期知识和行动依据的，是 reviewed knowledge core。
dashboard、retrieval、metadata、brief、feedback 都可以帮忙，但不能当 truth。
```

## 下个窗口先读

```text
AGENTS.md
00_handoff/2026-05-28-verified-action-knowledge-system-v0-2-handoff.md
README.md
FUSION_ARCHITECTURE_V0_2_DRAFT.md
SECOND_BRAIN_MODEL.md
ARCHITECTURE_PRINCIPLES.md
SCHEMA.md
IMPLEMENTATION_BLUEPRINT.md
SOURCE_INTAKE.md
REFERENCE_REVIEW_PROTOCOL.md
MEMORY_TIER.md
DEV_CONTEXT.md
REVIEW_QUEUE.md
FEEDBACK.md
wiki/indexes/knowledge-graph-index.md
wiki/indexes/memory-tier-reference-index.md
templates/architecture-review-window-prompt.md
```

如果只是继续看文章/仓库/论文，先读 handoff、README、FUSION、SECOND_BRAIN、REFERENCE_REVIEW_PROTOCOL、architecture review prompt 就够；需要落地实现或改 schema 时，再读完整清单。

`AGENTS.md` 是项目级入口地图：它不替代 handoff，也不替代 schema/docs，只负责告诉新窗口先读什么、各目录是什么、已经吸收过哪些资料、当前边界是什么。

## 对外主叙事

不要再用十几层大脑结构做开源第一叙事。

对外只讲五层：

```text
1. Capture
   先保存来源，不强迫立刻判断。

2. Understand
   把资料整理成 summary、candidate point、candidate claim / pattern / risk。

3. Review
   只有有来源、有证据、经过 review 的内容进入 reviewed memory。

4. Connect
   新点和旧点做 supports / contradicts / refines / risk_of / derived_from。

5. Act and Learn
   生成 context pack / action basis，记录使用反馈，改进下一次激活路径，但不直接改 truth。
```

边界句：

```text
The system can suggest.
Only reviewed evidence can support action.
Feedback improves activation, not truth.
```

总原则：

```text
Strict checks are lazy gates.

Capture stays light.
Promotion gets strict.
Action basis gets auditable.
Feedback improves activation, not truth.
```

普通 capture / ordinary query 不默认触发完整 review、evidence_support、coverage_map 或 point_graph_fragment。
这些严格检查只在 promotion、action basis、decision、strong reviewed relation、高影响、stale、contested 或 explicit challenge 时打开。

## 内部主循环

内部可以用 verified loop 解释：

```text
raw source
-> Capture / Provenance
-> Candidate Comprehension
-> Knowledge Calibration / Point Collision
-> Review / Consolidation
-> Association / Reviewed Relations
-> Activation / Dev Context
-> Context Pack
-> Decision / Action
-> Use Ledger / Feedback
-> Cooling / Reactivation / Review Due
```

横切控制：

```text
Provenance
Risk / Inhibition
Traceability
Safety Gate
```

旁路能力：

```text
Proactive Synthesis:
  on-demand first, scheduled later, candidate only.

Expression / Publishing:
  future output surface.

Agent Tool Safety:
  future execution safety, only needed when agents can write or execute.
```

## 第二大脑模型怎么用

`SECOND_BRAIN_MODEL.md` 是解释模型和设计校验表，不是工程模块目录。

它有价值的点是：

```text
入库时建立连接。
查询时激活连接。
用后修正连接。
风险层负责刹车。
主动思考负责后台回放。
```

但不要把每个脑结构都做成独立模块。

正确用法：

```text
对外 README:
  五层主叙事。

内部设计:
  用大脑模型检查有没有漏掉 capture / activation / review / association / feedback / risk。

实现路线:
  仍然按最小 verified loop 试跑，不按脑层开十几个子系统。
```

## Pro review 后已采纳的修正

已采纳：

```text
Attention -> Activation
Memory Tier -> Activation Tier where possible
Verified Memory -> Reviewed Memory / Evidence-backed Memory
Forgetting -> Cooling
Feedback Learning -> Use Ledger when referring to records
Risk Control -> Cross-cutting Risk / Inhibition
```

已收缩：

```text
MVP relation types:
  supports
  contradicts
  refines
  risk_of
  derived_from
```

暂缓：

```text
replaces
implements
applies_to
inspired_by
alternative_to
blocked_by
```

这些不是永远拒绝，只是不进入第一版核心关系集合。

## Pro review 15 点落地口径

15 点评审不拆成 15 条新约束，只归并为五个当前口径：

```text
1. 对外主架构固定为五层：
   Capture -> Understand -> Review -> Connect -> Act and Learn。

2. 内部工程主线固定为 verified loop：
   source -> candidate points -> calibration / point collision -> review -> reviewed node / relation -> context pack -> action -> feedback。

3. SECOND_BRAIN_MODEL.md 降权：
   它是解释模型和设计校验表，不是实现结构或模块目录。

4. Risk / Inhibition 是横切层：
   它贯穿 capture、understand、review、connect、act、feedback，不是最后一站。

5. Proactive Synthesis、Expression / Publishing、Agent Tool Safety 不进 truth core：
   它们分别是候选生成器、未来输出面、未来执行安全层。
```

所以现在要改的是口径和分层位置，不是新增实现、自动化或更多制度。

## Knowledge Calibration / Point Collision

新增确定口径：

```text
Point Collision 不是自动联想。
它是 knowledge calibration：
外部资料先蒸馏成 candidate points，
再和本地 reviewed knowledge 做双向校准。
```

借鉴来源：

```text
Jon Doyle, "A Truth Maintenance System" (1979)
```

只吸收它的控制思想，不照搬老式 AI 系统：

```text
不要只记录结论。
要记录为什么相信这个结论。
新证据进入时，要知道哪些旧判断被支持、被挑战、被细化、暴露风险或需要复查。
行动依据要能解释来源、理由和风险。
```

校准输出只可能是 review input：

```text
candidate_relation
contradiction_candidate
scope_mismatch
stale_assumption_candidate
missing_evidence
review_question
review_due
```

校准输出不能直接创建：

```text
reviewed_claim
reviewed_relation
truth confidence update
automatic promotion
automatic conflict resolution
```

边界：

```text
raw source 不直接撞库，candidate points 才做校准。
Point Collision 由 candidate / review / promotion / action 需求触发，不由原始 capture 自动触发。
light capture 默认只保留 source；只有生成 candidate point 且需要 review、晋级、行动、处理冲突或用户明确要求处理时，才进入 collision。
本地 reviewed knowledge 不是永远的裁判，外部新资料也不会自动赢。
相似不是支持。
冲突不是自动推翻。
重复出现不是自动真理。
review 决定是否更新本地可信世界观。
```

## Evidence-Aware Review / 支持-反对式 Review

新增确定口径：

```text
Review 不只是 source check。
Review 是 standing check：
看一个判断在支持、反对、范围限制和风险都摆出来后，现在还站不站得住。
```

懒触发边界：

```text
普通 candidate 不强制展开完整 review 面板。
只需要 uncertainty / risk 短注即可。

完整 support / challenge / qualification / risk 面板只在这些场景展开：
claim / pattern / anti-pattern / decision promotion
context pack / action basis
strong reviewed relation
explicit contradiction
stale or contested claim
reviewer-requested standing check
```

人话关系族：

```text
support        -> supports
attack         -> contradicts
qualification  -> refines
risk           -> risk_of
provenance     -> derived_from
```

注意：

```text
这个映射是大致对应，不是完全等价。
provenance 不是 support。
有引用不等于有证据。
支持变多不自动提高 confidence，只增加 review evidence。
confidence 只能通过 review 修改。
```

状态建议：

```text
candidate:
  还没审

standing:
  审过，目前站得住

contested:
  有重要挑战，不能无脑用

stale:
  可能过时或 scope 已变

superseded:
  被新判断替代

rejected:
  审过，不采纳
```

挑战严重度：

```text
fatal
major
minor
out_of_scope
unresolved
```

行动可用性单独记录：

```text
action_readiness:
  ready / not_ready / risky / needs_review
```

每个重要 claim / pattern / decision 至少回答：

```text
为什么现在还站得住？
已知最强反对是什么？
适用范围是什么？
主要风险是什么？
什么时候要复查？
```

## Pro 补充 3：轻量 Source Provenance

已吸收 W3C PROV 的轻量思想，但不实现完整 PROV 标准，也不把 Source node 做成使用日志。

```text
Source node 负责：
  source identity
  capture provenance
  optional extraction trace for medium/heavy sources

Reviewed node / relation 负责：
  reviewed_by

Promotion event / reviewed node 负责：
  promoted_by

Context pack / Use Ledger 负责：
  used_sources / used_nodes
```

边界：

```text
provenance 只记录来源和处理轨迹。
它不判断 truth、support、confidence 或 action_readiness。
它不让 source 自动支持 claim。
claim 是否站得住，仍然交给 calibration 和 evidence-aware review。
```

source record:

```text
raw/articles/2026-05-29-w3c-prov-source.md
```

## Pro 补充 4：Verifiability Routing

已吸收 VERISCORE 的核心启发，但不实现它的 factuality metric。

```text
不是所有 candidate point 都是 claim。
candidate point 是 atomic review unit。
进入 review 前先判断：
  point_type
  verifiability
  review_route
```

最小字段：

```text
point_type:
  claim / interpretation / hypothesis / pattern / risk / preference / decision / open_question / implementation_note

verifiability:
  verifiable / partially_verifiable / not_verifiable / unknown

review_route:
  evidence_check / rationale_check / instance_check / risk_check / action_basis_check / personalization_only / research_question / code_anchor_check
```

边界：

```text
review_route 默认从 point_type 推导，可以人工覆盖。
不可验证不等于没用。
不可验证只是不拿 truth confidence。
只有可验证 claim 可以有 truth / evidence confidence。
preference、hypothesis、open_question 不走 truth verification。
```

source record:

```text
raw/papers/2026-05-29-veriscore-source.md
```

## Pro 补充 5：Claim / Point Coverage Map

已吸收 PaperTrail 的核心启发，但不实现完整 UI，也不做全量遗漏扫描。

```text
Context pack 不是 citation list。
Context pack 是 key point coverage map。
```

最小字段：

```text
coverage_overview:
  supported
  weakly_supported
  challenged
  missing_evidence
  out_of_scope
  risk_flags

coverage_map:
  point
  point_type
  coverage_status
  support_refs
  challenge_refs
  risk_refs
  critical_omissions
  note

action_readiness:
  state
  reason
```

coverage_status:

```text
supported
weakly_supported
challenged
missing_evidence
out_of_scope
not_verifiable
```

边界：

```text
coverage_map 是 Context Pack / Action Basis 的审计面，不是 truth layer。
Context pack 必须 coverage-aware，但不默认展开完整审计表。
完整 coverage_map 只要求覆盖回答或行动依据中实际使用的关键判断。
ordinary query / 普通回答不强制生成完整 coverage_map。
coverage_status 不能自动提高 confidence。
missing_evidence 不等于 false。
challenged 不等于 rejected。
risk_flags 只做 overview 风险提示；具体风险仍放在 risk_refs，行动可用性仍看 action_readiness: risky / needs_review。
critical_omissions 只记录已知重大遗漏，不做全库遗漏扫描。
默认只显示 coverage overview、高风险项、被挑战项和缺证据项；decision、action basis、agent context pack、高影响回答、显式 audit 或回答被挑战时，再展开 key point 和 evidence detail。
```

source record:

```text
raw/papers/2026-05-29-papertrail-source.md
```

## Pro 补充 6：Optional Point Graph Fragment

已吸收 GraphFC 的轻量启发，但不实现完整 graph fact-checking pipeline。

```text
普通 candidate:
  保持自然语言 atomic review unit。

复杂 / 高影响 / 多跳 / 跨文档 / action-relevant / ambiguous candidate:
  可选附 point_graph_fragment。
```

用途：

```text
帮助 Understand 不只是抽句子。
帮助 Point Collision 比较 entity / relation / qualifier / scope。
帮助 Evidence-Aware Review 看清复杂判断由哪些关系组成。
必要时帮助 coverage_map 展开 triplet-level detail。
```

边界：

```text
point_graph_fragment 是 review aid，不是 reviewed relation。
triplet extraction 不是 truth。
triplet similarity 不是 support。
triplet conflict 不是 automatic rejection。
只有 reviewed relation 可以进入 formal knowledge graph。
普通 candidate 不需要 graph fragment。
不做完整 GraphFC pipeline。
超过 3-5 个 essential triplets 时，应拆成多个 candidate point。
```

source record:

```text
raw/papers/2026-05-29-graphfc-source.md
```

## Pro 补充 7：Evidence Support Check

已按 Pro 复核吸收，但有一个重要收缩：这不是完整 Citation Faithfulness 系统。

```text
A source link is not evidence.
Evidence must support the specific point.
```

当前定位：

```text
Evidence Support Check:
  检查某个 source span / excerpt / code range / table anchor 是否真的支持目标 point、reviewed node 或 reviewed relation。

Citation Faithfulness:
  只作为启发和警告。
  完整因果 faithfulness verification 不在当前范围内。
```

最小字段：

```yaml
evidence_support:
  span_supports_target: supported | partial | unsupported | unclear
  evidence_role: direct_support | inferential_support | background_context | counterexample
  reviewer_note:
```

边界：

```text
字段放在 evidence item / source_refs 下，不放 Source node 主字段。
URL-only source_refs 是 provenance，不是 support。
background_context 不能计入 supported，不能提高 confidence。
inferential_support 要有 reviewer_note 才能作为 promotion support。
counterexample 进入 challenge_refs / risk_refs。
span_supports_target = unsupported / unclear 不能作为 promotion support。
强 reviewed relation 的 evidence 必须支持 relation edge 本身，而不是只支持两个端点。
不做自动 ProVe pipeline、NLI、RTE、support score 或 causal citation faithfulness。
```

coverage / support 映射：

```text
supported + direct_support 可计入 supported。
partial + inferential_support + reviewer_note 可计入 weakly_supported，或由 reviewer 接受为 promotion support。
background_context 永远不能计入 support。
counterexample 进入 challenge_refs / risk_refs，不进 support_refs。
unsupported / unclear 不能作为 promotion support。
```

source records:

```text
raw/papers/2026-05-29-prove-provenance-verification-source.md
raw/papers/2026-05-29-rag-attribution-faithfulness-source.md
```

## Pro 补充 8：Evidence Sufficiency Gate

已吸收 Self-RAG / CRAG / A2RAG 的轻量控制思想，但不实现完整检索/纠错 pipeline。

```text
Evidence Support Check:
  单条证据是否真的支持某个 point / relation。

Evidence Sufficiency Gate:
  这一组证据是否足够支撑当前 context pack / action basis / decision / promotion / strong relation。
```

放置位置：

```text
Connect
-> draft evidence / context envelope
-> Evidence Sufficiency Gate
-> final Context Pack / Action Basis
-> Act
```

更精确地说：Gate 不是空跑在 context pack 之前；它在初步 evidence envelope / draft context pack 组好后运行，用来判断这包东西能不能被定稿为 action-ready。

最小字段：

```yaml
evidence_sufficiency:
  state: sufficient | weak | insufficient | out_of_scope | risky
  checked_for: context_pack | action_basis | decision | promotion | reviewed_relation | risk_sensitive_answer
  missing: []
  required_next_step: proceed | ask_user | retrieve_more | create_missing_point | narrow_scope | mark_not_actionable | needs_review
  reviewer_note:
```

触发边界：

```text
普通 capture / ordinary query 不触发。
只在 promotion、decision、strong reviewed relation、context pack / action basis、risk_sensitive_answer，或用户明确问“证据够不够 / 能不能行动”时触发。
```

规则：

```text
sufficient:
  可以继续。

weak:
  必须暴露 gaps 和 weak support。

insufficient:
  不能输出 ready action basis。

out_of_scope:
  必须标出 scope mismatch。
  如果证据只是不支持原来的大范围判断，应优先考虑 narrow_scope。

risky:
  必须进入 action_readiness: risky / needs_review。

retrieve_more:
  是建议动作，不是自动检索，除非用户明确授权。
```

不吸收：

```text
不实现 Self-RAG / CRAG / A2RAG pipeline。
不做自动 retrieval evaluator。
不做自动 web search / agentic retriever。
不做 automated correction loop。
不让 LLM 自评直接决定 sufficiency。
不让 evidence_sufficiency 改 truth confidence。
```

source records:

```text
raw/papers/2026-05-29-self-rag-source.md
raw/papers/2026-05-29-crag-source.md
raw/papers/2026-05-29-a2rag-source.md
```

## 已更新的关键文件

```text
AGENTS.md
README.md
FUSION_ARCHITECTURE_V0_2_DRAFT.md
SECOND_BRAIN_MODEL.md
ARCHITECTURE_PRINCIPLES.md
SCHEMA.md
IMPLEMENTATION_BLUEPRINT.md
SOURCE_INTAKE.md
REFERENCE_REVIEW_PROTOCOL.md
MEMORY_TIER.md
DEV_CONTEXT.md
REVIEW_QUEUE.md
FEEDBACK.md
templates/architecture-review-window-prompt.md
templates/claim-record.md
templates/decision-record.md
templates/dev-context-pack.md
templates/design-pattern.md
templates/library-review.md
templates/anti-pattern.md
templates/review-candidate.md
templates/source-record.md
wiki/indexes/knowledge-graph-index.md
wiki/indexes/memory-tier-reference-index.md
raw/articles/2026-05-29-w3c-prov-source.md
raw/papers/2026-05-29-veriscore-source.md
raw/papers/2026-05-29-papertrail-source.md
raw/papers/2026-05-29-graphfc-source.md
raw/papers/2026-05-29-prove-provenance-verification-source.md
raw/papers/2026-05-29-rag-attribution-faithfulness-source.md
raw/papers/2026-05-29-self-rag-source.md
raw/papers/2026-05-29-crag-source.md
raw/papers/2026-05-29-a2rag-source.md
```

## 当前明确没有做

```text
没有实现脚本。
没有跑 dev context pack。
没有跑 query-run。
没有写 feedback-event。
没有做 PUBLISHING_PIPELINE。
没有做自动化 daily / weekly synthesis。
没有做 API / MCP / viewer。
没有 push。
```

## 下一步建议

方向已经清晰，不建议继续无止境看资料堆设计。

下一步应该从“架构设计”转入“最小闭环试跑”，但要很小：

```text
1. 选 3-5 条已有资料。
2. 生成 candidate point。
3. 做 supports / contradicts / refines / risk_of / derived_from 关系试撞。
4. 人工 review 一个小 cluster。
5. 产出一个 context pack / action basis 样例。
6. 记录一次 feedback / review_due。
```

验证目标不是自动化，而是判断：

```text
这套 reviewed second brain 是否真的比普通 Karpathy wiki 更会形成行动依据？
point collision 是否真的减少重复阅读？
Use Ledger 是否真的改善下次激活路径？
Risk / Inhibition 是否能防止漂亮但错误的连接？
```

## 当前风险提醒

```text
1. 不要把大脑模型变成十几个工程模块。
2. 不要把 scheduled synthesis 做进 MVP。
3. 不要让 dashboard / retrieval / metadata / brief 变成 reviewed knowledge。
4. 不要把 feedback 写成 truth confidence 自动更新。
5. 不要为了兼容旧关系类型，把 relation enum 重新扩成一长串。
6. 不要急着做 agent security platform；现在只需要轻规则，等 agent 真能写/执行再升级。
```

## 给下个窗口的口径

```text
当前主线成立，而且比单纯 Karpathy LLM Wiki 更强：
Karpathy 负责简单可用，
Dusk 负责项目桌面，
Reviewed-action core 负责来源、证据、关系、风险和行动依据，
Use Ledger 负责用后校准，
Proactive Synthesis 只做候选生成器。

但现在必须收缩。
不要继续把所有好点子塞进核心。
下一步优先做最小闭环试跑。
```
