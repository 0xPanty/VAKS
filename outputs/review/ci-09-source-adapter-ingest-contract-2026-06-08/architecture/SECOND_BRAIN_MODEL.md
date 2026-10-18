# Second Brain Model

这个资料库不是普通笔记库，也不是单纯 RAG 或 Obsidian 模板。

这个文件是解释模型和设计校验表，不是工程模块目录。

工程主线以 `FUSION_ARCHITECTURE_V0_2_DRAFT.md` 里的 verified loop 为准；对外 README 只讲五层：

```text
Capture -> Understand -> Review -> Connect -> Act and Learn
```

当前落地口径：

```text
1. 大脑模型降权：
   它解释系统为什么需要输入、理解、复核、联想、激活、行动、反馈和风险抑制。
   它不定义实现模块。

2. 主架构不变：
   Capture -> Understand -> Review -> Connect -> Act and Learn。

3. 内部主线不变：
   source -> candidate points -> calibration / point collision -> review -> reviewed relation / node -> context pack -> action -> feedback。

4. Risk / Inhibition 是横切层：
   它贯穿 capture、comprehension、review、association、activation、action、feedback。

5. Proactive Synthesis、Expression / Publishing、Agent Tool Safety 不进 truth core：
   它们分别是候选生成器、未来输出面、未来执行安全层。
```

不要把下面的编号读成线性执行顺序。更准确的分组是：

```text
Input:
  Capture / Provenance

Comprehension:
  summary
  candidate point
  missing point

Reviewed Memory:
  claim
  pattern
  anti-pattern
  decision

Association:
  knowledge calibration / point collision
  reviewed relations

Activation:
  activation tier
  dev context
  context activation
  association neighborhood activation

Action:
  context pack
  decision support
  implementation note

Learning:
  use ledger
  feedback event
  review_due
  cooling / reactivation

Cross-cutting Inhibition:
  risk
  negative evidence
  contradiction
  source hygiene
  safety gate

Optional Output:
  proactive synthesis
  expression / publishing
```

它的目标是做一个有可信边界的第二大脑：

```text
会摄取信息。
会管理激活和注意力。
会整理理解。
会沉淀 reviewed / evidence-backed memory。
会建立联想。
会主动回看和提出候选问题。
会支持判断和行动。
会从反馈中学习。
会降温和再激活。
会保护自己不被错误信息污染。
```

一句话：

```text
This is a verified second brain:
it captures sources, turns them into candidates, reviews evidence-backed knowledge,
connects points through traceable relations, builds action context,
and learns from use without rewriting truth.
```

中文大白话：

```text
它不是一个存笔记的地方。
它是一个会摄取、会整理、会联想、会提醒、会复盘、会帮你形成行动依据的第二大脑。

但它不会把灵感直接当真理。
也不会把自动总结直接当决策。
```

## 1. Capture：感官输入

人脑先接收外界刺激。

资料库也一样。文章、截图、语音、链接、repo、论文、对话、项目材料都先进入 raw source / inbox。

对应系统：

```text
raw/
00-INBOX style capture
source ingest
source record
```

核心原则：

```text
先收进来。
保留来源。
不要要求当场分类、总结、判断。
```

Source record 里保留轻量 provenance：资料是什么、从哪里来、什么版本、什么时候收录、谁或什么工具捕获/提取过。

review、promotion、context-pack 使用记录不塞回 source 文件；它们分别属于 reviewed node、promotion record、context pack 或 use ledger。

这只是来源追溯，不是判真。

边界：

```text
capture 不是 truth。
原始资料不能被自动改写成结论。
```

## 2. Activation：激活与当前工作记忆

人脑不会同时加载全部记忆。

它会决定现在什么最重要、什么暂时放后台。

对应系统：

```text
MEMORY_TIER.md
Activation Tier:
  hot / warm / cold
DEV_CONTEXT.md
Core / Support / Risk / Cold References
```

核心原则：

```text
hot 不是 true。
hot 只是当前 scope 下要先看。

cold 不是没用。
cold 只是现在不占注意力。
```

对外说法：

```text
The vault has activation tiers, not truth tiers.
Hot means read early, not believe more.
```

MemGPT 给这里的启发是 virtual context management：在有限 context window 里管理快/慢记忆。
本资料库只吸收这个 activation / context discipline，不吸收 agent OS 或自动 memory manager。

边界：

```text
memory_tier 更准确地说是 activation layer。
它不能改变 verification_status、evidence_level 或 confidence。
```

## 3. Comprehension：理解与整理

人脑会把原始输入压缩成理解。

资料库也需要把 raw source 变成 summary、candidate point、claim 候选和 pattern 候选。

对应系统：

```text
ingest / compiler
summary
review candidate
candidate point
```

核心原则：

```text
理解结果先是候选。
候选不是正式知识。
不是所有候选都是 claim。
```

Candidate 进入 review 前要先做轻量分流：

```text
它是什么类型？
它能不能事实验证？
它该走哪条 review 路径？
```

说人话：

```text
事实走验证。
解释走理由。
假设走研究问题。
模式走实例。
风险走失败证据。
偏好只做个性化。
决策走行动依据。
代码笔记走代码锚点。
```

复杂、高影响、跨文档或有歧义的 candidate，可以可选拆成 `point_graph_fragment`：

```text
不是只看一句话像不像。
而是看清楚：
  哪些 entity 参与？
  它们之间是什么 relation？
  scope / version / condition 是什么？
  哪些 triplet 有 source anchor？
```

它只帮助校准和 review 更精确，不自动生成 truth 或 reviewed relation。

边界：

```text
LLM 可以帮助整理。
但 LLM 编译结果不能直接进入 reviewed knowledge layer。
summary 只是 source-level digest。
只有 reviewed claim / pattern / risk / decision 才能进入长期可信记忆。
不可验证不等于没用，但不能获得 truth confidence。
```

## 4. Reviewed Memory / Evidence-backed Memory：有证据的长期记忆

人脑会把反复使用、证据更稳、经得起复查的东西沉淀为长期记忆。

资料库的长期记忆不是所有笔记，而是有来源、有证据、经过关系/反例/复查的正式节点。

对应系统：

```text
wiki/claims/
wiki/patterns/
wiki/anti-patterns/
wiki/decisions/
SCHEMA.md
```

核心原则：

```text
Markdown/YAML 是主记录。
dashboard、retrieval、metadata、cache、context pack 都不是 reviewed knowledge。
```

边界：

```text
没有 provenance、verification_status、evidence_level、confidence 的高影响结论，
不能作为行动依据。
```

## 5. Association：联想网络

人脑靠联想把不同记忆连接起来。

资料库也需要记录资料之间的 supports、contradicts、refines、risk_of、derived_from 等关系。

对应系统：

```text
relations
semantic relation edge
point collision
knowledge graph
```

核心原则：

```text
连接可以启发思考。
强连接必须有 evidence 和 rationale。
查询时点亮的是 evidence-aware association neighborhood，不是孤立 chunk。
GraphRAG / LightRAG 提醒我们：这个 neighborhood 可以分低层具体证据、高层主题模式、关系邻域三层召回。
```

边界：

```text
link overlap、tag、backlink、search score 可以提示相关。
但它们不能替代 reviewed relations。
graph traversal / PPR / association score 也不能替代 support、confidence 或 truth。
community report 不是 truth。
graph rank 不是 trust。
auto-extracted relation 不是 reviewed relation。
candidate relation neighborhood 不能冒充 reviewed relation neighborhood。
```

## 6. Proactive Synthesis：主动思考（候选生成器）

人脑不会只在被问时思考。

它会在睡觉、散步、复盘时重新整理最近输入，发现重复模式、矛盾、遗漏和旧记忆的新用途。

资料库也需要这种主动回流，但它不是 truth core。

对应系统：

```text
on-demand synthesis
daily / weekly / monthly brief later
conversation-derived feedback routing
```

核心原则：

```text
系统按需回看最近输入。
找连接。
找模式。
找矛盾。
找被降温但现在相关的旧资料。
提出值得继续想的问题。
```

边界：

```text
主动思考可以产生 candidate。
主动思考不能直接产生 truth。

brief 是提醒。
connection 是线索。
pattern 需要 review。
decision 需要行动依据。
```

最小优雅吸收版：

```text
MVP 先做 on-demand synthesis，把最近材料、旧资料、连接、矛盾和问题推出来。
所有输出先进入 brief / candidate / review。
不直接改 reviewed knowledge layer。
daily / weekly / monthly automation 先 parked。
```

## 7. Decision Support：判断与执行功能

人脑的高级功能不是只记住信息，而是用信息做判断。

资料库也不能停在“知道很多”。它要帮助回答：

```text
现在能不能行动？
前提是什么？
风险是什么？
如果错了怎么回退？
成功指标是什么？
```

对应系统：

```text
decision
action basis
context pack
implementation-note
```

核心原则：

```text
知识要能变成行动依据。
行动依据必须带 risk、preconditions、rollback、success metric 和 feedback path。
context pack 不能只给 citation，还要显示关键判断的 coverage。
哪些被支持、哪些证据弱、哪些被挑战、哪些缺证据、哪些 out of scope、哪些有风险。
还要检查 temporal applicability：这个判断在当前时间、版本、项目、环境下是否仍然适用，是否已经 stale / superseded。
如果新决策替代旧决策，旧决策不删除；要链接 replacement，并把受影响的 claims / patterns / relations / context packs 标记 review_due。
行动前还要问 evidence_sufficiency：这组证据够不够支撑当前 action basis / decision / promotion。
重大行动前还要确认 intent：我理解你的目的、假设、范围和成功标准对不对。
```

边界：

```text
context pack 是调用层输出。
它不能发明未记录的 truth。
coverage_map 是审计面，不是 truth layer。
coverage_status 不能自动提高 confidence。
Temporal Applicability Check 不改 truth；它只判断一个已审过的判断现在能不能用。
Decision superseding 不抹掉历史，只改变当前适用性并触发复查压力。
Evidence Sufficiency Gate 不改 truth confidence；证据不足时只能 ask_user / retrieve_more / create_missing_point / narrow_scope / mark_not_actionable / needs_review。
Intent confirmation 不判真，只防止行动跑偏；普通问答不用触发。
```

## 8. Use Ledger / Feedback：使用记录与反馈校准

人脑会从结果中学习。

一个判断后来对了、错了、漏了、过时了，都应该反过来改变系统的激活路径和复查任务。

对应系统：

```text
FEEDBACK.md
query-run
context-pack snapshot
feedback-event
action feedback
next_review
review_due
```

核心原则：

```text
Use Ledger 记录知识被怎么用过。
反馈让系统知道哪些回答有用、哪些跑偏、哪些范围错、哪些资料该重新看。
Decision outcome calibration 记录“当时建议怎么做、用户怎么选、后来结果怎样”，用来改进未来 recommendation。
```

边界：

```text
反馈可以调整 usefulness、scope fit、activation ranking。
反馈不能直接修改 truth confidence。
truth confidence 仍然必须通过 review / promotion 修改。
```

## 9. Cooling And Reactivation：降温与再激活

人脑会让暂时不用的信息退到后台，但不是删除一切。

好的第二大脑也应该让暂时不用的东西降温，而不是永久占据注意力。

对应系统：

```text
cold references
archive-first lazy reactivation
project closeout scan
memory_tier cooling
```

核心原则：

```text
不用的资料降温。
需要时重新激活。
复用后才考虑变 warm。
真正成为当前任务必需时才进入 Core。
```

边界：

```text
不要靠搬文件制造记忆层级。
优先用 metadata、index、dashboard 和 dev context 投影。
这里是 activation decay，不是 memory deletion。
```

## 10. Cross-Cutting Risk / Inhibition：横切风险与抑制层

人脑需要怀疑、纠错和自我保护。

第二大脑也需要免疫系统，防止自动总结、伪连接、错误来源、过度自信和架构臃肿污染长期记忆。

对应系统：

```text
anti-pattern
source hygiene
review gate
lint / health check
risk layer
```

核心原则：

```text
负面证据和反模式不是噪音。
它们是决策前必须检查的风险层。
Risk / Inhibition 不是最后一步，而是贯穿每一步的横切控制。
```

边界：

```text
自动化只能生成候选。
不能自动裁决冲突。
不能自动晋级 truth。
不能把 dashboard、retrieval、metadata 当作可信来源。
```

它贯穿：

```text
Capture:
  source hygiene

Understand:
  summary / extraction uncertainty

Review:
  contradiction / negative evidence

Connect:
  false relation risk

Context Pack:
  known risks and gaps

Action:
  intent confirmation / preconditions / rollback / failure mode

Feedback:
  missed contradiction -> review_due
  decision outcome -> future recommendation calibration
```

Maintenance manifest 是这个免疫系统的清单：它列出缺证据、缺 source anchor、过期适用范围、缺 intent confirmation、confidence cap 违规等问题。它只提醒，不自动修。

## System Shape

对外不要讲 10 个并列脑层。

README 只讲五层：

```text
Capture
  Save sources without forcing instant judgment.

Understand
  Turn sources into summary, candidate points, candidate claims, risks, and questions.

Review
  Promote only source-backed, reviewed knowledge into durable memory.

Connect
  Compare new points with old points:
  supports / contradicts / refines / risk_of / derived_from.

Act and Learn
  Build context packs and action basis.
  Record feedback.
  Improve activation without rewriting truth.
```

内部主循环是：

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

横切控制贯穿整条链：

```text
Provenance
Risk / Inhibition
Traceability
Safety Gate
```

旁路能力是候选生成器或输出面，不是 truth core：

```text
Proactive Synthesis:
  on-demand first, scheduled later, candidate only.

Expression / Publishing:
  future output surface.

Agent Tool Safety:
  future execution safety, only needed when agents can write or execute.
```

对应到当前架构：

```text
Karpathy spine:
  简单入口、raw/wiki/index/log、ingest/query/lint。

Dusk workbench:
  当前项目桌面、scope dashboard、任务和资料候选面。

Verified-action core:
  source provenance、review gate、schema、relations、pattern、anti-pattern、decision。

Activation tier:
  注意力和激活优先级，不是真值。

Dev context:
  当前任务的临时工作记忆，不是永久知识层。

Proactive synthesis:
  按需回看，提出连接、矛盾、模式和问题。
  自动 daily / weekly / monthly 先不进 MVP。

Use Ledger / Feedback loop:
  从真实使用和行动结果里校准 activation、usefulness、scope fit。
  不直接改 truth confidence。

Risk / Inhibition layer:
  防止错误资料、伪连接、自动真理和过度设计污染系统。
  它是横切层，不是最后一站。
```

## Neural Design：神经式连接机制

这个系统不只是把资料放进文件夹。

它更像一个可验证的联想网络：

```text
入库时建立连接。
查询时激活连接。
用后修正连接。
风险层负责刹车。
主动思考负责后台回放。
```

### 1. Knowledge Calibration / Point Collision：校准式记忆形成

新资料进入时，不是孤立保存，也不是整篇 raw source 直接撞库。

系统先把外部资料理解成少量 candidate points，再把这些点和本地 reviewed knowledge 做校准。

说人话：

```text
外部资料 = 新证据
本地 reviewed knowledge = 当前判断
校准 = 看新证据会不会影响当前判断
review = 决定到底改不改
```

它会检查：

```text
它支持了哪些已有判断？
它挑战了哪些已有判断？
它细化了哪些 pattern？
它暴露了哪些 risk？
它说明哪些旧判断可能过时？
它在哪些 scope / version / time / condition 下才成立？
它提出了哪些需要复查的问题？
```

`replaces`、`implements`、`applies_to`、`inspired_by`、`alternative_to`、`blocked_by`
这些关系先不进 MVP。等五种核心关系跑顺以后，再看是否真的需要扩展。

这相当于新证据和本地判断体系互相校准。

它吸收了 Truth Maintenance System / Reason Maintenance 的一个核心思路：

```text
不要只记录结论。
还要记录为什么相信这个结论。
新证据进来时，要知道哪些旧判断需要复查。
行动依据要能解释来源、理由和风险。
```

边界：

```text
校准只生成 review input。
相似不是支持。
冲突不是自动推翻。
重复出现不是自动真理。
本地旧知识不是永远的裁判。
外部新资料也不会自动赢。
强关系必须有 evidence 和 rationale。
reviewed relation 必须经过 review。
```

### 1.1 Evidence-Aware Review：支持-反对式复核

Review 不是简单问“有没有来源”。

它要问：

```text
这个判断有谁支持？
有谁挑战？
挑战是不是致命？
它只在哪些条件下成立？
风险是什么？
现在能不能用于行动？
```

说人话：

```text
Review 是看这个判断在支持、反对、范围限制和风险都摆出来后，还站不站得住。
```

状态建议用来表达“当前站立状态”：

```text
candidate:
  还没审

standing:
  审过，目前站得住

contested:
  有重要争议，不能无脑用

stale:
  可能过时或换了 scope

superseded:
  被新判断替代

rejected:
  审过，不采纳
```

行动可用性要单独判断：

```text
action_readiness:
  ready / not_ready / risky / needs_review
```

核心边界：

```text
有引用不等于有支持。
derived_from 只是来源，不是证据强度。
反对意见不一定推翻结论，可能只是限制范围或触发 review_due。
支持变多不会自动提高 confidence，只会增加 review evidence。
```

### 2. Context Activation：联想激活

用户提问时，系统不是只做关键词搜索。

它也不是只拿几个相似 chunk。

它会沿着 activation tier、reviewed relations、dev context、risk layer 点亮一片经过审查的联想邻域：

```text
Core:
  当前任务必须看的内容。

Support:
  有帮助但不必全部加载的背景材料。

Risk:
  决策前必须检查的反例、冲突、反模式。

Decision:
  旧决策、适用范围、回退和已知结果。

Scope:
  项目、版本、时间、环境和条件限制。

Cold References:
  可追溯旧资料，需要证据时再打开。
```

HippoRAG 给这里的启发是 association retrieval：从一个查询出发，沿图上的相关连接找到一片邻域。
但在本资料库里，这片邻域必须服从 reviewed-action 边界。

GraphRAG / LightRAG 给这里的补充是 retrieval stratification：

```text
low-level:
  source / text unit / claim / entity

high-level:
  pattern / theme / community

relation neighborhood:
  reviewed relation 周边上下文
```

这让 context pack 不只是几个相似 chunk，而是同时拿到具体锚点和大范围背景。

边界：

```text
激活顺序不是可信度。
搜索相似度不是 truth。
graph traversal / PPR / association score 不是 support。
community report 不是 truth。
graph rank 不是 trust。
auto-extracted relation 不是 reviewed relation。
candidate relation neighborhood 不能冒充 reviewed relation neighborhood。
被点亮的邻居不是 reviewed relation。
context pack 不能发明未记录结论。
```

### 3. Activation Feedback：突触修正

一次回答用完以后，系统要记录这条激活路径有没有帮上忙。

反馈不直接改 truth。

反馈修正的是：

```text
usefulness:
  这条资料对这类问题有没有用。

scope fit:
  这条资料适不适合当前项目、版本、时间、场景。

activation ranking:
  下次同类问题要不要更早点亮这条路径。

review_due:
  负反馈、明确纠错、漏证据或漏矛盾会触发复查压力。
```

反馈不能直接修改：

```text
truth confidence
verification_status
source reliability
decision outcome
```

例子：

```text
答偏了:
  降低这条 route 在当前 scope 下的激活权重。

漏了:
  生成 missing-point 或 missing-relation candidate。

过时了:
  标记 review due。

忽略了矛盾:
  下次 context pack 必须带 contradiction。

用户明确纠错:
  创建 review_due。
```

Reflexion 给这里的启发是：agent 不靠更新权重学习，而是把反馈写成 verbal reflection / episodic memory，供后续决策使用。
在本资料库里，这对应 Use Ledger：反馈进入记录，影响未来激活，不直接改 truth。

强规则：

```text
Positive feedback is weak.
Negative feedback creates review pressure.
Explicit correction creates review_due.
Decision outcome improves future recommendation, not truth.
```

### 4. Conversation-Derived Feedback：从对话里提取弱反馈

用户不一定每次都会打分。

但下一句话本身就有信号：

```text
继续沿同一条线问:
  方向可能有用。

把问题问得更窄:
  方向可能对，但 scope 需要变细。

说“不是这个意思”:
  route 错了。

说“漏了 X”:
  要补 missing point 或 missing route。

直接换题:
  关闭上一条 route，不做持久强化。
```

边界：

```text
conversation-derived feedback 默认是弱信号。
它优先调整 route、keyword、scope 和 missing candidate。
它不能把某个观点直接变成 truth。
```

RMM 给这里的启发是 forward-looking / backward-looking reflection：

```text
forward-looking:
  总结下一次检索该看什么、避开什么、补什么。

backward-looking:
  回看引用证据、漏掉的矛盾和失败 route。
```

这些都只能生成 feedback-event、missing-point、missing-evidence 或 review_due，不直接改 truth。

### 5. Inhibition / Risk：抑制信号

人脑不只需要兴奋，也需要抑制。

资料库也一样。

anti-pattern、negative evidence、contradiction、source hygiene warning 是系统的抑制信号：

```text
它们阻止系统沿着漂亮但错误的路线一路兴奋下去。
```

边界：

```text
Risk 不是 Support 的附属品。
Risk 是行动前必须检查的一等层。
```

### 6. Proactive Synthesis：后台回放

人脑会在睡眠、散步、复盘时重新整理最近输入。

资料库也需要这种后台回放：

```text
on-demand synthesis
daily brief later
weekly connections later
monthly belief / gap review later
```

它负责主动找：

```text
重复出现的模式
跨资料连接
矛盾
遗漏
被降温但现在相关的旧资料
今天值得继续想的问题
```

边界：

```text
主动思考可以提出问题和候选。
主动思考不能直接写入 reviewed truth。
MVP 先按需触发，不先做定时自动化。
```

## Original And Fusion Innovations：自主创新与融合创新

这里的“创新”不是说全世界没人想过。

它指的是：在这个资料库架构里，我们自己定义出来的控制规则，或把外部系统的好零件拆开后重新融合成更适合本系统的设计。

### 自主创新

```text
Verified Action Knowledge System:
  不是普通 second brain，也不是普通 RAG。
  目标是让资料可追溯、可验证、可连接、可行动，并能从行动反馈中学习。

Point Collision:
  新知识先蒸馏成 candidate points，再和本地 reviewed knowledge 做双向校准，形成 supports / contradicts / refines / risk_of / derived_from 等候选信号和复查问题。

Activation Feedback:
  用后修正联想路径，而不是直接改 truth。

Conversation-Derived Feedback:
  从连续追问、纠偏、问题变窄、说漏了、换题里提取弱反馈。

Feedback Polarity Rule:
  正反馈弱，负反馈制造 review pressure，明确纠错触发 review_due。

Truth / Usefulness / Scope Fit 三分:
  truth 管真假。
  usefulness 管有没有帮上忙。
  scope fit 管适不适合当前项目、版本、时间、场景。

Activation Tier 不是 Truth:
  hot 只是先看，不是更真。
  cold 只是暂时不占注意力，不是没用。
  对外叫 Activation Tier，不叫 truth tier。

Dev Context 四层:
  Core / Support / Risk / Cold References。
  其中 Risk 是决策 checkpoint，不是噪音。

Traceability-First, Graduated Verification:
  普通资料先保证来源可追溯。
  严格验证只在晋级或用于行动时触发。

Context Pack 作为行动包:
  它帮助人或 agent 行动。
  但它不是 reviewed knowledge layer，不能发明未记录结论。
```

### 融合创新

```text
Karpathy-simple outside + verified-action strict inside:
  外层保留 raw/wiki/index/log、ingest/query/lint 的简单体验。
  内层增加 review gate、evidence、relations、decision、feedback。

llm-wiki-compiler 工程能力 + 我们的 truth 边界:
  吸收 ingest、review queue、provenance、context pack、lint、MCP/viewer。
  不采用 generic page schema 作为 truth。

gbrain 认识论 + Markdown truth:
  吸收 facts / takes / hypothesis / bet / decision、holder、timeline、gaps。
  不提前复制完整 runtime。

OpenKB 长文档和 Skill Factory + review gate:
  吸收 long-document tree index、generator surface、path-scoped writes、ghost-link lint。
  拒绝 auto-compiled generic concept wiki 直接成为 reviewed truth。

PARA + Kepano + Dusk 的 activation / workbench 融合:
  PARA 提供“为什么现在激活”。
  Kepano 提供“用 metadata / view 浮出，不靠搬文件”。
  Dusk 提供“scope dashboard 当前项目桌面”。
  我们融合成 dashboard candidate surface -> dev context pack -> reviewed action basis。

knowledge-base-server + Kagantic 的 briefing-before-full-read:
  先给低 token briefing，再决定打开哪些全文。
  没有 SQL/MCP 前，用 Markdown index 做 routing。

Vellum / daily brief 的 proactive synthesis:
  吸收 Connections / Patterns / Contradictions / Open Questions 的输出结构。
  MVP 先 on-demand，daily / weekly / monthly 自动化先 parked。
  但所有输出先是 brief / candidate / review item，不直接变 truth。

Obsidian Bases / dashboard / graph view:
  作为 workbench 和 review surface。
  不定义 schema，不决定可信度。

QMD / nano-NotebookLM retrieval:
  BM25、vector、RRF、GraphRAG、generated graph 做候选召回和关系探索。
  搜索分数永远排在 verified 字段之后。

GraphRAG / LightRAG retrieval:
  吸收 low-level / high-level / relation-neighborhood 检索分层。
  不吸收 community summary as truth、graph rank as trust、auto-extracted relation as reviewed relation。

HippoRAG retrieval:
  吸收 association neighborhood activation。
  不吸收 Personalized PageRank / graph traversal 作为 truth、support、confidence 或 reviewed relation。

Graphiti / Zep temporal graph:
  吸收 validity window / supersession / episode-backed provenance。
  不吸收自动构图、自动 invalidation 或图数据库 runtime 作为 truth core。

Publishing feedback loop:
  发布后的评论、指标、读者反馈可以生成 feedback 或 missing-point。
  不能自动改 truth。

Claude / Obsidian creator workflow:
  作为未来 Expression / Publishing 层参考。
  完整流程是 capture -> automation routing -> Obsidian memory -> Claude daily synthesis -> weekly connection session -> content output -> feedback。
  现在只吸收流程设计和输出结构，不实现自动化。
```

一句话总结：

```text
我们的自主核心：
  入库建连接，查询点亮连接，用后修正连接。
  但 truth 永远由 review 和 evidence 决定。

我们的融合核心：
  外部系统给好零件。
  本系统负责边界、裁决和行动依据。
```

## Parked Future Layer：Expression / Publishing（未来输出面）

这个层先记录，等整体框架打磨稳定后再做。

它解决的问题是：

```text
第二大脑不能只吸收、整理、联想。
它还应该把筛选后的连接、模式、矛盾、问题和决策，转成外部输出。
```

对应人脑：

```text
Motor Output / Expression
```

也就是把内部思考变成：

```text
文章
推文
报告
README
架构说明
研究摘要
决策 memo
产品文档
```

Claude / Obsidian 文章里的完整流程可以先作为参考：

```text
1. Capture:
   Readwise / Whisper / Telegram 把资料低摩擦收进 vault。

2. Automation:
   N8N 负责格式化、自动打标、inbox routing、定时触发。

3. Memory:
   Obsidian 按 note type 组织，不按 topic 组织。
   CLAUDE.md 给 agent 提供身份、项目、思考风格和硬规则。

4. Daily Synthesis:
   每天读取最近 7 天 captures，输出四栏：
   Connections / Patterns / Contradictions / Open Questions。

5. Weekly Connection Session:
   每周读取最近 30 天，找真正意外的连接，并建议可以变成什么内容。

6. Content Output:
   把强 connection、pattern、contradiction 或 open question 转成 post / article / memo。

7. Feedback:
   发布表现、读者反应、外部质疑、行动结果回流为 feedback-event、missing-point 或 review item。
```

我们未来最小优雅版不是照搬整套工具链。

先只定义这个动作，不急着定时自动化：

```text
On-demand / Future Daily / Weekly Synthesis Output:
1. Connections:
   非显然连接，必须引用具体 note。

2. Patterns:
   三个以上 note 形成的重复模式。

3. Contradictions:
   两条 note 的冲突，先浮出，不自动解决。

4. Open Questions:
   反复出现但还没有解决的问题。
```

硬规则：

```text
不要总结。
不要泛泛建议。
每条输出必须能追到具体 note。
没有具体 note 就不要输出。
输出先进入 brief / candidate / review。
不自动改 raw。
不自动晋级 truth。
不自动发布。
```

等后续要做这一层时，优先补：

```text
EXPRESSION_OR_PUBLISHING.md
publish-draft template
voice / audience context
pre-publish risk gate
post-publish feedback loop
```

## Parked Future Layer：Agent Tool Safety（未来执行安全层）

这个层也是先记录，等未来 Codex、Claude Code、MCP、hooks、skills 或其他 agent 真正接入资料库执行任务时再正式落地。

它不是新的大脑核心。

它是给会动手的 agent 加安全带：

```text
谁能动资料库？
能读哪里？
能写哪里？
能不能跑命令？
能不能接 MCP / hooks / plugins？
能不能把会话经验变成长期规则？
```

对应人脑：

```text
Motor Safety / Immune Gate
```

也就是“手要动之前，先确认工具没有毒、动作不会越界”。

ECC / AgentShield 文章里的完整工具栈可以作为参考，但现在不照搬：

```text
ECC:
  大量 agents / skills / slash commands，提供工程团队式能力。

AgentShield:
  扫 CLAUDE.md、settings、MCP、hooks、agents、skills 的安全风险。

claude-mem:
  跨会话记忆，让 agent 记住项目习惯。

Superpowers:
  强制先计划、先思考、先测试，再写代码。

CLAUDE.md rules:
  项目级 agent 行为规则。
```

我们现在只吸收轻规则，不吸收整套插件运行时。

最小优雅版：

```text
1. 能力按需启用
   不全量加载 agents / skills / MCP。

2. 读宽写窄
   可以读上下文，但写 formal reviewed knowledge、schema、template、decision 必须更严格。

3. 危险操作先确认
   删除、批量改、外部网络、密钥、hooks、MCP、插件安装、权限扩大都要先说明。

4. 执行前先计划
   重要写入前先说明目标、文件、风险和回退方式。

5. 会话学习先当候选
   agent 从任务中学到的经验先进入 feedback / candidate，不自动变长期规则。

6. 不确定就停下
   agent 不猜、不硬做，先说明缺口或请求确认。
```

边界：

```text
Agent Tool Safety 不决定 truth。
它不替代 SCHEMA.md。
它不替代 review gate。
它不要求现在实现扫描器、CI、MCP 管控或自动化平台。
```

以后如果正式落地，优先补一个轻文件：

```text
AGENTS.md
或 TOOL_SAFETY.md
```

目标是一页规则，不是安全平台。

## README Short Version

可以直接放进 README 的短版：

```text
This vault is designed as a verified second brain.

It captures sources, turns them into candidates, reviews evidence-backed knowledge,
connects points through traceable relations, and builds action context with risks,
assumptions, rollback, and feedback path.

It can suggest connections, questions, and patterns.
Only reviewed evidence can support action.
Feedback improves activation, not truth.
```

中文短版：

```text
这个资料库是一个有可信边界的第二大脑。

它负责收集来源、整理候选、审查证据、建立可追溯连接，并把知识变成带风险、前提、回退和反馈路径的行动依据。

它会主动提出连接、问题和模式。
但主动思考只生成候选，不直接生成真理。
真正能用于行动的内容，必须经过来源、证据、关系、风险和复查。
反馈只改进下一次激活路径，不直接改 truth。
```
