---
type: library_review
record_kind: library_review
status: draft
knowledge_status: candidate
processing_tier: heavy
library_name: AgriciDaniel/claude-obsidian
repo_url: https://github.com/AgriciDaniel/claude-obsidian
source_url: https://github.com/AgriciDaniel/claude-obsidian
checked_commit: 1c1bc49c03a685ee8f5d09c99efe52b42d6673f5
commit_time: 2026-08-01T14:03:27+02:00
source_status: active
reviewed_at: 2026-08-24
domain:
  - local-first-knowledge-runtime
  - obsidian
  - content-addressed-capture
  - recoverable-transactions
  - provenance-ledgers
  - retrieval-cache-integrity
  - agent-skills
related_projects:
  - verified-action-knowledge-system
current_branch: "master / Source Capture Store verification; VAKS Guard landed; Bases and runtime surfaces parked"
extracted_patterns:
  - vault-bound-approved-operation-plan
  - operation-type-write-capability
  - single-writer-recoverable-transaction
  - content-addressed-create-only-capture
  - source-independence-collapse
  - hash-chained-derived-retrieval-cache
  - bounded-untrusted-context-briefing
  - research-dossier-canonical-merge-separation
fusion_decision: adapt
confidence: medium
evidence_count: 36
cross_validated_with:
  - FUSION_ARCHITECTURE_V0_2_DRAFT.md
  - ARCHITECTURE_PRINCIPLES.md
  - SCHEMA.md
  - IMPLEMENTATION_BLUEPRINT.md
  - SOURCE_INTAKE.md
  - REFERENCE_REVIEW_PROTOCOL.md
  - MEMORY_TIER.md
  - DEV_CONTEXT.md
  - REVIEW_QUEUE.md
  - FEEDBACK.md
  - tools/vaks_guard.py
negative_evidence:
  - "No repository tests, workflows, hooks, Obsidian integration, WSL write path, network adapters, model paths, release builder, or recovery drill were executed in this intake."
  - "Accepted claims can pass without reviewer identity, mandatory source span, warrant, support-bearing validation, scope, omission check, temporal applicability, or confidence/evidence coupling."
  - "Skill-level Ingest/Save coupling is not generally enforced by the transaction core."
  - "Retrieval collects broad wiki Markdown and does not mechanically gate candidate/hot/log/meta/reviewed status."
  - "The repository has no VAKS-equivalent Act-and-Learn loop."
  - "Native Windows mutation is intentionally unsupported."
extension_potential: "Future VAKS operation-executor adapter, capture adapter, evidence-independence lint, retrieval-cache integrity contract, or export gate; no current runtime integration."
retrieval_policy:
  policy_kind: orientation_only
  pack_allowed: review_input_only
  action_basis_allowed: false
  warning_code: candidate_review_not_action_basis
promotion_gate: v0_2_13_required
action_basis_allowed: false
truth_mutation_allowed: false
relations: []
tags:
  - library-review
  - candidate
  - obsidian
  - transaction-integrity
  - evidence-boundary
  - agent-tool-safety
---

# 架构分析：AgriciDaniel/claude-obsidian

Remote main 在 2026-08-24 再次核对，HEAD 仍为 1c1bc49c03a685ee8f5d09c99efe52b42d6673f5。

## Boundary

这是固定提交的候选架构 review，不是正式 pattern、decision、review pass、truth confidence 或 action basis。

本次只做静态源码与文档审阅。没有安装依赖，没有运行 tests、project scripts、hooks、Obsidian、WSL writes、models、network adapters、release 或 recovery。

## 它实际解决什么

claude-obsidian 试图把一个用户 vault 变成可由 Claude 驱动、但关键写边界由本地 Python core 约束的知识系统：

    explicit user vault
    + visible raw inbox
    + content-addressed captured sources
    + source / claim ledgers
    + Agent Skills for semantic workflows
    + deterministic transaction core
    + derived retrieval caches
    + optional read-only session context

它不是单一“智能 Obsidian 插件”。更准确地说，它是：

    semantic workflow contracts
    + deterministic local mutation boundary
    + repository/vault separation
    + capability and platform honesty

## 模块架构

| Module | Role | Canonical or derived | Main boundary |
|---|---|---|---|
| skills/ | Save/Ingest/Query/Research/Fold/Mode/Canvas 等语义流程 | contract | 多数由 agent 遵守，不等于机械 enforcement |
| agents/ | worker prompts | transient | workers draft-only |
| claude_obsidian/paths.py | vault resolution、containment、plugin-tree rejection | deterministic core | fail closed |
| claude_obsidian/capture.py | filesystem capture、URL/OCR/YouTube action plan | deterministic core | local capture implemented；external runner inert |
| claude_obsidian/transaction.py | inspect/apply/lock/journal/rollback/recovery | deterministic core | 单写者 mutation boundary |
| claude_obsidian/ledgers.py | source/claim schema 与 validator | canonical metadata validator | structural grounding，不是完整 evidence review |
| scripts/contextual-prefix.py | Markdown chunk + contextual prefix | derived | cache generation |
| scripts/bm25-index.py | local deterministic BM25 | derived | stale cache exclusion |
| scripts/retrieve.py | hash-checked retrieval | derived/read-only | relevance，不是 authority |
| scripts/rerank.py | optional embedding rerank | derived | all-or-nothing fallback |
| claude_obsidian/hook_adapter.py | SessionStart / Stop adapter | read-only adapter | opt-in、bounded、untrusted |
| claude_obsidian/release.py | fixed clean-tree release builder | product/export | allowlist and sanitizer |
| config/ | product, adapter, capability, release contracts | declarative | implemented vs metadata/external honesty |
| templates/vault/ | initialized vault shape | user data template | not VAKS schema |

## 核心数据流

### Capture

    visible inbox or explicit source
    -> bounded preflight
    -> resolve and reject unsafe alias/symlink/path
    -> verify file identity while hashing
    -> SHA-256 content address
    -> inspect create-only capture bundle
    -> approval-bound apply
    -> .raw/captured/<sha>.<suffix>
    -> leave inbox intact

### Ingest

    source + hot/index + selected existing pages
    -> agent worker draft packet
    -> page proposals + source/claim ledger proposals
    -> orchestrator merge
    -> expected hashes
    -> one transaction

注意：后半段的 page/ledger/index/log/hot 耦合主要是 Skill contract。transaction core 只有在 ledger 被纳入时才验证 prospective ledger state，不普遍要求 Ingest 一定包含 ledger 或 hot/index/log。

### Query / Retrieval

    wiki non-hidden Markdown
    -> paragraph chunks + prefix
    -> chunks cache
    -> BM25 index
    -> optional rerank
    -> page paths/snippets
    -> wiki-query reads pages and separately interprets ledgers

缓存完整性很强；知识 eligibility 很弱。Rank 只代表 lexical/semantic relevance。

### Mutation

    complete draft bundle
    -> inspect only
    -> expand metadata writes
    -> prepare exact bytes and modes
    -> approval hash
    -> lock canonical vault
    -> recheck namespace and expected state
    -> journal
    -> atomic per-file writes
    -> rollback/recovery or exact result

## Source / Code Anchors

| Anchor | What exists | Design extraction | Boundary |
|---|---|---|---|
| AGENTS.md:3-6 | Skills, core, hooks 分工。 | 语义与确定性边界分层。 | Skills 仍依赖 agent compliance。 |
| claude_obsidian/paths.py:178-257 | 解析后 containment、配置 identity/size。 | vault selection 是 security boundary。 | 只保护通过该 resolver 的调用。 |
| claude_obsidian/paths.py:329-413 | 拒绝 plugin tree；显式→env→workspace config→initialized ancestor。 | product/vault 分离且选择失败停写。 | 环境/配置仍需用户治理。 |
| claude_obsidian/capture.py:408-492 | count/file/total byte budget 与 visible inbox。 | 写前 bounded preflight。 | 不等于内容可信。 |
| claude_obsidian/capture.py:585-705 | symlink/alias/TOCTOU 身份检查。 | capture source identity hardening。 | 仍只验证 bytes/path。 |
| claude_obsidian/capture.py:865-1029 | SHA-256 target、batch transaction、inbox retained。 | immutable create-only capture。 | Snapshot 只是 provenance。 |
| claude_obsidian/capture.py:1045-1217 | URL safety 与 inert external action plan。 | consent 与 execution 分离。 | runner 仍需外部安全边界。 |
| transaction.py:1-7 | 多文件不是物理原子；锁+journal+rollback。 | 能力宣称诚实。 | crash/recovery 仍需实际验证。 |
| transaction.py:89-137 | operation types 与 write domains。 | 操作类型成为 capability。 | 不能阻止绕过 core 的直写。 |
| transaction.py:1287-1308 | approval hash 绑定 vault、bundle、prepared writes。 | review-to-bytes binding。 | Python API 可空 approval；外层必须强制。 |
| transaction.py:1646-1813 | mutation lock、token、pinned descriptors。 | 单写者与 namespace hardening。 | 依赖支持的文件系统语义。 |
| transaction.py:3130-3235 | operation-specific write scope。 | label 与 capability 对齐。 | 只覆盖定义过的操作。 |
| transaction.py:3237-3255 | bundle coupling 只对 fold 特判。 | 揭示 Skill/core gap。 | Ingest/Save 未同等强制。 |
| transaction.py:3506-3623 | prospective source/claim ledger validation。 | 耦合 metadata 应整态验证。 | ledger 未纳入 bundle 时直接跳过。 |
| transaction.py:4098-4250 | recover prepared/applying/rollback-failed journal。 | 可恢复事务。 | 本次未做 crash drill。 |
| transaction.py:4273-4680 | inspect/apply、expected state、journal、rollback、receipt。 | 最强工程机制。 | 巨型实现、私有 API 耦合。 |
| cli.py:72-108,372-442 | CLI apply 必须传 exact approval hash。 | 外层强制 review plan。 | core API 仍需防绕过设计。 |
| provenance.md:14-49 | manifest/source ledger/claim ledger 分离。 | provenance 与 claim assessment 区分。 | 仍不是 VAKS Evidence Packet。 |
| ledgers.py:407-414 | stable source ID。 | canonical source identity。 | locator 规范化策略需场景验证。 |
| ledgers.py:635-758 | active source dates/hash/refresh_due/dynamic stale。 | stale 作为派生状态。 | source freshness 不等于 claim applicability。 |
| ledgers.py:797-837 | source/origin/hash/independence key 归并。 | 独立性 lint。 | 数量不产生 sufficiency truth。 |
| ledgers.py:942-1029 | falsifiable claim text/page/anchor。 | claim 可定位结构。 | 不验证页面陈述与 evidence bearing。 |
| ledgers.py:1030-1150 | accepted/fresh support/high-risk two-source/contradiction。 | fail-closed 结构 lint。 | locator 可空；无 reviewer/warrant/scope/omission。 |
| contextual-prefix.py:476-814 | chunk cap、prefix、hash、cache invalidation。 | derived cache integrity。 | synthetic prefix 不是证据。 |
| contextual-prefix.py:834-849 | 遍历 wiki 下全部非隐藏 Markdown。 | 明确 eligibility gap。 | hot/log/meta/candidate 可进入候选集。 |
| retrieve.py:191-223,259-365 | chunk/index/page hash 复核与检索。 | stale/corrupt cache fail closed。 | 不读 ledger，不做 authority filter。 |
| rerank.py:193-215,400-477 | exact input cache key；失败全组回退。 | 不混合分数空间。 | relevance 仍不等于 trust。 |
| hook_adapter.py:25,122-139,172-214 | 32 KiB、sanitize、opt-in、untrusted envelope。 | bounded safe context injection。 | hot 内容本身由 agent 维护。 |
| skills/wiki-query/SKILL.md:8-96 | hot orientation、depth budget、fallback、read-only。 | query/persist 分离。 | ledger assessment 主要是 prompt contract。 |
| skills/autoresearch/SKILL.md:27-121 | budget、counter-position、dossier/canonical split。 | candidate research boundary。 | 无 E2E verifier。 |
| release.py:246-405,685-1079 | exclusions、scan、sanitized fixed Git snapshot。 | future export gate。 | defense in depth，不是泄密证明。 |
| release.py:2391-2588 | deterministic build；不 stage/commit/push/publish。 | build 与发布权限分离。 | 当前 VAKS publishing parked。 |
| docs/windows-wsl.md:7-33 | native Windows read-only；WSL mutation。 | platform fail closed。 | 当前环境不可直接采用写 runtime。 |
| config/capabilities.json | 多个 workflow 无 E2E verifier。 | capability honesty。 | 文档承认不等于功能正确。 |

## README / Contract 宣称核验

| 宣称 | 静态结论 | 说明 |
|---|---|---|
| product 与 user vault 分离 | 源码强支持 | plugin tree 被拒绝，vault 解析 fail closed。 |
| 可见 inbox、不可变内容寻址 capture | 源码强支持 | budget、identity、SHA-256、create-only、no delete。 |
| one operation / one recoverable transaction | 源码强支持 | inspect、approval、lock、journal、rollback、recovery。 |
| parallel workers 不竞写 | 条件支持 | 遵守 worker/core contract 时成立；无法阻止绕过 core。 |
| source/claim ledger grounded knowledge | 部分支持 | 结构与 freshness/independence 有约束；support semantics 不足。 |
| grounded query | 部分支持 | cache integrity 强；authority interpretation 依赖 Skill。 |
| deterministic BM25 + rerank fallback | 源码支持 | 多层 hash 与 all-or-nothing fallback。 |
| 15 Skills 构成完整系统 | 文件/协议存在，E2E 不足 | 多个 capability 明确无自动 verifier。 |
| compounding knowledge | 到 authoring/retrieval 为主 | 缺 action basis、outcome、Use Ledger、feedback/review_due。 |

## 最强机制：Transaction

transaction.py 明确承认多文件操作不是真正物理原子，而是：

    process lock
    + precondition hashes
    + durable journal
    + atomic per-file replace
    + deterministic rollback/recovery

这是可信的能力表述。它没有用“atomic”掩盖系统限制。

### 审批绑定

plan approval hash 把 expanded bundle 与 prepared writes 纳入。同一个自然语言意图，只要：

- vault 不同；
- 旧文件不同；
- 新字节不同；
- file mode 不同；
- operation type 不同；

就应产生不同 plan。

### 单写者

锁不只是创建一个 lockfile。实现还检查 process token、stale lock、root/meta directory identity，并通过 pinned descriptors 防止 namespace swap。

### 失败处理

journal 区分 prepared、applying、rollback-failed 等状态。失败时保留足够材料恢复；成功后返回 exact changed paths。

### 不能夸大的地方

- 未执行本次 recovery test。
- 脚本依赖 transaction.py 私有函数，长期演化有耦合风险。
- core 只约束通过它的写入。
- core API 可空 approval；authorization 仍需外层强制。
- 可靠执行不验证知识内容正确。

## Claim Ledger 与 VAKS Review 的关键差距

上游 accepted 的机械要求可以概括为：

    reviewed_at exists
    + fresh active non-synthetic support exists
    + high-risk has two independent groups
    + contradiction has notes or contested status

VAKS 要求的最小重要 review envelope 还包括：

    atomic candidate point
    + exact source span
    + evidence item
    + support-bearing check
    + warrant
    + scope and risk
    + challenge kind
    + known omission/conflict when required
    + reviewer/approval provenance
    + temporal/version/project/environment applicability

差距不是字段多少，而是语义职责：

    upstream validator asks whether the record is structurally plausible
    VAKS asks whether this specific evidence supports this point for this scope and use

所以 Ledger 只能作为 lint，不得直连 Promotion。

## Retrieval 的强弱分裂

### 强：Cache integrity

- canonical vs derived 分离；
- chunk/page/index hashes；
- stale chunk 不入索引；
- corrupt/stale index fail closed；
- optional rerank 不混合 partial scores；
- remote/local model egress 必须显式。

### 弱：Artifact authority

- collect_pages 收所有非隐藏 Markdown；
- retrieve 不读取 ledgers；
- hot/index/log/meta/candidate 不机械降级；
- authority assessment 留给 wiki-query prompt；
- no Context Pack coverage map；
- no Temporal Applicability Check；
- no reviewed-relation requirement。

VAKS 可借后端 cache，不借候选集定义。

## hot.md 校准

旧候选句“hot.md 是跨会话 recent context cache”应改写为：

    hot.md 是由显式 Save/Ingest/Autoresearch 刷新的有界 orientation briefing；
    后续任务可读，SessionStart 注入默认关闭；
    它既不是 evidence，也不是 transcript，更不是自治记忆。

额外风险：

- vault 级单文件没有 scope_key；
- 模板 Key Recent Facts 与非证据边界有认知冲突；
- 500 words 与淘汰策略主要靠 Skill；
- core 没普遍强制 Save/Ingest 同写 hot；
- agent draft 决定选入内容。

VAKS 最多吸收 safe injection contract，不新增 Hot Memory。

## 当前支线价值

当前支线已有：

- Source Capture Store / verification；
- raw/candidate/review/promotion 分层；
- Evidence Packet、Support、Sufficiency；
- Activation Tier / Dev Context / Context Pack；
- read-only VAKS Guard；
- Operation Receipt 字段；
- agent memory quarantine；
- Bases 与 runtime surfaces parked。

对当前支线：

| Finding | Value |
|---|---|
| content-addressed capture | 直接压力测试现有 Capture Store 的 create-only、budget、identity 不变量。 |
| approval-bound transaction | 暴露 Guard 与真正 executor 之间尚未实现、也不应急着实现的边界。 |
| source independence collapse | 可补 maintenance lint 候选，不改 truth schema。 |
| retrieval cache hash chain | future adapter reference；当前不启动 retrieval runtime。 |
| hot briefing | 校准旧 REVIEW_QUEUE 句子，不新建模块。 |
| Claim Ledger ceiling | 反证 VAKS Evidence Packet/Promotion Gate 不能降级。 |
| native Windows fail closed | 直接阻止当前环境中的草率集成。 |

本次不应修改主线 docs、schema、patterns、decisions、handoff 或 indexes。先保存 candidate + overlay + exact annotations。

## 全貌架构价值

| VAKS public stage | Upstream value | Decision |
|---|---|---|
| Capture | visible inbox、budget、content address、create-only、inert external plan | adopt invariants |
| Understand | bounded reads、worker draft packet、type-aware workflow | adapt as candidate-only |
| Review | source/claim structure and independence lint | reject direct authority |
| Connect | coupled writes and derived index integrity | adapt; reviewed relations stay VAKS |
| Act and Learn | transaction execution integrity only；缺 action/use feedback | keep VAKS |
| Cross-cutting risk | vault selection、untrusted data、egress consent、rollback、platform fail closed | strong reference |

## 风险与反证清单

1. Skill contract 与 deterministic core 之间存在 enforcement gap。
2. accepted claim 可在无 reviewer identity、无必填 locator、无 warrant 下通过。
3. confidence 是不受 evidence 约束的枚举。
4. contradiction 可被自由 notes 覆盖。
5. source freshness 不是 point applicability。
6. broad retrieval 没有 artifact eligibility。
7. hot 是 agent-maintained briefing，不是自动 memory。
8. operation log 不是 Use Ledger。
9. transaction core 不是 authorization。
10. core 无法阻止 direct file writes。
11. 巨型 transaction module 与私有 API 引用提高搬运成本。
12. release sanitizer 不是通用安全证明。
13. tests/capabilities 为项目自证，本次未运行。
14. native Windows mutation unsupported。
15. 没有完整 Act-and-Learn。

## Adoption Matrix

| Mechanism | Decision | Minimal VAKS landing |
|---|---|---|
| content-addressed capture | adopt invariants | Capture Store adapter checks |
| visible inbox / no implicit delete | adopt | Source Intake boundary |
| operation write scope | adapt | actor/mode/target write-set lint |
| approval-bound exact plan | strong adapt later | Operation Receipt to plan binding |
| journal/rollback/recovery | park until writer | future executor only |
| source independence collapse | adapt | maintenance manifest warning |
| dynamic stale | adapt | source freshness lint, not truth |
| Claim Ledger accepted | reject as authority | review input only |
| cache hash chain | adapt | derived retrieval adapter |
| broad wiki retrieval | reject | eligibility first |
| hot briefing | narrow adapt | scoped pointer briefing |
| Query/Save split | validate existing | no new object |
| dossier/canonical split | validate existing | candidate/promotion boundary |
| fold invariants | narrow adapt | derived Use Ledger rollup |
| release builder | park | future products/export |
| native Windows writes | reject | no current runtime |
| full plugin runtime | reject now | design reference only |

## Verification Status

### 静态核对完成

- remote HEAD 固定并复查；
- commit/version/license 记录；
- git archive 快照与 SHA256；
- path/capture/transaction/ledger/retrieval/hook/research/release/platform 源码锚点；
- 当前 VAKS architecture collision；
- claim-to-implementation gap；
- 12 个 exact source annotation spans。

### 未执行

- dependency installation；
- project tests；
- capability verifiers；
- live Obsidian；
- Claude hooks；
- WSL mutation；
- model/embedding/Ollama；
- URL/OCR/YouTube runner；
- concurrency/recovery/failure injection；
- release build；
- real end-to-end Save/Ingest/Query/Research。

因此 confidence 只表示对固定源码结构的静态理解，不表示运行行为、通用安全或适用性已验证。

## Final Judgment

当前结论：

    fusion_decision: adapt
    direct install: no
    current runtime integration: no
    engineering extraction value: strong
    epistemic replacement value: reject

最值得保留的不是“Claude 会管理 Obsidian”，而是：

    知识授权与文件执行必须分层；
    审阅过的意图必须绑定到真正将被写入的字节；
    来源捕获必须不可变且可追溯；
    检索完整性不能冒充知识权威；
    transaction success 不能冒充 truth 或 action approval。

