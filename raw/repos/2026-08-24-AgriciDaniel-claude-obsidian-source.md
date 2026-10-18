---
type: source
record_kind: source_card
status: source-captured
title: "AgriciDaniel/claude-obsidian"
source_id: github-AgriciDaniel-claude-obsidian
source_uri: https://github.com/AgriciDaniel/claude-obsidian
source_url: https://github.com/AgriciDaniel/claude-obsidian
source_type: repository
source_identity:
  schema_version: 1
  source_id: github-AgriciDaniel-claude-obsidian
  kind: repository
  canonical_locator: https://github.com/AgriciDaniel/claude-obsidian
  identity_profile: github-repository
  aliases:
    - kind: git_locator
      value: "git+https://github.com/AgriciDaniel/claude-obsidian.git"
author: Daniel Agrici
publisher: GitHub
updated_at: 2026-08-01T14:03:27+02:00
captured_at: 2026-08-24T01:14:00+08:00
captured_by: Codex
version_or_commit: 1c1bc49c03a685ee8f5d09c99efe52b42d6673f5
adapter_ingest:
  adapter_name: git-clone-and-archive
  adapter_version: git 2.52.0.windows.1
  capture_method: "git ls-remote; git clone --depth 1 --branch main; git archive HEAD"
  extraction_trace: "Read-only static inspection of README, architecture contracts, path and vault resolution, capture, transaction, source/claim ledgers, retrieval/index/rerank scripts, hooks, research/save/ingest/query/fold Skills, release sanitizer, Windows/WSL boundary, product/capability contracts, tests and CI manifests. No repository code, dependency, test, hook, model, network adapter, Obsidian workflow, or write runtime was executed."
  known_limits:
    - "Static source review confirms what the checked commit contains, not that every workflow claim works end to end."
    - "Repository-authored tests and capability declarations were inspected but not executed or independently reproduced."
    - "Most semantic workflows are Agent Skill contracts; deterministic Python boundaries do not mechanically enforce every Skill-level obligation."
    - "No live Claude Code, Obsidian, WSL write path, local model, remote model, OCR, YouTube, URL fetch, release, or recovery drill was exercised."
    - "GitHub popularity and issue metadata are volatile and were not used as quality, authority, or evidence signals."
    - "The archive is a fixed git-tree snapshot, not a VAKS Source Capture Envelope v1 bundle."
source_status: active
raw_location: raw/repos/_snapshots/2026-08-24-AgriciDaniel-claude-obsidian-1c1bc49-source.zip
processing_tier: heavy
knowledge_status: raw
overlay_state: none
review_pressure: none
retrieval_policy:
  policy_kind: source_identity_only
  pack_allowed: drilldown_required
  action_basis_allowed: false
  warning_code: raw_is_provenance_only
promotion_gate: none
action_basis_allowed: false
truth_mutation_allowed: false
review_priority: high
review_owner: Codex
formalization_status: raw-only
why_saved: "User explicitly requested a strong VAKS distillation of AgriciDaniel/claude-obsidian."
topics:
  - obsidian
  - local-first-knowledge-system
  - content-addressed-capture
  - recoverable-transactions
  - provenance-ledgers
  - retrieval-cache-integrity
  - agent-skills
  - capability-contracts
projects:
  - verified-action-knowledge-system
source_family:
  - repository
  - local-first-agent-runtime
  - knowledge-workflow
upstream_sources: []
verification_status: unverified
candidate_relation_suggestions: []
tags:
  - repo-intake
  - strong-distillation
  - candidate-only
  - obsidian
  - transaction-integrity
---

# 来源记录：AgriciDaniel/claude-obsidian

## 为什么收录

用户明确要求对 AgriciDaniel/claude-obsidian 做强蒸馏。

这个仓库不是普通 Obsidian 模板。它把 source capture、provenance ledger、检索缓存、Agent Skills、vault 路径隔离和多文件写事务拼成一个本地优先知识工作流。对 VAKS 最有价值的不是目录结构或 Skills 数量，而是若干可拆出的工程不变量：

- 内容寻址、create-only 的原始源捕获；
- 把目标 vault、操作类型、预期文件状态、最终字节与模式绑定到审批哈希；
- 单写者、journal、逐文件原子替换和确定性回滚；
- 来源同一性与独立性折叠；
- 派生检索缓存的逐级哈希失效与整组回退；
- 外部能力必须显式标注 implemented、metadata-only 或 external-runner-required。

这些仍只是候选输入。本 Source Card 不携带采纳、真值、review verdict 或 action basis。

## 来源信息

- 作者 / 维护者：Daniel Agrici / GitHub contributors
- 发布方：GitHub
- 原始链接：https://github.com/AgriciDaniel/claude-obsidian
- 默认分支：main
- checked commit：1c1bc49c03a685ee8f5d09c99efe52b42d6673f5
- remote main rechecked：2026-08-24，HEAD unchanged
- commit time：2026-08-01T14:03:27+02:00
- commit subject：docs(windows): WSL troubleshooting guide; point UNSUPPORTED_PLATFORM at it (#152)
- plugin version：2.1.0
- license：MIT，Copyright 2026 AgriciDaniel (AI Marketing Hub)
- source_status：active
- 采集方式：git ls-remote + shallow clone + git archive HEAD
- 本地快照：raw/repos/_snapshots/2026-08-24-AgriciDaniel-claude-obsidian-1c1bc49-source.zip
- 快照 SHA256：260c4e7aba4d85b08c79aee18f703c16dc3403c78d0b9fd513b6f3d8c26a049f
- 快照大小：1,610,769 bytes
- archive entries：280
- tracked files：201

## Intake Boundary

    processing_tier: heavy
    knowledge_status: raw
    overlay_state: none
    review_pressure: none
    action_basis_allowed: false
    truth_mutation_allowed: false

强蒸馏只提高静态抽取深度，不自动提高知识地位。本次没有运行 tests、仓库脚本、hook、Obsidian、WSL 写路径、模型、外部 runner 或网络适配器。

## Inspected Repository Areas

| Area | Anchor | Why inspected |
|---|---|---|
| Product boundary | README.md; AGENTS.md:3-47 | 核对公开故事、Skills 与 deterministic core 的职责划分。 |
| Vault selection | claude_obsidian/paths.py:178-413 | 核对显式 vault、配置优先级、containment 和插件树拒绝。 |
| Capture preflight | claude_obsidian/capture.py:408-705 | 核对 budget、可见 inbox、symlink/alias、TOCTOU 和 hash。 |
| Content-addressed capture | claude_obsidian/capture.py:865-1029 | 核对 SHA-256 目的路径、批事务与 inbox 保留。 |
| External action plan | claude_obsidian/capture.py:1045-1217 | 核对 URL 安全、显式同意和 inert argv plan。 |
| Transaction contract | skills/wiki/references/operation-transactions.md:5-139 | 核对 single orchestrator、inspect、approval、apply、recovery。 |
| Approval binding | claude_obsidian/transaction.py:1287-1308 | 核对 approval hash 的输入边界。 |
| Mutation lock | claude_obsidian/transaction.py:1646-1813 | 核对 vault lock、process token、pinned descriptors。 |
| Write authority | claude_obsidian/transaction.py:3130-3235 | 核对 operation type 对允许写路径的机械限制。 |
| Prospective validation | claude_obsidian/transaction.py:3506-3623 | 核对 source/claim ledger 成对的 prospective-state validation。 |
| Inspect/apply/recovery | claude_obsidian/transaction.py:4098-4680 | 核对 journal、expected hashes、atomic replace、rollback、idempotency。 |
| Source/claim provenance | skills/wiki/references/provenance.md:14-49; claude_obsidian/ledgers.py:407-1165 | 核对 source identity、freshness、independence、accepted/contested 条件。 |
| Claim ceiling | claude_obsidian/ledgers.py:1030-1150 | 核对 locator、reviewed_at、支持来源和 contradiction 的实际校验上限。 |
| Query contract | skills/wiki-query/SKILL.md:8-96 | 核对 hot 仅 orientation、分档查询、fallback 和 read-only。 |
| Retrieval cache | scripts/contextual-prefix.py; scripts/bm25-index.py; scripts/retrieve.py; scripts/rerank.py | 核对 chunk/index/page hash、失效和 rerank 全组回退。 |
| Retrieval eligibility | scripts/contextual-prefix.py:834-849; scripts/retrieve.py:259-365 | 核对全量 wiki Markdown 收集与 ledger 脱钩风险。 |
| Session context | claude_obsidian/hook_adapter.py:25-214; hooks/README.md | 核对 opt-in、32 KiB、untrusted envelope 与 hook 不写。 |
| Research split | skills/autoresearch/SKILL.md:27-121 | 核对预算、counter-position、dossier 与 canonical merge 分离。 |
| Save/Ingest/Fold | skills/save/SKILL.md; skills/wiki-ingest/SKILL.md; skills/wiki-fold/SKILL.md | 核对显式写入、hot/log/index 约定和 fold 不产生证据。 |
| Release sanitizer | claude_obsidian/release.py:246-405,685-1079,2391-2588 | 核对 clean snapshot、allowlist、secret/path scan、deterministic build。 |
| Capability honesty | config/adapters.json; config/capabilities.json; config/product-contract.json | 核对实现成熟度、verifier 和未验证工作流的公开上限。 |
| Windows/WSL | docs/windows-wsl.md:7-71 | 核对 native Windows read-only、WSL 写支持和文件身份要求。 |

## 初步看点

1. 最强机制是 execution integrity，不是 epistemic authority。
2. VAKS Operation Receipt 可描述谁、为何、凭什么、获何种写权限；本仓库 transaction 可描述写到哪个 vault、哪些字节、哪些模式，以及失败如何恢复。两者未来可以互补，但当前不应直接接线。
3. Capture Store 的 create-only 内容寻址和可见 inbox 与 VAKS 当前 Capture/Provenance 方向高度相容。
4. Source identity、refresh_due 和独立性归并可作为 Evidence Sufficiency 的维护 lint，但不能以来源数量自动生成真值。
5. 检索缓存完整性做得扎实；检索 eligibility 却弱，默认遍历 wiki 下所有非隐藏 Markdown，不能直接沿用到 VAKS action context。
6. hot.md 是显式 Save/Ingest/Autoresearch 刷新的 bounded briefing；hook 默认关闭且只读。它不是自治记忆、证据或 transcript。
7. Query/Save 分离、research dossier/canonical merge 分离、parallel workers draft-only 都验证了 VAKS 现有严格边界。

## 明显疑点

- accepted claim 只要求 reviewed_at、fresh support 和少量 contradiction 处理；没有 reviewer identity、warrant、必填 source span、support-bearing 检查、scope、omission 或 temporal applicability。
- evidence.locator 可为空，confidence 只是自由枚举；结构通过不等于证据通过。
- Skill 要求 Ingest 同批更新 page/source ledger/claim ledger/index/log/hot，但 transaction core 没有普遍强制这些耦合。
- retrieval engine 不读取 claim/source ledger，也不按 candidate/reviewed/hot/log/meta 做 eligibility 分层。
- apply_bundle 的 Python API 本身可不传 approved plan hash；CLI/orchestrator 才强制。事务完整性不能单独视为行动授权。
- Python core 能阻止通过它执行的越权写，不能阻止 agent 绕过 core 直接改普通文件。
- 4680 行 transaction.py 和脚本对私有内部函数的引用意味着整套搬运成本高、耦合深。
- Compounding loop 缺少 VAKS 意义上的 action basis、outcome calibration、Use Ledger、feedback 和 review_due 传播。
- native Windows 写入明确拒绝；当前 Windows/H: vault 不适合未经设计就直接安装运行。
- release 扫描是 defense in depth，不是通用泄密证明；其中还有项目特定的私有仓库片段规则。

## 可抽取 Candidate Points

1. Authority receipt 与 execution plan 必须明确分层，再以审批哈希绑定。
2. 一次逻辑操作只允许一个 orchestrator、一个 bundle、一个 apply 和一份 exact changed-path receipt。
3. Operation type 应成为真实写能力边界，而不仅是日志标签。
4. Capture 应采用 visible inbox、bounded preflight、content-addressed create-only snapshot 和 no implicit delete。
5. 来源同一性、字节重复和 independence key 应传递式折叠，避免把转述链算成多个独立来源。
6. 派生检索缓存应保存 page/chunk/index hash，失效时 fail closed，模型 rerank 失败应整组回退。
7. 未实现的外部能力只生成 inert consent plan，不伪装已执行。
8. hot 只应是 scoped orientation briefing，并以 untrusted data 注入；不能叫 truth 或 memory tier。
9. Query 与 Save、research dossier 与 canonical merge 必须是不同权限操作。
10. Ledger validator 只能作为结构 lint / review input，不能替代 VAKS Evidence Packet 和 Promotion Gate。

## Source Annotation Sidecars

本次创建 12 个精确源码 locator，位于：

outputs/review/source_annotations/2026-08-24-AgriciDaniel-claude-obsidian/

它们分别固定 approval binding、single-writer transaction、operation write authority、content-addressed capture、provenance split、claim validator ceiling、hot opt-in、retrieval eligibility gap、external action plan、release snapshot、Windows fail-closed 和 research/canonical split。

每个 annotation 均为 candidate locator：

    support_checked: false
    evidence_support_status: not_checked
    action_basis_allowed: false
    truth_mutation_allowed: false

## 后续去向

- 候选蒸馏：outputs/review/2026-08-24-AgriciDaniel-claude-obsidian-candidate-distillation.md
- 架构评审：wiki/summaries/2026-08-24-AgriciDaniel-claude-obsidian-architecture-review.md
- VAKS Project Overlay：outputs/review/project_overlays/2026-08-24-AgriciDaniel-claude-obsidian-vaks-transaction-and-evidence-overlay.md

## License Note

源码按 MIT 许可证发布。本次仅保存固定源快照、静态分析、短 locator 和候选设计抽取；未复制其运行时到 VAKS，也未将上游结论标记为 VAKS 正式知识。

