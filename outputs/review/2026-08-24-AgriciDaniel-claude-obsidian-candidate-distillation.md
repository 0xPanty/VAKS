---
record_kind: candidate_distillation
status: candidate
provisional: true
knowledge_status: candidate
processing_tier: heavy
lifecycle_state: candidate_provisional
overlay_state: confirmed
review_pressure: none
source_ref: raw/repos/2026-08-24-AgriciDaniel-claude-obsidian-source.md
derived_from:
  - raw/repos/2026-08-24-AgriciDaniel-claude-obsidian-source.md
  - raw/repos/_snapshots/2026-08-24-AgriciDaniel-claude-obsidian-1c1bc49-source.zip
  - wiki/summaries/2026-08-24-AgriciDaniel-claude-obsidian-architecture-review.md
retrieval_policy:
  policy_kind: orientation_only
  pack_allowed: activation_only
  action_basis_allowed: false
  warning_code: candidate_not_action_basis
promotion_gate: v0_2_13_required
action_basis_allowed: false
truth_mutation_allowed: false
v0_2_13_trigger: no
routing_hint:
  - source-capture
  - execution-integrity
  - operation-receipt
  - evidence-maintenance-lint
  - retrieval-cache-integrity
  - agent-tool-safety
possible_project_refs:
  - verified-action-knowledge-system
source_annotation_refs:
  - outputs/review/source_annotations/2026-08-24-AgriciDaniel-claude-obsidian/vault-bound-plan-approval.md
  - outputs/review/source_annotations/2026-08-24-AgriciDaniel-claude-obsidian/single-writer-operation-transaction.md
  - outputs/review/source_annotations/2026-08-24-AgriciDaniel-claude-obsidian/operation-type-write-authority.md
  - outputs/review/source_annotations/2026-08-24-AgriciDaniel-claude-obsidian/content-addressed-capture.md
  - outputs/review/source_annotations/2026-08-24-AgriciDaniel-claude-obsidian/provenance-ledger-separation.md
  - outputs/review/source_annotations/2026-08-24-AgriciDaniel-claude-obsidian/claim-support-validator-ceiling.md
  - outputs/review/source_annotations/2026-08-24-AgriciDaniel-claude-obsidian/hot-context-opt-in-boundary.md
  - outputs/review/source_annotations/2026-08-24-AgriciDaniel-claude-obsidian/retrieval-authority-gap.md
  - outputs/review/source_annotations/2026-08-24-AgriciDaniel-claude-obsidian/external-egress-inert-plan.md
  - outputs/review/source_annotations/2026-08-24-AgriciDaniel-claude-obsidian/release-clean-snapshot-boundary.md
  - outputs/review/source_annotations/2026-08-24-AgriciDaniel-claude-obsidian/native-windows-fail-closed.md
  - outputs/review/source_annotations/2026-08-24-AgriciDaniel-claude-obsidian/research-dossier-canonical-merge-split.md
point_anchor_refs:
  - snapshot_ref: raw/repos/_snapshots/2026-08-24-AgriciDaniel-claude-obsidian-1c1bc49-source.zip
    selector_type: file_line
    selector_value: claude_obsidian/transaction.py:1287-1308
  - snapshot_ref: raw/repos/_snapshots/2026-08-24-AgriciDaniel-claude-obsidian-1c1bc49-source.zip
    selector_type: file_line
    selector_value: claude_obsidian/transaction.py:3130-3235
  - snapshot_ref: raw/repos/_snapshots/2026-08-24-AgriciDaniel-claude-obsidian-1c1bc49-source.zip
    selector_type: file_line
    selector_value: claude_obsidian/capture.py:908-1029
  - snapshot_ref: raw/repos/_snapshots/2026-08-24-AgriciDaniel-claude-obsidian-1c1bc49-source.zip
    selector_type: file_line
    selector_value: claude_obsidian/ledgers.py:1030-1150
borrow_value: strong
borrow_order:
  - "P1: future binding between VAKS authority receipts and vault/bytes/modes execution plans"
  - "P2: immutable content-addressed capture plus operation-scoped single-writer recovery"
  - "P3: source-independence lint, derived-cache integrity, inert egress and bounded untrusted context"
dev_context_hint:
  default_layer: support_with_required_risk
  core_only_when: "An explicitly authorized VAKS task is designing a multi-file writer, action executor, content-addressed capture adapter, or approval-bound operation transaction."
  support_when: "Reviewing source deduplication, evidence independence, retrieval cache integrity, capability contracts, bounded context injection, or release/export hygiene."
  risk_when: "Agent-authored accepted claims, hot/index/log, retrieval rank, a passing validator, source count, or transaction success is being treated as reviewed truth or action authority."
  cold_references:
    - raw/repos/2026-08-24-AgriciDaniel-claude-obsidian-source.md
    - raw/repos/_snapshots/2026-08-24-AgriciDaniel-claude-obsidian-1c1bc49-source.zip
avoid:
  - "Do not install, fork, execute, or enable claude-obsidian from this candidate intake."
  - "Do not replace VAKS Evidence Packet, Support/Sufficiency, Promotion, Temporal Applicability, Operation Receipt, Use Ledger, or feedback boundaries."
  - "Do not treat its accepted claim, reviewed_at, source count, confidence enum, validator pass, retrieval rank, hot briefing, or transaction success as truth or action readiness."
  - "Do not index all VAKS Markdown without an artifact-eligibility layer."
  - "Do not copy the full 15-Skill runtime or 4680-line transaction implementation before a concrete authorized writer exists."
  - "Do not assume native Windows writes are supported."
tags:
  - candidate
  - provisional
  - obsidian
  - transaction-integrity
  - source-capture
  - evidence-lint
---

# 候选强蒸馏：AgriciDaniel/claude-obsidian

## Boundary

这是 heavy candidate distillation。

它可以做架构比较、项目路由、未来设计输入和风险提醒；它不是 reviewed knowledge、pattern、decision、promotion、action basis 或安装许可。

源码锚点证明的是固定 commit 中存在什么，不证明这些机制已适合 VAKS，也不证明仓库工作流端到端成立。

## 一句话结论

这个仓库真正的干货不是 hot.md、15 个 Skills 或 Obsidian 文件夹模板，而是：

    把“可以写”拆成 authority 与 execution 两半，
    再把 execution 绑定到具体 vault、具体旧状态、具体新字节与可恢复事务。

对 VAKS 的融合判断：

    adapt strongly as engineering invariants
    validate existing epistemic spine
    reject as truth engine or current runtime

## 最值得压榨的架构张力

VAKS 已经擅长回答：

    这个判断是否有 source span、warrant、scope、challenge、omission？
    谁批准了什么意图？
    什么材料可以进入 action basis？
    使用结果如何进入 feedback / review_due？

claude-obsidian 更擅长回答：

    写的是哪个 canonical vault？
    operation type 实际允许碰哪些路径？
    审阅者看到的 plan 与最终写入字节是否完全一致？
    文件在 inspect 与 apply 之间变了怎么办？
    写到一半失败如何恢复？

最正确的吸收不是替换，而是未来在二者之间建立可验证绑定。

## Candidate Point 1：Authority Receipt 与 Execution Plan 分层

transaction.py 的 plan approval hash 绑定：

- operation identity / type；
- canonical vault identity；
- expanded bundle；
- prepared writes；
- 最终字节内容；
- file modes。

这比“用户说可以写”更精确。未来 VAKS writer 的候选合同应是：

    VAKS reviewed operation receipt
    -> authorized actor / intent / basis / target scope

    deterministic inspect
    -> canonical vault / paths / expected hashes / prepared bytes / modes

    binding
    -> receipt body hash references exact approval hash

    apply
    -> no plan drift / one transaction / exact changed-path receipt

关键边界：transaction 本身不是授权。仓库 CLI/orchestrator 强制 approval hash，但 Python apply API 的默认参数仍允许空 approval；任何未来适配必须同时保留 authority gate 与 execution-integrity gate。

## Candidate Point 2：Operation Type 是真实写能力

仓库的 operation_type 不只出现在日志中，而是限制可写路径：

- setup / migration 只允许精确 policy paths；
- mode 只允许配置；
- fold 只允许一个 fold page、index、log；
- capture 只允许 content-addressed raw 目标且 create-only；
- ingest / autoresearch 有独立范围；
- generic / save 不能随意写 runtime metadata。

这对 VAKS 的启发不是新增 operation taxonomy，而是让现有 actor tier、operation mode、target scope、intent 与实际 write-set 校验一致。

若字段只记录、不限制路径，它仍是审计文字，不是 capability boundary。

## Candidate Point 3：一次逻辑操作，一个写者，一个可恢复事务

仓库把并行与写入分开：

    parallel workers
    -> read and draft only

    one orchestrator
    -> merge proposal
    -> inspect
    -> reviewed approval hash
    -> one apply

apply 过程包含：

- mutation lock；
- pinned root / metadata directory identity；
- expected hash 与 mode；
- idempotent operation ID；
- prepared / applying / rollback-failed journal；
- 每文件 atomic replace；
- 异常回滚；
- crash recovery；
- exact changed paths；
- Git checkpoint 另行显式执行。

对 VAKS 最小吸收是合同与测试不变量，不是复制巨型模块。

## Candidate Point 4：Content-Addressed Create-Only Capture

Capture 是本仓库最适合当前 VAKS Capture spine 的部分：

    visible inbox
    -> preflight count / file bytes / total bytes
    -> reject symlink / alias / path escape
    -> check file identity before and after hashing
    -> SHA-256 addressed raw target
    -> create-only transaction
    -> keep inbox intact

它避免了三个常见问题：

1. 采集时源文件被替换；
2. 同一字节被多次伪装成不同原始来源；
3. “整理完成”顺手删掉唯一可见入口。

VAKS 当前已有 Source Capture Store/Envelope 方向。这个仓库提供的是工程旁证和未来 adapter 不变量，不要求另建 Capture lane。

## Candidate Point 5：Source Identity 与 Independence Collapse

仓库用 origin kind、规范化 locator 与 content hash 生成稳定 source ID，并通过以下关系传递式归并独立性：

- same source ID；
- same canonical origin；
- same content hash；
- declared independence key。

这可以发现：

    三条 citation
    实际是同一篇原文的镜像、转述或重复字节

对 VAKS 的正确落点是 Evidence Sufficiency 的 maintenance lint 或 known-omission input。

错误落点是：

    independent source count >= 2
    -> automatically true / high confidence / action ready

来源独立性是必要压力，不是充分真值。

## Candidate Point 6：Ledger Validator 的价值与天花板

仓库 Claim Ledger 有实用的 fail-closed 结构：

- assessment：accepted / provisional / contested / unsupported / deprecated；
- accepted 要有 reviewed_at；
- accepted 要有 fresh active non-synthetic support；
- high-risk accepted 要两组独立支持；
- fresh contradiction 要 contested 或 adjudication notes。

但它仍远弱于 VAKS Evidence Review：

- reviewer identity 不要求；
- evidence locator 可空；
- locator 不验证 span 是否 bearing；
- 没有 warrant；
- 没有 scope / risk / applicability；
- 没有 typed challenge；
- 没有 known omission check；
- confidence 与 evidence/assessment 无机械耦合；
- 一个非空 notes 可让 accepted 在 contradiction 下继续存在；
- 普通 accepted 的一个 community source 也可能满足结构要求。

因此应把 validator 视为：

    structural lint + review queue pressure

而不是：

    truth engine + promotion gate

## Candidate Point 7：Derived Retrieval Cache Integrity

检索工程的强点：

- canonical page 与 derived chunk/index 分离；
- paragraph chunk 有 overlap 与 hard cap；
- chunk 记录 source page、page hash、body hash；
- 更新 chunk 前使旧 BM25 index 失效；
- index/retrieve 再核验 chunk、index、page 三层 hash；
- rerank cache key 绑定 model、scheme、exact input hash；
- 任一 embedding 失败，整组回退原 BM25，不混合分数空间。

这适合进入 future retrieval/cache adapter 或 Guard lint。

但当前 eligibility 存在硬缺口：collect_pages 会收集 wiki 下所有非隐藏 Markdown，retrieve 只验证字节与缓存，不读取 source/claim ledger，也不区分 hot、log、meta、candidate、reviewed 或 action-ready。

VAKS 顺序必须相反：

    artifact selection / eligibility
    -> retrieval cache
    -> ranked context
    -> coverage / applicability

不是：

    rank everything
    -> hope caller remembers authority

## Candidate Point 8：Capability Honesty 与 Inert Egress Plan

仓库把 adapter 能力分成 implemented、metadata-only、external-runner-required。

URL/OCR/YouTube 等外部能力在 core 中只生成：

- 规范化 HTTPS URL；
- public-host / redirect / allowlist 条件；
- credential-like query rejection；
- 明确 consent；
- inert argv plan；
- runner placeholder。

它不会在 planner 内偷偷发起网络或进程。

对 VAKS 可借为 maintenance manifest 的小合同：

    declared capability
    + verifier
    + actual observed status
    + degraded/unavailable reason

不能把“有 adapter 名字”当成“能力已实现”。

## Candidate Point 9：hot 是有界 Briefing，不是自治记忆

旧 REVIEW_QUEUE 里“hot.md 是跨会话 recent context cache”的方向基本正确，但必须收窄：

    wiki/hot.md is a bounded orientation cache
    refreshed by explicit Save/Ingest/Autoresearch operations
    and read on later runs.

更严格的事实：

- Query 不更新；
- Fold 不更新；
- session end 不更新；
- hook 只读；
- SessionStart 注入默认关闭；
- 必须显式设置环境变量；
- 上限 32 KiB；
- 跨项目需精确 vault 同意；
- 内容包在 untrusted-data envelope；
- hot 不是 evidence、truth 或 transcript。

此外，500 words、Key Recent Facts 和淘汰策略主要是 Skill 文本合同，并非全面机械验证。transaction core 也没有普遍强制 Save/Ingest 必须同写 hot/index/log。

VAKS 若借，只借 bounded + explicit + scoped + untrusted injection。它应是 pointer briefing，不是第二套 Activation Tier。

## Candidate Point 10：Query/Persist 与 Research/Canonical Merge 分离

仓库明确：

- wiki-query 只读；要保存答案必须另开 Save；
- autoresearch 先形成独立 dossier；
- workers 只 draft；
- 更新 canonical pages 是第二个、单独审核的 transaction；
- research 要预设 topic/exclusion、egress、source class、轮数、搜索、抓取、时间和页数预算；
- 明确找 counter-position、contradiction、gap、source independence；
- 达到停止条件就停，不为满足深度捏造。

这些不是 VAKS 新层，而是对现有候选研究、promotion separation、lazy gates 和 agent memory quarantine 的强旁证。

## Candidate Point 11：Additive Fold 只应是派生理解

Fold 的可借不变量：

- additive；
- 不删 child；
- 每个数字和结论回指 child；
- 冲突保留；
- fold 不产生新 evidence；
- fold 不升级 claim；
- preview 后一次 transaction。

局限：

- 不是实际压缩，原 log/child 都保留；
- 禁止 fold-of-fold，长期仍增长；
- fold ID 只绑定日期、数量与 k，没绑定 child IDs/hash；
- 无端到端 verifier。

若用于 VAKS，应基于真实 Use Ledger event IDs/hash 生成 derived rollup，绝不能用 operation log 替代 feedback 或 outcome learning。

## Candidate Point 12：Release / Platform 边界

Release builder 值得留作未来 product/export 参考：

- allowlist；
- clean tracked/untracked snapshot；
- worktree bytes 必须与 index blob 一致；
- symlink/special-file 与 portable collision 拒绝；
- home path / email / token / unreviewed binary 扫描；
- 构建前后 Git snapshot 一致；
- deterministic temp build 与 atomic output；
- 不 stage / commit / tag / push / publish。

但它不是通用泄密证明，且目前 VAKS publishing runtime parked。

Windows 方面，上游明确 native Windows 只读，写事务需要 WSL/Linux 语义和稳定文件身份。当前 Windows + H: formal vault 不应直接试装。

## 与 VAKS 现有架构的碰撞

| 上游机制 | VAKS 已有 | 真正增量 | 路由 |
|---|---|---|---|
| immutable capture | Source Card / Snapshot / Capture Store | create-only、TOCTOU、budget 的实现不变量 | adapt |
| plan approval hash | Operation Receipt / action preflight | exact vault/bytes/modes binding | strong adapt later |
| transaction/journal | Guard 是只读检查器 | future executor integrity | park until writer |
| source ledger | provenance/source identity | independence collapse 与 dynamic stale lint | adapt |
| claim ledger | Evidence Packet / Support / Sufficiency / Promotion | 少量 fail-closed structure | lint only |
| hot.md | Activation Tier / Dev Context / Context Pack | explicit bounded untrusted injection | validate / narrow adapt |
| retrieval cache | Association Neighborhood / artifact selection | hash chain 与 deterministic fallback | adapt after eligibility |
| autoresearch | candidate research / promotion separation | budget and stop-condition wording | validate |
| operation log | Use Ledger / feedback | 几乎无增量 | reject substitution |
| release builder | publishing parked | future clean-snapshot contract | park |

## 直接借 / 改造后借 / 不借

### 直接借工程不变量

- visible bounded inbox；
- content-addressed create-only source snapshot；
- external action inert plan；
- one operation / one writer / one bundle / one apply；
- expected old state；
- vault/bytes/modes approval binding；
- journal / rollback / recovery / exact changed paths；
- source independence collapse；
- derived-cache hash chain；
- whole-set rerank fallback；
- capability maturity honesty。

### 改造后借

- hot → scoped pointer briefing；
- ledgers → Evidence Packet preparation / lint；
- BM25/rerank → eligibility-filtered retrieval；
- two-source rule → independence warning；
- fold → event-ID-bound derived rollup；
- Canvas → visual-only relation；
- release sanitizer → future product/export gate；
- Skills → bounded operation contracts with mechanical receipts where needed。

### 明确不借

- agent-authored accepted 等价 reviewed truth；
- reviewed_at 时间戳等价 review provenance；
- citation 等价 support；
- source count 等价 sufficiency；
- nonempty notes 覆盖 contradiction；
- free confidence enum；
- 全 wiki 检索后靠 prompt 维持 authority；
- hot/index/log 进入 evidence pool；
- operation log 替代 Use Ledger；
- folder modes 变成 lane；
- native Windows 写；
- full runtime / 15 Skills / giant transaction copy；
- Ground 自动合并 Understand + Review；
- transaction success 等价 action approval。

## 最小融合形状

当前只保存 design candidate：

    VAKS authority receipt
    -> future adapter boundary
    -> deterministic inspect
    -> approval-bound plan
    -> single-writer apply
    -> operation result receipt

现在不实现。未来只在出现真实 writer 后重开，并优先写小适配合同与 adversarial tests，而非复制上游 runtime。

## Final Candidate Verdict

强度判断：

    engineering reference: high
    epistemic authority: insufficient for VAKS
    current integration readiness: no
    direct installation value: no
    future executor-design value: strong

这个仓库值得入库，因为它把“可靠写入”做到了接近可以借鉴的工程颗粒度；更值得入库的原因，是它同时暴露了“可靠写入不等于可靠知识”的清晰反例。

