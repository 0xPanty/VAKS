# Framework Reference Research - candidate-only

Date: 2026-05-29

Status: candidate-only. 本报告只做外部参考调研与候选分析，不把任何外部资料直接升级为 reviewed knowledge，不新增核心约束，不修改主架构源文件。

Scope: 围绕 Verified Action Knowledge System v0.2 当前主线 `Capture -> Understand -> Review -> Connect -> Act and Learn`，查找可补强但不推翻主线的思想、论文、系统和开源项目。

Method: 先读本地 v0.2 架构、schema、review protocol、review queue、source intake、知识图谱索引与模板；中途按用户提醒补读最新 `wiki/` 设计 pattern / anti-pattern；再按经典 AI / claim verification / provenance / agent memory / RAG / KG / second brain / risk hygiene / LLM-Wiki frontier 分线搜索外部资料；最后只保留能降低负担、提高 review 稳定性、增强 calibration 或让 context pack 更可行动的候选 alpha。

Important boundary:

- candidate-only: 以下所有判断都是候选输入，不是 reviewed truth。
- provenance is not support: 来源、引用、出处只能说明“从哪里来”，不能自动说明“支持这个判断”。
- more citations do not automatically raise confidence: 支持材料变多不自动提高置信度，必须看独立性、反证、范围限制和风险。
- similarity is not relation: 向量相似、检索分数、共同主题都不能直接写成 supports / contradicts / refines。
- feedback is not truth: 使用反馈只能影响 activation / usefulness / scope fit，不能直接改 truth confidence。

## 1. Executive Summary

最值得继续看的资料有四组。

第一组是 `Toulmin + Pollock/defeasible reasoning + Dung/ASPIC+ + TMS/ATMS/AGM`。它们最适合补强 Evidence-Aware Review 和 Knowledge Calibration，但只能吸收轻量结构：`claim / grounds / warrant / qualifier / rebuttal`、`rebuttal / undercut / scope_limit / source_hygiene`、`minimal_revision_needed`。不要把本库变成形式逻辑引擎。

第二组是 `AVeriTeC / FEVEROUS / Loki / ClaimVer / Provenance for RAG / PROV-O / Web Annotation / Memento / Nanopublications`。它们最适合把“有引用”拆成“可复核证据包”：claim、verification questions、evidence items、source range、support/refute/not enough/conflicting/cherry-picking、review activity。最关键的 alpha 是 Evidence Packet。

第三组是 `Obsidian Web Clipper / ArchiveBox / Memex / Logseq / SiYuan / Evergreen Notes`。它们最贴合 Capture 和 Understand：低摩擦保存、摘录、高亮、快照、block anchor、候选点颗粒度。它们能补“从 inbox 到 source record”的来源保全和“候选点不太粗也不太碎”的粒度控制。

第四组是 `TrustGraph / Graphiti-Zep / Neo4j Agent Memory / A-MEM / Mem0 / Letta / OriginTrail / ORKG`。它们对 Activation、Context Pack、Use Ledger 和 agent memory 有参考价值：区分 raw/source/provenance/retrieval trace/candidate/reviewed/use trace；引入 temporal validity、retrieval trace、source_type、traversal_path、used/ignored 记录。但不能吸收自动记忆更新、自动关系推广、区块链/大型平台化运行时。

第五组是更前沿的 `WiCER / Retrieval as Reasoning / Context Engineering Survey / MemOS-MemoryOS / Basic Memory / Engram / AICTX Memory / CodeWiki-RepoDoc-Codebase-Memory / LightRAG-HippoRAG`。这组最贴近“LLM Wiki / agent-native knowledge base”的未来方向。真正值得吸收的是 compiled wiki 会丢事实、retrieval 应像 reasoning、context pack 需要 sufficiency/gap/warning、Markdown source of truth + rebuildable cache、repo-local continuity 小而可审查。必须拒绝 self-evolving wiki 直接改 truth、agent 直接写核心知识库、图检索分数当 relation/confidence。

普通参考或 watch-only：SilverBullet、Foam、Dendron、Anytype、AFFiNE、TiddlyWiki、Khoj、Reor、Argdown/Cytoscape，以及多数 repo-wiki / agent-memory MCP 项目。这些对 workbench、局部图谱可视化、检索体验和 agent continuity 有启发，但目前不应进入核心后端。可以借它们的界面/视图/导出思想，不吸收完整系统。

最小优雅吸收方向：

1. Evidence Packet: 把 Review 输入从“source + 摘要”升级为“claim + evidence item + support/challenge/scope/risk”。
2. Warrant separation: 在高价值判断中区分 provenance、grounds、warrant、rebuttal。
3. Challenge taxonomy: `rebuttal | undercut | scope_limit | source_hygiene | stale_assumption | action_failure`。
4. Minimal revision: collision 后只问最小必要动作：keep / refine_scope / mark_contested / mark_stale / supersede / reject。
5. Source anchor: 对网页/论文/代码采用 url/path + exact quote + prefix/suffix + position/hash + captured_at + archived_url。
6. Context pack trace: 输出 source_type、traversal_path、retrieved/selected/used/ignored、risk flags 和 unresolved contradictions。
7. Agent memory quarantine: agent memory 默认只生成 candidate 或 feedback-event，不能直改 reviewed truth。

## 2. Candidate References

### 2.1 High-Value Candidate Table

| 资料 | 来源链接 | 核心价值 | 适配层 | 采用判断 |
|---|---|---|---|---|
| Jon Doyle, Truth Maintenance System | https://www.sciencedirect.com/science/article/pii/0004370279900080 | reasons / dependencies / contradiction pressure | Knowledge Calibration, Review | adapt |
| de Kleer, ATMS | https://cdn.aaai.org/AAAI/1986/AAAI86-003.pdf | assumptions, environments, breaks-when thinking | Calibration, Risk | adapt/watch |
| AGM Belief Revision | https://arxiv.org/abs/2112.13557 | minimal change / belief revision discipline | Calibration, Review Due | adapt |
| Dung Abstract Argumentation | https://ojs.aaai.org/index.php/AAAI/article/view/5661 | attack/support standing check ancestor | Evidence-Aware Review | adapt |
| Toulmin Argument Model | https://owl.purdue.edu/owl/general_writing/academic_writing/historical_perspectives_on_argumentation/toulmin_argument.html | claim / grounds / warrant / qualifier / rebuttal | Review | adopt-lite |
| ASPIC+ | https://journals.sagepub.com/doi/10.1080/19462166.2013.869766 | structured arguments and attack types | Review, Connect | watch/adapt |
| Defeasible Reasoning / Pollock | https://plato.stanford.edu/entries/reasoning-defeasible/ | rebutting vs undercutting defeaters | Review, Risk | adapt |
| FEVER | https://aclanthology.org/N18-1074/ | claim + evidence + label benchmark | Understand, Review | adapt |
| FEVEROUS | https://arxiv.org/abs/2106.05707 | structured + unstructured evidence | Understand, Review | adapt |
| AVeriTeC | https://arxiv.org/abs/2305.13117 | real-world claim verification with QA evidence | Review | adapt |
| Loki / OpenFactVerification | https://github.com/Libr-AI/OpenFactVerification | claim decomposition + checkworthy + evidence crawl | Understand, Review | adapt/watch |
| Provenance for RAG output | https://arxiv.org/abs/2411.01022 | trace generated claims to retrieved chunks | Act and Learn, Risk | adapt |
| ClaimVer | https://arxiv.org/abs/2403.09724 | claim-level evidence attribution and rationale | Review, Activation | adapt |
| FactKG | https://arxiv.org/abs/2305.06590 | KG reasoning types for claim verification | Review, Connect | watch/adapt |
| W3C PROV-O | https://www.w3.org/ns/prov | provenance as Entity / Activity / Agent | Capture, Source Hygiene | adopt-thin |
| Nanopublications | https://nanopub.net/ | atomic assertion + provenance + publication info | Understand, Review | adapt |
| ORKG | https://arxiv.org/abs/1901.10816 | research contribution decomposition | Understand, Heavy Source Review | adapt/watch |
| Obsidian Web Clipper | https://obsidian.md/help/web-clipper/variables | low-friction capture with metadata/highlights | Capture | adapt |
| ArchiveBox | https://github.com/ArchiveBox/ArchiveBox | web snapshots, WARC/PDF/screenshot | Capture, Source Hygiene | adapt |
| Memex / WorldBrain | https://github.com/WorldBrain/Memex | highlights, annotations, reading intent | Capture, Use Ledger | adapt |
| Logseq | https://logseq.com/ | block-first notes, journal-first capture | Understand, Workbench | adapt |
| SiYuan | https://b3log.org/siyuan/en/?lang=en | block references and local/offline structure | Understand, Activation | adapt |
| Evergreen Notes | https://notes.andymatuschak.org/About_these_notes | atomic but useful note grain | Understand, Connect | adapt |
| Reor | https://github.com/reorproject/reor | local embeddings and related-note activation | Activation | watch/adapt |
| Khoj | https://github.com/khoj-ai/khoj | multi-source personal AI search | Activation, Workbench | watch |
| Neo4j Agent Memory | https://neo4j.com/labs/agent-memory/ | conversation/entity/reasoning memory layers | Activation, Use Ledger | adapt |
| TrustGraph | https://docs.trustgraph.ai/ | GraphRAG with provenance/retrieval traces | Activation, Context Pack | adapt |
| OriginTrail DKG | https://docs.origintrail.io/ | verifiable knowledge assets and provenance | Source Hygiene | watch |
| A-MEM | https://arxiv.org/abs/2502.12110 | dynamic memory linking / Zettelkasten-like memory | Activation, Calibration | adapt with caution |
| Graphiti / Zep | https://github.com/getzep/graphiti | temporal context graph with provenance | Activation, Review Due | adapt/watch |
| Mem0 / OpenMemory | https://github.com/mem0ai/mem0 | production agent memory and MCP memory | Activation, Agent Memory | watch/adapt |
| Letta / MemGPT memory | https://docs.letta.com/guides/agents/architectures/memgpt | core vs archival memory split | Activation, Dev Context | adapt |
| NIST AI RMF | https://airc.nist.gov/airmf-resources/airmf/5-sec-core/ | risk as cross-cutting function | Risk/Inhibition | adapt |
| NCSC prompt injection | https://www.ncsc.gov.uk/blog-post/prompt-injection-is-not-sql-injection | instruction/data cannot be reliable boundary | Agent Access, Risk | adopt boundary |
| OWASP Agentic AI Threats | https://genai.owasp.org/resource/agentic-ai-threats-and-mitigations/ | excessive agency, tool misuse, memory poisoning | Risk, Agent Access | adapt |
| MCP Security Best Practices | https://modelcontextprotocol.io/docs/tutorials/security/security_best_practices | least privilege and confused deputy controls | Agent Access | adapt |
| Web Annotation Data Model | https://www.w3.org/TR/annotation-model/ | stable quote/position selectors | Source Hygiene | adapt |
| Memento RFC 7089 | https://datatracker.ietf.org/doc/html/rfc7089 | time-based access to old web states | Source Hygiene, Review Due | adapt |
| Cochrane review updating | https://www.cochrane.org/node/93 | update triggers: new data/method/analysis/correction | Review Due | adapt |
| SLSA Provenance / OpenSSF Scorecard | https://slsa.dev/spec/v1.0-rc1/provenance | software provenance and repo health warnings | Source Hygiene, Repo Review | adapt |
| Argdown / Cytoscape.js | https://argdown.org/syntax/ ; https://js.cytoscape.org/ | local support/attack cluster visualization | Connect, Workbench | adapt/watch |

### 2.1b Frontier / Late-Pass Addendum Table

| 资料 | 来源链接 | 核心价值 | 适配层 | 采用判断 |
|---|---|---|---|---|
| Zotero | https://www.zotero.org/about/ | low-friction bibliographic capture and attachments | Capture, Source Intake | adapt |
| Hypothesis / Web Annotation | https://hypothesis-project.org/ ; https://www.w3.org/TR/annotation-model/ | quote anchors and annotations | Capture, Evidence Packet | adapt |
| Webrecorder / Browsertrix | https://webrecorder.net/browsertrix | WARC/WACZ web preservation | Capture, Provenance | adapt/watch |
| ALCE | https://arxiv.org/abs/2305.14627 | citation precision/recall vs answer correctness | Context Pack, Review | adapt |
| RARR | https://arxiv.org/abs/2210.08726 | post-hoc attribution and unsupported content revision | Understand, Review | adapt |
| FActScore | https://arxiv.org/abs/2305.14251 | atomic fact decomposition | Understand, Review | adopt/adapt |
| RAGAS | https://arxiv.org/abs/2309.15217 | context precision / recall / faithfulness metrics | Context Pack, Use Ledger | adapt |
| TruLens RAG Triad | https://www.trulens.org/getting_started/core_concepts/rag_triad/ | context relevance / groundedness / answer relevance split | Context Pack, Action Basis | adopt as checklist |
| PRISMA 2020 | https://www.prisma-statement.org/prisma-2020-statement | transparent search/screening/reporting | Heavy Review | adapt/watch |
| ROBIS | https://pmc.ncbi.nlm.nih.gov/articles/PMC4687950/ | risk of bias and relevance separation | Review, Risk | adapt |
| Wikidata statement model | https://www.wikidata.org/wiki/Wikidata:Data_model/en | qualifiers/references/ranks for statement metadata | Connect | adopt principle |
| Context Engineering Survey | https://arxiv.org/abs/2507.13334 | context as managed engineering surface | Activation, Context Pack | adapt |
| MemOS / MemoryOS | https://arxiv.org/abs/2505.22101 ; https://github.com/BAI-LAB/MemoryOS | memory lifecycle as managed resource | Activation, Use Ledger | watch/adapt |
| LightRAG | https://github.com/HKUDS/LightRAG | KG + vector retrieval for context discovery | Activation, Connect | adapt/watch |
| HippoRAG / EcphoryRAG | https://arxiv.org/abs/2405.14831 ; https://arxiv.org/abs/2510.08958 | associative multi-hop retrieval | Activation, Context Pack | adapt/watch |
| DeepWiki-Open | https://github.com/AsyncFuncAI/deepwiki-open | repo-to-wiki generated briefing | Understand, Source Intake | adapt/watch |
| CodeWiki / RepoDoc / Codebase-Memory | https://arxiv.org/abs/2510.24428 ; https://arxiv.org/abs/2604.26523 ; https://arxiv.org/abs/2603.27277 | repo-level docs / RepoKG / code KG via MCP | Understand, Dev Context | watch/adapt |
| WiCER | https://arxiv.org/abs/2605.07068 | compile-evaluate-refine to catch dropped facts | Understand, Review Queue | adopt principle |
| Retrieval as Reasoning | https://arxiv.org/abs/2605.25480 | retrieval as search/read/traverse/sufficiency process | Activation, Review | adapt/watch |
| Basic Memory | https://basicmemory.com/features | local-first Markdown MCP memory | Agent Memory, Source of Truth | adapt/watch |
| Engram | https://engram-kb.org/ | Markdown source of truth with rebuildable cache | Connect, Activation | adopt principle |
| AICTX Memory | https://memory.aictx.dev/ | repo-local continuity artifacts for coding agents | Dev Context, Handoff | adapt |
| PaperQA2 | https://github.com/Future-House/paper-qa | scientific RAG with citations and literature synthesis | Source Intake, Review | adapt/watch |
| OpenAlex / Semantic Scholar | https://explore.openalex.org/ ; https://www.semanticscholar.org/product/api | scholarly graph discovery and citation expansion | Source Discovery | adapt |

### 2.2 Detailed Candidate Analysis

#### 1. Jon Doyle, Truth Maintenance System

资料名称 / 链接: Jon Doyle, "A Truth Maintenance System" / https://www.sciencedirect.com/science/article/pii/0004370279900080

解决什么问题: 记录系统为什么相信某个命题，并在冲突出现时追踪 belief dependencies。

和我们哪一层有关: Knowledge Calibration / Point Collision, Evidence-Aware Review, Connect。

它支持我们什么: 支持“新资料进入后先触发 review pressure，而不是直接改 truth”。也支持“判断必须有 reason，不只是 provenance”。

它挑战或削弱我们什么: 如果吸收过重，会把本库变成自动 truth propagation 系统，和当前轻量 review-first 主线冲突。

它能细化我们什么: 可以把 candidate point 的 collision 输出分成 `affected_reason: conclusion | warrant | scope | source_quality`。

它暴露什么风险: provenance 很容易被误写成 reason；一个来源 URL 只能说明出处，不能说明这个出处为什么支持结论。

可吸收的 alpha 设计: `reason_record` 只记录“为什么这个证据支持/削弱这个判断”，不做自动 in/out truth 状态传播。

不该吸收的部分: TMS 的自动状态维护、全库依赖传播、形式化 belief engine。

和当前框架融合方式: Candidate Comprehension 产生 candidate point；Point Collision 只生成 reason/collision review input；Review 决定 standing。

最小优雅吸收版: 在高价值 review candidate 中加一个可选字段 `warrant_or_reason`，要求说明证据和判断之间的支持路径。

结论: adapt。

#### 2. de Kleer, Assumption-Based Truth Maintenance System

资料名称 / 链接: de Kleer, Assumption-Based Truth Maintenance System / https://cdn.aaai.org/AAAI/1986/AAAI86-003.pdf

解决什么问题: 在多组 assumptions 下追踪哪些结论成立，哪些环境会导致冲突。

和我们哪一层有关: Knowledge Calibration, Risk/Inhibition, Review Due。

它支持我们什么: 支持“scope limit”和“breaks_when”比单一 confidence 更重要。

它挑战或削弱我们什么: ATMS 的环境集合很重，容易把轻量 review 系统拖成逻辑求解器。

它能细化我们什么: 对 pattern / decision 增加 `holds_when` 和 `breaks_when` 的候选字段。

它暴露什么风险: 如果不给 scope，reviewed knowledge 会被误用到不适合的上下文。

可吸收的 alpha 设计: `assumption_scope` 和 `invalidating_condition`。

不该吸收的部分: label propagation、nogood set 计算、全库 assumption engine。

和当前框架融合方式: Point Collision 发现“新 candidate 只在某些 assumption 下挑战旧判断”，Review 再决定是否 refine scope。

最小优雅吸收版: 在 review checklist 中问一句：这个判断在哪些条件下不成立？

结论: adapt/watch。

#### 3. AGM Belief Revision

资料名称 / 链接: AGM belief revision / https://arxiv.org/abs/2112.13557

解决什么问题: 新信息与旧 belief 冲突时，如何尽量少地修改现有 belief set。

和我们哪一层有关: Knowledge Calibration, Evidence-Aware Review, Review Due。

它支持我们什么: 支持“collision 不等于推翻，先找最小修订动作”。

它挑战或削弱我们什么: AGM 假设形式化 belief set，本库是文件化、证据化、人工 review gate，不适合直接套。

它能细化我们什么: 给 collision 输出增加 `minimal_revision_needed`。

它暴露什么风险: 系统可能为了保持一致性而过度收缩结论，丢失有用的 contested knowledge。

可吸收的 alpha 设计: 修订动作枚举：keep / refine_scope / mark_contested / mark_stale / supersede / reject。

不该吸收的部分: AGM postulates、deductive closure、形式化 revision operator。

和当前框架融合方式: Candidate point 进入 Point Collision 后，不直接改 reviewed note，而是给 Review Queue 提供最小修订建议。

最小优雅吸收版: Review window 中加一行“最小必要动作是什么？”

结论: adapt。

#### 4. Dung Abstract Argumentation

资料名称 / 链接: Dung abstract argumentation / https://ojs.aaai.org/index.php/AAAI/article/view/5661

解决什么问题: 用 argument node 和 attack relation 判断争议中哪些 argument 可接受。

和我们哪一层有关: Evidence-Aware Review, Connect。

它支持我们什么: 支持“standing check”：一个判断要在支持、反对、scope limit、risk 下仍站得住。

它挑战或削弱我们什么: Formal semantics 容易诱惑我们做自动接受/拒绝，这会越过 human review。

它能细化我们什么: reviewed relations 可以区分 supports / contradicts / refines / risk_of；但 relation 必须 review 过。

它暴露什么风险: 图结构漂亮不代表判断正确，attack/support 也需要证据与 warrant。

可吸收的 alpha 设计: 局部 point cluster 的 support/challenge map。

不该吸收的部分: extension computation、自动 debate resolution、全库 argument engine。

和当前框架融合方式: Review 使用局部 graph 帮人看清挑战，不让图谱自己裁决 truth。

最小优雅吸收版: 对高价值 claim/pattern 显示 unresolved challenges 和 accepted scope limits。

结论: adapt。

#### 5. Toulmin Argument Model

资料名称 / 链接: Toulmin argument model / https://owl.purdue.edu/owl/general_writing/academic_writing/historical_perspectives_on_argumentation/toulmin_argument.html

解决什么问题: 把论证拆成 claim、grounds、warrant、qualifier、rebuttal、backing。

和我们哪一层有关: Evidence-Aware Review。

它支持我们什么: 正好补“provenance 不是 support”：grounds 是证据，warrant 是为什么证据能支撑 claim。

它挑战或削弱我们什么: 如果每条普通 note 都填完整 Toulmin，会太官僚。

它能细化我们什么: 高价值判断的 review form 可以采用 Toulmin-lite。

它暴露什么风险: 没有 warrant 的判断，即使有很多引用也可能站不住。

可吸收的 alpha 设计: `claim / grounds / warrant / qualifier / strongest_rebuttal`。

不该吸收的部分: 把所有 capture 或 light source 都强制变成完整 argument form。

和当前框架融合方式: 只在 heavy review、architecture decision、high-impact pattern 中启用。

最小优雅吸收版: 高价值 review 增加两问：证据是什么？证据为什么支持这个判断？

结论: adopt-lite。

#### 6. ASPIC+

资料名称 / 链接: ASPIC+ framework / https://journals.sagepub.com/doi/10.1080/19462166.2013.869766

解决什么问题: 让 argument 有内部结构，并区分规则、前提、攻击与 defeat。

和我们哪一层有关: Evidence-Aware Review, Connect。

它支持我们什么: 支持把 challenge 分成 premise attack、inference attack、conclusion attack。

它挑战或削弱我们什么: ASPIC+ 适合形式化 argumentation research，不适合本库 MVP。

它能细化我们什么: `attack_type: premise | inference | conclusion | scope | source_quality`。

它暴露什么风险: 过度结构化会让 review 负担变大。

可吸收的 alpha 设计: challenge 分类，不吸收推理引擎。

不该吸收的部分: strict/defeasible rule machinery、preference semantics、formal computation。

和当前框架融合方式: 作为 review metadata vocabulary，而不是 schema core。

最小优雅吸收版: 在 challenge note 中可选标记“挑战的是证据、推理桥、结论、范围还是来源卫生”。

结论: watch/adapt。

#### 7. Pollock / Defeasible Reasoning

资料名称 / 链接: Defeasible reasoning / https://plato.stanford.edu/entries/reasoning-defeasible/

解决什么问题: 处理“通常成立但可被新证据击败”的推理，区分 rebutting 和 undercutting defeaters。

和我们哪一层有关: Evidence-Aware Review, Risk/Inhibition。

它支持我们什么: 支持反对证据不只有“相反结论”，也可能是“证据不再能支撑结论”。

它挑战或削弱我们什么: 如果只记录 contradicts，会漏掉 undercutting challenges。

它能细化我们什么: `challenge_kind: rebuttal | undercutting | scope_limit | source_hygiene`。

它暴露什么风险: 很多判断失败不是因为结论相反，而是因为 warrant 失效、来源污染、scope 不匹配。

可吸收的 alpha 设计: Evidence-Aware Review 中把 challenge 拆为 rebuttal 和 undercut。

不该吸收的部分: 形式化 defeasible rule calculus。

和当前框架融合方式: Review 不只问“有没有反例”，还问“这个证据链有没有被削弱”。

最小优雅吸收版: Review 表单中增加 `strongest_undercutter`。

结论: adapt。

#### 8. FEVER

资料名称 / 链接: FEVER / https://aclanthology.org/N18-1074/

解决什么问题: 将自然语言 claim 与证据句、verdict label 连接起来。

和我们哪一层有关: Understand, Review。

它支持我们什么: 支持“source digest 后抽取 candidate claim，再找 evidence item”。

它挑战或削弱我们什么: FEVER 的 label 适合 benchmark，不应被当成本库 truth state。

它能细化我们什么: candidate point 可以记录 `evidence_items` 和 `support_status`。

它暴露什么风险: 单一语料内的 evidence 不等于真实世界证据完整。

可吸收的 alpha 设计: claim-level evidence packet。

不该吸收的部分: 自动 entailment label、benchmark metric、dataset-style truth assumption。

和当前框架融合方式: Understand 产出 candidate claim；Review 再做 evidence-aware standing check。

最小优雅吸收版: 每个高价值 claim 至少有一个可复核 evidence item 或明确 `not_enough_evidence`。

结论: adapt。

#### 9. FEVEROUS

资料名称 / 链接: FEVEROUS / https://arxiv.org/abs/2106.05707

解决什么问题: 将表格、列表、infobox、文本等混合证据纳入 claim verification。

和我们哪一层有关: Understand, Evidence-Aware Review。

它支持我们什么: 支持 source record 不只保存段落引用，也要保存 evidence medium。

它挑战或削弱我们什么: 如果把所有结构化证据都建模得太细，source intake 会变重。

它能细化我们什么: `source_medium: paragraph | table | code | issue | changelog | benchmark | discussion`。

它暴露什么风险: 表格/代码/issue 中的证据容易在摘要中被扁平化，丢失上下文。

可吸收的 alpha 设计: Evidence item 记录 medium 和 source range。

不该吸收的部分: 复杂 table reasoning benchmark pipeline。

和当前框架融合方式: Heavy source intake 可选识别不同证据媒介。

最小优雅吸收版: evidence item 增加 `medium` 字段。

结论: adapt。

#### 10. AVeriTeC

资料名称 / 链接: AVeriTeC / https://arxiv.org/abs/2305.13117

解决什么问题: 对真实世界 claim，用开放网页和多步 QA 证据进行验证。

和我们哪一层有关: Evidence-Aware Review, Knowledge Calibration。

它支持我们什么: 支持“review 不是只找一个来源，而是围绕 claim 生成 verification questions”。

它挑战或削弱我们什么: 开放网页验证会引入网页漂移、来源独立性和检索偏差。

它能细化我们什么: Evidence Packet 中加入 `verification_questions[]` 和 `answer_evidence[]`。

它暴露什么风险: 搜到的证据可能只是重复同一来源家族；也可能 cherry-pick。

可吸收的 alpha 设计: claim review 先列 2-5 个 verification questions，再收证据。

不该吸收的部分: 自动 web crawling、自动最终 verdict。

和当前框架融合方式: Review Queue 的高价值 candidate 可以附 QA packet，作为 reviewer input。

最小优雅吸收版: 对 architecture claim 问“要验证它，需要回答哪几个小问题？”

结论: adapt。

#### 11. Loki / OpenFactVerification

资料名称 / 链接: Loki OpenFactVerification / https://github.com/Libr-AI/OpenFactVerification

解决什么问题: 自动化 fact verification 流程中的 claim decomposition、checkworthiness、query generation、evidence crawling 和 verdict。

和我们哪一层有关: Understand, Review。

它支持我们什么: 支持“source digest 不应只摘要全文，应抽出可 review 的 claim / risk / pattern”。

它挑战或削弱我们什么: 自动 crawler 和 verifier 很容易绕过本库的 review gate。

它能细化我们什么: Understand 可拆成 `decompose -> checkworthy -> evidence questions -> candidate packet`。

它暴露什么风险: checkworthy 选择会带来遗漏偏差，自动 verdict 会产生伪确定性。

可吸收的 alpha 设计: claim decomposition 和 checkworthy ranking 作为候选排序。

不该吸收的部分: evidence crawler、online auto-verdict、自动 truth writeback。

和当前框架融合方式: 只做 candidate extraction helper，不做 reviewer。

最小优雅吸收版: source digest 输出 `candidate_points` 时标记 `why_checkworthy`。

结论: adapt/watch。

#### 12. Provenance: Lightweight Fact-checker for RAG Output

资料名称 / 链接: Provenance for RAG generation output / https://arxiv.org/abs/2411.01022

解决什么问题: 检查 RAG 输出中的事实性声明能否追溯到检索上下文 chunk。

和我们哪一层有关: Act and Learn, Context Pack, Use Ledger, Risk/Inhibition。

它支持我们什么: 支持 context pack 要输出 retrieval trace，而不是只输出答案。

它挑战或削弱我们什么: chunk grounded 不等于 truth；它只能说明输出是否被检索内容支持。

它能细化我们什么: `generated_claim -> supporting_context_chunk -> relevance_score -> fact_check_flag` 作为 action audit。

它暴露什么风险: RAG 系统容易把“答复被 chunk 支持”误作“现实为真”。

可吸收的 alpha 设计: Context Pack 使用后记录哪些 evidence 被 used / ignored / contradicted。

不该吸收的部分: 把 RAG fact-check score 写成 reviewed confidence。

和当前框架融合方式: Use Ledger 记录 action basis 的出处与使用情况，后续 failure 触发 review_due。

最小优雅吸收版: Action basis 中列出 used evidence 和 unresolved contradiction。

结论: adapt。

#### 13. ClaimVer

资料名称 / 链接: ClaimVer / https://arxiv.org/abs/2403.09724

解决什么问题: 对文本中的每个 claim 做可解释验证和证据归因。

和我们哪一层有关: Understand, Review, Activation。

它支持我们什么: 支持 claim-level highlight、rationale 和 evidence attribution。

它挑战或削弱我们什么: KG verification 容易让人误以为图谱可以自动裁决。

它能细化我们什么: source digest 可把长文本分成“需要 review 的具体 claim”。

它暴露什么风险: KG coverage 不足会导致 false negative；KG relation 也可能有 provenance 问题。

可吸收的 alpha 设计: Review UI/报告中突出 claim-level evidence and rationale。

不该吸收的部分: trusted KG 作为唯一裁判。

和当前框架融合方式: Candidate claim 的 evidence attribution 进入 Review Queue，不直接生成 reviewed relation。

最小优雅吸收版: 每条 candidate point 后附“支持它的具体片段”和“一句 rationale”。

结论: adapt。

#### 14. FactKG

资料名称 / 链接: FactKG / https://arxiv.org/abs/2305.06590

解决什么问题: 用知识图谱上的不同推理类型验证 claim。

和我们哪一层有关: Review, Connect。

它支持我们什么: 支持 relation 不只是 one-hop；有些判断依赖 multi-hop、existence、negation。

它挑战或削弱我们什么: 本库当前不应引入 KG reasoning engine。

它能细化我们什么: `reasoning_shape: one_hop | multi_hop | conjunction | negation | existence`。

它暴露什么风险: 多跳路径更容易产生 hallucinated relation 或过度解释。

可吸收的 alpha 设计: 对复杂 relation 标记 reasoning shape，帮助 reviewer 看风险。

不该吸收的部分: KG completion、embedding-based inference、自动 support/deny。

和当前框架融合方式: Connect 层只接受 reviewed relations；reasoning_shape 是 review 辅助信息。

最小优雅吸收版: 对 derived_from/refines 关系记录“是一跳还是多跳推导”。

结论: watch/adapt。

#### 15. W3C PROV-O

资料名称 / 链接: W3C PROV-O / https://www.w3.org/ns/prov

解决什么问题: 表达数据、活动、代理之间的 provenance lineage。

和我们哪一层有关: Capture, Source Hygiene, Review。

它支持我们什么: 支持 source record 不只存 URL，还要记录谁/何时/通过什么活动生成。

它挑战或削弱我们什么: RDF/OWL 完整模型太重，不适合当前 Markdown-first vault。

它能细化我们什么: `wasDerivedFrom`, `wasQuotedFrom`, `wasRevisionOf`, `generatedAtTime`, `wasAttributedTo` 的轻量字段。

它暴露什么风险: “derived from”可能被滥用；不是所有 consulted source 都是 primary source。

可吸收的 alpha 设计: PROV-thin profile。

不该吸收的部分: RDF serialization、ontology enforcement、SPARQL pipeline。

和当前框架融合方式: Source Intake 和 Evidence Packet 用轻字段记录 lineage。

最小优雅吸收版: source record 增加 `derived_from`, `quoted_from`, `captured_by`, `captured_at`。

结论: adopt-thin。

#### 16. Nanopublications

资料名称 / 链接: Nanopublications / https://nanopub.net/

解决什么问题: 把单个原子 assertion 与 provenance、publication info 分开。

和我们哪一层有关: Understand, Review, Connect。

它支持我们什么: 支持 candidate point 是 atomic assertion，不是整篇 source summary。

它挑战或削弱我们什么: nanopub 的 RDF/linked-data 生态太重。

它能细化我们什么: candidate point 可拆成 assertion / provenance / curation info。

它暴露什么风险: 原子化过度会导致知识碎片太多，review 成本上升。

可吸收的 alpha 设计: `assertion + evidence/provenance + review/publication metadata`。

不该吸收的部分: decentralized publishing、cryptographic identifiers、full RDF model。

和当前框架融合方式: Candidate point 和 reviewed claim note 可参考三段结构。

最小优雅吸收版: candidate point 明确区分“它说什么”和“它从哪里来/谁整理的”。

结论: adapt。

#### 17. Open Research Knowledge Graph

资料名称 / 链接: ORKG / https://arxiv.org/abs/1901.10816

解决什么问题: 将论文内容拆成 research problem、method、result、contribution 等结构化知识。

和我们哪一层有关: Understand, Heavy Source Review。

它支持我们什么: 支持论文/重资料 review 不只是摘要，而是抽取 contribution、method、limitation。

它挑战或削弱我们什么: 研究领域 ontology 和 comparison tooling 很重。

它能细化我们什么: Heavy paper review template 可增加 `problem / method / evidence / limitation / reusable pattern`。

它暴露什么风险: 学术结构化可能让普通 article intake 变繁琐。

可吸收的 alpha 设计: 对论文只吸收 contribution decomposition，不做 ORKG 平台。

不该吸收的部分: 完整 scholarly KG、semantic publishing workflow。

和当前框架融合方式: REFERENCE_REVIEW_PROTOCOL 的 heavy 模式可借用 ORKG 式贡献分解。

最小优雅吸收版: paper digest 输出 “problem, method, finding, limitation, candidate alpha”。

结论: adapt/watch。

#### 18. Obsidian Web Clipper

资料名称 / 链接: Obsidian Web Clipper / https://obsidian.md/help/web-clipper/variables

解决什么问题: 降低网页 capture 摩擦，同时保留 title、url、site、author、published、selection、highlights 等元数据。

和我们哪一层有关: Capture。

它支持我们什么: 支持 inbox 到 source record 的低摩擦采集，不必先做深 review。

它挑战或削弱我们什么: prompt variables / LLM extraction 可能把模型判断混入 raw source。

它能细化我们什么: source record 的 capture profile。

它暴露什么风险: 自动剪藏可能保存噪声；网页模板字段不等于 evidence quality。

可吸收的 alpha 设计: `web-source capture profile`。

不该吸收的部分: 把 clipper LLM 输出当 reviewed summary。

和当前框架融合方式: Capture 阶段只生成 raw/source record，Understand 再抽 candidate points。

最小优雅吸收版: 对网页 source record 统一保存 `url/title/site/author/published/selection/highlights/captured_at`。

结论: adapt。

#### 19. ArchiveBox

资料名称 / 链接: ArchiveBox / https://github.com/ArchiveBox/ArchiveBox

解决什么问题: 网页会变或消失，需要快照保全。

和我们哪一层有关: Capture, Source Hygiene, Review Due。

它支持我们什么: 支持高价值来源保存 HTML/PDF/screenshot/WARC/text 等 snapshot。

它挑战或削弱我们什么: 全量归档会带来存储、版权、隐私和维护成本。

它能细化我们什么: `archive_snapshot`, `checksum`, `captured_at`, `checked_latest_at`。

它暴露什么风险: archived copy 也可能不完整，动态网页和登录内容需要谨慎。

可吸收的 alpha 设计: high-value source snapshot only。

不该吸收的部分: 全库自动爬取、后台归档服务、把归档完整性当证据质量。

和当前框架融合方式: Source Intake 的 heavy/high-value path 可选择保存 snapshot location。

最小优雅吸收版: 对关键网页 source record 记录一个 archived_url 或 raw snapshot path。

结论: adapt。

#### 20. Memex / WorldBrain

资料名称 / 链接: Memex / WorldBrain / https://github.com/WorldBrain/Memex

解决什么问题: 阅读过程中的高亮、注释和保存动机容易丢失。

和我们哪一层有关: Capture, Understand, Use Ledger。

它支持我们什么: 支持把 highlight/annotation 当 source-side fragment，而不是后续凭记忆复述。

它挑战或削弱我们什么: full-text search 和 AI search 容易被误作 evidence relation。

它能细化我们什么: `reading_intent`, `highlight_fragment`, `annotation_note`, `later_usefulness`。

它暴露什么风险: 高亮是读者注意力，不是证据本身；annotation 可能混入 reviewer bias。

可吸收的 alpha 设计: 保存 “why saved” 和 “what was highlighted”。

不该吸收的部分: 浏览器历史级别的全量个人搜索系统。

和当前框架融合方式: Capture 保存 fragment；Understand 抽 candidate point；Use Ledger 记录后续是否有用。

最小优雅吸收版: source record 可选 `capture_reason` 和 `highlighted_fragments`。

结论: adapt。

#### 21. Logseq

资料名称 / 链接: Logseq / https://logseq.com/

解决什么问题: 页面级笔记太粗，候选点需要更小颗粒。

和我们哪一层有关: Capture, Understand, Workbench。

它支持我们什么: 支持 block-like candidate point，一条候选点表达一个可 review 的小判断。

它挑战或削弱我们什么: backlink/query 很容易被误读为 reviewed relation。

它能细化我们什么: candidate point 的颗粒度规则。

它暴露什么风险: 过度 block 化会造成碎片化和维护噪声。

可吸收的 alpha 设计: 2-8 个 candidate points，one thing, whole useful point。

不该吸收的部分: 把 block graph 当作 truth graph。

和当前框架融合方式: Understand 输出 block-like candidate points，Review 再决定是否 promotion。

最小优雅吸收版: source digest 不只摘要全文，还列少量候选点。

结论: adapt。

#### 22. SiYuan

资料名称 / 链接: SiYuan / https://b3log.org/siyuan/en/?lang=en

解决什么问题: 长文档移动、重组、引用后，source anchor 容易断。

和我们哪一层有关: Understand, Activation, Source Hygiene。

它支持我们什么: 支持 block-level ref / anchor 思想。

它挑战或削弱我们什么: 工具内数据库模型不该锁定本库 schema。

它能细化我们什么: `block_anchor` / `source_range` / `stable_fragment_id`。

它暴露什么风险: 工具生成 id 迁移困难，不能变成唯一真相。

可吸收的 alpha 设计: source range 和 block anchor 约定。

不该吸收的部分: SiYuan 数据库/rollup 模型。

和当前框架融合方式: Evidence item 指向 source range，不要求运行 SiYuan。

最小优雅吸收版: 每个摘录保存 `path/url + heading + quote + local anchor`。

结论: adapt。

#### 23. Evergreen Notes

资料名称 / 链接: Andy Matuschak Evergreen Notes / https://notes.andymatuschak.org/About_these_notes

解决什么问题: Understand 需要“够小但不碎”的知识颗粒。

和我们哪一层有关: Understand, Connect。

它支持我们什么: 支持 atomic notes 和 dense linking 的思想。

它挑战或削弱我们什么: 如果照搬，会把 source intake 变成长期写作系统，增加前置负担。

它能细化我们什么: candidate point 要 one thing，但要能独立有用。

它暴露什么风险: “原子化”如果没有 review gate，会制造大量未验证小断言。

可吸收的 alpha 设计: atomic candidate point but review-gated relation。

不该吸收的部分: 把所有 raw notes 改成 evergreen writing workflow。

和当前框架融合方式: Candidate points 可以 evergreen-like；reviewed knowledge 仍由 schema 控制。

最小优雅吸收版: 2-8 candidate points rule 中补“每点只讲一件事，但要完整到可复用”。

结论: adapt。

#### 24. Reor

资料名称 / 链接: Reor / https://github.com/reorproject/reor

解决什么问题: 本地知识写作时需要召回语义相近内容。

和我们哪一层有关: Activation, Understand。

它支持我们什么: 支持 local embeddings 作为 activation cache。

它挑战或削弱我们什么: vector similarity 很容易伪装成 relation。

它能细化我们什么: `nearby_candidate` / `near_miss` 和 `candidate_relation` 的边界。

它暴露什么风险: 语义相似可能只是同词、同场景，不代表支持、反驳或 refine。

可吸收的 alpha 设计: 语义召回只进入 calibration input，不写 reviewed relation。

不该吸收的部分: 把 embedding edge 写成 graph edge。

和当前框架融合方式: Activation 使用 vector retrieval，但 Connect 只接受 reviewed relations。

最小优雅吸收版: Context Pack 标注 “retrieved_by: semantic_similarity”，并禁止自动 relation。

结论: watch/adapt。

#### 25. Khoj

资料名称 / 链接: Khoj / https://github.com/khoj-ai/khoj

解决什么问题: 多入口个人知识库搜索、问答和 agent workflow。

和我们哪一层有关: Activation, Workbench, Use Ledger。

它支持我们什么: 支持 read-only context consumer 和 query-run log。

它挑战或削弱我们什么: agents/automations 容易绕过 Review 和 Act boundaries。

它能细化我们什么: 查询输出必须附 citations 和 query trace。

它暴露什么风险: 便利的 agent 搜索可能产生“看似知道”的回答。

可吸收的 alpha 设计: query-run record：query, retrieved, selected, cited, ignored。

不该吸收的部分: 自动行动、自动长期记忆写入、跨工具 agent runtime。

和当前框架融合方式: 作为未来 Activation/Workbench 参考，不进 truth core。

最小优雅吸收版: 任何回答型 context pack 都附 retrieval/citation log。

结论: watch。

## 3. Strongest Alpha Ideas

### 3.1 Evidence Packet

最强 alpha: 把 review input 统一成 Evidence Packet，而不是 source summary。

候选字段:

```yaml
claim_text:
candidate_type: claim | pattern | risk | decision_input
verification_questions:
  - question:
evidence_items:
  - source:
    source_medium: paragraph | table | code | issue | changelog | benchmark | discussion
    anchor:
      url_or_path:
      quote_exact:
      quote_prefix:
      quote_suffix:
      position:
      captured_at:
      archived_url:
    relation_to_claim: supports | refutes | limits_scope | undercuts | background | irrelevant
    rationale:
challenge_status: none | rebutted | undercut | conflicting | not_enough_evidence | cherry_pick_risk
scope_limit:
risk_flags:
review_question:
```

为什么无缝: 它正好落在 Understand -> Review 之间，不改变主架构，也不直接升级 truth。

### 3.2 Warrant Is Separate From Provenance

最强 alpha: 对高价值判断增加 Toulmin-lite：`claim / grounds / warrant / qualifier / strongest_rebuttal`。

它解决的问题: 有来源不等于有证据；有证据不等于证据能支持该判断。

最小吸收: 只在 architecture decision、high-impact pattern、reviewed claim 中启用，不强制普通 capture 填写。

### 3.3 Challenge Taxonomy

候选 challenge kinds:

- `rebuttal`: 有证据支持相反结论。
- `undercut`: 不是反结论，而是削弱证据到结论的 warrant。
- `scope_limit`: 在某范围内成立，超出范围失效。
- `source_hygiene`: 来源质量、独立性、引用锚点、版本状态有问题。
- `stale_assumption`: 旧判断依赖的假设过期。
- `action_failure`: 基于该知识行动失败，触发复查。

为什么无缝: 它只是 Review Queue 的候选标签，不是推理引擎。

### 3.4 Minimal Revision Needed

候选枚举:

- keep
- refine_scope
- mark_contested
- mark_stale
- supersede
- reject

为什么无缝: 它让 Point Collision 不再只有“推翻/接受”，而是给 reviewer 更小的修订动作。

### 3.5 Source Anchor Mini-Profile

候选字段:

```yaml
source_anchor:
  url_or_path:
  exact_quote:
  prefix:
  suffix:
  position:
  content_hash:
  captured_at:
  archived_url:
  checked_latest_at:
  source_changed: unknown | yes | no
```

为什么无缝: 它补 Capture/Source Hygiene，不改变 truth schema。

### 3.6 Context Pack Trace

候选字段:

```yaml
context_pack_trace:
  source_type: reviewed | candidate | raw | feedback | live_query
  activation_role: core | support | risk | cold_reference
  traversal_path:
  retrieved_state: retrieved | selected | used | ignored
  ignored_reason:
  unresolved_contradictions:
  risk_flags:
```

为什么无缝: 它强化 Act and Learn 的可追溯性，不让 retrieval 分数变成 relation。

### 3.7 Agent Memory Quarantine

最强 alpha: agent memory 默认是 candidate/feedback-event，不是 reviewed memory。

最小吸收:

```yaml
agent_memory_write:
  status: candidate_only
  source:
  source_hash:
  scope:
  expires_or_review_due:
  allowed_effect: activation | usefulness | scope_fit
  forbidden_effect: truth_confidence
```

为什么无缝: 它保护现有 reviewed knowledge gate，也为未来 agent lane 留口。

### 3.8 Review Due Triggers

候选触发器:

- new primary source
- contradiction
- correction / retraction
- source version change
- dependency/repo release change
- action failure
- missed feedback
- stale assumption

为什么无缝: 它把 review_due 从日历提醒变成低噪声复查信号。

### 3.9 Omission Check For Compiled Wiki / Digest

最强 alpha: WiCER 提醒我们，source digest / compiled wiki 最大风险不是写错，而是丢掉关键事实、边界条件、反例和风险。

候选字段:

```yaml
omission_check:
  likely_dropped_facts:
  missing_risks:
  missing_scope_limits:
  diagnostic_questions:
  needs_full_source_read: true | false
```

为什么无缝: 它只加强 Understand -> Review 的候选质量，不让自动编译结果变成 truth。

### 3.10 Evidence Granularity / Escalation

最强 alpha: 对论文、网页、repo 等来源，不必一开始就 full read，但必须知道当前证据粒度停在哪一层。

候选枚举:

- metadata_only
- abstract_or_summary
- excerpt_or_passage
- table_or_code_anchor
- full_source_reviewed

为什么无缝: 它能降低 capture/review 负担，同时让 high-risk 判断显式升级证据粒度。

### 3.11 Rebuildable Cache Doctrine

最强 alpha: 任何 index、embedding、graph retrieval、MCP memory、generated wiki 都只能是可重建缓存或候选工作台，不能拥有 truth。

候选规则:

```yaml
derived_artifact:
  artifact_type: index | embedding | graph_cache | generated_wiki | context_pack
  source_of_truth: false
  rebuildable: true
  allowed_effect: activation | discovery | briefing | candidate_generation
  forbidden_effect: truth_confidence | reviewed_relation | promotion
```

为什么无缝: 它直接保护本地 `derived-relatedness-as-truth-signal` 和 `auto-promotion-without-review-gate` 边界。

## 4. Fit Against Our Main Loop

### 4.1 Capture

最适合吸收:

- Obsidian Web Clipper: 低摩擦 capture metadata/highlights。
- ArchiveBox: 高价值网页 snapshot。
- Memex: highlight/annotation/reading intent。
- PROV-O thin: captured_at / attributed_to / derived_from。
- Web Annotation + Memento: stable anchor + web version awareness。

候选补强:

- `capture_profile`: web / paper / repo / discussion / code / issue。
- `capture_reason`: 为什么保存。
- `source_anchor`: exact quote + prefix/suffix + position/hash。
- `archive_snapshot`: 只对 high-value source 启用。

不吸收:

- 全量爬取。
- 自动剪藏后直接总结为 truth。
- 让 capture 阶段做 review 决策。

### 4.2 Understand

最适合吸收:

- FEVER / ClaimVer / Loki: claim decomposition。
- ORKG: paper contribution decomposition。
- Logseq / Evergreen Notes: candidate point 粒度。
- FEVEROUS: 多媒介 evidence。

候选补强:

- `candidate_points` 分 claim / pattern / risk / decision_input。
- 每个 source digest 输出 2-8 个“one thing, whole useful point”。
- `why_checkworthy` 解释为什么值得 review。
- `source_medium` 标记 evidence 来自段落、表格、代码、issue、benchmark 等。

不吸收:

- 自动 verdict。
- 把 summary 当 reviewed knowledge。
- 把 semantic similarity 当 relation。

### 4.3 Review

最适合吸收:

- Toulmin-lite: grounds / warrant / qualifier / rebuttal。
- AVeriTeC: verification questions。
- Pollock: rebuttal vs undercut。
- Dung / ASPIC+: 局部 support/challenge standing check。

候选补强:

- Evidence Packet。
- `challenge_kind`。
- `standing_status`: standing / limited / contested / stale / rejected / not_enough_evidence。
- `minimal_revision_needed`。

不吸收:

- formal argumentation engine。
- 自动 confidence calculator。
- citation count 或 support count 自动加分。

### 4.4 Connect

最适合吸收:

- Dung/Argdown 的 support/attack 可视化思想。
- FactKG 的 reasoning_shape。
- PROV-O 的 lineage relations。
- TrustGraph 的 edge provenance 警惕。

候选补强:

- reviewed relation 继续只允许 review-gated。
- `relation_state`: candidate / reviewed / contested / deprecated。
- `relation_origin`: extracted / reviewed / inferred_candidate / ambiguous。
- `reasoning_shape`: one_hop / multi_hop / negation / conjunction / derived。

不吸收:

- KG completion。
- embedding edge。
- 全库图谱产品。

### 4.5 Act and Learn

最适合吸收:

- Provenance for RAG output: generated claim -> context chunk trace。
- TrustGraph: retrieved/selected/used/ignored。
- Neo4j Agent Memory: reasoning trace 与 memory layers。
- Letta: core vs archival memory。

候选补强:

- Context Pack 输出 activation role、source_type、traversal_path、risk flags。
- Use Ledger 记录 action basis 和哪些证据被 used/ignored。
- action failure 只触发 review_due，不直接改 truth。

不吸收:

- agent self-editing reviewed memory。
- autonomous action based on candidate-only source。
- feedback 直接提高 confidence。

## 5. Fit Against Internal Mechanisms

### 5.1 Knowledge Calibration / Point Collision

可吸收:

- TMS 的 reasons/dependencies。
- ATMS 的 assumption scope。
- AGM 的 minimal revision。
- A-MEM 的 possible related memories。

候选机制:

```yaml
point_collision:
  new_candidate:
  touched_reviewed_nodes:
  collision_type: supports | contradicts | refines | duplicates | undercuts | scope_mismatch | stale_signal
  affected_reason: conclusion | warrant | scope | source_quality | relation
  minimal_revision_needed: keep | refine_scope | mark_contested | mark_stale | supersede | reject
  review_input_only: true
```

边界:

- calibration output 是 review input，不是 truth。
- 不做自动 belief propagation。
- 不让 similarity 或 retrieval score 生成 reviewed relation。

### 5.2 Evidence-Aware Review

可吸收:

- Toulmin-lite。
- AVeriTeC QA evidence。
- Pollock rebuttal/undercut。
- Dung/ASPIC+ 局部 attack/support。
- FEVER-style evidence packet，但不吸收 benchmark verdict。

候选机制:

```yaml
review_standing_check:
  support:
  strongest_rebuttal:
  strongest_undercutter:
  scope_limit:
  source_hygiene_warning:
  risk_flags:
  standing_status:
```

边界:

- provenance 不是 support。
- support 变多不自动提高 confidence。
- `not_enough_evidence` 是有效 review 结论，不是失败。

### 5.3 Activation

可吸收:

- Letta core/archive split。
- Reor local semantic retrieval as cache。
- TrustGraph context trace。
- Graphiti temporal validity。

候选机制:

```yaml
activation_item:
  source_type: reviewed | candidate | raw | feedback | live_query
  activation_role: core | support | risk | cold_reference
  retrieved_by: reviewed_relation | explicit_scope | semantic_similarity | recency | use_history
  validity:
  unresolved_risk:
```

边界:

- memory_tier 是 activation priority，不是 truth。
- hot/warm/cold 不等于 confidence。
- semantic retrieval 只能召回，不能判断关系。

### 5.4 Use Ledger

可吸收:

- Provenance for RAG: output claim grounding。
- TrustGraph: retrieval trace。
- Memex: reading intent / later usefulness。
- Neo4j reasoning trace。

候选机制:

```yaml
use_ledger_event:
  action:
  context_pack_id:
  evidence_used:
  evidence_ignored:
  ignored_reason:
  outcome:
  usefulness_signal:
  action_failure:
  review_due_candidate:
```

边界:

- usefulness 影响 activation，不改 truth。
- action failure 触发 review_due，不自动 reject 知识。

### 5.5 Risk / Inhibition

可吸收:

- NIST RMF cross-cutting risk。
- NCSC prompt injection residual risk。
- OWASP memory poisoning / excessive agency。
- MCP least privilege。
- Cochrane update triggers。
- SLSA/OpenSSF repo hygiene warnings。

候选机制:

```yaml
risk_signal:
  risk_kind: prompt_injection | memory_poisoning | stale_source | low_independence | missing_anchor | tool_misuse | excessive_agency | repo_hygiene | source_changed
  severity: low | medium | high
  mitigation:
  review_due_when:
  blocks_action: true | false
```

边界:

- risk 是横切刹车，不是另一个大型治理模块。
- source hygiene warning 不能自动否定一个判断，只能触发 review pressure。

## 6. Rejected / Watch-only Ideas

### 6.1 不该吸收的重型系统

- Full TMS / ATMS / ASPIC+ / AGM engine: 过重，会把 human review 变成形式系统维护。
- KG completion / embedding inferred truth: 与 reviewed relation gate 冲突。
- Full GraphRAG platform: 会过早把 MVP 变成运行时平台。
- Blockchain / DKG / decentralized provenance: 对未来外部发布可能有用，但当前本地 vault 不需要。
- Full ORKG semantic publishing: 对论文 review 有启发，但不应引入完整 scholarly KG。
- Automatic memory evolution: 与 reviewed truth 不可自动改写的边界冲突。

### 6.2 Watch-only 或只吸收 UI/工作台思想

- Khoj: 可以学习 citation/query-run log，但 agent 自动化不进核心。
- Reor: 可以学习本地 semantic activation，但 similarity 不进 relation。
- SilverBullet: 可学习声明式视图，不引入隐藏脚本/后台任务。
- Foam: 可学习 orphan/lint/block-anchor，不把开发者工具链变成用户前提。
- Dendron: 可学习 scope key/route hint，不引入层级 truth。
- Anytype/AFFiNE: 可学习 object/set/canvas workbench，不把 graph/database UI 当 truth source。
- TiddlyWiki: 可学习字段驱动静态视图，不迁移格式。
- Argdown/Cytoscape: 可做局部 point cluster visualization，不做全库图谱产品。

### 6.3 明确拒绝的误吸收

- 把 citation count 当 confidence。
- 把 provenance 当 support。
- 把 retrieval score 当 relation。
- 把 agent memory 当 reviewed memory。
- 把 feedback 当 truth update。
- 把 review_due 变成纯日历提醒。
- 把 risk taxonomy 扩成安全平台。
- 把 workbench UI 扩成架构核心。

## 7. Suggested Next Discussion

1. Evidence Packet 要不要作为 Review Queue 的候选输入格式，而不是现在直接扩 SCHEMA？
2. Toulmin-lite 只用于哪些对象：claim、pattern、decision，还是 high-impact source review？
3. `challenge_kind` 是否采用最小五类：rebuttal / undercut / scope_limit / source_hygiene / stale_assumption？
4. `minimal_revision_needed` 是否适合作为 Point Collision 的标准输出？
5. Capture 是否只对 high-value source 记录 `archived_url/content_hash`，普通 source 只保留 url + captured_at？
6. `source_anchor` 最小字段要多轻：exact quote + prefix/suffix 是否足够，position/hash 是否只在 heavy source 用？
7. WiCER 暴露的 “compiled wiki 会丢关键事实” 是否要转成 heavy source review 的 `omission_check`？
8. Context Pack 是否应输出 `why_included`、`activation_role`、`evidence_is_partial`、`needs_full_source_read`，以免 hot memory 被误读成 truth？
9. Agent memory / MCP memory 的未来边界是否明确写成：只能读 context 或写 candidate/feedback-event，不能写 reviewed truth？
10. 所有 graph/RAG/index/cache 是否统一标注为 activation infrastructure，不允许拥有 truth/confidence/relation promotion？

## Appendix A. Candidate-Only Absorption Map

| Alpha | Main Loop 插入点 | Internal Mechanism | Complexity Risk | Candidate Verdict |
|---|---|---|---|---|
| Evidence Packet | Understand -> Review | Evidence-Aware Review | medium | strongest adapt |
| Toulmin-lite warrant | Review | Evidence-Aware Review | low | adopt-lite |
| challenge_kind | Review | Risk / Point Collision | low | adapt |
| minimal_revision_needed | Calibration -> Review | Point Collision | low | adapt |
| source_anchor mini-profile | Capture | Source Hygiene | low/medium | adapt |
| web snapshot for high-value sources | Capture | Source Hygiene | medium | adapt |
| context_pack_trace | Act and Learn | Activation / Use Ledger | medium | adapt |
| agent memory quarantine | Act and Learn | Risk / Agent Access | low | adapt |
| review_due_when triggers | Review Due | Risk / Feedback | low | adapt |
| omission_check | Understand -> Review | Source Digest / Review Queue | low | strongest adapt |
| evidence_granularity | Capture -> Review | Source Intake / Evidence-Aware Review | low | adapt |
| rebuildable_cache_doctrine | Activation / Connect | Risk / Agent Access | low | adopt principle |
| local point cluster visualization | Connect | Evidence-Aware Review | medium | watch/adapt |

## Appendix B. Notes On Already-Considered Sources

本库本地索引已经把 TMS/Dung 作为 conceptual ancestors 记录过，也已经讨论过 A-MEM、FEVER、Karpathy/LLM wiki、OpenKB、Dusk、PARA、Obsidian AI patterns 等资料。本文没有把这些资料重新升级为 reviewed knowledge，只做更细的 candidate-only 设计碰撞：

- TMS/Dung: 保留为 conceptual reference，新增候选细化是 reason/warrant、challenge_kind、standing check。
- A-MEM/FEVER: 保留为候选 extraction/calibration/review inspiration，明确不吸收自动 truth/update。
- Obsidian/PKM 工具: 只吸收 capture/workbench 粒度，不让工具模型成为核心 schema。
- Agent memory/RAG 项目: 只吸收 activation trace/use ledger/source separation，不吸收 autonomous memory truth。

## Appendix C. Second-Pass Watchlist: Contradiction-Aware RAG / KG Consistency

这一轮补查的重点是：有没有能直接增强 Point Collision、Evidence Packet、Context Pack 质量的近期系统。结论是：有几个方向值得 watch/adapt，但仍然不能自动进 truth core。

### C1. ArbGraph

资料名称 / 链接: ArbGraph: Conflict-Aware Evidence Arbitration for Reliable Long-Form RAG / https://arxiv.org/abs/2604.18362

解决什么问题: 长文 RAG 在生成前先把检索材料拆成 atomic claims，并显式组织 support / contradiction evidence graph。

和我们哪一层有关: Knowledge Calibration, Evidence-Aware Review, Context Pack。

它支持我们什么: 非常支持“先做 candidate point collision，再行动/生成”的顺序。

它挑战或削弱我们什么: 它服务于 RAG 生成，本库服务于 reviewed knowledge；不能把 arbitration 输出当 truth。

它能细化我们什么: `pre_action_evidence_arbitration` 可以作为 Context Pack 的候选质量检查。

它暴露什么风险: pre-generation graph 可能仍由模型抽取，错误边会制造伪冲突或漏冲突。

可吸收的 alpha 设计: 在高风险 action 前，Context Pack 标出 unresolved contradictions 和 chosen evidence basis。

不该吸收的部分: 自动 evidence graph construction 直接写 Connect。

和当前框架融合方式: 作为 Act 前的候选仲裁检查，不改变 reviewed relations。

最小优雅吸收版: Context Pack 加 `unresolved_conflicts` 和 `evidence_basis_choice`。

结论: adapt/watch。

### C2. Dealing with Inconsistency for Reasoning over Knowledge Graphs: A Survey

资料名称 / 链接: KG inconsistency reasoning survey / https://arxiv.org/abs/2502.19023

解决什么问题: 总结 KG 不一致处理的三类方向：检测不一致、修复不一致、容忍不一致继续推理。

和我们哪一层有关: Connect, Knowledge Calibration, Review Due。

它支持我们什么: 支持“发现冲突”和“修复冲突”必须分开；冲突存在时仍可保留 contested knowledge。

它挑战或削弱我们什么: KG 领域常见的 automatic repair 不适合本库。

它能细化我们什么: `conflict_detected` 不等于 `relation_removed`；可以有 `contested` 和 `needs_review` 状态。

它暴露什么风险: 自动修复会删除少数派但正确的 evidence。

可吸收的 alpha 设计: Connect 层保留 inconsistency-tolerant stance：冲突先显示，不急于修。

不该吸收的部分: KG repair algorithms、inconsistency metrics as confidence。

和当前框架融合方式: Point Collision 生成 review input；Review 决定 keep/refine/contested/supersede。

最小优雅吸收版: relation_state 增加或继续保留 `contested` 语义。

结论: adapt。

### C3. ProVe: Automated Provenance Verification of KG Triples Against Text

资料名称 / 链接: ProVe / https://arxiv.org/abs/2210.14846

解决什么问题: 检查知识图谱 triple 是否真的被其 documented provenance textual source 支持。

和我们哪一层有关: Connect, Source Hygiene, Evidence-Aware Review。

它支持我们什么: 强烈支持“documented provenance 还要验证是否 actually supports triple”。

它挑战或削弱我们什么: 自动 triple verification 仍可能错，不应替代 review。

它能细化我们什么: reviewed relation 需要 `evidence_supports_relation`，不是只需要 `source_url`。

它暴露什么风险: 很多 graph edge 可能只是从文本抽取出来，但文本并不支持该关系。

可吸收的 alpha 设计: Relation review 时问：引用片段是否支持这条边，而不只是提到两个节点？

不该吸收的部分: KG triple verification pipeline。

和当前框架融合方式: Connect promotion 前做 human-readable relation support check。

最小优雅吸收版: reviewed relation 增加一句 `relation_rationale`。

结论: adapt。

### C4. LongTracer

资料名称 / 链接: LongTracer / https://endevsols.com/open-source/longtracer

解决什么问题: 用 STS + NLI 检查 RAG response 中每个 claim 是否被 source documents entail / contradict / neutral。

和我们哪一层有关: Act and Learn, Context Pack, Risk/Inhibition。

它支持我们什么: 支持 action output 的 claim-level grounding audit。

它挑战或削弱我们什么: NLI verdict 不是 truth；neutral/contradiction 分类可能漏掉 qualifier 和 scope。

它能细化我们什么: Use Ledger 可以记录 `supported_claims`, `contradicted_claims`, `unsupported_claims`。

它暴露什么风险: post-hoc detector 容易成为主防线，但真正防线应是 review gate 和 action basis。

可吸收的 alpha 设计: 对未来 RAG/context answer 做 lightweight grounding lint。

不该吸收的部分: trust_score 直接变 confidence 或 action permission。

和当前框架融合方式: Act 后 lint 输出只能生成 feedback/review_due candidate。

最小优雅吸收版: Use Ledger 记录“本次回答哪些句子没有 source support”。

结论: watch/adapt。

### C5. RAGLint

资料名称 / 链接: RAGLint / https://github.com/Prashanth1998-18/raglint

解决什么问题: 在文档进入 RAG 前审计 contradictions、duplicates、stale content、metadata gaps、noise。

和我们哪一层有关: Capture, Source Hygiene, Risk/Inhibition。

它支持我们什么: 支持 source hygiene warning 成为一等候选信号。

它挑战或削弱我们什么: 项目较新，且 health score 不能直接当 evidence quality。

它能细化我们什么: `source_hygiene_warning: duplicate | stale | contradiction | missing_metadata | draft_noise`。

它暴露什么风险: 自动 lint 可能误报；低分不代表资料无价值。

可吸收的 alpha 设计: 对 source corpus 做 candidate-only hygiene lint。

不该吸收的部分: corpus health score 直接影响 truth confidence。

和当前框架融合方式: Capture/Source Intake 后生成 warnings，Review 决定是否处理。

最小优雅吸收版: Source record 可选 `hygiene_warnings`。

结论: watch/adapt。

### C6. ContextSchema

资料名称 / 链接: ContextSchema / https://github.com/Novice-ninja/contextschema-py

解决什么问题: agent 行动前检查 retrieved context 是否有必需字段、可接受来源、provenance、freshness、invalidation events。

和我们哪一层有关: Act and Learn, Context Pack, Risk/Inhibition。

它支持我们什么: 非常贴合“context pack 更可行动”而不是“更多材料”。

它挑战或削弱我们什么: 项目很早期，不应引入为依赖。

它能细化我们什么: action 前 context validation：freshness、source acceptability、missing required evidence。

它暴露什么风险: context schema 如果太硬，会让系统官僚；如果太软，又没有刹车效果。

可吸收的 alpha 设计: Context Pack 可有 `action_readiness: ready | qualify | retrieve_more | refuse`.

不该吸收的部分: 作为运行时库纳入当前架构。

和当前框架融合方式: Act 前只做 checklist，不做脚本。

最小优雅吸收版: Context Pack 输出一句 `action_readiness_reason`。

结论: watch/adapt。

### C7. Omnigraph

资料名称 / 链接: Omnigraph / https://www.omnigraph.dev/

解决什么问题: 让 knowledge graph 像 Git 一样 branch / diff / merge，并带 provenance。

和我们哪一层有关: Connect, Review Queue, Candidate Promotion。

它支持我们什么: 支持 candidate branch 和 reviewed main 的概念边界。

它挑战或削弱我们什么: 把 graph repository/runtime 引进来会显著变重。

它能细化我们什么: 候选关系可以像 branch 一样存在，merge 需要 review。

它暴露什么风险: “graph as source of truth”口号可能冲突 Markdown-first reviewed knowledge。

可吸收的 alpha 设计: candidate graph branch as metaphor, not runtime。

不该吸收的部分: graph repo engine、schema plan、mutation CLI、install scripts。

和当前框架融合方式: REVIEW_QUEUE 继续是 candidate branch；wiki reviewed notes 是 main。

最小优雅吸收版: 在术语上把 promotion 看成 review merge，而不是自动 sync。

结论: watch。

## Appendix D. Second-Pass Watchlist: Design Rationale / IBIS / QOC

这一组资料对“待碰撞问题”和“架构讨论窗口”有帮助，但不应进入 truth core。它们更像 review window 的思考脚手架。

### D1. IBIS / gIBIS

资料名称 / 链接: Issue-Based Information System / gIBIS / https://www.tandfonline.com/doi/abs/10.1080/07370024.1991.9667172

解决什么问题: 在复杂、开放、多人或长期设计问题中，把问题、候选立场和支持/反对理由组织起来。

和我们哪一层有关: Review Queue, Evidence-Aware Review, Architecture Discussion。

它支持我们什么: 支持“待碰撞问题”不应只是散列表，而应保持 issue -> position/option -> pro/con/rationale 的结构。

它挑战或削弱我们什么: IBIS 图谱很容易越长越乱，变成讨论系统而不是知识系统。

它能细化我们什么: `review_question` 可以有候选 options，每个 option 有支持、反对、scope、risk。

它暴露什么风险: 如果每个小问题都 IBIS 化，会显著增加讨论成本。

可吸收的 alpha 设计: 对 architecture review window 使用 IBIS-lite：issue / options / strongest pro / strongest con / decision status。

不该吸收的部分: 完整 issue mapping tool、会议协作图谱、全库设计理据数据库。

和当前框架融合方式: 只作为 `Suggested Next Discussion` 和 Review Queue 中高价值问题的候选结构。

最小优雅吸收版: 下次架构讨论时，把 5-10 个问题写成 `Issue -> Option A/B -> pro/con -> smallest decision`。

结论: adapt。

### D2. QOC: Questions, Options, Criteria

资料名称 / 链接: QOC design space analysis / https://acawiki.org/Questions%2C_Options%2C_and_Criteria%3A_Elements_of_design_space_analysis

解决什么问题: 决策不是只比较方案，还要明确评判标准。

和我们哪一层有关: Review, Architecture Decision, Act and Learn。

它支持我们什么: 支持 adoption 判断要看标准：减少负担、提高判断质量、让 review 更稳、让 context pack 更可行动、避免官僚化。

它挑战或削弱我们什么: 如果 criteria 太多，会把轻量吸收变成评分表。

它能细化我们什么: 每个 alpha idea 可用 3-5 个 criteria 快速过滤。

它暴露什么风险: 没有 criteria 的讨论容易被“高级感”带偏；criteria 过多则会僵化。

可吸收的 alpha 设计: Alpha adoption checklist：burden, judgment_quality, review_stability, actionability, complexity_risk。

不该吸收的部分: 定量打分、复杂 design-space matrix。

和当前框架融合方式: 作为 architecture review 的轻量评判标准，而不是 schema 字段。

最小优雅吸收版: 每个候选 alpha 只问一句：它是否以低复杂度改善 judgment/review/action？

结论: adapt。

## Appendix E. Second-Pass Watchlist: Content Provenance Standards

### E1. C2PA / Content Credentials

资料名称 / 链接: C2PA technical specification / https://c2pa.org/specifications/specifications/1.0/specs/C2PA_Specification.html

解决什么问题: 给数字内容提供可验证的 provenance/authenticity manifest，尤其面向图片、视频和 AI 生成内容。

和我们哪一层有关: Capture, Source Hygiene, Future Publishing。

它支持我们什么: 支持对 high-value media/source snapshot 记录 provenance manifest、content hash、creator/tool chain。

它挑战或削弱我们什么: C2PA 证明的是内容来源/处理链的某些声明，不证明内容中的 claim 为真，也不证明该内容支持本库判断。

它能细化我们什么: `content_manifest`, `content_hash`, `creator_or_tool`, `claim_generator`, `tamper_evidence`。

它暴露什么风险: authenticated content can still be misleading；可验证来源不等于 evidence quality。

可吸收的 alpha 设计: 对未来产品发布或媒体来源，记录 content credential 状态作为 source hygiene warning/metadata。

不该吸收的部分: 把 cryptographic provenance 当 support，把 content credential 当 truth confidence。

和当前框架融合方式: 只进入 Capture/Source Hygiene；Review 仍需 Evidence Packet 判断内容是否支持 claim。

最小优雅吸收版: Source record 可选 `content_credentials_present: yes | no | unknown` 和 `credential_notes`。

结论: watch/adapt。

## Appendix F. Second-Pass Watchlist: Documentation Cards / Dataset Provenance

这一组不是知识推理系统，而是“来源记录怎么写得清楚”。它能补 Capture 和 Source Hygiene，尤其适合 repo / paper / dataset / model 这类复杂来源。

### F1. Datasheets for Datasets

资料名称 / 链接: Datasheets for Datasets / https://arxiv.org/abs/1803.09010

解决什么问题: 数据集常缺乏标准化文档，使用者不知道动机、组成、采集过程、推荐用途和限制。

和我们哪一层有关: Capture, Source Intake, Source Hygiene。

它支持我们什么: 支持 source record 不只是 bibliographic metadata，还要写 intended use、composition、collection process、known limits。

它挑战或削弱我们什么: 完整 datasheet 问题集太长，不适合普通资料 intake。

它能细化我们什么: 对数据集/benchmark source 增加 `intended_use`, `out_of_scope`, `collection_process`, `known_bias_or_gap`。

它暴露什么风险: 文档完整不等于数据可信；自述也可能错误或缺失。

可吸收的 alpha 设计: Dataset-source mini card。

不该吸收的部分: 全量 datasheet template、强制所有 source 填长问卷。

和当前框架融合方式: SOURCE_INTAKE 的 heavy dataset path 可选使用 mini card。

最小优雅吸收版: 对 dataset/benchmark 只问四件事：从哪来、怎么做、适合什么、不适合什么。

结论: adapt。

### F2. Data Statements for NLP

资料名称 / 链接: Data Statements for NLP / https://aclanthology.org/Q18-1041/

解决什么问题: NLP 数据的语言、说话人、语境、标注和社会语言属性缺失会导致偏差和误用。

和我们哪一层有关: Source Hygiene, Risk/Inhibition。

它支持我们什么: 支持 scope fit：资料在哪些语言/人群/语境下成立，不能泛化到哪里。

它挑战或削弱我们什么: 本库不应变成数据治理系统。

它能细化我们什么: `scope_population`, `language_context`, `collection_context`, `annotation_context`。

它暴露什么风险: 不写数据语境会让 action basis 在错误人群/场景上过度泛化。

可吸收的 alpha 设计: 对人群/语言/语境敏感资料加 scope context。

不该吸收的部分: 全量 NLP data statement。

和当前框架融合方式: Review 的 scope_limit 和 Risk 可引用这些字段。

最小优雅吸收版: 对涉及人群/语言的 source 增加 `scope_context`。

结论: adapt。

### F3. Model Cards

资料名称 / 链接: Model Cards for Model Reporting / https://arxiv.org/abs/1810.03993

解决什么问题: 模型发布缺少 intended uses、limitations、evaluation conditions 和 ethical considerations。

和我们哪一层有关: Source Intake, Risk/Inhibition, Act and Learn。

它支持我们什么: 支持“工具/模型/库 source review 不只看功能，也看适用边界和失败模式”。

它挑战或削弱我们什么: 模型卡是模型透明度文档，不是模型质量证明。

它能细化我们什么: repo/library review 中增加 `intended_use`, `out_of_scope_use`, `evaluation_conditions`, `known_limitations`。

它暴露什么风险: model card 可能是营销材料；缺失评估不等于模型不可用，但必须标风险。

可吸收的 alpha 设计: Model/tool source mini card。

不该吸收的部分: 把 model card presence 当 adoption signal。

和当前框架融合方式: templates/library-review 可在未来讨论是否吸收 mini fields。

最小优雅吸收版: 评估工具/模型时明确“适合什么、不适合什么、证据是什么”。

结论: adapt。

### F4. Data Cards

资料名称 / 链接: Data Cards / https://research.google/pubs/data-cards-purposeful-and-transparent-dataset-documentation-for-responsible-ai/

解决什么问题: 数据文档不仅要全面，还要对不同使用者可读、可比较、可行动。

和我们哪一层有关: Capture, Activation, Context Pack。

它支持我们什么: 支持 briefing before full read：先给使用者看够用的结构化摘要，再决定是否深读。

它挑战或削弱我们什么: 如果做成复杂卡片系统，会增加维护负担。

它能细化我们什么: `briefing_card` 可以把 source origin / purpose / limits / risk / review status 放在一屏。

它暴露什么风险: 摘要卡可能遮蔽细节，尤其不能替代 source full read。

可吸收的 alpha 设计: Briefing card as activation artifact, not truth。

不该吸收的部分: 大型 card tooling、stakeholder workflow。

和当前框架融合方式: Context Pack 先给 Core/Support/Risk briefing，必要时再 full read。

最小优雅吸收版: 每个重资料 summary 顶部给 5 行 source briefing。

结论: adapt。

### F5. Data Provenance Initiative

资料名称 / 链接: Data Provenance Initiative / https://github.com/Data-Provenance-Initiative/Data-Provenance-Collection

解决什么问题: AI 数据集的来源、许可证、创建者、派生链和可用性经常缺失或误标。

和我们哪一层有关: Source Hygiene, Risk/Inhibition。

它支持我们什么: 支持 provenance 不只是一条 URL，而是 source chain / license / creator / derivative relationship。

它挑战或削弱我们什么: 法律/许可证审计很重，不应默认纳入所有 source。

它能细化我们什么: 对 dataset/model/repo source 记录 `license_status`, `creator`, `source_chain`, `derivative_of`, `use_restriction`。

它暴露什么风险: 开源/公开不等于可自由使用；许可证误标本身就是 source hygiene risk。

可吸收的 alpha 设计: license/provenance warning as candidate-only risk signal。

不该吸收的部分: 完整许可证合规系统。

和当前框架融合方式: Source Intake 对 dataset/model 类资料生成 hygiene warning，不改 truth。

最小优雅吸收版: 对高价值外部资料记录 license/use restriction unknown/known。

结论: adapt。

## Appendix G. Second-Pass Watchlist: Intelligence Analysis / Evidence Discipline

这一组最贴近“支持-反对式 Review”。它提醒我们：证据质量、来源可靠性、信息可信度、证据诊断性必须分开。

### G1. Analysis of Competing Hypotheses

资料名称 / 链接: Heuer, Analysis of Competing Hypotheses / https://www.cia.gov/resources/csi/books-monographs/psychology-of-intelligence-analysis-2/

解决什么问题: 防止只寻找支持最喜欢假设的证据，通过比较多个竞争假设和每条证据的诊断性来降低确认偏误。

和我们哪一层有关: Evidence-Aware Review, Knowledge Calibration。

它支持我们什么: 强烈支持“支持变多不自动提高 confidence”；真正重要的是哪些 evidence 能区分竞争判断。

它挑战或削弱我们什么: ACH matrix 如果完整套用，会过重。

它能细化我们什么: Review 可以记录 `alternative_hypotheses` 和 `diagnostic_evidence`。

它暴露什么风险: 只看一个候选结论时，review 容易变成找支持材料。

可吸收的 alpha 设计: 对高价值 claim/decision 先列 2-3 个 competing interpretations。

不该吸收的部分: 完整 ACH matrix、定量打分、群体分析流程。

和当前框架融合方式: Evidence-Aware Review 增加“是否有可区分竞争解释的证据？”

最小优雅吸收版: Review 中加一行 `most_plausible_alternative`。

结论: adapt。

### G2. Admiralty Code / NATO Source Reliability vs Information Credibility

资料名称 / 链接: Admiralty Code source reliability and information credibility / https://resolve.cambridge.org/core/journals/judgment-and-decision-making/article/effect-of-source-reliability-and-information-credibility-on-judgments-of-information-quality-in-intelligence-analysis/E67548E8010A47345C3439D45D9EC6B3

解决什么问题: 把 source reliability 和 information credibility 独立评价，避免“好来源说的每句话都可信”或“坏来源说的每句话都无效”。

和我们哪一层有关: Source Hygiene, Evidence-Aware Review。

它支持我们什么: 直接支持 provenance/source quality 与 evidence support 分离。

它挑战或削弱我们什么: A-F / 1-6 编码会制造伪精确感，不适合本库照搬。

它能细化我们什么: `source_reliability` 和 `information_credibility` 两个弱标签，且必须可解释。

它暴露什么风险: 来源声誉会污染对具体信息的判断。

可吸收的 alpha 设计: 只用 qualitative labels：source known/unknown/questionable；information corroborated/plausible/uncorroborated/contradicted。

不该吸收的部分: 数字等级矩阵和自动 confidence。

和当前框架融合方式: Evidence item review 时分别问“这个来源平时可靠吗？”和“这条信息本身有支撑吗？”

最小优雅吸收版: Evidence Packet 加 `source_reliability_note` 与 `information_credibility_note`。

结论: adapt。

### G3. Analytic Confidence / Tradecraft Standards

资料名称 / 链接: Analytic confidence overview / https://en.wikipedia.org/wiki/Analytic_confidence

解决什么问题: 分析产品需要说明来源质量、协同证据、假设、复杂度和不确定性，而不只是给结论。

和我们哪一层有关: Evidence-Aware Review, Act and Learn。

它支持我们什么: 支持 reviewed judgment 应表达 uncertainty、assumptions、source quality。

它挑战或削弱我们什么: 情报产品标准不应原样迁移为本库流程。

它能细化我们什么: `confidence_note` 应解释信心来自哪里、主要不确定性是什么。

它暴露什么风险: confidence language 容易变成装饰性词汇。

可吸收的 alpha 设计: Confidence requires rationale, not just label。

不该吸收的部分: 完整 tradecraft checklist。

和当前框架融合方式: Review 可选记录 `confidence_basis` 和 `main_uncertainty`。

最小优雅吸收版: 如果写 confidence，必须同时写一句 because/uncertainty。

结论: adapt。

## Appendix H. Second-Pass Watchlist: Evidence Certainty / Bias

这组来自 evidence-based medicine。它不适合直接套用，但“风险偏差、不一致、间接性、精确性、发表偏差”很适合转译为知识 review 的风险提示。

### H1. GRADE Evidence Certainty

资料名称 / 链接: GRADE approach / https://book.gradepro.org/guideline/overview-of-the-grade-approach

解决什么问题: 证据确定性不只由研究类型决定，还受 risk of bias、inconsistency、indirectness、imprecision、publication bias 影响。

和我们哪一层有关: Evidence-Aware Review, Risk/Inhibition。

它支持我们什么: 支持“证据多”不等于“证据稳”；要看不一致、间接性和偏差。

它挑战或削弱我们什么: 医学 GRADE 很重，不适合普通架构资料 review。

它能细化我们什么: `evidence_risk_flags: bias | inconsistency | indirectness | imprecision | selection_or_publication_bias`。

它暴露什么风险: 高级框架如果照搬，会让本库过度官僚化。

可吸收的 alpha 设计: 五个 evidence risk flags 作为轻量 warning。

不该吸收的部分: GRADE rating system、医学证据等级、recommendation strength。

和当前框架融合方式: Evidence-Aware Review 只借风险维度，不借评分体系。

最小优雅吸收版: Review 问一句：这个证据有偏差、不一致、间接或过窄吗？

结论: adapt。

### H2. Cochrane Risk of Bias

资料名称 / 链接: Cochrane Risk of Bias / https://methods.cochrane.org/bias/risk-bias-tool

解决什么问题: 系统化识别单项研究或证据在方法上的偏差风险。

和我们哪一层有关: Source Hygiene, Evidence-Aware Review。

它支持我们什么: 支持 source hygiene warning 不只是“来源差”，还要问“这个证据怎么可能偏”。

它挑战或削弱我们什么: RoB 工具高度医学/研究设计相关，不能泛化为通用 checklist。

它能细化我们什么: 对论文/benchmark/repo claims 记录 `method_bias_risk`。

它暴露什么风险: 很多 external alpha 来自 demo/benchmark，方法偏差会导致过度吸收。

可吸收的 alpha 设计: 对实验型论文只做轻量 `bias_risk_note`。

不该吸收的部分: RoB 2 protocol、完整医学评审工具。

和当前框架融合方式: Heavy paper review 可加“方法风险/benchmark 风险”一行。

最小优雅吸收版: Paper review 问：这个结论是否依赖窄 benchmark、样本选择或未披露方法？

结论: adapt。

### H3. Evidence to Decision Framework

资料名称 / 链接: GRADE Evidence to Decision / https://health-policy-systems.biomedcentral.com/articles/10.1186/s12961-018-0320-2

解决什么问题: 决策不只看证据确定性，还要看 benefits/harms、values、resources、equity、acceptability、feasibility。

和我们哪一层有关: Act and Learn, Architecture Decision。

它支持我们什么: 支持 adoption 判断不能只问“理论上更真”，还要问负担、可行性、复杂度和风险。

它挑战或削弱我们什么: 完整 EtD 框架太重。

它能细化我们什么: Alpha adoption criteria: benefit, harm, burden, feasibility, reversibility。

它暴露什么风险: 一个设计点判断质量高，但如果维护成本太高，也不该吸收。

可吸收的 alpha 设计: 轻量 adoption gate。

不该吸收的部分: health-system recommendation framework。

和当前框架融合方式: Suggested Next Discussion 可用这些 criteria 筛 alpha。

最小优雅吸收版: 每个 alpha 只问：收益是否大于维护负担，失败是否可逆？

结论: adapt。

## Appendix I. Second-Pass Watchlist: Critical Questions / Forecast Calibration

### I1. Walton Argumentation Schemes / Critical Questions

资料名称 / 链接: Walton argumentation schemes / https://www.reasoninglab.com/patterns-of-argument/argumentation-schemes/waltons-argumentation-schemes/

解决什么问题: 不同类型论证需要不同 critical questions；例如 expert opinion、analogy、cause、sign 都有不同弱点。

和我们哪一层有关: Evidence-Aware Review。

它支持我们什么: 支持 Review 不只是固定问“支持/反对”，还要根据 claim 类型问更针对性的反问。

它挑战或削弱我们什么: 25+ argument schemes 会太复杂。

它能细化我们什么: `review_question_templates` 按 claim type 生成不同 critical questions。

它暴露什么风险: 固定模板可能让 reviewer 机械填表，不真正思考。

可吸收的 alpha 设计: 只保留少量通用 critical questions：source? warrant? alternative? exception? scope? risk?

不该吸收的部分: 完整 Walton scheme catalog。

和当前框架融合方式: Evidence-Aware Review 的提示词可借鉴 critical questions。

最小优雅吸收版: Review 增加“什么情况会让这个论证不成立？”

结论: adapt。

### I2. Good Judgment / Brier Calibration

资料名称 / 链接: Good Judgment Project / Brier score overview / https://en.wikipedia.org/wiki/The_Good_Judgment_Project

解决什么问题: 概率判断需要事后校准；过度自信和欠自信都可以通过 resolved outcomes 学习。

和我们哪一层有关: Use Ledger, Feedback, Confidence Calibration。

它支持我们什么: 支持 feedback 不直接改 truth，但可以改 activation/usefulness/scope fit，并长期校准“我们在某类判断上是否过度自信”。

它挑战或削弱我们什么: 本库大多数 knowledge claim 不像预测题那样有清晰 resolution。

它能细化我们什么: 对可验证 action prediction 记录 expected outcome 和 actual outcome。

它暴露什么风险: 把非预测知识硬改成概率题会变形。

可吸收的 alpha 设计: 只对 action decision / forecast-like claim 记录 calibration，不对普通 reviewed truth 强制概率化。

不该吸收的部分: 全库 Brier scoring、预测市场化、概率化所有判断。

和当前框架融合方式: Use Ledger 可以积累 action outcome，用于 activation tuning 和 review_due。

最小优雅吸收版: 对明确行动预期记录 `expected_outcome`, `actual_outcome`, `lesson_for_activation`。

结论: watch/adapt。

## Appendix J. Second-Pass Watchlist: Public Claim Review Metadata

### J1. Schema.org ClaimReview

资料名称 / 链接: Schema.org ClaimReview / https://schema.org/ClaimReview

解决什么问题: 给 fact-checking article 提供结构化字段，说明被 review 的 claim、itemReviewed、reviewRating、author、date 等。

和我们哪一层有关: Evidence-Aware Review, Source Hygiene, Future Publishing。

它支持我们什么: 支持 claim review 应该围绕一个明确的 `claimReviewed`，而不是整篇文章泛泛判断。

它挑战或削弱我们什么: reviewRating 的 True/False/Mixed 等标签过于粗糙，不适合直接映射本库 standing。

它能细化我们什么: `claim_review_record` 的最小字段：claim, item_reviewed, reviewer, rating/verdict, review_body, positive/negative notes。

它暴露什么风险: 结构化 markup 存在不代表 review 质量高，也不代表证据充分。

可吸收的 alpha 设计: 未来公开产品可用 ClaimReview-like metadata，但内部仍用 Evidence Packet。

不该吸收的部分: 把 reviewRating 当 confidence；把 search rich result 格式当内部 schema。

和当前框架融合方式: Reviewed claim note 可借鉴 claimReviewed/itemReviewed 的分离。

最小优雅吸收版: 每条 reviewed claim 必须能一句话说明“被 review 的具体 claim 是什么”。

结论: adapt。

### J2. Google Fact Check Tools API

资料名称 / 链接: Google Fact Check Tools API / https://developers.google.com/fact-check/tools/api/reference/rest/

解决什么问题: 搜索和管理网络上已发布的 ClaimReview fact-check metadata。

和我们哪一层有关: Understand, Evidence-Aware Review。

它支持我们什么: 支持外部 fact-check 可作为 candidate evidence source，而不是自动裁判。

它挑战或削弱我们什么: 覆盖率有限，相同 claim 的不同表述可能检索不到同一 fact-check。

它能细化我们什么: `external_claim_reviews` 可以作为 candidate evidence item，但要记录 query 和 coverage risk。

它暴露什么风险: 搜不到 fact-check 不代表 claim 未被验证；搜到也不代表本库可直接采纳。

可吸收的 alpha 设计: 对事实性资料可选查找 existing claim reviews，作为 review input。

不该吸收的部分: API 查询结果自动 verdict。

和当前框架融合方式: Understand 阶段可生成 `known_fact_checks` 候选列表；Review 再判断。

最小优雅吸收版: 对高风险 claim 记录“是否存在外部 fact-check；没查不代表无”。

结论: watch/adapt。

### J3. ClaimsKG

资料名称 / 链接: ClaimsKG / https://users.ics.forth.gr/~fafalios/files/pubs/ISWC2019_ClaimsKG.pdf

解决什么问题: 把 fact-checked claims、claim reviews、authors、ratings、topics 等组织成知识图谱。

和我们哪一层有关: Connect, Evidence-Aware Review。

它支持我们什么: 支持 claim/review/provenance 可以分层建模，而不是一条 source summary。

它挑战或削弱我们什么: fact-check KG 仍然可能继承各 fact-checker 的 bias、口径差异和更新滞后。

它能细化我们什么: 外部 claim review 关系需要记录 reviewer、date、rating vocabulary、language、url。

它暴露什么风险: 聚合后的 KG 让 fact-check 看起来更权威，但聚合不是证据增强。

可吸收的 alpha 设计: 如果未来做 claim index，可分 claim node 和 review node。

不该吸收的部分: 外部 fact-check KG 直接并入 reviewed knowledge。

和当前框架融合方式: 只作为 Connect 层建模参考；本库 reviewed relation 仍需本地 review。

最小优雅吸收版: 记录 external review as source, not relation。

结论: watch/adapt。

### J4. ClaimDB / Abstention in Structured Claim Verification

资料名称 / 链接: ClaimDB / https://arxiv.org/abs/2601.14698

解决什么问题: 面向大型结构化数据的 claim verification，并强调模型在无证据时难以 abstain。

和我们哪一层有关: Evidence-Aware Review, Risk/Inhibition。

它支持我们什么: 支持 `not_enough_evidence` / `unverifiable` 是一等结论，不应强行 true/false。

它挑战或削弱我们什么: 结构化数据 benchmark 不等于本库通用 review。

它能细化我们什么: Review standing 可以包含 `unverifiable_with_current_sources`。

它暴露什么风险: 系统为了输出结论会过度推断，尤其在证据缺失时。

可吸收的 alpha 设计: Review checklist 明确允许 abstain。

不该吸收的部分: benchmark pipeline。

和当前框架融合方式: Evidence Packet 如果证据不足，输出 review_due/retrieve_more，而不是结论。

最小优雅吸收版: Standing status 保留 `not_enough_evidence`。

结论: adapt。

## Appendix K. Second-Pass Watchlist: Workflow / Run / Data Lineage

这组资料对未来 Act and Learn、Use Ledger、source snapshot、action basis 可追溯性有帮助。当前只吸收设计思想，不引入运行时。

### K1. Flowcept

资料名称 / 链接: Flowcept / https://github.com/ORNL/flowcept

解决什么问题: 捕获 AI/scientific workflow runtime provenance，记录 activity used/generated、resource use、workflow provenance card。

和我们哪一层有关: Act and Learn, Use Ledger, Agent Access。

它支持我们什么: 支持 action 不只要结果，还要记录 used/generated 和 run context。

它挑战或削弱我们什么: 当前用户明确不要跑项目脚本或自动化；Flowcept 是运行时系统，不能现在引入。

它能细化我们什么: Use Ledger 可借 `used/generated/activity/status/elapsed/artifacts` 思想。

它暴露什么风险: provenance capture 很容易膨胀成 observability 平台。

可吸收的 alpha 设计: `action_run_card` 作为未来轻量输出，不是现在实现。

不该吸收的部分: decorators、MCP agent、telemetry、runtime instrumentation。

和当前框架融合方式: Act and Learn 未来可记录 action basis 和 generated artifacts，仍不改 truth。

最小优雅吸收版: Use Ledger 增加 `used_sources` 和 `generated_outputs`。

结论: watch/adapt。

### K2. RO-Crate / Workflow Run RO-Crate

资料名称 / 链接: RO-Crate / Workflow Run RO-Crate / https://www.researchobject.org/workflow-run-crate/

解决什么问题: 把研究对象、输入、输出、代码、workflow run provenance 打包成机器/人可读 metadata。

和我们哪一层有关: Source Hygiene, Act and Learn, Future Publishing。

它支持我们什么: 支持重要输出最好能带 inputs/outputs/code/provenance bundle。

它挑战或削弱我们什么: 完整 RO-Crate JSON-LD 对本库当前过重。

它能细化我们什么: 未来 external products 可以有 `artifact_bundle_manifest`。

它暴露什么风险: 打包完整不等于判断正确。

可吸收的 alpha 设计: For high-value outputs, keep a small manifest of source inputs and produced artifacts。

不该吸收的部分: JSON-LD crate standard、workflow packaging tooling。

和当前框架融合方式: outputs/review 或 products 未来可带轻量 manifest。

最小优雅吸收版: 报告头部记录 source scope、date、status、allowed effect。

结论: watch/adapt。

### K3. OpenLineage

资料名称 / 链接: OpenLineage / https://openlineage.io/

解决什么问题: 数据 pipeline 的 job/run/dataset lineage 需要开放标准记录。

和我们哪一层有关: Source Hygiene, Use Ledger。

它支持我们什么: 支持 run-level lineage 与 source-level provenance 分开。

它挑战或削弱我们什么: 这是 data engineering pipeline 标准，远重于本库。

它能细化我们什么: `run`, `job`, `dataset`, `input`, `output` 的概念可借给 action ledger。

它暴露什么风险: 自动 lineage 可能给人错觉：有 lineage 就可复现、有 lineage 就可信。

可吸收的 alpha 设计: Use Ledger 未来区分 action run 和 knowledge source。

不该吸收的部分: backend repository、pipeline integrations。

和当前框架融合方式: 只作为 terminology reference。

最小优雅吸收版: Action log 记录 inputs/outputs，不引入 lineage service。

结论: watch。

### K4. DVC

资料名称 / 链接: DVC / https://dvc.org/doc/user-guide/what-is-dvc

解决什么问题: 数据、模型、pipeline 和实验需要可版本化、可复现。

和我们哪一层有关: Source Hygiene, Act and Learn。

它支持我们什么: 支持 source snapshot / version / lockfile 思想。

它挑战或削弱我们什么: 本库不是 ML pipeline repo；引入 DVC 会过度工程化。

它能细化我们什么: 对大型 source snapshot 可以记录 version/hash/lock。

它暴露什么风险: 如果没有 version pin，后续 action basis 可能不可复现。

可吸收的 alpha 设计: `source_version_or_hash`。

不该吸收的部分: DVC pipeline execution。

和当前框架融合方式: Capture high-value source 时可记录 version/hash。

最小优雅吸收版: 对 repo/paper/dataset 记录 commit/version/date。

结论: adapt。

### K5. MLflow Model Registry

资料名称 / 链接: MLflow Model Registry / https://mlflow.org/docs/latest/ml/model-registry

解决什么问题: 模型生命周期需要 lineage、version、alias、metadata、annotation、stage 管理。

和我们哪一层有关: Source Intake, Activation, Review Due。

它支持我们什么: 支持 “current/latest” 不是稳定事实，版本和 alias 必须分开。

它挑战或削弱我们什么: Model registry 是 MLOps 系统，不应进入知识库核心。

它能细化我们什么: `version`, `alias`, `stage`, `deprecated/superseded` 的概念可借给 source records。

它暴露什么风险: latest alias 漂移会使过去 review 失去复现性。

可吸收的 alpha 设计: source record 区分 fixed version 与 floating latest。

不该吸收的部分: registry runtime、deployment lifecycle。

和当前框架融合方式: Review_due 可由 new version 或 alias drift 触发。

最小优雅吸收版: 对动态 source 标 `version_pinned: yes/no`。

结论: adapt。

### K6. FAIRSCAPE Evidence Graph

资料名称 / 链接: FAIRSCAPE / https://fairscape.net/

解决什么问题: AI-ready scientific datasets 需要 FAIR metadata 和 Evidence Graph，连接数据、软件、计算、人员和结果。

和我们哪一层有关: Source Hygiene, Evidence-Aware Review, Future Publishing。

它支持我们什么: 支持 evidence graph 是 provenance/explainability 工具，不是自动 truth。

它挑战或削弱我们什么: FAIR/EVI ontology 过重。

它能细化我们什么: 对复杂 computation source，记录 dataset/software/computation/personnel/result。

它暴露什么风险: 机器可解释 evidence graph 会显得很正式，但仍需人审证据是否支持 claim。

可吸收的 alpha 设计: 对高价值 computational source 用 mini evidence graph summary。

不该吸收的部分: ontology/server/validation tooling。

和当前框架融合方式: Heavy source review 可加 computation provenance。

最小优雅吸收版: 论文/计算型资料记录 `data -> method -> output -> claim`。

结论: watch/adapt。

## Appendix L. Second-Pass Watchlist: Semantic Wiki / Ontology / Constraint Systems

这一组资料的价值主要是“借小概念，拒绝大平台”。它们能解释为什么本库要保留 Markdown-first、review-gated、candidate-only 的轻量路径。

### L1. Wikibase / Wikidata Data Model

资料名称 / 链接: Wikibase Data Model / https://www.mediawiki.org/wiki/Wikibase/DataModel

解决什么问题: 把一个 statement 拆成 main claim、qualifiers、references、rank，并允许同一实体有多条带不同语境的 statement。

和我们哪一层有关: Connect, Reviewed Relations, Source Hygiene。

它支持我们什么: 强烈支持“relation 需要 qualifier/scope/reference”，尤其时间、角色、范围等限定信息。

它挑战或削弱我们什么: Wikibase rank 容易被误解为 truth confidence；references 仍然只是 provenance。

它能细化我们什么: reviewed relation 可考虑 `main_relation + qualifiers + references + relation_state`。

它暴露什么风险: 简单 subject-predicate-object 无法表达现实中的 scope/validity；但复杂 qualifiers 又会带来建模负担。

可吸收的 alpha 设计: qualified relation pattern。

不该吸收的部分: Wikibase runtime、rank semantics、SPARQL/RDF export。

和当前框架融合方式: Connect 层继续轻量，只在需要时给 relation 加 `scope_qualifier` 和 `validity`。

最小优雅吸收版: reviewed relation 支持可选 `qualifier: time/scope/role/context`。

结论: adapt。

### L2. Semantic MediaWiki

资料名称 / 链接: Semantic MediaWiki / https://github.com/SemanticMediaWiki/SemanticMediaWiki

解决什么问题: 在 wiki 页面中用语义注释和查询生成结构化知识视图。

和我们哪一层有关: Workbench, Connect, Activation。

它支持我们什么: 支持“页面仍是人读文本，结构化字段用于查询/视图”。

它挑战或削弱我们什么: MediaWiki/SMW 平台迁移成本巨大，不符合当前本地 vault。

它能细化我们什么: Markdown frontmatter + indexes 可以承担轻量 semantic annotations。

它暴露什么风险: 查询视图会被误读成 reviewed relation；结构化字段容易蔓延。

可吸收的 alpha 设计: in-document semantic hints and generated index views。

不该吸收的部分: MediaWiki platform、inline property syntax、semantic query engine。

和当前框架融合方式: wiki/indexes 继续作为轻量视图，不作为 truth layer。

最小优雅吸收版: 对少数字段保持可查询，不新增通用语义平台。

结论: watch/adapt。

### L3. SHACL

资料名称 / 链接: SHACL / https://www.w3.org/TR/shacl/

解决什么问题: 用 shapes/constraints 验证 RDF graph 的结构和数据约束。

和我们哪一层有关: Schema, Source Hygiene, Risk/Inhibition。

它支持我们什么: 支持 schema validation 可以发现缺字段、类型错误、结构异常。

它挑战或削弱我们什么: SHACL 验证的是 graph shape，不是 claim truth。

它能细化我们什么: 未来可以做 lightweight lint：required metadata, allowed relation types, missing provenance。

它暴露什么风险: 通过 schema validation 的知识仍然可能是错的；验证形状不等于证据充分。

可吸收的 alpha 设计: schema lint mindset。

不该吸收的部分: RDF/SHACL engine、constraint language。

和当前框架融合方式: 只作为未来 sanity check 思想，不在本轮运行脚本。

最小优雅吸收版: 人工 review checklist 中保留“必填字段是否缺失”。

结论: watch/adapt。

### L4. Conceptual Graphs

资料名称 / 链接: John Sowa, Conceptual Graphs / https://www.jfsowa.com/cg/cgonto.htm

解决什么问题: 用 concept nodes 和 relation nodes 表达自然语言语义和逻辑结构。

和我们哪一层有关: Connect, Understand。

它支持我们什么: 支持概念和关系分开建模；也提醒自然语言到图谱的转换有歧义。

它挑战或削弱我们什么: 形式化语义图太重，且不解决 evidence/review 本身。

它能细化我们什么: Understand 可以区分 concept extraction 和 claim extraction。

它暴露什么风险: 把文本转成图容易丢掉 modality、uncertainty、scope。

可吸收的 alpha 设计: concept note 与 claim/relation note 分离。

不该吸收的部分: conceptual graph formalism。

和当前框架融合方式: wiki/concepts 继续是概念层，不能替代 reviewed claims。

最小优雅吸收版: 概念相邻不等于关系支持。

结论: watch。

### L5. CYC

资料名称 / 链接: CYC overview / https://www.britannica.com/topic/CYC

解决什么问题: 试图构建包含大量 commonsense knowledge 的知识库和推理系统。

和我们哪一层有关: Rejected / Anti-pattern。

它支持我们什么: 作为反面参考，提醒不要追求全覆盖常识知识库。

它挑战或削弱我们什么: 如果本库追求“把所有东西都结构化”，会走向 CYC 式长期高成本。

它能细化我们什么: 明确“本库是 verified action knowledge，不是 universal commonsense KB”。

它暴露什么风险: frame problem、维护成本、知识永远不全、推理规则失控。

可吸收的 alpha 设计: 只吸收边界教训：不要做 universal ontology。

不该吸收的部分: commonsense KB ambition、formal expert-system reasoning。

和当前框架融合方式: Rejected/Watch-only 中明确重型 universal KB 是 anti-pattern。

最小优雅吸收版: 保持主线只服务 actionable reviewed knowledge。

结论: reject as architecture direction。

## Appendix M. Second-Pass Watchlist: Agent Memory / Reflection / Learning From Use

这一组补强 Act and Learn 与 Use Ledger。核心吸收边界：反思和历史使用可以改下一次 context pack 的激活方式，但不能直接改 reviewed truth。

### M1. Reflexion

资料名称 / 链接: Reflexion / https://arxiv.org/abs/2303.11366 ; https://github.com/noahshinn/reflexion

解决什么问题: agent 通过 verbal feedback/self-reflection 存入 episodic memory，在后续尝试中改善策略。

和我们哪一层有关: Act and Learn, Use Ledger, Feedback。

它支持我们什么: 支持 action failure 后生成 reflection/lesson，而不是沉没在聊天记录里。

它挑战或削弱我们什么: 自我反思文本可能是错误归因；不能直接改 truth 或 confidence。

它能细化我们什么: Use Ledger 可以有 `lesson_candidate`，只影响 activation 和 future action hints。

它暴露什么风险: agent 会从错误 feedback 学到错误策略；reflection 需要来源和 outcome。

可吸收的 alpha 设计: action failure -> feedback-event -> candidate lesson -> review_due/activation tuning。

不该吸收的部分: 自我反思自动写入长期 reviewed memory。

和当前框架融合方式: Feedback 改 usefulness/scope fit，不改 truth。

最小优雅吸收版: Use Ledger 记录“这次行动失败给下次 context pack 的候选提醒”。

结论: adapt。

### M2. Generative Agents Memory Stream

资料名称 / 链接: Generative Agents / https://arxiv.org/abs/2304.03442

解决什么问题: agent 通过 observation、reflection、planning 维持 believable behavior。

和我们哪一层有关: Activation, Context Pack, Act and Learn。

它支持我们什么: 支持 observation/reflection/planning 三者分开；reflection 是加工层，不是原始事实。

它挑战或削弱我们什么: 该系统目标是行为拟真，不是 verified action knowledge。

它能细化我们什么: `raw_observation`, `reflection_candidate`, `plan_context` 三层不要混。

它暴露什么风险: 反思摘要会压缩和扭曲原始观察。

可吸收的 alpha 设计: 反思只作为 candidate synthesis，必须可追溯到 observation。

不该吸收的部分: believable social simulation architecture。

和当前框架融合方式: Proactive synthesis candidate-only；raw/source record 保留。

最小优雅吸收版: 每条 reflection candidate 需要 `derived_from_observations`。

结论: adapt/watch。

### M3. MemoryBank

资料名称 / 链接: MemoryBank / https://arxiv.org/abs/2305.10250

解决什么问题: 长期对话记忆需要 summarization、memory strength 和遗忘/衰减机制。

和我们哪一层有关: Activation, Cooling/Reactivation, Use Ledger。

它支持我们什么: 支持 hot/warm/cold 和 cooling/reactivation 的 activation 思想。

它挑战或削弱我们什么: memory strength 容易被误读成 truth confidence。

它能细化我们什么: `activation_strength` 与 `truth_confidence` 必须分开。

它暴露什么风险: 高频使用的错误记忆会被强化。

可吸收的 alpha 设计: use frequency/recency 只影响 activation。

不该吸收的部分: 心理学式遗忘曲线作为 truth aging。

和当前框架融合方式: Memory tier 是 activation priority，不是 truth。

最小优雅吸收版: Use Ledger 可以让常用资料变 hot，但不提升 reviewed confidence。

结论: adapt。

### M4. MemGPT / Letta

资料名称 / 链接: Letta MemGPT architecture / https://docs.letta.com/guides/agents/architectures/memgpt

解决什么问题: LLM context window 有限，需要 core memory 和 archival memory 的分层管理。

和我们哪一层有关: Activation, Dev Context, Context Pack。

它支持我们什么: 支持 Core / Support / Risk / Cold References 的 context pack 分层。

它挑战或削弱我们什么: self-editing memory 与本库 reviewed knowledge gate 冲突。

它能细化我们什么: context pack 中哪些内容 always-in-context，哪些按需检索。

它暴露什么风险: core memory 放错会长期污染行动。

可吸收的 alpha 设计: core memory 只放明确 reviewed 或当前任务必要约束；candidate 放 support/risk。

不该吸收的部分: agent 自主 core_memory_replace。

和当前框架融合方式: DEV_CONTEXT 是临时工作集，不是 truth。

最小优雅吸收版: Context Pack 输出 Core/Support/Risk/Cold。

结论: adapt。

### M5. LightMem / Lightweight Memory-Augmented Generation

资料名称 / 链接: LightMem / https://arxiv.org/abs/2510.18866

解决什么问题: 试图用轻量、模块化 memory system 降低长上下文成本。

和我们哪一层有关: Activation, Context Pack。

它支持我们什么: 支持“轻量激活优先于全量读入”。

它挑战或削弱我们什么: 新近系统、实现细节和 benchmark 需要更多复核。

它能细化我们什么: Topic-aware short-term memory 可作为 context pack clustering 思路。

它暴露什么风险: memory compression 会丢 qualifier、scope、risk。

可吸收的 alpha 设计: activation compression must preserve risk and scope。

不该吸收的部分: memory runtime/benchmark claims。

和当前框架融合方式: Briefing before full read，但高风险时回到 full source。

最小优雅吸收版: briefing 中必须保留 risk/scope，不只保留摘要。

结论: watch。

## Appendix N: Third-Pass Capture / Annotation / Web Preservation Libraries (candidate-only)

这一轮专门补“低摩擦收集 + 来源保全”的实际工具。它们的价值不是把本库变成资料管理软件，而是提醒 Capture 层至少要保住 source identity、retrieval time、original snapshot、user annotation、quote anchor 这些最小证据条件。

### N1. Zotero

资料名称 / 链接: Zotero / https://www.zotero.org/about/ ; Why Zotero / https://www.zotero.org/why

解决什么问题: 研究资料的低摩擦收集、元数据保存、PDF/网页附件、笔记和引用导出。

和我们哪一层有关: Capture, Source Intake, Provenance, Understand。

它支持我们什么: 支持 inbox 到 source record 的路线；source record 先保存作者、标题、URL、附件、摘录、笔记，再进入理解层。

它挑战或削弱我们什么: 文献管理器的 citation metadata 容易让人误以为“引用齐全 = 证据成立”。

它能细化我们什么: `source_record` 可以区分 bibliographic metadata、snapshot/attachment、annotation、candidate extraction。

它暴露什么风险: 网页元数据经常错；自动抓取的标题、日期、作者需要 source hygiene。

可吸收的 alpha 设计: Source record 加 `metadata_quality` 和 `capture_artifacts`，让引用信息和内容证据分开。

不该吸收的部分: 复杂 citation workflow 和文献库 UI。

和当前框架融合方式: Capture 只借低摩擦与附件保全，不把 Zotero 式条目变成 reviewed knowledge。

最小优雅吸收版: source record 记录 `captured_url`、`canonical_url`、`title`、`author`、`captured_at`、`attachment_or_snapshot`、`metadata_warning`。

结论: adapt。

### N2. Hypothesis / Open Web Annotation

资料名称 / 链接: Hypothesis / https://hypothesis-project.org/ ; W3C Web Annotation / https://www.w3.org/TR/annotation-model/

解决什么问题: 在网页/PDF 上做开放标准的注释、高亮、评论和局部锚定。

和我们哪一层有关: Capture, Understand, Evidence Packet。

它支持我们什么: 支持“摘录不是裸文本”，而应带 source anchor、selector、上下文和用户注释。

它挑战或削弱我们什么: 过多 annotation 会让系统变成标注垃圾场；annotation 本身不是 support。

它能细化我们什么: candidate point 的 origin 可以追到 `source_segment`，而不是只追到整篇文章。

它暴露什么风险: 网页结构变动会导致锚点失效；需要保存 textual quote fallback。

可吸收的 alpha 设计: `quote_anchor` 包含 exact quote、prefix/suffix context、selector/source location。

不该吸收的部分: 社交批注层、公开讨论层、实时协作复杂度。

和当前框架融合方式: Understand 抽取 candidate point 时保留 annotation anchor；Review 时仍重新判断证据关系。

最小优雅吸收版: source digest 中每个 candidate point 附 `source_anchor` 与 `extract_note`。

结论: adapt。

### N3. Webrecorder / Browsertrix

资料名称 / 链接: Webrecorder / https://webrecorder.net/ ; Browsertrix / https://webrecorder.net/browsertrix ; GitHub / https://github.com/webrecorder

解决什么问题: 用 WARC/WACZ 等格式保存可回放的网页快照，尤其是动态网页和易消失资料。

和我们哪一层有关: Capture, Provenance, Risk, Review Due。

它支持我们什么: 支持“来源保全不是只存 URL”，关键来源需要 snapshot 或 archive reference。

它挑战或削弱我们什么: 全量归档成本高，不适合作为默认动作。

它能细化我们什么: Source Intake 的 heavy path 可以要求 snapshot；light path 只记录 URL 和时间。

它暴露什么风险: 动态网页、登录页、robots、版权和存储成本都可能让 capture 变重。

可吸收的 alpha 设计: `capture_level = url_only | clipped_text | archived_snapshot`。

不该吸收的部分: 默认把所有来源做 WARC 归档。

和当前框架融合方式: 高风险或易变资料进入 medium/heavy source intake 时才建议 snapshot。

最小优雅吸收版: source record 加 `snapshot_status` 和 `snapshot_reason`，默认可以为空。

结论: adapt/watch。

### N4. SingleFile

资料名称 / 链接: SingleFile / https://github.com/gildas-lormeau/SingleFile

解决什么问题: 将网页保存为单一 HTML 文件，降低个人资料保全和离线复核成本。

和我们哪一层有关: Capture, Source Hygiene。

它支持我们什么: 支持轻量 source preservation，比 WARC 更容易用于普通文章。

它挑战或削弱我们什么: 单文件快照不等于权威原文；脚本、动态内容、时间状态可能失真。

它能细化我们什么: 对普通文章可以设置 cheaper snapshot path。

它暴露什么风险: 保存后的页面可能包含广告、弹窗、追踪片段或被阅读模式改写。

可吸收的 alpha 设计: `snapshot_method` 明确记录，避免把 snapshot 当原始来源。

不该吸收的部分: 把 HTML 快照当唯一证据，不再回看原网页。

和当前框架融合方式: light/medium capture 可保留 single-file snapshot 作为复核辅助。

最小优雅吸收版: source record 中记录 `snapshot_method: singlefile` 和 `snapshot_caveat`。

结论: adapt。

### N5. Perma.cc

资料名称 / 链接: Perma.cc / https://perma.cc/

解决什么问题: 为引用创建可长期访问的 archived link，减少 link rot。

和我们哪一层有关: Capture, Provenance, Risk。

它支持我们什么: 支持 source permanence 和 review reproducibility。

它挑战或削弱我们什么: 第三方 archive link 仍不能证明内容支持某个 claim。

它能细化我们什么: `source_record` 可区分 live URL 与 archived URL。

它暴露什么风险: archive 服务可用性、访问权限、版权限制和动态内容缺失。

可吸收的 alpha 设计: 对关键外部来源记录 `archived_url`，并保留 live URL。

不该吸收的部分: 把 archived link 当成证据质量评分。

和当前框架融合方式: Capture/Source Intake 的 source hygiene 字段。

最小优雅吸收版: 关键 source 加 `archived_url`；没有也不阻塞 review。

结论: adapt/watch。

### N6. Monolith

资料名称 / 链接: Monolith / https://github.com/Y2Z/monolith

解决什么问题: 命令行把网页和资源打包成单个 HTML，适合轻量离线保存。

和我们哪一层有关: Capture, Source Intake。

它支持我们什么: 支持“简单来源快照”可以是可选工具，而不是复杂平台。

它挑战或削弱我们什么: 需要执行外部工具；当前框架不应默认引入运行链。

它能细化我们什么: Capture 可以定义 artifact 类型，而不绑定工具。

它暴露什么风险: 自动下载资源可能带来安全和版权问题。

可吸收的 alpha 设计: 只吸收 artifact taxonomy，不吸收工具依赖。

不该吸收的部分: 在系统内置网页下载器。

和当前框架融合方式: `capture_artifact_type = url | quote | pdf | html_snapshot | warc_snapshot`。

最小优雅吸收版: 文档层说明 snapshot 是可选 artifact。

结论: watch。

## Appendix O: Third-Pass Attribution / Citation / Factuality Evaluation (candidate-only)

这些资料更贴近 Context Pack 和 Review 的边界：它们证明“引用生成”和“证据成立”不是一回事。可吸收的是 atomic claim、citation precision/recall、post-hoc attribution、unsupported content repair 等轻量概念；不应吸收自动评分来替代人工 review。

### O1. ALCE

资料名称 / 链接: ALCE: Enabling Large Language Models to Generate Text with Citations / https://arxiv.org/abs/2305.14627 ; GitHub / https://github.com/princeton-nlp/ALCE

解决什么问题: 评估 LLM 长答案是否能正确生成带来源引用的回答。

和我们哪一层有关: Context Pack, Act and Learn, Evidence-Aware Review。

它支持我们什么: 支持 citation quality 应拆成 answer correctness、citation precision、citation recall，而不是“有链接就好”。

它挑战或削弱我们什么: 自动 NLI citation scoring 仍可能把表面蕴含当真实支持。

它能细化我们什么: Context Pack 输出可带 `citation_precision_risk` 或 `evidence_gap`。

它暴露什么风险: 引用可被模型后贴；citation after generation 不等于 action basis。

可吸收的 alpha 设计: 把 source citation 分为 `cited`, `actually_used`, `supports_claim`, `insufficient`。

不该吸收的部分: 用 benchmark metric 直接给本库 knowledge confidence 加分。

和当前框架融合方式: Act 前检查 action basis 是否有足够 evidence packet。

最小优雅吸收版: Context Pack 增加“引用覆盖缺口”提示，而不做分数系统。

结论: adapt。

### O2. RARR

资料名称 / 链接: RARR: Researching and Revising What Language Models Say / https://arxiv.org/abs/2210.08726

解决什么问题: 对已生成文本做检索、找归因、修订不支持内容。

和我们哪一层有关: Understand, Review, Act and Learn。

它支持我们什么: 支持候选输出先经过 attribution/revision，而不是直接进入知识库。

它挑战或削弱我们什么: Post-hoc attribution 可能为原本没有证据的句子找“看似相关”的材料。

它能细化我们什么: Review input 可以包含 `unsupported_sentence` 和 `revision_needed`。

它暴露什么风险: 过度依赖模型修订会掩盖原始生成错误。

可吸收的 alpha 设计: 生成后做“unsupported content pass”，但只产 review input。

不该吸收的部分: 自动改写后直接提升 truth status。

和当前框架融合方式: Candidate point 进入 review 前可做 attribution check。

最小优雅吸收版: 对 source digest 的每个 claim 标注 `needs_attribution` / `attributed` / `unsupported`。

结论: adapt。

### O3. FActScore

资料名称 / 链接: FActScore / https://arxiv.org/abs/2305.14251

解决什么问题: 将长文本拆成 atomic facts，再逐项检查是否被可靠来源支持。

和我们哪一层有关: Understand, Evidence-Aware Review。

它支持我们什么: 强力支持 candidate point extraction 的颗粒度应尽量 atomic、可验证。

它挑战或削弱我们什么: “被来源支持的比例”不等于系统判断可行动；范围、反例和风险仍需 review。

它能细化我们什么: source digest 可先拆 atomic candidate point，再做 collision。

它暴露什么风险: atomic fact 过细会增加 review 负担。

可吸收的 alpha 设计: 对复杂判断先拆成 atomic claims + linking rationale。

不该吸收的部分: 把 factual precision 百分比转成 truth confidence。

和当前框架融合方式: Understand 层做 claim decomposition；Review 层做 standing check。

最小优雅吸收版: 对长句只在必要时拆 atomic，不要求所有资料机械拆分。

结论: adopt/adapt。

### O4. Self-RAG

资料名称 / 链接: Self-RAG / https://arxiv.org/abs/2310.11511

解决什么问题: 让模型判断何时需要检索，并对生成内容做自我批评。

和我们哪一层有关: Activation, Context Pack, Act and Learn。

它支持我们什么: 支持 briefing before full read，以及“并非所有任务都需要全量检索”。

它挑战或削弱我们什么: Self-reflection 是模型内部信号，不是证据。

它能细化我们什么: Context Pack 可以显式区分 `retrieval_needed` 与 `sufficient_context`。

它暴露什么风险: 模型可能自信地判断不需要检索，从而遗漏 stale/risk。

可吸收的 alpha 设计: 检索需求判断必须受 risk gate 约束。

不该吸收的部分: 让模型自评直接决定 review 跳过。

和当前框架融合方式: Activation 层可先给 brief；高风险或冲突时强制回源。

最小优雅吸收版: Context Pack 增加 `need_full_source_read` 布尔/理由。

结论: adapt/watch。

### O5. Automatic Evaluation of Attribution by Large Language Models

资料名称 / 链接: Automatic Evaluation of Attribution by Large Language Models / https://arxiv.org/abs/2305.06311

解决什么问题: 自动判断回答中的内容是否被给定引用充分归因。

和我们哪一层有关: Evidence-Aware Review, Context Pack QA。

它支持我们什么: 支持 citation faithfulness 需要单独检查，不应与 answer quality 混在一起。

它挑战或削弱我们什么: 自动 attribution evaluator 本身会犯错，不能当 judge。

它能细化我们什么: `provenance != support` 可以扩展成 `citation != attribution != evidence`。

它暴露什么风险: 自动评估可能鼓励优化表面引用格式。

可吸收的 alpha 设计: Review checklist 加一问：引用是否真的覆盖这句话？

不该吸收的部分: 自动 attribution pass 作为 promotion gate。

和当前框架融合方式: Evidence packet 的 `support_relation` 需要人工/规则确认。

最小优雅吸收版: 每条 action basis claim 最少列一个 supporting excerpt 或标为 evidence gap。

结论: adapt。

### O6. CiteEval / CiteBench

资料名称 / 链接: CiteEval: Principle-Driven Citation Evaluation for Source Attribution / https://arxiv.org/abs/2506.01829

解决什么问题: 认为仅用 NLI 判断 citation support 不足，提出更原则化的 citation evaluation。

和我们哪一层有关: Evidence-Aware Review, Risk。

它支持我们什么: 支持“相似/蕴含/检索命中”不能替代 evidence relation。

它挑战或削弱我们什么: 新近 benchmark 与自动评估体系需要观望。

它能细化我们什么: Citation quality 可以分拆为相关性、完整性、必要性、无误导性。

它暴露什么风险: citation evaluation 越做越重，会把轻量 review 变成官僚流程。

可吸收的 alpha 设计: 只吸收 citation principles，不吸收评测框架。

不该吸收的部分: 大型 citation benchmark pipeline。

和当前框架融合方式: Evidence-Aware Review 的支持项可检查“是否 cherry-pick / 是否缺关键反证”。

最小优雅吸收版: Review 表单加 `citation_covers_claim: yes/no/partial`。

结论: watch/adapt。

## Appendix P: Third-Pass Argument Mapping / Decision-Rationale Tools (candidate-only)

这组资料用于校准 Evidence-Aware Review 的可视化和最小表达。结论很明确：可以借“问题-选项-理由-反对”的结构，但不要把本库变成复杂论证图平台。

### P1. Carneades Argumentation System

资料名称 / 链接: Carneades / https://carneades.github.io/carneades/

解决什么问题: 用 defeasible argument、argument schemes、multi-criteria decision analysis 组织可败推理。

和我们哪一层有关: Evidence-Aware Review, Point Collision, Decision/Action。

它支持我们什么: 支持 review 关注 warrant、burden、challenge、undercut，而非只数来源。

它挑战或削弱我们什么: 完整 argumentation system 对当前框架过重。

它能细化我们什么: `standing` 可以理解为在当前反对项下仍未被击败，而不是“永久为真”。

它暴露什么风险: 形式化推理会诱惑系统过早自动裁决。

可吸收的 alpha 设计: review output 可有 `standing_reason` 和 `defeaters_considered`。

不该吸收的部分: Carneades runtime、完整 argument evaluation semantics。

和当前框架融合方式: 只作为 Review vocabulary 的来源。

最小优雅吸收版: 在 review 结论里列“主要支持、主要反对、未击败原因、适用范围”。

结论: adapt。

### P2. Argdown

资料名称 / 链接: Argdown / https://argdown.org/ ; Markdown guide / https://argdown.org/guide/using-argdown-in-markdown.html

解决什么问题: 用类 Markdown 语法写 argument maps，区分 statement 和 argument。

和我们哪一层有关: Review, Connect, Architecture Discussion。

它支持我们什么: 支持用轻量文本表达 support/attack/refine，不必直接上图数据库。

它挑战或削弱我们什么: 如果引入专用 DSL，会增加学习成本和格式负担。

它能细化我们什么: 重要 collision cluster 可以用文本 argument map 解释。

它暴露什么风险: 图看起来清楚，不代表证据关系真实成立。

可吸收的 alpha 设计: 可选地为复杂 review 生成 small argument sketch。

不该吸收的部分: 把 Argdown 语法变成系统必填格式。

和当前框架融合方式: 作为 outputs/review 的可选表达，而不是 schema。

最小优雅吸收版: 人类可读的 `support/challenge/scope/risk` 小表已经足够。

结论: watch/adapt。

### P3. DebateGraph

资料名称 / 链接: DebateGraph / https://debategraph.org/debategraphabout

解决什么问题: 面向复杂公共议题的协作论证可视化和持续挑战。

和我们哪一层有关: Evidence-Aware Review, Connect。

它支持我们什么: 支持“复杂判断要保留 all sides”，尤其适合争议性问题。

它挑战或削弱我们什么: 协作公开辩论平台与个人 knowledge system 的摩擦太大。

它能细化我们什么: Review cluster 可按 thesis/position/pro/con/gap 组织。

它暴露什么风险: 讨论规模会膨胀，压过行动导向。

可吸收的 alpha 设计: 对高争议判断保留 `opposing_positions`。

不该吸收的部分: 公开协作平台、无限分叉讨论。

和当前框架融合方式: 只吸收“多方立场不合并”的意识。

最小优雅吸收版: 对 disputed claim 加 `known_opposition` 和 `open_question`。

结论: watch。

### P4. Kialo

资料名称 / 链接: Kialo / https://www.kialo.com/ ; Kialo Edu features / https://www.kialo-edu.com/features

解决什么问题: 用树状 pro/con 结构组织争论和课堂讨论。

和我们哪一层有关: Review, Risk/Inhibition。

它支持我们什么: 支持 pro/con 分层能降低“只收集支持证据”的偏差。

它挑战或削弱我们什么: Pro/con tree 容易把复杂证据压成二元赞反。

它能细化我们什么: Review UI 若未来出现，也应让反对证据和范围限制同等显眼。

它暴露什么风险: 讨论树会鼓励观点对抗，而不是证据校准。

可吸收的 alpha 设计: Review summary 中 support 与 challenge 对称呈现。

不该吸收的部分: 树状辩论产品形态。

和当前框架融合方式: Evidence-Aware Review 的表达层可借鉴，不进入核心机制。

最小优雅吸收版: 每个 reviewed judgment 下保留 `supporting_evidence` 与 `challenging_evidence` 两栏。

结论: reject as system / adapt as UI hint。

## Appendix Q: Third-Pass RAG Evaluation / Observability Libraries (candidate-only)

这些库值得看，但吸收边界要很硬：它们适合评估 retrieval/context pack/action output 的运行质量，不适合直接评定知识真伪。对本框架最有价值的是把“retrieval relevance、context precision、groundedness、answer relevance、trace”拆开。

### Q1. RAGAS

资料名称 / 链接: RAGAS / https://arxiv.org/abs/2309.15217 ; metrics docs / https://docs.ragas.io/en/stable/concepts/metrics/available_metrics/

解决什么问题: 为 RAG pipeline 提供 reference-free 或半自动评估，包括 context precision、context recall、faithfulness、answer relevancy。

和我们哪一层有关: Context Pack, Act and Learn, Use Ledger。

它支持我们什么: 支持把 retrieval 是否命中、context 是否可用、回答是否忠于上下文拆开看。

它挑战或削弱我们什么: faithfulness score 容易被误用为 truth confidence。

它能细化我们什么: Use Ledger 可记录一次 context pack 是否 useful、grounded、missing context。

它暴露什么风险: LLM-as-judge 指标不稳定；评估成本也可能高。

可吸收的 alpha 设计: `context_pack_eval` 只评价“这次使用质量”，不改变 reviewed knowledge。

不该吸收的部分: 自动指标驱动 knowledge promotion。

和当前框架融合方式: Act and Learn 后形成 feedback event，影响 activation/usefulness。

最小优雅吸收版: Use Ledger 加 `context_precision_issue`、`missing_context`、`answer_grounding_issue`。

结论: adapt。

### Q2. TruLens RAG Triad

资料名称 / 链接: TruLens RAG Triad / https://www.trulens.org/getting_started/core_concepts/rag_triad/

解决什么问题: 用 context relevance、groundedness、answer relevance 三个维度评估 RAG。

和我们哪一层有关: Context Pack, Action Basis, Use Ledger。

它支持我们什么: 非常贴合“搜索分数不是关系”：retrieved context 相关、回答相关、回答被上下文支撑是三件事。

它挑战或削弱我们什么: groundedness 仍是对当前上下文的判断，不是对世界事实的判断。

它能细化我们什么: action basis 可区分 `context_relevant`、`claim_grounded`、`answer_useful`。

它暴露什么风险: 自动 groundedness 可能漏掉上下文外的反证。

可吸收的 alpha 设计: 三分法作为 lightweight QA checklist。

不该吸收的部分: 把 RAG triad 分数写入 knowledge confidence。

和当前框架融合方式: Use Ledger 记录 context pack 质量；Review 仍独立。

最小优雅吸收版: 每次重要输出后可选打三类问题：资料对题吗、回答依资料吗、回答解决任务吗。

结论: adopt as checklist / reject as truth metric。

### Q3. Arize Phoenix / OpenInference

资料名称 / 链接: Arize Phoenix / https://github.com/Arize-ai/phoenix ; OpenInference semantic conventions / https://arize-ai.github.io/openinference/spec/semantic_conventions.html

解决什么问题: LLM/RAG/agent tracing、eval、实验记录和 OpenTelemetry 风格观测。

和我们哪一层有关: Act and Learn, Use Ledger, Context Pack Trace。

它支持我们什么: 支持 action trace 应记录 retriever、prompt、LLM、tool、response 等运行链路。

它挑战或削弱我们什么: Observability stack 对当前 vault 太重，不该进入核心。

它能细化我们什么: Use Ledger 可以借 span kind 思路区分 `retriever`、`context_pack`、`action`、`feedback`。

它暴露什么风险: trace 多了会变成日志系统，稀释知识系统的主线。

可吸收的 alpha 设计: 保留 minimal action trace schema，不引入完整 observability 平台。

不该吸收的部分: telemetry backend、dashboard、在线 tracing。

和当前框架融合方式: Act and Learn 保存少量人类可读的 use event。

最小优雅吸收版: Use Ledger 只记录 `used_sources`、`context_pack_id`、`decision_basis`、`outcome_feedback`。

结论: adapt/watch。

### Q4. DeepEval

资料名称 / 链接: DeepEval / https://github.com/confident-ai/deepeval ; faithfulness docs / https://deepeval.com/docs/metrics-faithfulness

解决什么问题: 为 LLM 应用提供测试和评估指标，包括 faithfulness、answer relevancy、hallucination 等。

和我们哪一层有关: Act and Learn, Risk, QA。

它支持我们什么: 支持对输出是否与 retrieval context 冲突做 smoke check。

它挑战或削弱我们什么: LLM judge 的 reason 看起来像解释，但不是 review。

它能细化我们什么: 对高风险 context pack 可加入“输出是否违背已给材料”的检查。

它暴露什么风险: 指标套件会诱导过度工程和 false confidence。

可吸收的 alpha 设计: 只借 `faithfulness_to_context` 这个失败类型。

不该吸收的部分: pytest 式评估体系、CI gate、在线 judge。

和当前框架融合方式: 用于未来实现时的 QA 候选，不写入当前架构源文件。

最小优雅吸收版: Review/Risk 词表加入 `context_contradiction`。

结论: watch/adapt。

### Q5. OpenInference Semantic Conventions

资料名称 / 链接: OpenInference Semantic Conventions / https://arize-ai.github.io/openinference/spec/semantic_conventions.html

解决什么问题: 给 LLM、embedding、retriever、reranker、agent、tool 等运行 span 提供统一属性。

和我们哪一层有关: Act and Learn, Use Ledger, Dev Context。

它支持我们什么: 支持“用过什么上下文、走过什么检索、调用过什么工具”要和知识关系分开。

它挑战或削弱我们什么: span schema 过细，不适合手写 vault。

它能细化我们什么: Use Ledger 未来若结构化，可借用 span kind 的最小集合。

它暴露什么风险: 观测字段爆炸。

可吸收的 alpha 设计: `trace_kind` 枚举只保留 retrieve/context/action/feedback。

不该吸收的部分: 全套 OpenTelemetry 语义约定。

和当前框架融合方式: Context Pack Trace 的候选字段来源。

最小优雅吸收版: `use_event.trace = [retrieved, packed, acted, feedback]`。

结论: watch。

## Appendix R: Third-Pass Systematic Review / Evidence Discipline (candidate-only)

系统综述方法很容易把本项目带向重流程，所以这里只吸收最轻的原则：问题要清楚、检索要可复现、纳入/排除要说明、偏倚和适用性分开、更新不是按时间机械触发。

### R1. PRISMA 2020

资料名称 / 链接: PRISMA 2020 Statement / https://www.prisma-statement.org/prisma-2020-statement

解决什么问题: 系统综述报告透明度，包含 checklist、流程图和更新综述报告建议。

和我们哪一层有关: Source Intake, Review, Review Queue。

它支持我们什么: 支持 review 应记录检索/纳入/排除理由，而不是只给结论。

它挑战或削弱我们什么: 完整 PRISMA 对本库过重，会把普通资料 review 变成学术综述。

它能细化我们什么: Heavy review 可以保留 `included_sources`、`excluded_sources`、`exclusion_reason`。

它暴露什么风险: checklist 化会让系统繁琐。

可吸收的 alpha 设计: 只在高影响架构判断中记录“看过哪些，为什么没采用”。

不该吸收的部分: 27 项 checklist、流程图、正式综述报告格式。

和当前框架融合方式: Review Queue 的 heavy path 候选，不影响 light/medium path。

最小优雅吸收版: 重要判断加 `review_scope` 和 `not_considered_or_excluded`。

结论: adapt/watch。

### R2. PICO Framework

资料名称 / 链接: PICO framework overview / https://libguides.mssm.edu/ebm/ebp_pico

解决什么问题: 将问题结构化为对象、干预、比较、结果，避免问题过宽。

和我们哪一层有关: Understand, Review, Activation。

它支持我们什么: 支持 review 前先明确“这个资料到底回答哪个问题”。

它挑战或削弱我们什么: PICO 源自医学，直接套到架构判断会别扭。

它能细化我们什么: 可泛化成 `question_scope = subject / intervention_or_pattern / comparator / desired_outcome`。

它暴露什么风险: 过度模板化会压低探索性思考。

可吸收的 alpha 设计: 对混乱问题先写一行 review question。

不该吸收的部分: 医学术语和固定字段。

和当前框架融合方式: Architecture review window 可以先明确比较问题。

最小优雅吸收版: `review_question` 字段。

结论: adapt。

### R3. ROBIS

资料名称 / 链接: ROBIS risk of bias in systematic reviews / https://pmc.ncbi.nlm.nih.gov/articles/PMC4687950/

解决什么问题: 评估系统综述本身的偏倚风险和对当前问题的相关性。

和我们哪一层有关: Evidence-Aware Review, Risk/Inhibition。

它支持我们什么: 强力支持“来源质量”和“对当前问题适用性”要分开。

它挑战或削弱我们什么: 偏倚评估工具本身较重。

它能细化我们什么: `source_reliability`、`evidence_relevance`、`scope_fit` 分离。

它暴露什么风险: 用单一 quality score 掩盖具体偏倚类型。

可吸收的 alpha 设计: 不打总分，只列 bias/risk flags。

不该吸收的部分: 完整 ROBIS domain checklist。

和当前框架融合方式: Evidence-aware review 的 risk 字段可包含 method bias、selection bias、conflict of interest。

最小优雅吸收版: `bias_or_scope_warning` 字段。

结论: adapt。

### R4. Cochrane MECIR Updating Standards

资料名称 / 链接: Cochrane conduct standards for updates / https://www.cochrane.org/authors/handbooks-and-manuals/mecir-manual/standards-planning-and-conduct-updates-cochrane-intervention-reviews-u1-u11/deciding-and-performing-update-u1-u11/conduct-standards-specific-updates-u6-u11

解决什么问题: 何时、如何更新综述，要求重新检索、筛选并说明新证据影响。

和我们哪一层有关: Review Due, Cooling/Reactivation, Risk。

它支持我们什么: 支持 review_due 应由新证据、过期假设、领域变化触发，而不只是定期刷新。

它挑战或削弱我们什么: 医学综述更新规则不能直接套到个人知识库。

它能细化我们什么: `review_due_reason` 比 `review_due_date` 更重要。

它暴露什么风险: 定期更新所有内容会制造维护债。

可吸收的 alpha 设计: update trigger 记录“为什么现在需要复核”。

不该吸收的部分: 固定 6/12 个月检索要求。

和当前框架融合方式: Risk/Inhibition 的 stale assumptions 触发 Review Queue。

最小优雅吸收版: `review_due_when = new_conflicting_evidence | stale_source | changed_domain | failed_use`。

结论: adopt as principle / adapt implementation。

### R5. AMSTAR 2

资料名称 / 链接: AMSTAR 2 / https://amstar.ca/Amstar-2.php

解决什么问题: 评价系统综述的方法学质量，尤其关注关键弱点。

和我们哪一层有关: Evidence-Aware Review, Risk。

它支持我们什么: 支持不把所有资料同等对待；综述/二手资料也要检查方法弱点。

它挑战或削弱我们什么: checklist 很重，不适合普通架构资料。

它能细化我们什么: 对“综述型文章”标注 `method_disclosure` 和 `selection_transparency`。

它暴露什么风险: 质量评估可能变成形式主义。

可吸收的 alpha 设计: 对二手综述问一句：它怎么选资料，漏了什么？

不该吸收的部分: 正式评分和完整 checklist。

和当前框架融合方式: Source hygiene 的候选检查。

最小优雅吸收版: `secondary_source_warning` 字段。

结论: watch/adapt。

## Appendix S: Third-Pass Source Criticism / Lateral Reading (candidate-only)

这组资料偏信息素养，但很适合补 Source Hygiene：先识别来源身份、目的和原始上下文，再讨论它能不能支持具体判断。它们的价值是轻，不是严密；适合 Capture/Understand 阶段做红旗提醒。

### S1. SIFT / Lateral Reading

资料名称 / 链接: SIFT source checking overview / https://fhsuguides.fhsu.edu/SIFT ; Stanford lateral reading report / https://news.stanford.edu/2017/10/24/fact-checkers-outperform-historians-evaluating-online-information/

解决什么问题: 快速判断网页来源可信度，强调停下来、查来源、找更好覆盖、追到原始上下文。

和我们哪一层有关: Capture, Source Hygiene, Risk/Inhibition。

它支持我们什么: 支持来源检查应发生在内容吸收前，尤其是网页、新闻、博客和 repo README。

它挑战或削弱我们什么: SIFT 是启发式，不是证据评审。

它能细化我们什么: `source_hygiene_warning` 可以包含 unknown author、secondary-only、missing original context。

它暴露什么风险: 过度 lateral reading 会让低风险收集变慢。

可吸收的 alpha 设计: 高风险来源先做 one-minute source identity check。

不该吸收的部分: 把 SIFT 当正式 review protocol。

和当前框架融合方式: Capture/Understand 只加轻量 warning，不阻断。

最小优雅吸收版: source intake 增加 `source_identity_checked: yes/no/needed`。

结论: adapt。

### S2. CRAAP Test

资料名称 / 链接: CRAAP source evaluation overview / https://library.nwacc.edu/sourceevaluation ; Scribbr overview / https://www.scribbr.com/working-with-sources/craap-test/

解决什么问题: 从 currency、relevance、authority、accuracy、purpose 几个维度评估来源。

和我们哪一层有关: Source Intake, Risk, Evidence-Aware Review。

它支持我们什么: 支持“来源质量”有多个维度，不能只看域名或引用数量。

它挑战或削弱我们什么: checklist 容易形式化，而且 authority 不等于 support。

它能细化我们什么: `source_quality_notes` 可以拆成 timeliness、authority、purpose、accuracy caveat。

它暴露什么风险: 可能鼓励给来源打总分，而总分会掩盖具体缺陷。

可吸收的 alpha 设计: 不打分，只保存具体 caveat。

不该吸收的部分: CRAAP 总分、强制表格。

和当前框架融合方式: Source hygiene 的候选字段来源。

最小优雅吸收版: 对可疑来源只写一句 `source_caveat`。

结论: adapt/watch。

### S3. Source Criticism

资料名称 / 链接: Source criticism overview / https://en.wikipedia.org/wiki/Source_criticism

解决什么问题: 判断文献、证言、材料来源的真实性、可靠性、独立性和偏向。

和我们哪一层有关: Evidence-Aware Review, Risk, Connect。

它支持我们什么: 支持独立来源、原始来源、二手解释、派生关系必须区分。

它挑战或削弱我们什么: 传统 source criticism 可能仍偏“来源可信”，不够强调 claim-level support。

它能细化我们什么: `derived_from` 不等于 `supports`；同源重复不增加支持强度。

它暴露什么风险: 多个引用可能只是同一原始来源的转载。

可吸收的 alpha 设计: Evidence packet 记录 `independence_of_source`。

不该吸收的部分: 历史学完整考证流程。

和当前框架融合方式: Connect 层 relation 里保留 `derived_from` 和 `independent_support` 区别。

最小优雅吸收版: Review 中增加“这些来源是否独立？”一问。

结论: adapt。

### S4. Media Background Checks for Source-Critical Reasoning

资料名称 / 链接: Generating Media Background Checks for Automated Source Critical Reasoning / https://arxiv.org/abs/2409.00781

解决什么问题: 为信息来源生成背景检查，帮助人和模型判断媒体/来源可信度。

和我们哪一层有关: Capture, Source Hygiene, Risk/Inhibition。

它支持我们什么: 支持在读取具体 claim 前，先获取 source background。

它挑战或削弱我们什么: 自动 source background 也可能偏见或过期。

它能细化我们什么: `source_profile` 可以是候选辅助，而不是证据。

它暴露什么风险: 对来源背景的判断会污染对具体证据的独立审查。

可吸收的 alpha 设计: source profile 标注 candidate-only，并和 evidence packet 分开。

不该吸收的部分: 自动可信度评级。

和当前框架融合方式: Source hygiene 的 optional warning，不进入 truth confidence。

最小优雅吸收版: 对陌生媒体来源记录 `source_background_note`。

结论: watch/adapt。

## Appendix T: Third-Pass Statement Provenance / Edge Metadata in Knowledge Graphs (candidate-only)

这组资料补 Connect 层的一个关键点：关系不是只有 subject-predicate-object，关系本身也需要 provenance、scope、rank/state、qualifier。可吸收的是“边/判断带元数据”，不是 RDF 技术栈。

### T1. Wikidata Qualifiers / References / Ranks

资料名称 / 链接: Wikidata qualifiers / https://www.wikidata.org/wiki/Help:Qualifiers ; Wikidata data model / https://www.wikidata.org/wiki/Wikidata:Data_model/en

解决什么问题: Wikidata statements 可带 qualifiers、references 和 ranks，用来表达上下文、来源和优先/弃用状态。

和我们哪一层有关: Connect, Reviewed Relations, Scope, Risk。

它支持我们什么: 强力支持 relation_state 不只是存在/不存在，还要表达 scope、source、deprecated/preferred。

它挑战或削弱我们什么: Wikidata 面向开放公共数据，字段复杂度远超当前框架。

它能细化我们什么: `reviewed_relation` 可有 `qualifier` 和 `relation_state`，例如 active/deprecated/disputed/scope_limited。

它暴露什么风险: rank 容易被误读成 truth confidence；preferred 只是当前展示/选择状态。

可吸收的 alpha 设计: 边上保留 qualifier 与 source，不把 qualifier 合并进正文。

不该吸收的部分: Wikibase item/property model、rank 机制全套复刻。

和当前框架融合方式: Connect 层保留 minimal relation metadata。

最小优雅吸收版: relation 加 `scope_qualifier`、`evidence_ref`、`relation_state`。

结论: adopt as principle / adapt schema。

### T2. Named Graphs

资料名称 / 链接: Named Graphs, Provenance and Trust / https://www.w3.org/2009/12/rdf-ws/p613.pdf ; W3C PROV named graph discussion / https://www.w3.org/2011/prov/wiki/Using_named_graphs_to_model_Accounts

解决什么问题: 给一组 RDF statements 命名，以便描述该 statement set 的来源、上下文、信任和版本。

和我们哪一层有关: Connect, Provenance, Review Queue。

它支持我们什么: 支持“同一条关系可以来自不同 source bundle”，source bundle 本身有 provenance。

它挑战或削弱我们什么: Named graph 技术细节对 Markdown vault 太重。

它能细化我们什么: Review cluster 可以视作一组候选 points/relations 的 context graph。

它暴露什么风险: 图层级过多会让人找不到实际判断。

可吸收的 alpha 设计: 用 `review_cluster_id` 表示一组相关 points/relations 的证据上下文。

不该吸收的部分: RDF dataset、SPARQL、graph URI 体系。

和当前框架融合方式: outputs/review 可把 collision cluster 当作 named context。

最小优雅吸收版: `collision_cluster` 记录 included points、local reviewed targets、open questions。

结论: adapt/watch。

### T3. RDF-star / Statement-Level Metadata

资料名称 / 链接: RDF-star and SPARQL-star / https://www.w3.org/2021/12/rdf-star.html

解决什么问题: 更方便地对 RDF triple 本身添加元数据，例如来源、置信、时间。

和我们哪一层有关: Connect, Evidence Packet。

它支持我们什么: 支持 relation/claim 的元数据必须挂在 statement 上，而不是只挂在 source 上。

它挑战或削弱我们什么: RDF-star 是表达技术，不解决 evidence standing。

它能细化我们什么: `claim_id` / `relation_id` 应作为一等对象，才能挂支持、反对、scope、risk。

它暴露什么风险: 过早技术化会让 schema 膨胀。

可吸收的 alpha 设计: 每个 reviewed judgment 有 stable id。

不该吸收的部分: RDF-star serialization 和查询语言。

和当前框架融合方式: Markdown schema 只保留 id 和元数据字段。

最小优雅吸收版: `judgment_id` 下挂 evidence packet 和 relation links。

结论: adapt。

### T4. CIDOC CRMdig

资料名称 / 链接: CRMdig / https://cidoc-crm.org/crmdig/ ; CRMdig model version / https://cidoc-crm.org/crmdig/ModelVersion/crmdig-v5.0

解决什么问题: 为数字对象、观察、处理过程和 provenance 建模，常用于文化遗产/研究数据。

和我们哪一层有关: Capture, Provenance, Source Intake。

它支持我们什么: 支持 provenance 可以追踪到生成/数字化/处理过程，而不只是作者和 URL。

它挑战或削弱我们什么: CIDOC CRM 家族非常复杂，不适合当前个人知识库。

它能细化我们什么: 对经过 AI digest、snapshot、conversion 的资料，要区分 original source 与 processing artifact。

它暴露什么风险: 处理链越多，越容易把处理产物当原文。

可吸收的 alpha 设计: source record 区分 `original_source`、`capture_artifact`、`processing_step`。

不该吸收的部分: CIDOC ontology。

和当前框架融合方式: Source provenance 字段轻量扩展。

最小优雅吸收版: digest 文件中记录 `generated_from` 和 `processing_note`。

结论: adapt/watch。

## Appendix U: Local Wiki Alignment Check Before Frontier Absorption (candidate-only)

按用户提醒，补读了本地 `wiki/` 里最新且最容易与前沿资料碰撞的设计页：

- `wiki/patterns/context-pack-evidence-envelope.md`
- `wiki/patterns/agent-context-pack-budget-guardrails.md`
- `wiki/patterns/scope-dashboard-live-context-surface.md`
- `wiki/patterns/hierarchical-index-context-routing.md`
- `wiki/patterns/token-efficient-context-briefing.md`
- `wiki/patterns/property-driven-context-workbench.md`
- `wiki/anti-patterns/derived-relatedness-as-truth-signal.md`
- `wiki/anti-patterns/auto-promotion-without-review-gate.md`

本地设计对齐结论：

1. 当前 wiki 已经把 index / dashboard / briefing / context pack 定位为 loading and activation surface，不是 truth layer。
2. `Context Pack Evidence Envelope` 已有核心形状：budget、primary/supporting、warnings、gaps、source windows，并且明确 pack 不写回 wiki。
3. `Agent Context Pack Budget Guardrails` 已经吸收了 deterministic trimming、source window 默认关闭、召回原因可解释等控制点。
4. `Scope Dashboard Live Context Surface` 和 `Property-Driven Context Workbench` 已经把“视图/属性/仪表盘”限定为候选上下文表面。
5. `Derived Relatedness As Truth Signal` 明确禁止把 backlinks、tags、recency、ratings、link overlap 当成 support/truth。
6. `Auto Promotion Without Review Gate` 明确禁止自动分类/摘要/合成直接写入 verified knowledge。

所以，下面的前沿资料只能按三类吸收：

- 作为 Activation / Context Pack 的召回、预算、trace、freshness 改进。
- 作为 Review Queue 的 candidate relation / conflict / stale / missing evidence 触发器。
- 作为 Source Hygiene / Risk 的警告来源。

不应吸收为：

- 自动 truth update。
- 自动 relation promotion。
- 自动 confidence scoring。
- 自主 agent memory writeback。

## Appendix V: Frontier Design Watchlist After Local Wiki Alignment (candidate-only)

这一轮按“最新资料库设计 wiki + 前沿系统”的方向补资料。重点不是追热点，而是判断它们能不能优雅补强现有 `Capture -> Understand -> Review -> Connect -> Act and Learn` 主线。

### V1. Context Engineering Survey

资料名称 / 链接: A Survey of Context Engineering for Large Language Models / https://arxiv.org/abs/2507.13334

解决什么问题: 把 context retrieval、generation、processing、management 统一成 context engineering，而不是把上下文窗口当被动输入。

和我们哪一层有关: Activation, Context Pack, Dev Context, Act and Learn。

它支持我们什么: 强力支持本地 `token-efficient-context-briefing` 和 `context-pack-evidence-envelope`：context 是可管理对象，必须有选择、预算、处理、失效和追踪。

它挑战或削弱我们什么: Survey 口径容易把所有上下文处理都纳入工程体系，可能诱导过度设计。

它能细化我们什么: Context Pack 可拆成 `context_retrieval`、`context_processing`、`context_management` 三个轻字段，便于 future implementation 但不增加当前流程。

它暴露什么风险: context optimization 指标会掩盖 evidence quality；高相关上下文仍可能没有支持关系。

可吸收的 alpha 设计: 把 `context_pack_trace` 定义为“为什么召回、如何裁剪、哪些 warning/gap 保留”。

不该吸收的部分: 全面 context engineering taxonomy 和复杂 pipeline。

和当前框架融合方式: 只补 Activation/Context Pack 的语言，不改主循环。

最小优雅吸收版: Context Pack 增加 `why_included`、`trimmed_due_to_budget`、`missing_context`。

结论: adopt as vocabulary / adapt as design。

### V2. MemOS / MemoryOS Family

资料名称 / 链接: MemOS / https://arxiv.org/abs/2505.22101 ; MemTensor/MemOS / https://github.com/MemTensor/MemOS ; BAI-LAB MemoryOS / https://github.com/BAI-LAB/MemoryOS

解决什么问题: 把 agent memory 提升为可管理的系统资源，强调长期记忆、跨任务复用、个性化和 memory lifecycle。

和我们哪一层有关: Activation, Use Ledger, Cooling/Reactivation, Risk。

它支持我们什么: 支持 hot/warm/cold、memory as managed resource、cooling/reactivation、use-based activation。

它挑战或削弱我们什么: Memory OS 容易走向大平台，且“自进化记忆”与本库 review gate 冲突。

它能细化我们什么: Memory tier 不只是位置，而是 lifecycle state；但 truth confidence 仍独立。

它暴露什么风险: 记忆自动复用会放大错误，跨任务记忆污染尤其危险。

可吸收的 alpha 设计: `memory_lifecycle` 可作为 activation metadata：created, used, cooled, reactivated, deprecated。

不该吸收的部分: 自主 memory write/update、跨 agent shared memory 默认开启、token-saving benchmark claims。

和当前框架融合方式: Use Ledger 驱动 activation lifecycle；Review Queue 决定 truth。

最小优雅吸收版: 在候选讨论中保留 `activation_lifecycle`，不新增 memory OS 子系统。

结论: watch/adapt。

### V3. Graphiti / Zep Temporal Knowledge Graph

资料名称 / 链接: Graphiti / https://github.com/getzep/graphiti ; Zep temporal KG paper / https://arxiv.org/abs/2501.13956

解决什么问题: 为 agent memory 构建 temporal knowledge graph，跟踪事实、关系和上下文随时间变化。

和我们哪一层有关: Connect, Activation, Review Due, Risk。

它支持我们什么: 支持 `review_due`、stale assumptions、relation_state、changing facts 都需要时间维度。

它挑战或削弱我们什么: 自动 fact extraction + temporal graph 如果直接进入 truth layer，会破坏 Evidence-Aware Review。

它能细化我们什么: 关系可以有 `valid_from`、`valid_until`、`observed_at`、`superseded_by`。

它暴露什么风险: 时间图很诱人，但对当前 Markdown vault 可能太重。

可吸收的 alpha 设计: 只吸收 temporal qualifiers 和 stale trigger。

不该吸收的部分: 实时 agent memory graph、自动写图、图数据库依赖。

和当前框架融合方式: Connect 层 relation metadata 与 Risk 的 review_due_reason。

最小优雅吸收版: 对易变判断加 `observed_at` 和 `stale_when`。

结论: adapt。

### V4. Cognee

资料名称 / 链接: Cognee / https://www.cognee.ai/

解决什么问题: 面向 agents 的开源 memory platform：capture context、graph memory、MCP/agent recall、provenance。

和我们哪一层有关: Capture, Connect, Activation, Agent Memory。

它支持我们什么: 支持 capture/model/recall 分层；provenance 与 graph memory 同时保留。

它挑战或削弱我们什么: 它的 agent read/write memory 目标比本库更自动化，容易越过 review gate。

它能细化我们什么: Capture 到 Model 不等于 Review；Model 只是 candidate graph。

它暴露什么风险: “memory that improves”这类产品口径可能把 feedback 与 truth 改写混在一起。

可吸收的 alpha 设计: Capture/Model/Recall 三段可作为对外解释，但要插入 Review gate。

不该吸收的部分: agents 直接写 durable memory。

和当前框架融合方式: `Capture -> Understand -> Review -> Connect` 比 capture/model/recall 更安全。

最小优雅吸收版: 借它的三段语言说明为什么本框架多一个 Review 层。

结论: watch/adapt。

### V5. LangMem

资料名称 / 链接: LangMem / https://github.com/langchain-ai/langmem

解决什么问题: 为 LangGraph agents 提供 long-term memory，包括 conversation extraction、behavior optimization、prompt refinement。

和我们哪一层有关: Use Ledger, Activation, Feedback, Risk。

它支持我们什么: 支持 feedback 可以优化 behavior/prompt/usefulness，而不是直接改 truth。

它挑战或削弱我们什么: Prompt refinement 和 behavior memory 容易隐性改变系统判断边界。

它能细化我们什么: Feedback 分为 behavior feedback、retrieval feedback、truth review input。

它暴露什么风险: agent 行为被记忆自动塑形后，用户很难看见为什么。

可吸收的 alpha 设计: `feedback_event.type = behavior | activation | missing_context | review_due`。

不该吸收的部分: 自动优化 prompt 或长期行为策略。

和当前框架融合方式: FEEDBACK/Use Ledger 只改 activation/usefulness/scope fit。

最小优雅吸收版: 在候选讨论中保留 feedback 分类，不实现 LangMem。

结论: adapt/watch。

### V6. LongMemEval-V2

资料名称 / 链接: LongMemEval-V2 / https://arxiv.org/abs/2605.12493

解决什么问题: 评估 agent memory 是否真正内化环境经验，而不是只记用户历史或短期 trace。

和我们哪一层有关: Use Ledger, Activation, Act and Learn。

它支持我们什么: 支持“行动后的经验”应该影响未来 context pack 和 activation，而不是只保存聊天摘要。

它挑战或削弱我们什么: Benchmark 成绩不能转成本库架构判断。

它能细化我们什么: Use Ledger 可区分 factual memory 与 experience memory。

它暴露什么风险: 经验记忆若未经审查，可能把一次失败泛化成错误规则。

可吸收的 alpha 设计: `experience_memory` 只能作为 scope-fit/usefulness 信号，不能直接生成 reviewed claim。

不该吸收的部分: benchmark-driven memory architecture。

和当前框架融合方式: Act and Learn 后只写 feedback/use event；需要真理更新时进 Review。

最小优雅吸收版: Suggested discussion 中加入“经验记忆是否需要单独字段”。

结论: watch/adapt。

### V7. Graph-Based Agent Memory Survey / Awesome GraphMemory

资料名称 / 链接: Graph-based Agent Memory: Taxonomy, Techniques, and Applications / https://arxiv.org/abs/2602.05665 ; Awesome GraphMemory / https://github.com/DEEP-PolyU/Awesome-GraphMemory

解决什么问题: 总结 graph-based agent memory 的 taxonomy、技术路线和开源资源。

和我们哪一层有关: Connect, Activation, Agent Memory, Risk。

它支持我们什么: 支持 structural memory 和 non-structural memory 分开；knowledge memory 和 experience memory 分开。

它挑战或削弱我们什么: 图记忆生态很热，容易把“有图”误解成“更真”。

它能细化我们什么: Connect 层 reviewed relations 和 Activation 层 graph retrieval 必须分开。

它暴露什么风险: graph extraction 的写入时误判会比 vector search 更隐蔽。

可吸收的 alpha 设计: 给图类资料统一打 `watch: graph_memory_not_truth_graph` 标签。

不该吸收的部分: 追逐图记忆实现框架。

和当前框架融合方式: 作为继续找资料的目录，不作为架构源。

最小优雅吸收版: 报告中保留它为 watchlist 索引。

结论: watch。

### V8. LightRAG

资料名称 / 链接: LightRAG / https://github.com/HKUDS/LightRAG ; paper / https://aclanthology.org/2025.findings-emnlp.568.pdf

解决什么问题: 结合知识图谱和向量检索，提高 RAG 检索效率和多跳关联能力。

和我们哪一层有关: Activation, Connect, Context Pack。

它支持我们什么: 支持 graph + vector 可作为 context discovery；尤其适合从大资料库找候选关系。

它挑战或削弱我们什么: 自动抽取实体/关系不是 reviewed relation。

它能细化我们什么: Context Pack 可以区分 `retrieval_edge` 与 `reviewed_relation`。

它暴露什么风险: 图增强检索会让输出看起来更“知识化”，但仍可能是相关性。

可吸收的 alpha 设计: Graph retrieval output 永远标为 candidate relation/source path。

不该吸收的部分: 直接把 LightRAG graph 当本库 Connect 层。

和当前框架融合方式: 未来只可作为 activation cache，不是 source of truth。

最小优雅吸收版: `retrieval_relation_candidate` 字段。

结论: adapt/watch。

### V9. HippoRAG / EcphoryRAG

资料名称 / 链接: HippoRAG / https://arxiv.org/abs/2405.14831 ; GitHub / https://github.com/OSU-NLP-Group/HippoRAG ; EcphoryRAG / https://arxiv.org/abs/2510.08958

解决什么问题: 用类人长期记忆/关联记忆思想，将 KG、PageRank、多跳检索结合起来。

和我们哪一层有关: Activation, Context Pack, Connect。

它支持我们什么: 支持 activation 不应只靠 top-k semantic similarity；多跳关系和关联路径可以帮助找到冷资料。

它挑战或削弱我们什么: Associative retrieval 更容易产生看似聪明的远距离关联，必须受 evidence gate 限制。

它能细化我们什么: `why_suggested` 可记录 entity hop / relation path，但不叫 support。

它暴露什么风险: 关联路径过长会导致 context drift。

可吸收的 alpha 设计: Cold Reference 可通过 bounded associative hop 进入 briefing。

不该吸收的部分: 神经/海马隐喻作为架构真理、PageRank 分数作为 confidence。

和当前框架融合方式: Activation 层的 candidate surfacing。

最小优雅吸收版: `activation_path` 字段限制跳数并标明 candidate-only。

结论: adapt/watch。

### V10. DeepWiki-Open

资料名称 / 链接: DeepWiki-Open / https://github.com/AsyncFuncAI/deepwiki-open

解决什么问题: 为 GitHub/GitLab/Bitbucket repo 自动生成交互式 wiki，并支持 RAG Ask / DeepResearch。

和我们哪一层有关: Understand, Context Briefing, Source Intake。

它支持我们什么: 支持 repo 级 source digest 可以自动生成 overview、目录、架构图、问答入口。

它挑战或削弱我们什么: 自动生成 wiki 很容易变成“流畅但不可靠”的二手资料。

它能细化我们什么: Repo review 可以有 generated briefing，但必须有 source/code anchors。

它暴露什么风险: Generated docs 如果进入 wiki 正文，会和 reviewed knowledge 混淆。

可吸收的 alpha 设计: 对 repo 资料生成 candidate-only source digest 和 architecture briefing。

不该吸收的部分: 自动 wiki 当作正式 reviewed docs。

和当前框架融合方式: Understand 层辅助，Review 仍按 `templates/library-review.md`。

最小优雅吸收版: `repo_digest.generated=true` 且 `requires_source_anchor=true`。

结论: adapt/watch。

### V11. CodeWiki / RepoDoc / Codebase-Memory

资料名称 / 链接: CodeWiki / https://arxiv.org/abs/2510.24428 ; RepoDoc / https://arxiv.org/abs/2604.26523 ; Codebase-Memory / https://arxiv.org/abs/2603.27277

解决什么问题: 为大型代码库生成 repository-level documentation、RepoKG、增量文档、Tree-Sitter/MCP code graph。

和我们哪一层有关: Understand, Source Intake, Context Pack, Agent Dev Context。

它支持我们什么: 支持“资料库/代码库先生成结构化地图，再按需读源文件”的路线。

它挑战或削弱我们什么: 代码库文档自动化更适合 software repo，不一定适合思想/知识 vault。

它能细化我们什么: 对 repo 资料可以分 hierarchical module map、data flow、call graph、decision context。

它暴露什么风险: Mermaid/diagram/generated docs 会制造视觉权威感。

可吸收的 alpha 设计: `generated_map` 只能作为 briefing，不能作为 evidence。

不该吸收的部分: 自动 Mermaid 架构图写入核心文档。

和当前框架融合方式: Source Intake heavy path 的候选辅助。

最小优雅吸收版: 对复杂 repo 资料输出 `source_map` + `open_questions`，仍要求 source anchors。

结论: watch/adapt。

### V12. Repowise

资料名称 / 链接: Repowise / https://docs.repowise.dev/

解决什么问题: 把 git repository 转成 queryable knowledge graph，并通过 MCP tools 给 coding agents 使用。

和我们哪一层有关: Dev Context, Context Pack, Agent API。

它支持我们什么: 支持 `context pack` 作为 agent-facing API，而不是给 agent 整库写权限。

它挑战或削弱我们什么: Repo code KG 与本库 reviewed knowledge schema 不是一回事。

它能细化我们什么: Agent-facing query tools 应保持只读、可解释、可预算。

它暴露什么风险: MCP tool surface 会扩大安全边界。

可吸收的 alpha 设计: 对未来 API/MCP 只暴露 context/query，不暴露 promotion/write。

不该吸收的部分: 直接接 MCP 写入知识图谱。

和当前框架融合方式: 作为未来 Agent Context Pack API 的参考。

最小优雅吸收版: `read_only_context_tools` 作为候选设计词。

结论: watch/adapt。

### V13. SwarmVault

资料名称 / 链接: SwarmVault / https://github.com/swarmclawai/swarmvault

解决什么问题: Local-first LLM Wiki / knowledge graph / RAG knowledge base / agent memory store，受 Karpathy LLM Wiki 启发。

和我们哪一层有关: Capture, Understand, Connect, Agent Memory。

它支持我们什么: 支持 local-first、raw/source 到 wiki、agent handoff/export、知识图谱与文档并存。

它挑战或削弱我们什么: 其目标覆盖 wiki、RAG、agent memory store，范围比本框架更宽，容易 all-in-one。

它能细化我们什么: Agent export pack 可以作为 Context Pack 的外部发布形态。

它暴露什么风险: persistent chat sessions 和 agent memory 如果写入核心 wiki，会污染 review boundary。

可吸收的 alpha 设计: `export pack` 概念：面向 agent 的只读上下文包，而非开放 vault。

不该吸收的部分: 一体化平台和自动 graph builder。

和当前框架融合方式: 对齐本地 `context-pack-evidence-envelope`，只吸收 export/hand-off 形态。

最小优雅吸收版: 将来 context pack 可导出 `llms.txt` / manifest / source pointer，但不改 truth。

结论: adapt/watch。

### V14. Omnigraph / Git-for-Data Direction

资料名称 / 链接: Omnigraph / https://www.omnigraph.dev/

解决什么问题: 把知识图谱变化做成类似 git 的 branch/merge/source-of-truth 工作流。

和我们哪一层有关: Review Queue, Connect, Change Control。

它支持我们什么: 支持 candidate changes 不应直接改主图，而应像 PR 一样 review/merge。

它挑战或削弱我们什么: 图数据库版本控制对当前 vault 过重。

它能细化我们什么: Point Collision 输出可以视作 patch proposal，而不是 truth mutation。

它暴露什么风险: Branch/merge 隐喻会让知识系统变成工程平台。

可吸收的 alpha 设计: `candidate_change_set` 作为 review input。

不该吸收的部分: Git-like KG backend。

和当前框架融合方式: REVIEW_QUEUE 的候选变更包概念。

最小优雅吸收版: collision report 里列“若采纳，最小需改哪些判断/关系”。

结论: watch/adapt。

## Appendix W: LLM-Wiki / Local-First Agent Memory Frontier (candidate-only)

这一组是最贴近“资料库设计 wiki”的前沿资料：它们不是传统 PKM，而是明确面向 agent 的 local wiki、compiled memory、repo continuity、MCP memory。它们和本项目同频，但风险也最大：越像我们，越容易把自动写入和 reviewed knowledge 混在一起。

### W1. WiCER

资料名称 / 链接: WiCER: Wiki-memory Compile, Evaluate, Refine Iterative Knowledge Compilation for LLM Wiki Systems / https://arxiv.org/abs/2605.07068

解决什么问题: LLM Wiki 把 raw documents 编译成 persistent wiki 时会丢关键事实；WiCER 用 diagnostic probes 找 dropped facts，再迭代 refine。

和我们哪一层有关: Understand, Review Queue, Knowledge Calibration, Risk。

它支持我们什么: 非常支持“source digest / candidate point extraction 不是一次性真理生成”；编译后的 wiki 需要评估、反例、缺失事实检测。

它挑战或削弱我们什么: 它仍然试图自动 refine compiled wiki，本项目不能让 refine 直接写入 reviewed knowledge。

它能细化我们什么: Candidate digest 后应有 `dropped_fact_probe` 或 `missing_point_check`，尤其对长资料和重要 repo。

它暴露什么风险: 摘要/编译会 catastrophic omission；越简洁的 wiki 越可能丢掉边界条件、反例和风险。

可吸收的 alpha 设计: 对 heavy source digest 加“遗漏事实复核”：用问题探针检查 digest 是否丢掉关键 claims、risks、scope limits。

不该吸收的部分: 自动迭代重写 wiki 并视作改进后的真相。

和当前框架融合方式: Understand 产出 candidate digest；WiCER 式 probes 只生成 Review Queue 的 `missing_evidence` / `missing_point`。

最小优雅吸收版: heavy source review 增加一项：`omission_check: what important fact/risk may the digest have dropped?`

结论: adopt as review principle / adapt workflow。

### W2. Retrieval as Reasoning / Agent-Native LLM-Wiki

资料名称 / 链接: Retrieval as Reasoning: Self-Evolving Agent-Native Retrieval via LLM-Wiki / https://arxiv.org/abs/2605.25480

解决什么问题: 把 retrieval 从一次性 top-k fetching 变成 search/read/traverse/判断证据是否足够的 reasoning process。

和我们哪一层有关: Activation, Knowledge Calibration, Context Pack, Evidence-Aware Review。

它支持我们什么: 支持 retrieval 不能只是 similarity；应能遍历索引、读源、发现缺口、判断证据是否足够。

它挑战或削弱我们什么: self-evolving retrieval 若自动更新 wiki，会冲击 review gate。

它能细化我们什么: Context Pack 可以输出 `evidence_sufficiency: sufficient | partial | missing | conflicting`，但这是 action-basis 状态，不是 truth。

它暴露什么风险: “retrieval as reasoning”容易让 agent 自己裁决何时足够，忽略人工 review。

可吸收的 alpha 设计: Context Pack Builder 未来可有 sufficiency checklist：有没有 core source、反例、scope、risk。

不该吸收的部分: 自演化 wiki/retrieval 自动改库。

和当前框架融合方式: Activation/Context Pack 负责找和组织；Review 负责 standing。

最小优雅吸收版: 在 context pack warning 中加入 `evidence_is_partial` / `needs_full_source_read`。

结论: adapt/watch。

### W3. Basic Memory

资料名称 / 链接: Basic Memory / https://basicmemory.com/features ; MCP listing / https://benchgecko.ai/mcp/basic-memory

解决什么问题: Local-first Markdown knowledge management，通过 MCP 让 LLM 与本地 Markdown/semantic graph 交互。

和我们哪一层有关: Capture, Agent Memory, Dev Context, Source of Truth。

它支持我们什么: 支持 local-first、Markdown as inspectable source、MCP access、agent memory 不必放在黑盒云里。

它挑战或削弱我们什么: 它允许 AI read/write local knowledge；本项目必须默认 read-only，写入经 review/用户确认。

它能细化我们什么: Agent-facing 接口应该明确 read path 和 write path，并默认禁写核心 wiki。

它暴露什么风险: 对话驱动写入会把临时偏好、误解、候选结论写成 durable memory。

可吸收的 alpha 设计: local-first + inspectable Markdown + rebuildable semantic graph。

不该吸收的部分: LLM 直接写核心知识库。

和当前框架融合方式: 未来只可借鉴 MCP read tools 或 candidate write queue。

最小优雅吸收版: `agent_write_mode = disabled | candidate_only | approved_core_write`。

结论: adapt/watch。

### W4. Engram

资料名称 / 链接: Engram / https://engram-kb.org/

解决什么问题: 用 Markdown/YAML 作为 source of truth，搜索索引作为 rebuildable cache，并提供 typed graph relations。

和我们哪一层有关: Connect, Activation, Agent API。

它支持我们什么: 非常贴合本项目：Markdown 是源，索引只是缓存；关系是 typed，但仍可由人检查。

它挑战或削弱我们什么: Agent 可 forget/remember，若无 review boundary 仍危险。

它能细化我们什么: `index/cache != truth` 这条可以作为将来实现边界。

它暴露什么风险: typed graph relations 若由 agent 生成，仍只是 candidate relation。

可吸收的 alpha 设计: Rebuildable cache doctrine：任何搜索/图索引都可重建，不拥有 truth。

不该吸收的部分: 直接开放记忆增删给 agent。

和当前框架融合方式: 强化 `incremental-vault-index-retrieval-cache` 和 `derived-relatedness-as-truth-signal` 边界。

最小优雅吸收版: 明确未来所有索引文件都标注 `cache_not_source_of_truth`。

结论: adopt as principle / adapt implementation。

### W5. AICTX Memory

资料名称 / 链接: AICTX Memory / https://memory.aictx.dev/ ; technical overview / https://aictx.org/TECHNICAL_OVERVIEW.html

解决什么问题: 为 coding agents 提供 repo-local continuity，保存产品意图、架构决策、约束、已知坑和下一次 agent 可安全假设的内容。

和我们哪一层有关: Dev Context, Handoff, Context Pack, Act and Learn。

它支持我们什么: 支持“不是更多上下文，而是更好的 continuity artifacts”；与本地 handoff、DEV_CONTEXT、Use Ledger 同频。

它挑战或削弱我们什么: Repo-local continuity 如果不断累积，会变成第二套文档系统。

它能细化我们什么: Handoff/context pack 应区分 stable rules、current work state、known gotchas、open questions。

它暴露什么风险: agent-maintained wiki 会积累 stale assumptions。

可吸收的 alpha 设计: Continuity artifact 必须小、可审查、源链接清楚、可冷却。

不该吸收的部分: 每个项目都启一个独立 agent memory runtime。

和当前框架融合方式: 现有 handoff/DEV_CONTEXT 已覆盖；只吸收“continuity cheaper than rediscovery”的判断标准。

最小优雅吸收版: Context Pack / handoff 增加 `safe_assumptions` 与 `open_questions`。

结论: adapt。

### W6. agentmemory / Local Markdown Memory for Coding Agents

资料名称 / 链接: agentmemory / https://github.com/jayzeng/agentmemory

解决什么问题: 为 Claude Code、Codex、Cursor 等 coding agents 提供 local markdown storage、daily logs、scratchpad 和 semantic search。

和我们哪一层有关: Act and Learn, Dev Context, Use Ledger。

它支持我们什么: 支持 session traces / daily logs / scratchpad 应与 durable knowledge 分开。

它挑战或削弱我们什么: Daily logs 很容易膨胀，且聊天/执行痕迹不是 reviewed knowledge。

它能细化我们什么: Use Ledger 可像 scratchpad/log 一样轻，但必须可冷却、可忽略。

它暴露什么风险: 语义搜索旧日志会把过时 context 拉回热区。

可吸收的 alpha 设计: `scratchpad` 与 `reviewed wiki` 分层。

不该吸收的部分: 长期保存全部 agent logs 作为默认记忆。

和当前框架融合方式: outputs/handoff/feedback 是工作痕迹；wiki 才是 reviewed/candidate 知识结构。

最小优雅吸收版: Agent session outputs 只在必要时生成 candidate points。

结论: watch/adapt。

### W7. PaSaMaster / Self-Evolving Agentic Literature Retrieval

资料名称 / 链接: Towards Self-Evolving Agentic Literature Retrieval / https://arxiv.org/abs/2605.14306

解决什么问题: 把文献检索从一次性 query-ranking 变成 intent analysis、retrieval、ranking、gap refinement 的迭代过程。

和我们哪一层有关: Source Intake, Knowledge Calibration, Review Queue。

它支持我们什么: 支持“找资料”本身可以随着缺口和反证迭代；这和 Point Collision 发现 missing_evidence 很贴。

它挑战或削弱我们什么: self-evolving literature retrieval 可能扩大搜索范围，导致过度调研。

它能细化我们什么: Review Queue 可输出 `followup_search_intent`，而不是只输出结论。

它暴露什么风险: 检索排名不等于采用价值；新资料多不等于更真。

可吸收的 alpha 设计: 当 collision 发现缺口时，生成 targeted follow-up search questions。

不该吸收的部分: 自动持续文献代理。

和当前框架融合方式: 只作为调研窗口的候选方法。

最小优雅吸收版: Suggested Next Discussion 加“哪些缺口值得下一轮定向检索？”

结论: adapt/watch。

### W8. Agent-as-a-Graph

资料名称 / 链接: Agent-as-a-Graph: Knowledge Graph-Based Tool and Agent Retrieval for LLM Multi-Agent Systems / https://arxiv.org/abs/2511.18194

解决什么问题: 把 tools 和 agents 表示成知识图谱节点/边，用图检索选择合适工具/agent。

和我们哪一层有关: Act and Learn, Dev Context, Tool/Agent Routing。

它支持我们什么: 支持“哪个 agent/tool 适合当前任务”也可以是可解释的 routing，而不是靠隐性 prompt。

它挑战或削弱我们什么: 多 agent/tool graph 对当前资料库主线偏远，容易过早平台化。

它能细化我们什么: 未来子 agent 分工可记录 `agent_role`、`capability`、`evidence_limit`。

它暴露什么风险: agent graph 如果能写知识库，安全边界扩大。

可吸收的 alpha 设计: 子 agent 只产 candidate findings；主 agent 汇总并保留 source links。

不该吸收的部分: 多 agent routing graph 系统。

和当前框架融合方式: 仅作为调研协作模式参考。

最小优雅吸收版: 调研报告中标明资料来源线，而不是保存 agent graph。

结论: watch。

## Appendix X: Scientific Literature / Evidence-Table Assistants (candidate-only)

这一组不是“个人第二大脑”，而是更接近 evidence synthesis。它们对本项目的价值在于：如何把搜索、筛选、抽取、引用图谱、证据表和反证发现做成可复核流程。

### X1. PaperQA2

资料名称 / 链接: Future House PaperQA / https://github.com/Future-House/paper-qa ; Language agents achieve superhuman synthesis of scientific knowledge / https://arxiv.org/abs/2409.13740

解决什么问题: 面向科学文献的高准确 RAG/agent，强调带引用回答、文献综合和 benchmark-driven factuality。

和我们哪一层有关: Source Intake, Evidence-Aware Review, Context Pack。

它支持我们什么: 支持科学/论文资料不该只做摘要，而应生成 question-specific evidence with citations。

它挑战或削弱我们什么: “agent synthesis 超过专家”这类结论不能迁移到本库架构判断。

它能细化我们什么: 对论文/文献 review 可以区分 answer、citations、contradictions、uncertainty。

它暴露什么风险: 高性能研究 agent 仍可能把领域问题缩成问答，不覆盖系统架构适配性。

可吸收的 alpha 设计: Paper review 输出可以有 `answer_claims` + `supporting_papers` + `contradictions_found`。

不该吸收的部分: 自动文献综述替代 Evidence-Aware Review。

和当前框架融合方式: 作为 heavy paper intake 的候选参考；输出仍是 candidate points。

最小优雅吸收版: 对论文资料加入“是否发现反对/不一致文献？”一项。

结论: adapt/watch。

### X2. Elicit Systematic Review

资料名称 / 链接: Elicit Systematic Review / https://blog.elicit.com/systematic-review/ ; Evaluation / https://blog.elicit.com/how-we-evaluated-elicit-systematic-review/

解决什么问题: 支持文献搜索、标题摘要筛选、全文数据抽取和 evidence table。

和我们哪一层有关: Capture, Source Intake, Evidence-Aware Review。

它支持我们什么: 支持“筛选/抽取/表格化证据”是 review workflow 的核心环节。

它挑战或削弱我们什么: 速度提升不等于判断质量；AI extraction 仍需人工复核。

它能细化我们什么: Review Queue 可保留 `screened_in` / `screened_out` / `extraction_caveat`。

它暴露什么风险: 自动抽取变量错误会直接污染后续判断。

可吸收的 alpha 设计: 对 heavy source review，记录纳入/排除与 extraction uncertainty。

不该吸收的部分: 自动 systematic review 作为本库默认流程。

和当前框架融合方式: 仅在重要研究窗口作为方法参考。

最小优雅吸收版: `source_screening_note` + `extraction_uncertainty`。

结论: adapt/watch。

### X3. OpenAlex

资料名称 / 链接: OpenAlex / https://explore.openalex.org/ ; OpenAlex paper / https://arxiv.org/abs/2205.01833

解决什么问题: 开放的全球研究系统目录，提供 works/authors/venues/institutions/concepts/citations 等 API 与数据。

和我们哪一层有关: Source Discovery, Provenance, Connect。

它支持我们什么: 支持文献 discovery 和 citation graph 可以帮助找到相关/反对/后续资料。

它挑战或削弱我们什么: Citation graph 是 scholarly relation，不是 evidence support。

它能细化我们什么: 文献资料可记录 `citation_context` 但不等于支持关系。

它暴露什么风险: 数据源分类差异、元数据错误、引用动机不明。

可吸收的 alpha 设计: 用开放学术图谱辅助 follow-up search，不写入 truth。

不该吸收的部分: 引用次数/图中心性作为 confidence。

和当前框架融合方式: Source Intake 的 discovery layer。

最小优雅吸收版: `found_via: OpenAlex/SemanticScholar/etc` 和 `citation_graph_note`。

结论: adapt/watch。

### X4. Semantic Scholar Academic Graph

资料名称 / 链接: Semantic Scholar API / https://www.semanticscholar.org/product/api ; The Semantic Scholar Open Data Platform / https://arxiv.org/abs/2301.10140

解决什么问题: 大规模论文、作者、引用、嵌入、数据集和推荐 API，支持学术图谱探索。

和我们哪一层有关: Source Discovery, Capture, Source Hygiene。

它支持我们什么: 支持系统化找文献，避免只靠搜索引擎和热门博客。

它挑战或削弱我们什么: 推荐/相似论文会强化相关性偏差，不保证找到反证。

它能细化我们什么: follow-up search 可区分 keyword search、citation expansion、recommendation expansion。

它暴露什么风险: 学术图谱覆盖不均、metadata 抽取错误、推荐偏向。

可吸收的 alpha 设计: 文献检索记录 `search_strategy` 和 `coverage_caveat`。

不该吸收的部分: Semantic Scholar score / recommendation 直接影响 review confidence。

和当前框架融合方式: Source Intake 的候选 discovery source。

最小优雅吸收版: 在调研报告里记录“从哪里找的”和“为什么认为覆盖还不完整”。

结论: adapt。

### X5. Scite Smart Citations

资料名称 / 链接: scite: A smart citation index / https://direct.mit.edu/qss/article/2/3/882/102990/scite-A-smart-citation-index-that-displays-the ; Scite overview / https://scite.org/

解决什么问题: 显示 citation statement / citation context，并将引用分类为 supporting、contrasting 或 mentioning。

和我们哪一层有关: Evidence-Aware Review, Connect, Source Discovery。

它支持我们什么: 非常支持“citation != support”；一个引用可以只是 mention，也可能是 contrast。

它挑战或削弱我们什么: 自动分类会误判，不能把 Scite label 当最终证据关系。

它能细化我们什么: `citation_role` 和 `evidence_relation` 应分开；citation role 只是 review input。

它暴露什么风险: 研究者可能看到 supporting 数字就提高 confidence，忽略具体引用上下文。

可吸收的 alpha 设计: 引用关系最小三类：mentions / supports / contrasts，并要求保留 citation context。

不该吸收的部分: 用 supporting/contrasting 计数给 confidence 加分。

和当前框架融合方式: Connect 层可借鉴 `relation_state`，但 promotion 仍需 review。

最小优雅吸收版: 文献型 Evidence Packet 加 `citation_context` 和 `citation_role_candidate`。

结论: adapt。

### X6. Semantic Scholar Citation Intent

资料名称 / 链接: Semantic Scholar Citation Intent / https://webflow.semanticscholar.org/faq/citation-intent

解决什么问题: 将 citation intent 分为 background、method、result extension 等类型，帮助理解引用用途。

和我们哪一层有关: Source Discovery, Evidence-Aware Review。

它支持我们什么: 支持引用用途要拆开；background citation 通常不能当直接支持。

它挑战或削弱我们什么: citation intent 覆盖受 full text 可得性限制，也不等于 evidence relation。

它能细化我们什么: 文献 review 中可记录 `citation_intent_candidate`。

它暴露什么风险: 引用意图是作者写作功能，不一定等价于支持/反对判断。

可吸收的 alpha 设计: 对关键论文引用，问“它是在铺背景、借方法，还是扩展结果？”

不该吸收的部分: intent 自动分类进入 truth。

和当前框架融合方式: Heavy paper intake 的辅助字段。

最小优雅吸收版: `citation_intent_note`。

结论: adapt/watch。

### X7. SciFact / Scientific Claim Verification

资料名称 / 链接: SciFact: Verifying Scientific Claims / https://aclanthology.org/2020.emnlp-main.609.pdf ; SciFact-Open / https://arxiv.org/abs/2210.13777

解决什么问题: 专门针对科学 claim 的 evidence retrieval 和 support/refute/insufficient verification。

和我们哪一层有关: Understand, Evidence-Aware Review, Knowledge Calibration。

它支持我们什么: 支持 scientific/source-heavy 判断要 claim-level 验证，而不是 paper-level 摘要。

它挑战或削弱我们什么: SciFact 多基于摘要或有限语料，不能代表完整证据综合。

它能细化我们什么: Paper digest 可拆为 claim -> candidate evidence abstract/sentence -> label。

它暴露什么风险: 只看 abstract 会漏掉方法限制、表格、补充材料。

可吸收的 alpha 设计: 对科学/论文类资料采用 `support/refute/not_enough_information` 三分法作为候选输入。

不该吸收的部分: benchmark label 直接移植成 review conclusion。

和当前框架融合方式: Evidence-Aware Review 的资料型参考。

最小优雅吸收版: 论文 review 加 `claim_verification_label_candidate`。

结论: adapt。

### X8. DeepSciVerify / Claim-Citation Alignment

资料名称 / 链接: DeepSciVerify / https://arxiv.org/abs/2605.27710

解决什么问题: 科学 claim-citation verification：先做 abstract-level reasoning，必要时升级到 passage-level evidence。

和我们哪一层有关: Evidence-Aware Review, Source Intake, Context Pack。

它支持我们什么: 支持“逐步升级证据粒度”：不是每个问题都 full-text，但关键/不确定时要升级。

它挑战或削弱我们什么: 最新论文，尚需进一步复核；自动 evidence escalation 仍可能错。

它能细化我们什么: Review 可以有 `evidence_escalation_needed`：abstract enough / passage needed / full source needed。

它暴露什么风险: 只在模型认为需要时升级，可能漏掉隐藏反证。

可吸收的 alpha 设计: Evidence Packet 的 source granularity：metadata -> abstract -> passage -> full source。

不该吸收的部分: 自动 claim-citation verifier 作为 judge。

和当前框架融合方式: Source Intake heavy path 的候选升级策略。

最小优雅吸收版: `evidence_granularity` 字段。

结论: watch/adapt。

### X9. Crossmark / Crossref Update Signals

资料名称 / 链接: Crossmark / https://www.crossref.org/services/crossmark/ ; Crossref relations / https://www.crossref.org/documentation/schema-library/markup-guide-metadata-segments/relations/

解决什么问题: 给 scholarly content 提供更新、修正、撤稿、版本和关系 metadata。

和我们哪一层有关: Review Due, Source Hygiene, Risk/Inhibition。

它支持我们什么: 支持 review_due 不只是日期，而应由 correction、retraction、new version、related work 触发。

它挑战或削弱我们什么: Metadata 不完整，且不同出版商更新质量不一。

它能细化我们什么: `source_version_change` 和 `correction_or_retraction` 可作为 review_due_reason。

它暴露什么风险: 旧 PDF/快照可能仍被引用，而 live source 已更新。

可吸收的 alpha 设计: 对关键论文 source record 记录 `checked_for_updates_at` 和 `update_signal`。

不该吸收的部分: 自动周期性检查所有论文。

和当前框架融合方式: Risk/Inhibition 的 stale source trigger。

最小优雅吸收版: high-impact paper 加 `update_status: unknown | checked_no_update | correction | retraction | new_version`。

结论: adapt。

### X10. Retraction Watch / PubMed Retraction Metadata

资料名称 / 链接: Retraction Watch Database / https://retractionwatch.com/retraction-watch-database-user-guide/ ; PubMed retracted publication type / https://pubmed.ncbi.nlm.nih.gov/help/

解决什么问题: 标识撤稿、retraction notice、erratum、expression of concern 等学术风险信号。

和我们哪一层有关: Review Due, Risk, Source Hygiene。

它支持我们什么: 支持 negative evidence / source hygiene 需要包含 publication-status risk。

它挑战或削弱我们什么: 撤稿数据库覆盖和时效不同，不能只靠一个来源。

它能细化我们什么: 对论文 evidence item 增加 `publication_status_warning`。

它暴露什么风险: 被撤稿的论文若已进入 reviewed knowledge，会污染后续 action basis。

可吸收的 alpha 设计: high-impact paper review 时检查 retraction/correction 状态。

不该吸收的部分: 对所有低风险 source 强制查撤稿。

和当前框架融合方式: Review Due trigger；撤稿信号产生 review input，不自动删除旧判断。

最小优雅吸收版: `review_due_reason: correction_or_retraction_signal`。

结论: adapt。

## Appendix Y: Closeout Status (candidate-only)

Closeout time noted: 2026-05-29 04:49 Asia/Shanghai.

已完成:

- 已按本地 v0.2 主线和最新 `wiki/` 设计边界对齐，不推翻 `Capture -> Understand -> Review -> Connect -> Act and Learn`。
- 已覆盖 classic AI / argumentation / claim verification / provenance / PKM / agent memory / RAG / KG / source hygiene / LLM-Wiki frontier / scientific evidence assistant 等资料线。
- 已把每个资料按 candidate-only 方式分析，保留链接、对应层、支持/挑战/细化/风险、最小吸收版和 adopt/adapt/watch/reject 判断。
- 已回填 Executive Summary、Candidate References frontier addendum、Strongest Alpha Ideas、Appendix absorption map。
- 已标明本地 wiki 对齐结论：dashboard / index / briefing / context pack 是 activation/loading surface，不是 truth layer。

未完成/保留:

- 没有把任何候选写入 README、FUSION、SCHEMA、REVIEW_QUEUE、AGENTS、handoff 等核心文档。
- 没有把外部资料升级成 reviewed knowledge。
- 没有 clone / download / run external repos，也没有跑项目脚本。
- 没有 commit / push。

后续建议:

- 下一轮人工讨论优先看 10 个 Suggested Next Discussion 问题。
- 最值得深看的前沿资料是 WiCER、Retrieval as Reasoning、Engram、Context Engineering Survey、Scite/SciFact/DeepSciVerify。
- 最该谨慎的方向是 self-evolving wiki、agent memory writeback、graph/RAG/index cache 直接拥有 truth。

#### 26. Neo4j Agent Memory

资料名称 / 链接: Neo4j Agent Memory / https://neo4j.com/labs/agent-memory/

解决什么问题: agent 需要短期对话、长期实体/事实、reasoning trace 的统一 memory graph。

和我们哪一层有关: Activation, Context Pack, Use Ledger。

它支持我们什么: 支持 memory layer 分层，以及 reasoning trace 不等于 knowledge truth。

它挑战或削弱我们什么: graph-native memory 容易把 agent-learned fact 直接混入 reviewed knowledge。

它能细化我们什么: `message/entity/reasoning_trace/tool_call -> touched reviewed node` 的 use trace。

它暴露什么风险: 多 agent 共享记忆时污染会扩散。

可吸收的 alpha 设计: agent memory 分层：session memory / project activation / reviewed memory / reasoning trace。

不该吸收的部分: POLE+O core、auto preference learning 写入 truth、Neo4j runtime dependency。

和当前框架融合方式: Agent memory 只能读 reviewed context 或写 candidate/feedback-event。

最小优雅吸收版: Use Ledger 记录 reasoning trace 与 touched nodes，但不把 trace 当 relation。

结论: adapt。

#### 27. TrustGraph

资料名称 / 链接: TrustGraph / https://docs.trustgraph.ai/

解决什么问题: GraphRAG/agent intelligence 平台需要 provenance 和 retrieval trace。

和我们哪一层有关: Activation, Context Pack, Use Ledger。

它支持我们什么: 支持 query-time reasoning trace、source-to-edge provenance、retrieval graph。

它挑战或削弱我们什么: 平台化 GraphRAG 很重，会扩大本库 MVP。

它能细化我们什么: `retrieved / selected / used / ignored / reason`。

它暴露什么风险: GraphRAG 的 trace 仍是 retrieval/process trace，不是 truth evidence 本身。

可吸收的 alpha 设计: Context Pack 的 trace schema。

不该吸收的部分: full platform, ingestion pipeline, always-on graph infrastructure。

和当前框架融合方式: Act and Learn 记录 action basis 和 retrieval decision。

最小优雅吸收版: Use Ledger 增加 selected/used/ignored evidence 状态。

结论: adapt。

#### 28. OriginTrail DKG

资料名称 / 链接: OriginTrail DKG / https://docs.origintrail.io/

解决什么问题: 对外部知识资产做可验证、可追溯、可引用的发布和 provenance。

和我们哪一层有关: Source Hygiene, External Publishing。

它支持我们什么: 支持 source identity、digest、tamper-evident provenance 对未来发布有价值。

它挑战或削弱我们什么: 区块链/去中心化知识图谱完全超出当前本地 vault MVP。

它能细化我们什么: high-value export 可以考虑 source digest 和 content hash。

它暴露什么风险: verifiable existence 不等于内容为真。

可吸收的 alpha 设计: 对重要外部发布 artifact 记录 checksum/source identity。

不该吸收的部分: DKG runtime、token/chain dependency、public trust layer。

和当前框架融合方式: 仅作为未来 products/export provenance 的 watch reference。

最小优雅吸收版: 在 source snapshot 中保留 content hash，不引入链。

结论: watch。

#### 29. A-MEM

资料名称 / 链接: A-MEM / https://arxiv.org/abs/2502.12110

解决什么问题: LLM agent memory 不应只是 flat retrieval，而应动态组织和连接历史记忆。

和我们哪一层有关: Activation, Knowledge Calibration, Use Ledger。

它支持我们什么: 支持新 memory 与旧 memory 的 candidate linking。

它挑战或削弱我们什么: 它的 memory evolution 可能自动修改旧 memory representation，这与 reviewed truth gate 冲突。

它能细化我们什么: `possible_related_points` 和 `candidate_relation` 可进入 calibration。

它暴露什么风险: agent 自我重写 memory 可能带来 memory drift。

可吸收的 alpha 设计: 新 candidate 进入时提出可能相关点，而不是更新旧点。

不该吸收的部分: 自动 memory evolution、自动重写历史 memory、performance benchmark-driven design。

和当前框架融合方式: 只用作 Activation/Calibration 的候选召回，不碰 reviewed notes。

最小优雅吸收版: Candidate point 附 `suggested_collisions`，人工 review 决定。

结论: adapt with caution。

#### 30. Graphiti / Zep

资料名称 / 链接: Graphiti / Zep temporal KG / https://github.com/getzep/graphiti

解决什么问题: agent memory 中事实会随时间变化，需要 temporal validity 和 provenance。

和我们哪一层有关: Activation, Review Due, Use Ledger。

它支持我们什么: 支持 reviewed knowledge 不该只有 timeless fact，也要知道 valid time 和 source episode。

它挑战或削弱我们什么: temporal KG engine 对本库当前过重。

它能细化我们什么: `valid_from`, `valid_until`, `observed_at`, `review_due_reason`。

它暴露什么风险: 自动 temporal fact extraction 会产生错误关系。

可吸收的 alpha 设计: time-aware activation and stale detection。

不该吸收的部分: temporal graph database runtime、automatic fact merge。

和当前框架融合方式: Review_due 可由 source version/date/action failure 触发。

最小优雅吸收版: 对易过时判断记录 `validity` 和 `stale_signal`。

结论: adapt/watch。

#### 31. Mem0 / OpenMemory

资料名称 / 链接: Mem0 / OpenMemory / https://github.com/mem0ai/mem0

解决什么问题: 给 agent 提供跨会话、跨工具的长期记忆。

和我们哪一层有关: Activation, Agent Memory, Dev Context。

它支持我们什么: 支持 memory as service / MCP memory 的现实需求。

它挑战或削弱我们什么: persistent memory 如果默认可写，会成为污染源。

它能细化我们什么: `memory_type: preference | implementation | project_context | candidate | feedback_event`。

它暴露什么风险: memory poisoning、过期偏好、跨项目泄漏。

可吸收的 alpha 设计: agent memory write 默认 quarantine，必须有 source/hash/review status。

不该吸收的部分: agent 自动记忆、自动 personalization 写入核心 truth。

和当前框架融合方式: Future agent access 只能写 candidate/feedback，不写 reviewed knowledge。

最小优雅吸收版: Agent memory outputs 必须标记 source、scope、ttl/review_due。

结论: watch/adapt。

#### 32. Letta / MemGPT Memory Architecture

资料名称 / 链接: Letta / MemGPT memory architecture / https://docs.letta.com/guides/agents/architectures/memgpt

解决什么问题: 区分 core memory 和 archival memory，处理 context window 限制。

和我们哪一层有关: Activation, Dev Context, Context Pack。

它支持我们什么: 支持 hot/warm/cold、Core/Support/Risk/Cold References 的 activation 分层。

它挑战或削弱我们什么: agent self-editing memory 不适合直接进入 reviewed truth。

它能细化我们什么: `core context` 和 `archival reference` 的输出边界。

它暴露什么风险: always-in-context memory 容易把旧假设长期激活。

可吸收的 alpha 设计: Context Pack 明确区分 core、support、risk、cold refs。

不该吸收的部分: self-editing core memory、autonomous memory management。

和当前框架融合方式: DEV_CONTEXT 是临时 working set，不是 truth；activation tier 不等于 confidence。

最小优雅吸收版: Context Pack 输出时注明每条材料的 activation role。

结论: adapt。

#### 33. NIST AI RMF

资料名称 / 链接: NIST AI Risk Management Framework Core / https://airc.nist.gov/airmf-resources/airmf/5-sec-core/

解决什么问题: 风险管理不能只做事后检查，而要横切设计、测量、管理。

和我们哪一层有关: Risk/Inhibition across all layers。

它支持我们什么: 支持本库“Risk / Inhibition 是 cross-cutting”的设计。

它挑战或削弱我们什么: 完整治理框架会过重，不适合个人/轻量 vault。

它能细化我们什么: 每层都可以有同一组轻字段：risk, scope, mitigation, review_due。

它暴露什么风险: 风险标签过多会变成官僚 checklist。

可吸收的 alpha 设计: `risk_gate` as small cross-cutting metadata。

不该吸收的部分: 完整 RMF governance process、组织级角色矩阵。

和当前框架融合方式: Capture/Understand/Review/Connect/Act 都只保留轻量 risk signal。

最小优雅吸收版: Review 中记录 `risk_flags` 和 `mitigation_note`。

结论: adapt。

#### 34. NCSC Prompt Injection Boundary

资料名称 / 链接: NCSC, "Prompt injection is not SQL injection" / https://www.ncsc.gov.uk/blog-post/prompt-injection-is-not-sql-injection

解决什么问题: LLM 无法可靠区分 data 和 instruction，prompt 不是安全边界。

和我们哪一层有关: Agent Access, Risk/Inhibition, Capture。

它支持我们什么: 支持外部内容进入后必须降权，不能让模型自己判断安全边界。

它挑战或削弱我们什么: 任何“让 agent 自动读资料并写 truth”的路线都必须非常受限。

它能细化我们什么: `untrusted_external_content` 和 deterministic gate。

它暴露什么风险: 间接 prompt injection 可以通过网页、论文、issue、README、评论进入。

可吸收的 alpha 设计: 外部来源内容默认 untrusted；高风险动作必须 deterministic approval gate。

不该吸收的部分: 只靠 prompt 规则做防护。

和当前框架融合方式: Source Intake 可以读外部资料；写 reviewed knowledge 或执行 action 必须走人工 review。

最小优雅吸收版: Agent Access 文档未来加一句：外部内容不能提升权限，只能降低信任。

结论: adopt boundary。

#### 35. OWASP Agentic AI Threats / Memory Guard

资料名称 / 链接: OWASP Agentic AI Threats / https://genai.owasp.org/resource/agentic-ai-threats-and-mitigations/ ; Agent Memory Guard / https://github.com/OWASP/www-project-agent-memory-guard

解决什么问题: agent 的 excessive agency、tool misuse、memory poisoning 等风险需要明确标签。

和我们哪一层有关: Risk/Inhibition, Agent Memory, Agent Access。

它支持我们什么: 支持 agent memory 是可写攻击面，必须 quarantine。

它挑战或削弱我们什么: 过早引入安全平台会拖慢架构主线。

它能细化我们什么: `agent_risk_tags: prompt_injection | excessive_agency | tool_misuse | memory_poisoning | context_leak`。

它暴露什么风险: 记忆污染可跨会话生效，比一次错误回答更危险。

可吸收的 alpha 设计: memory writes need source, hash/snapshot, scope, rollback/review status。

不该吸收的部分: 完整 OWASP tooling、中间件、防护系统。

和当前框架融合方式: Future agent write lane 只能产 candidate/feedback-event，不直写 reviewed truth。

最小优雅吸收版: 对 agent 产生的记忆标 `agent_generated_candidate` 和 `requires_review`。

结论: adapt。

#### 36. MCP Security Best Practices

资料名称 / 链接: MCP Security Best Practices / https://modelcontextprotocol.io/docs/tutorials/security/security_best_practices

解决什么问题: MCP/tool 系统容易出现权限膨胀、confused deputy、scope 混乱。

和我们哪一层有关: Agent Access, Act and Learn, Risk。

它支持我们什么: 支持 read-only default、least privilege、progressive scope。

它挑战或削弱我们什么: 如果未来 tool access 便利化，会冲击当前 review/execute 边界。

它能细化我们什么: scope 分 path/surface/tool/action type。

它暴露什么风险: 一个有权限的 agent 可被低信任内容诱导去做高权限动作。

可吸收的 alpha 设计: `access_scope: read | write_candidate | write_reviewed | execute | publish`。

不该吸收的部分: MCP-specific architecture before agent layer exists。

和当前框架融合方式: 只作为未来 Agent Access 边界，当前不启动自动化。

最小优雅吸收版: 默认 read-only，任何 write/execute/publish 都记录 approval source。

结论: adapt。

#### 37. W3C Web Annotation Data Model

资料名称 / 链接: Web Annotation Data Model / https://www.w3.org/TR/annotation-model/

解决什么问题: 网页/文档里的引用片段需要 stable selector，否则以后难复核。

和我们哪一层有关: Capture, Source Hygiene, Review。

它支持我们什么: 支持 exact quote + prefix/suffix + text position 的 source anchor。

它挑战或削弱我们什么: 完整 annotation JSON-LD 过重。

它能细化我们什么: `quote_exact`, `quote_prefix`, `quote_suffix`, `position_start`, `position_end`。

它暴露什么风险: 只有 URL 没有 quote/position，网页更新后 review 无法复现。

可吸收的 alpha 设计: source anchor mini-profile。

不该吸收的部分: full W3C annotation serialization。

和当前框架融合方式: Evidence item 保存可复核 anchor。

最小优雅吸收版: 高价值网页摘录保存 exact quote + prefix/suffix。

结论: adapt。

#### 38. Memento RFC 7089

资料名称 / 链接: Memento RFC 7089 / https://datatracker.ietf.org/doc/html/rfc7089

解决什么问题: Web 资源会随时间变化，需要按时间访问旧状态。

和我们哪一层有关: Source Hygiene, Review Due。

它支持我们什么: 支持 `captured_at`, `archived_url`, `checked_latest_at`, `source_changed`。

它挑战或削弱我们什么: Memento 生态和 archive availability 不能保证所有资源可恢复。

它能细化我们什么: source drift 触发 review_due。

它暴露什么风险: 旧判断可能基于旧网页版本；新网页版本不能自动替换旧证据。

可吸收的 alpha 设计: source version awareness。

不该吸收的部分: TimeGate/TimeMap protocol integration。

和当前框架融合方式: Source record 记录 capture time；Review_due 由 source changed 触发。

最小优雅吸收版: 网页 evidence item 必填 `captured_at`，可选 `archived_url`。

结论: adapt。

#### 39. Cochrane Review Updating

资料名称 / 链接: Cochrane, Updating a review / https://www.cochrane.org/node/93

解决什么问题: review 更新不只是到期提醒，还要看新数据、新方法、新分析、评论、修正/撤稿。

和我们哪一层有关: Review Due, Risk/Inhibition。

它支持我们什么: 支持 `review_due_when` 作为触发条件集合。

它挑战或削弱我们什么: 医学系统综述流程太重，不能直接套。

它能细化我们什么: `new_primary_source | contradiction | correction | retraction | version_change | action_failure | missed_feedback`。

它暴露什么风险: 仅按日期复查会产生噪声；仅有新资料也不一定需要改结论。

可吸收的 alpha 设计: trigger-based review_due。

不该吸收的部分: systematic review workflow、GRADE-like heavy evaluation。

和当前框架融合方式: Feedback 不改 truth，但 action failure 可触发 review_due。

最小优雅吸收版: reviewed note 可选 `review_due_when`。

结论: adapt。

#### 40. SLSA Provenance / OpenSSF Scorecard

资料名称 / 链接: SLSA Provenance / https://slsa.dev/spec/v1.0-rc1/provenance ; OpenSSF Scorecard / https://github.com/ossf/scorecard

解决什么问题: repo/source quality 不能只看 star、README 或营销文案。

和我们哪一层有关: Source Hygiene, Repo Review。

它支持我们什么: 支持 repo review 记录 commit、release age、CI/test signal、security policy、dependency/update signal。

它挑战或削弱我们什么: 分数和 provenance 仍不能证明设计适合本库。

它能细化我们什么: repo source record 的 hygiene warning。

它暴露什么风险: repo health 低说明风险高，但 repo health 高也不代表架构 alpha 值高。

可吸收的 alpha 设计: `repo_hygiene_warnings`。

不该吸收的部分: 自动 score gate、supply-chain attestation pipeline。

和当前框架融合方式: REFERENCE_REVIEW_PROTOCOL 中可作为 warning，不作为 adoption 决策本身。

最小优雅吸收版: repo review 记录 `commit_or_version`, `last_release`, `tests_or_ci_signal`, `security_policy`.

结论: adapt。

#### 41. Argdown / Cytoscape.js

资料名称 / 链接: Argdown / https://argdown.org/syntax/ ; Cytoscape.js / https://js.cytoscape.org/

解决什么问题: 支持/反对/冲突如果只写正文，不够可见。

和我们哪一层有关: Connect, Evidence-Aware Review, Workbench。

它支持我们什么: 支持局部 argument map / point cluster visualization。

它挑战或削弱我们什么: 全库大图谱会变成产品工程和维护负担。

它能细化我们什么: `supports`, `contradicts`, `refines`, `risk_of` 的局部展示。

它暴露什么风险: 可视化边不等于 reviewed relation；图很容易产生权威感。

可吸收的 alpha 设计: 只渲染当前 point cluster，不做全库图谱产品。

不该吸收的部分: 图谱编辑器、自动 argument parsing、全库可视化。

和当前框架融合方式: Review 时作为局部认知辅助。

最小优雅吸收版: 对一个 claim 展示支持/反对/范围限制/风险四列，而不是上图。

结论: adapt/watch。

