---
record_kind: project_overlay
status: candidate
knowledge_status: candidate
processing_tier: heavy
overlay_state: confirmed
review_pressure: none
overlay_scope: project_sidecar_only
overlay_storage: confirmed_persistent_project_bucket
retrieval_scope: active_project_only
default_retrieval: false
retrieval_policy:
  policy_kind: project_context_only
  default_scope: project_only
  pack_allowed: activation_only
  action_basis_allowed: false
  warning_code: overlay_not_authority
promotion_gate: v0_2_13_required
action_basis_allowed: false
truth_mutation_allowed: false
project_id: verified-action-knowledge-system
target_ref: outputs/review/2026-08-24-AgriciDaniel-claude-obsidian-candidate-distillation.md
target_selector: "VAKS transaction integrity, immutable capture, evidence lint, retrieval cache and bounded-context sidecar"
target_hint: "authority receipt plus vault-bound plan / single-writer transaction / create-only capture / ledger ceiling / retrieval eligibility"
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
project_borrow_scope: "For VAKS, retain claude-obsidian as a design and future-executor reference. Borrow content-addressed create-only capture, operation-scoped write authority, expected-state plus vault/bytes/modes approval binding, one-orchestrator recoverable transactions, source-independence collapse, derived-cache hash invalidation, inert external-action plans, and bounded untrusted context injection. A future adapter may bind a VAKS authority receipt to a reviewed execution plan, but only after a concrete writer exists."
project_non_borrow_scope: "Do not currently install, fork, or run the repository; do not replace VAKS Source Card, Evidence Packet, Evidence Support/Sufficiency, Promotion, Temporal Applicability, Operation Receipt, Use Ledger, or feedback boundaries with its JSON ledgers or Skills; do not accept agent-authored accepted claims, broad wiki retrieval, hot/index/log as evidence, folder modes as formal lanes, native Windows writes, or the full 15-Skill/runtime surface."
project_reopen_trigger: "Reopen an execution adapter only when VAKS has an explicitly authorized multi-file writer or action runtime, a concrete coupled-write use case, a reviewed mapping from VAKS authority receipt to exact vault/bytes/modes approval, a compatible WSL/Linux or otherwise validated execution environment, and separately authorized adversarial recovery, bypass, concurrency, symlink, stale-plan, and eligibility tests."
confirmation_basis: "User explicitly requested a strong VAKS distillation of this repository; this confirmed overlay persists only project-scoped borrow/non-borrow/reopen routing and does not imply adoption, installation, promotion, or action authority."
last_checked_at: 2026-08-24
expires_at:
tags:
  - transaction-integrity
  - content-addressed-capture
  - evidence-lint
  - retrieval-integrity
  - agent-tool-safety
---

# Project Overlay：claude-obsidian 对 VAKS 的融合边界

## Boundary

这是 confirmed project-scoped candidate sidecar。

confirmed 只表示用户已明确要求把这次强蒸馏持久化为 VAKS 项目路由；它不表示：

- 架构已采纳；
- 代码可安装；
- Claim 已 review；
- Snapshot 已成为 evidence support；
- 任何写操作已获授权；
- VAKS 主线、pattern、decision 或 reviewed relation 已改变。

## 核心融合判断

最强融合不是把 claude-obsidian 装进来，而是把两种不同责任对齐：

    VAKS Operation Receipt
    -> 回答谁、为何、基于什么、允许做哪类动作

    reviewed execution plan
    -> 回答写哪个 vault、哪些路径、预期旧状态、最终字节与模式

    approval-bound transaction
    -> 单写者、锁、journal、atomic replace、rollback、exact changed paths

一句话：

    VAKS 提供 authority / evidence / intent 语义；
    claude-obsidian 提供 execution integrity 的工程参考。

二者必须分层，不能互相冒充。

## Project Borrow Scope

### 1. Future authority-to-execution binding

未来若 VAKS 真有多文件 writer，候选最小合同是：

    reviewed Operation Receipt
    + canonical vault identity
    + operation type
    + expected old hashes/modes
    + prepared new bytes/modes
    -> one approval hash
    -> one apply
    -> one exact receipt

审批哈希应绑定真正被审阅的写计划，不只绑定一句自然语言意图。

### 2. Operation type as capability

operation_type 不能只是日志标签。它应限制可写域，例如 capture 只能 create-only raw snapshot，config 只能写配置目标，普通 save 不能触碰 runtime metadata。

VAKS 若吸收，应优先复用现有 actor tier、operation mode、target scope 和 intent 字段，不新增一条形式化 lane。

### 3. Immutable source capture

Capture 层可借：

- visible inbox；
- count/file/total byte budget；
- symlink、alias、containment 和 read-identity check；
- SHA-256 content-addressed destination；
- create-only；
- 成功后不隐式删除 inbox；
- 外部 URL 仅生成 inert plan，实际 runner 另行授权。

### 4. Recoverable one-operation transaction

未来 writer 可借：

- parallel workers 只 draft；
- 单 orchestrator 合并；
- inspect 不写；
- expected-state conflict check；
- global mutation lock；
- durable journal；
- atomic per-file replace；
- failure rollback/recovery；
- idempotent operation ID；
- exact changed-path result；
- Git checkpoint 仍是另一个显式操作。

不复制 4680 行实现；先抽小合同，再针对 VAKS 风险验证。

### 5. Evidence maintenance lint

Source canonical identity、相同 content hash、canonical origin、independence key 的传递式折叠可用于发现伪独立来源。

refresh_due 可动态计算 stale，避免再存一个可漂移的 stale truth。

这些只能进入 maintenance manifest、Evidence Packet 准备或 sufficiency warning，不能自动创建 truth confidence、reviewed relation 或 action readiness。

### 6. Derived retrieval integrity

可借 page/chunk/index hash、cache invalidation、禁止 partial rerank、整组 deterministic fallback。

但在 VAKS 中必须先有 artifact eligibility：

    eligible reviewed/support material
    -> derived retrieval cache
    -> candidate context
    -> coverage/applicability check

不能先把全 wiki 都塞进索引，再靠调用者自觉区分。

### 7. Bounded context injection

hot 的增量只在工程合同：

- 显式 knowledge operation 才刷新；
- 有尺寸上限；
- 默认不注入；
- 跨项目要精确同意；
- 注入时标记 untrusted data；
- query/fold/session end 不暗写。

VAKS 里应叫 scoped orientation briefing，内容只放 pointer、scope、why-loaded、active thread 和 risk reminder，不叫 Facts，不替代 Activation Tier、Dev Context 或 Context Pack。

## Project Non-Borrow Scope

当前明确不借：

1. 整套插件、fork、15 Skills、hook、runtime 或 Obsidian 写入安装。
2. 两个集中 JSON ledger 作为 VAKS truth source。
3. agent 自写 accepted、单一 non-synthetic source 即 accepted、空 locator 仍算 support。
4. 任意 notes 即可覆盖 contradiction。
5. confidence 枚举脱离 Evidence Packet、support check 和 reviewer provenance。
6. 对 wiki 下全部 Markdown 建索引后再靠 prompt 区分 reviewed/candidate/hot/log。
7. hot.md 作为自治记忆、证据或第二套 Activation Tier。
8. operation log 替代 Use Ledger、feedback、outcome calibration 或 review_due。
9. LYT/PARA/Zettelkasten mode 变成 VAKS 正式 lane。
10. Canvas edge 变成 reviewed relation。
11. native Windows/H: vault 写入假设。
12. transaction core 单独充当 action authorization。
13. release sanitizer 被解释为通用隐私或安全证明。

## Current VAKS Fit

| VAKS zone | Overlay routing |
|---|---|
| Capture / Provenance | 直接借工程不变量；不改现有 Source Card/Envelope 语义。 |
| Candidate Comprehension | Skills 可作有界操作合同；输出仍是 candidate。 |
| Review / Promotion | 保留 VAKS；Claim Ledger 只作结构 lint。 |
| Connect | 多文件原子合并有候选价值；关系仍须 reviewed。 |
| Activation / Context | hot 仅作 scoped briefing 旁证；不建新层。 |
| Decision / Action | Operation Receipt 与 execution plan 分层；当前不接 runtime。 |
| Use / Feedback | 上游明显不足；继续 VAKS 主线。 |
| Risk / Inhibition | vault selection、untrusted injection、egress consent、rollback 可作工程参考。 |

## Reopen Trigger

只有同时满足以下条件才讨论实现：

1. 出现真实、明确授权的 VAKS 多文件 writer 或 action runtime。
2. 有一个必须耦合写入的具体操作，普通文件编辑不足以安全完成。
3. 已设计 VAKS authority receipt 到 vault/bytes/modes approval 的一一映射。
4. 执行环境不是未验证的 native Windows 写路径。
5. 用户明确允许安装、运行和测试。
6. adversarial suite 覆盖 bypass、stale plan、symlink、namespace swap、concurrency、rollback failure、recovery、eligibility 和 receipt/body mismatch。
7. 结果表明最小适配器足够，无需复制整套 runtime。

## Confirmation

    confirmation_basis: explicit strong VAKS distillation request
    overlay_effect: project-scoped routing only
    adoption_effect: none
    action_authority: none

