---
record_kind: architecture_upgrade_plan
status: draft
created_at: 2026-06-14
target_system: VAKS
truth_boundary: planning_and_research_only_not_architecture_change
write_scope: outputs_review_single_document
schema_change: none
reviewed_knowledge_change: none
---

# VAKS Architecture Upgrade Plan

## 0. Read Me First

这份文档是架构升级调研和开发规划，不是主架构修改。

本次只落一份规划文档，不修改：

```text
SCHEMA.md
FUSION_ARCHITECTURE_V0_2_DRAFT.md
ARCHITECTURE_PRINCIPLES.md
README.md
reviewed claims / decisions / patterns
templates/
tools/
wiki/bases/
```

核心判断：

```text
VAKS 现在不缺更大的 RAG、图数据库或 agent 平台。
VAKS 缺的是把现有强边界变成收据、validator、failure matrix、工作台和真实只读试跑。
```

一句话版本：

```text
别人强在“找得到、聊得顺、记得住”。
VAKS 要强在“这东西能不能作为行动依据，谁批准了哪个版本，证据够不够，风险有没有露出来”。
```

## 1. Executive Verdict

VAKS 当前架构主干是对的：

```text
Capture -> Understand -> Review -> Connect -> Act and Learn
```

内部链路也已经清楚：

```text
source
-> candidate points
-> calibration / point collision
-> review
-> reviewed node / reviewed relation
-> context pack / action basis
-> action
-> feedback
```

真正短板不是“概念不够高级”，而是“工程闸门还不够硬”：

- review 对象需要固定到 exact body hash。
- support 需要从 citation/rank/summary 里解耦出来。
- action readiness 需要独立于 answer-ready 和 truth status。
- retrieval 需要 receipt，证明 selected_by 不是 support。
- feedback 需要 validator，证明 feedback 只改 activation/review pressure，不改 truth。
- agent/plugin/tool write 需要 operation receipt，证明谁基于什么依据做了什么，并且能回滚。
- Bases/workbench 需要清楚显示状态，但不能变成 truth/approval/schema。

升级方向：

```text
保留主干。
不重写 schema。
不先上重型 runtime。
先把每个 action-facing 环节做成可检查、可拒绝、可复盘。
```

## 2. Current State Facts

只读核验到的当前事实：

- 目标规划文档在写入前不存在：`outputs/review/vaks-architecture-upgrade-plan-2026-06-13.md`。
- 工作区已有大量预存改动，写入前 `git status --porcelain=v1` 计数为 220。
- 当前 `wiki/bases/` 只有：
  - `claims.base`
  - `decisions.base`
  - `patterns.base`
  - `sources.base`
- 当前 `tools/` 里已有 Source Intake 系列 validator：
  - `validate_source_intake_contract.py`
  - `validate_source_intake_failure_matrix.py`
  - `validate_source_intake_hardening_package.py`
- 下面这些计划中的 P0/P1/P2 工程件在写入前不存在：
  - `templates/retrieval-receipt.md`
  - `templates/operation-receipt.md`
  - `tools/validate_review_candidate_body_hash.py`
  - `tools/validate_support_boundary.py`
  - `tools/validate_action_readiness.py`
  - `tools/validate_feedback_events.py`
  - `tools/validate_retrieval_receipts.py`
  - `tools/validate_operation_receipts.py`
  - `wiki/bases/review-candidates.base`
  - `wiki/bases/context-packs.base`
  - `wiki/bases/feedback-events.base`
  - `wiki/bases/operator-cockpit.base`

这个文档只规划这些工程件，不实现它们。

## 3. Non-Negotiable Boundaries

这些边界不能破：

```text
Only reviewed evidence can support action.
Feedback improves activation, not truth.
Retrieval finds candidates; it does not verify them.
Context Pack prepares attention; it is not action basis by itself.
Operation Receipt records action basis and write intent; it does not create truth.
```

禁止项：

- 不把 candidate summary 当 support。
- 不把 URL-only citation 当 direct support。
- 不把 source summary 当 independent anchor。
- 不把 retrieval rank、semantic score、graph rank 当 trust/confidence。
- 不把 feedback 当 truth mutation。
- 不把 Base/dashboard 当 schema、approval 或 reviewed truth。
- 不把 plugin/agent memory 当 reviewed memory。
- 不让 MCP write、watch scripts、bulk scripts、Obsidian sync 绕过 review queue。
- 不把 auto-extracted relation 直接写成 reviewed relation。
- 不把 runtime/test artifact 放进默认 retrieval/support。

## 4. Evidence Map

本规划依据当前本地架构文件，不靠聊天记忆单独判断。

| Planning claim | Local evidence |
|---|---|
| Only reviewed evidence can support action | `README.md`, `FUSION_ARCHITECTURE_V0_2_DRAFT.md`, `ARCHITECTURE_PRINCIPLES.md` |
| Feedback improves activation, not truth | `README.md`, `FEEDBACK.md`, `templates/feedback-event.md` |
| Context pack is not action basis by itself | `SCHEMA.md`, `IMPLEMENTATION_BLUEPRINT.md`, `templates/context-pack-manifest.md`, `DEV_CONTEXT.md` |
| Review object must be fixed by body hash | `REVIEW_QUEUE.md`, `templates/review-candidate.md` |
| Source Intake uses orthogonal fields and fail-closed enum | `SOURCE_INTAKE.md`, `tools/source_intake_enum_registry.json` |
| External repo/paper review needs source/code anchors | `REFERENCE_REVIEW_PROTOCOL.md`, `templates/library-review.md` |
| Activation Tier is not truth tier | `MEMORY_TIER.md`, `SECOND_BRAIN_MODEL.md` |
| Bases/workbench are views, not authority | `ARCHITECTURE_PRINCIPLES.md`, `wiki/summaries/2026-05-26-obsidian-base-hub-view-layer-review.md`, `wiki/summaries/2026-06-12-breferrari-obsidian-mind-architecture-review.md` |
| Runtime read-only loop is not production proof yet | `outputs/review/source-intake-runtime-readonly-loop-2026-06-13/RUNTIME_READONLY_LOOP_REPORT.md`, `outputs/review/source-intake-runtime-readonly-loop-2026-06-13/RUNTIME_AUDIT_RESPONSE.md` |

## 5. Full Architecture Upgrade By Link

### 5.1 Capture / Provenance

Current gap:

- Source identity, capture activity, extraction activity, human/model/tool trace are present conceptually, but not fully receipt-shaped.

Upgrade:

- Add lightweight receipt language for source/activity/agent.
- Keep source records light.
- Put review, promotion, context-pack usage, operation usage into their own records rather than stuffing Source nodes.

Borrow:

- W3C PROV: entity/activity/agent idea.

Reject:

- Full provenance ontology.
- Graph stack as required runtime.
- Source-node usage ledger that makes source cards heavy.

Acceptance:

- A future source/action trace can answer: what was captured, by whom/what, when, by which extraction path, and where the raw anchor lives.

### 5.2 Source Intake

Current gap:

- Structural Source Intake lint exists.
- Semantic migration debt still exists.
- Some operational checks are not yet connected to query/action loops.

Upgrade:

- Keep the current orthogonal fields:
  - `processing_tier`
  - `knowledge_status`
  - `overlay_state`
  - `review_pressure`
  - `retrieval_policy`
  - `promotion_gate`
- Add semantic-debt queue as operational work, not schema rewrite.
- Make receipt validators consume the same enum registry and fail closed.
- Add a future raw parser router / extraction bundle path for messy inputs, where parser output remains raw/candidate and must preserve original hash, parser config, retained outputs, anchors, and boundary flags.

Borrow:

- Existing Source Intake hardening package.
- OmniParse-style multimodal intake router as design reference only.

Reject:

- Collapsing `processing_tier` into authority.
- Treating heavy processing as reviewed status.
- Treating parser Markdown, OCR/VLM output, transcript text, or crawler text as reviewed evidence.

Acceptance:

- Raw/candidate/overlay/feedback surfaces cannot allow action basis or truth mutation.

### 5.3 Candidate Distillation

Current gap:

- Candidate records can be useful enough that users or agents may treat them as conclusions.

Upgrade:

- Candidate points must carry:
  - source references
  - provisional status
  - scope
  - allowed use
  - warning code
  - promotion gate
- Candidate is review input, never action basis.

Borrow:

- VERISCORE-style verifiability routing.

Reject:

- Turning candidate point into atomic truth claim by default.
- Using a metric/evaluator pipeline as truth authority.

Acceptance:

- Candidate can help orientation or review, but validator blocks it as support/action basis.

### 5.4 Review Candidate / Body Hash

Current gap:

- Review can approve a body, but if the body changes later, the approval may drift.

Upgrade:

- Enforce body hash validator for review candidates.
- Hash algorithm:

```text
sha256_utf8_lf_trim_body_without_heading
```

Rules:

- Resolve `candidate_body_location`.
- Exclude the heading.
- Normalize CRLF to LF.
- Trim leading/trailing whitespace.
- SHA256 UTF-8.
- Compare with `body_hash`.
- If `approval_integrity.checked_body_hash` exists, it must match too.

Acceptance:

- Any post-review body edit forces review state back to review.

### 5.5 Evidence Packet

Current gap:

- Evidence Packet exists as design, but not enough tooling forces its use for promotion/action.

Upgrade:

Evidence Packet must make visible:

- point
- evidence item
- source anchor
- warrant
- scope limit
- risk
- gap
- strongest rebuttal
- omission check when needed
- minimal revision

Borrow:

- PaperTrail: claim/point coverage and progressive disclosure.
- ProVe/RAG attribution work: citation correctness is not the same as support.

Reject:

- Automated NLI/RTE/support scores as authority.
- Exhaustive omission scan for ordinary query.

Acceptance:

- Promotion/action/strong relation cannot rely on loose source summaries.

### 5.6 Evidence Support Check

Current gap:

- URL, citation, rank, source summary, candidate note, or prior chat can be mistaken as support.

Upgrade:

Add `validate_support_boundary.py`.

Hard errors:

- candidate marked as `support`
- URL-only citation marked `direct_support`
- retrieval score / graph rank / semantic score used as trust
- feedback event used as support
- `legacy_raw_metadata` selected as support anchor
- source summary supports its own extracted claim without independent anchor
- claim note supports itself
- `background_context` counted as supported
- `inferential_support` without reviewer_note counted as promotion support

Acceptance:

- Support means the evidence bears on the specific point/relation under scope.

### 5.7 Evidence Sufficiency / Action Readiness

Current gap:

- There is a dangerous gap between “has some evidence” and “safe action basis”.

Upgrade:

Add `validate_action_readiness.py`.

Block `action_readiness: ready` when:

- `evidence_sufficiency` is `insufficient`
- `evidence_sufficiency` is `out_of_scope`
- point is stale/superseded/out_of_scope without replacement basis
- key risk is unresolved
- key warning/gap/missing evidence was trimmed
- intent confirmation is required but missing
- action basis relies on candidate, feedback, retrieval rank, or source summary

Borrow:

- Self-RAG / CRAG / A2RAG: escalate only when evidence is insufficient for intended use.

Reject:

- Automatic retrieve-more loop as default.
- Action readiness from retrieval confidence.

Acceptance:

- A cautious answer may pass while action-ready remains blocked.

### 5.8 Calibration / Point Collision

Current gap:

- Candidate/local conflicts are visible conceptually, but risk becoming noisy or auto-decisive.

Upgrade:

- Keep collision as review pressure and routing, not truth.
- Collision outputs:
  - supports
  - contradicts
  - refines
  - risk_of
  - derived_from
  - missing_evidence
  - stale_assumption
  - decision_superseded
  - review_question

Borrow:

- Truth Maintenance System / Reason Maintenance: reasons and contradiction pressure.
- Dung abstract argumentation: support/challenge/standing-check habit.

Reject:

- Automatic truth machine.
- Formal argumentation semantics as runtime requirement.

Acceptance:

- Collision creates review work, not reviewed truth.

### 5.9 Review-Gated Writeback

Current gap:

- Candidate-to-reviewed writeback needs exact object, approval, support, sufficiency, and operation trace.

Upgrade:

- Writeback queue must require:
  - fixed candidate body
  - body hash
  - Evidence Packet
  - support check
  - sufficiency check
  - approval integrity
  - operation receipt when tool/agent/action is involved

Borrow:

- RKA review queue taxonomy, decision superseding, intent confirmation, maintenance manifest, confidence cap, outcome calibration.

Reject:

- RKA runtime, MCP, dashboard, SQLite truth source.

Acceptance:

- Nothing writes formal reviewed knowledge just because a tool, script, or reviewer said “looks good”.

### 5.10 Reviewed Nodes

Current gap:

- Reviewed nodes are strong, but future tooling must not bypass them.

Upgrade:

- Reviewed claim/pattern/anti-pattern/decision remains Markdown/YAML source of record.
- Runtime index/API/vector/graph output stays derived.
- If derived artifact disagrees with Markdown record, Markdown wins until reviewed update.

Acceptance:

- No plugin/runtime output can override reviewed node fields.

### 5.11 Reviewed Relations

Current gap:

- Graph relation suggestions are useful, but easy to confuse with reviewed relations.

Upgrade:

- Keep candidate relations separate from reviewed relations.
- Strong reviewed relation needs evidence for the edge itself, not just both endpoint nodes.

Borrow:

- GraphFC / GraphRAG: relation decomposition as review aid.

Reject:

- Auto-extracted triple as reviewed relation.
- Graph traversal as support.

Acceptance:

- `candidate_relation` cannot enter formal graph without review.

### 5.12 Retrieval

Current gap:

- Retrieval is powerful enough to look authoritative.

Upgrade:

Add `templates/retrieval-receipt.md` and `validate_retrieval_receipts.py`.

Receipt must expose:

- query id/time/mode
- requested authority bucket
- included buckets
- excluded buckets
- `rrf_scope: same_authority_bucket_only`
- retrieval engines
- retrieval filters
- selected items
- excluded items
- selected_by
- support checks
- warnings
- gaps

Borrow:

- BM25/vector/RRF/QMD/GraphRAG/LightRAG as recall aids.

Reject:

- Retrieval rank as trust.
- Cross-bucket rank mixing as authority.

Acceptance:

- Retrieval can decide what to read next, not what to believe or act on.

### 5.13 Activation Tier

Current gap:

- Hot/warm/cold can be mistaken as confidence.

Upgrade:

- Public wording: Activation Tier.
- Hot means read early, not believe more.
- Activation can be affected by feedback, recency, project context, and use, but not truth confidence.

Borrow:

- MemGPT / Mem0: fast/slow context and memory paging intuition.

Reject:

- Agent OS.
- Autonomous memory manager as truth system.

Acceptance:

- Activation fields cannot increase truth confidence or action readiness.

### 5.14 Context Pack

Current gap:

- Context Pack prepares attention, but users/agents may treat it as action basis.

Upgrade:

Context Pack must show:

- coverage overview
- key used points
- support checks
- warnings
- gaps
- risk flags
- stale/superseded/out_of_scope notes
- action readiness
- evidence sufficiency
- source-window loss if trimmed

Acceptance:

- Pack can be useful for orientation while action readiness is `not_ready`.

### 5.15 Temporal Applicability

Current gap:

- A standing reviewed point can be stale or out of scope for a current action.

Upgrade:

- Check time/version/project/environment/scope before action-ready.
- Preserve historical decisions.
- Superseded decision is linked, not deleted.

Borrow:

- Graphiti / Zep temporal knowledge graph: validity windows, supersession, episode/source traceability.

Reject:

- Automatic graph invalidation as truth.
- Graph database as Markdown source of record.

Acceptance:

- Stale/superseded/out_of_scope item can appear as background, but cannot create ready action basis without replacement basis or narrowed scope.

### 5.16 Decision / Action

Current gap:

- Decision/action can over-trust context pack output.

Upgrade:

Add `templates/operation-receipt.md` and `validate_operation_receipts.py`.

Operation Receipt must show:

- actor
- actor tier
- operation mode
- intent confirmation
- basis
- target paths
- proposed changes
- approval
- rollback
- result

Acceptance:

- Read-only/suggest-only actor cannot write.
- Reviewed write needs approval and checked body hash.
- Schema change needs owner-final.
- Destructive operation needs rollback plan.

### 5.17 Feedback

Current gap:

- Feedback is useful enough that it may be mistaken for truth update.

Upgrade:

Add `validate_feedback_events.py`.

Rules:

- positive feedback is weak
- negative feedback creates review pressure
- explicit correction creates review_due
- feedback cannot change truth confidence
- feedback cannot change verification status
- feedback cannot change source reliability
- feedback cannot mutate reviewed note/relation directly

Borrow:

- Reflexion / Reflective Memory Management: feedback as use-memory and future routing.

Reject:

- Hidden reinforcement learning over reviewed knowledge.

Acceptance:

- Feedback improves future activation and review routing, not truth.

### 5.18 Agent Gateway

Current gap:

- Future agent/plugin/MCP write paths are the biggest way to break VAKS.

Upgrade:

Permission tiers:

| Tier | Role | May do | Must not do |
|---|---|---|---|
| L1 | Plugin/search | read, retrieve, display | write reviewed knowledge |
| L2 | Agent suggest | propose, summarize, draft | direct action/writeback |
| L3 | Candidate writer | write candidate/receipt | promote |
| L4 | Reviewer | review evidence, approve exact body | owner-final schema/destructive action |
| L5 | Owner | final approve, schema unlock, destructive operation | bypass receipt |

Borrow:

- Geminese: visible Plan/Agent mode and context chips.
- Kova: quick capture and visible tool stream.
- Copilot: context selection and chat UI.

Reject:

- Direct note mutation as trusted write.
- Plaintext broad file tools without receipt.

Acceptance:

- Agent may suggest or create candidate-only records, but cannot write reviewed layer without review gate.

### 5.19 Workbench / Bases

Current gap:

- Bases currently cover only basic reviewed surfaces.
- Review, context, feedback, and operator cockpit are not visible enough.

Upgrade:

Add four Bases later:

- `wiki/bases/review-candidates.base`
- `wiki/bases/context-packs.base`
- `wiki/bases/feedback-events.base`
- `wiki/bases/operator-cockpit.base`

Rules:

- Base displays state.
- Base filters work.
- Base does not approve.
- Base does not define schema.
- Base does not create truth.

Borrow:

- Obsidian Bases / Base Hub.
- Dusk/Kepano-style workbench.
- Obsidian Mind Bases/workbench pattern.

Acceptance:

- Operator can see missing evidence, stale anchors, hash mismatch, action_not_ready, review_due, and blocked items.

### 5.20 Product Workflow

Current gap:

- VAKS is architecture-rich but product surface is still too engineering-shaped.

Upgrade:

Seven user entries:

1. Add Source
2. Process This
3. Ask What Vault Knows
4. Check Vault
5. Make Context Pack
6. Review Candidates
7. Record Feedback

Rules:

- User sees simple verbs.
- System keeps strict boundaries in the background.
- Product labels must not imply truth before review.

Borrow:

- Dify / AnythingLLM for workflow product shape.

Reject:

- Workflow node as truth authority.

Acceptance:

- A non-schema user can operate the system without accidentally promoting candidates or acting on weak evidence.

## 6. External Fit Matrix

| Source / tool | Use in VAKS | Boundary |
|---|---|---|
| Obsidian Bases | Workbench and review views | View only, not truth/schema |
| Smart Connections | Activation/discovery | Retrieval signal, not support |
| Omnisearch | Fast recall | Search result, not support |
| mdvs | Markdown frontmatter validation, vault health lint, local hybrid search sidecar | Valid metadata/search rank is not reviewed truth, support, or action readiness |
| agentmemory | MISA runtime memory, Hermes/MCP bridge, project/agent-scoped recall, VAKS context-pack adapter reference | Runtime memory is not reviewed knowledge; MISA writeback limited to feedback/candidate/review_due through receipts |
| Obsidian Copilot | Context UX reference | Must stay suggest-only/candidate-only |
| Geminese | Permission modes/context chips/MCP-on-demand inspiration | Do not import direct write authority |
| Kova | Quick capture/tool stream inspiration | Do not import SQLite truth or direct mutation |
| Obsidian Mind | Workbench/lifecycle hooks inspiration | Not truth/review authority |
| Microsoft GraphRAG / LightRAG | Retrieval strata, TextUnit anchors, local/global/DRIFT route design | Community summary not truth; graph rank not trust; extracted graph edge not reviewed relation |
| Kwipu | Local Obsidian/Markdown Graph RAG sidecar: wikilink/frontmatter candidate triples, vector+BM25+temporal retrieval, derived-cache lifecycle, thin read-only MCP query | Derived retrieval/cache only; triples are not reviewed relations; MCP stays read-only/suggest-only; cited answer is not support/action basis |
| OmniParse | Raw intake parser router and extraction bundle reference for documents/images/audio/video/web | Parser output is raw/candidate only; no reviewed truth/action basis; license/runtime must be sandboxed |
| Reminds | Personal knowledge product UX: quick capture, card/note split, local-first sync, onboarding, constrained MCP/LLM entry | Do not turn VAKS into generic card notes; AI recommendation and graph views are not evidence/review/truth |
| TimeFriend / Timarkin | Product workbench UX: time/block timeline, heatmap/calendar, low-friction capture, AI-after-data, export package, cross-device entry | Do not turn VAKS into time management; activity/heat/usage signals are activation only, not confidence/support/action readiness |
| kk-knowledge-agent | MISA external knowledge-base bridge reference: thin MCP tool -> backend retrieval core -> returned context | MISA read/list first; write tools candidate/feedback only; retrieval score/chunk is activation, not VAKS support or memory truth |
| Graphiti / Zep | Temporal applicability | No automatic graph truth |
| Mem0 / MemGPT | Activation/memory UX | Memory is not reviewed knowledge |
| Dify / AnythingLLM | Product workflow shell | Workflow execution is not evidence |
| RKA | Review queue/intent/outcome calibration | Do not import runtime/SQLite/MCP |

## 6.1 Robust RAG Diagram Integration Plan

Source:

```text
User-provided diagram: "Building a Robust RAG System"
```

This diagram is useful, but it belongs in the retrieval/indexing/query-routing
layer. It is not a replacement for VAKS review, evidence, action-readiness, or
writeback boundaries.

Plain-language judgment:

```text
The diagram is a strong "find better context" architecture.
VAKS is a "can this become trusted action basis?" architecture.
Borrow the retrieval engineering.
Do not borrow any implication that better retrieval equals verified knowledge.
```

### 6.1.1 What The Diagram Adds

The diagram covers six RAG engineering blocks:

| Diagram block | Meaning | VAKS placement |
|---|---|---|
| Query Construction | Translate a question into DB/vector/graph/search queries | Query planner + retrieval receipt |
| Routing | Choose graph DB, relational DB, vector store, prompt route, or semantic route | `query_mode` + authority bucket router |
| Indexing | Semantic split, multi-representation indexing, hierarchical indexing, RAPTOR | Derived retrieval/index layer |
| Retrieval | Refinement and reranking | Selected-items preparation, never support by itself |
| Generation | Self-RAG, RRF, active retrieval | Answer drafting, before support/action gates |
| Evals | RAGAS, DeepEval, GroUSE style diagnostics | Maintenance lint only, not reviewer approval |

### 6.1.2 What VAKS Already Does Better

VAKS has boundaries that the diagram does not show:

- citation is not support by itself;
- retrieval score is not trust;
- graph rank is not reviewed relation;
- generated answer is not action basis;
- eval pass is not review approval;
- feedback does not change truth;
- stale/superseded/out-of-scope knowledge cannot become ready action basis;
- agent/tool writes need permission tier and operation receipt.

So the diagram can strengthen recall, but VAKS must still decide:

```text
What is evidence?
What is reviewed?
What is merely candidate?
What is action-ready?
Who approved which exact body?
What risk/gap remains visible?
```

### 6.1.3 Borrowable Design Set

Borrow these as a retrieval-enhancement set:

1. Query Construction Pack
   - Convert user input into explicit retrieval intent.
   - Emit `question_summary`, `verbatim_input`, `query_mode`, `requested_authority_bucket`.
   - Do not rewrite user intent silently for action-sensitive queries.

2. Routing Pack
   - Logical route: choose graph / relational / source / reviewed records based on task.
   - Semantic route: choose prompt/retrieval profile based on intent.
   - Must emit included/excluded buckets in retrieval receipt.

3. Multi-Representation Index Pack
   - Keep source chunks, summaries, entities, candidate points, reviewed nodes, and relation neighborhoods as separate retrieval strata.
   - Do not collapse summaries into support.

4. Hierarchical Index Pack
   - Use RAPTOR-like or tree summaries only for exploration and briefing.
   - Any action-facing support must drill back to raw/reviewed anchors.

5. Refinement / Reranking Pack
   - Use rerankers to order what to inspect next.
   - Persist `selected_by` as trace metadata only.
   - Rerank score must never update confidence or action readiness.

6. Eval Diagnostics Pack
   - Use RAGAS/DeepEval-like checks as lint.
   - Store eval result as diagnostic evidence only.
   - Eval green cannot approve reviewed knowledge.

### 6.1.4 Forbidden Imports

Do not import these assumptions:

- better retrieval means better truth;
- graph DB relation means reviewed relation;
- RRF/rerank score means source reliability;
- generated answer with citations means evidence support;
- Self-RAG self-critique means reviewer approval;
- eval pass means production readiness;
- active retrieval can automatically decide to promote or write back.

### 6.1.5 VAKS Fusion Architecture

The fused retrieval layer should look like this:

```text
User question
-> Query Construction
-> Route selection
-> Bucket-filtered retrieval
-> Multi-representation recall
-> Rerank/refinement
-> Retrieval Receipt
-> Context Pack draft
-> Evidence Support Check
-> Evidence Sufficiency Gate when needed
-> Action Readiness
-> Answer / decision / operation receipt
```

Important split:

```text
Robust RAG layer decides what to read.
VAKS evidence layer decides what can support.
VAKS action layer decides what can be acted on.
```

### 6.1.6 Implementation Package

Add a future package after P1 receipt validators:

```text
P1.5 Robust RAG Retrieval Enhancement Sandbox
```

Artifacts:

- query-construction fixture set
- route-selection fixture set
- indexing-strata manifest
- retrieval-receipt examples for graph/relational/vector routes
- rerank trace examples
- eval diagnostic examples
- failure cases proving retrieval outputs cannot become support without evidence checks

Acceptance cases:

```text
RR-01 query construction preserves verbatim input for action-sensitive tasks
RR-02 route selection records included/excluded authority buckets
RR-03 vector rerank cannot set confidence
RR-04 graph path cannot create reviewed relation
RR-05 RAPTOR/tree summary cannot become action support without raw/reviewed anchor
RR-06 eval pass cannot become reviewer approval
RR-07 generated answer with citation still needs support check for action mode
RR-08 active retrieval cannot auto-promote candidate
```

### 6.1.7 Final Judgment

Adopt this diagram as a retrieval/indexing reference, not as the whole VAKS
architecture.

VAKS is stronger because it adds:

- candidate/reviewed/action separation;
- evidence support boundary;
- evidence sufficiency gate;
- temporal applicability;
- operation receipt;
- feedback quarantine;
- review-gated writeback.

The correct product claim is:

```text
VAKS can use robust RAG to find better context, then use VAKS gates to decide
whether that context is actually support, review input, or action-ready basis.
```

## 6.2 Microsoft GraphRAG Strong Distillation Supplement

Source:

```text
Microsoft GraphRAG
repo: https://github.com/microsoft/graphrag
docs: https://microsoft.github.io/graphrag/
strong distillation: outputs/review/2026-06-14-microsoft-graphrag-strong-distillation.md
checked_at: 2026-06-14
upstream HEAD: 6d02c2355c3fed4c49007572fbe951d73258a37f
package checked: graphrag 3.1.0
```

Plain-language judgment:

```text
GraphRAG is excellent at making a messy corpus easier to retrieve from.
It is not a verified knowledge system.

Use it to improve VAKS' retrieval brain.
Do not let it touch VAKS' truth spine.
```

### 6.2.1 What Microsoft GraphRAG Adds

GraphRAG gives the robust-RAG block more concrete mechanics:

```text
Documents
-> TextUnits
-> Entity / Relationship extraction
-> optional Claim / Covariate extraction
-> Community Detection
-> Community Reports
-> Embeddings
-> Local / Global / DRIFT / Basic query routes
```

The strongest useful pieces are:

| GraphRAG piece | Meaning | VAKS placement |
|---|---|---|
| TextUnit | Source chunk with links to document, extracted entities, relationships, covariates, token count, attributes | Optional heavy-source navigation/anchor manifest |
| Entity / Relationship extraction | LLM-derived graph objects from source text | Candidate graph fragment only |
| Community Report | LLM-generated summary of a cluster/community | Theme briefing, not proof |
| Local Search | Entity-centered expansion into text units, relationships, covariates, and reports | Detail route for context-pack preparation |
| Global Search | Community-report map-reduce for whole-corpus themes | Theme route for broad questions |
| DRIFT Search | Community-level primer plus local follow-up expansion | Bounded exploratory route |
| Query factory / adapters | Separate route engines and indexer-to-query adaptation | Optional adapter/plugin boundary |

### 6.2.2 Why VAKS Still Beats It On Authority

GraphRAG does not solve these VAKS problems:

- whether a source span actually supports a point;
- whether a candidate claim is reviewed;
- whether a graph relation is reviewed;
- whether a community report omitted a fatal counterpoint;
- whether the result is stale, superseded, or out of scope;
- whether evidence is sufficient for action;
- whether an agent/tool write is permitted and reversible;
- whether feedback should create review pressure without mutating truth.

So the fused design remains:

```text
GraphRAG-style retrieval decides what to inspect.
VAKS Evidence Support Check decides what supports.
VAKS Evidence Sufficiency Gate decides whether support is enough.
VAKS Action Readiness decides whether action is allowed.
```

### 6.2.3 Strong Borrow Set

P1 borrow:

```text
TextUnit-style source anchors
explicit query mode in retrieval receipt
local / global / DRIFT route separation
```

P2 borrow:

```text
community reports as theme briefings
adapter boundary between index outputs and query objects
source-to-derived-cache rebuildability
```

P3 watch:

```text
provider/factory modularity
GraphRAG runtime as optional read-only retrieval plugin
prompt tuning / cache / vector-store providers
```

### 6.2.4 Minimal VAKS Addition

Do not add a full GraphRAG subsystem now.

Add only one future P1.5 sandbox slice:

```text
P1.5-RR-GR: GraphRAG-Inspired Retrieval Strata Sandbox
```

Candidate artifacts:

```text
source_text_unit_manifest.example.yml
retrieval_strata_manifest.example.yml
query_mode_receipt.local_entity.example.yml
query_mode_receipt.global_theme.example.yml
query_mode_receipt.drift_explore.example.yml
theme_briefing_with_drilldown.example.md
graph_candidate_fragment.example.yml
graph_rank_not_support.failure.md
community_report_not_truth.failure.md
```

New receipt field candidate:

```yaml
query_mode:
  selected: local_entity | global_theme | drift_explore | basic_vector | hybrid_bucketed
  why_selected:
  authority_buckets_included:
  authority_buckets_excluded:
  selected_context_types:
    - raw_source_anchor
    - candidate_point
    - reviewed_node
    - reviewed_relation_neighborhood
    - theme_briefing
  forbidden_support_types:
    - retrieval_score
    - graph_rank
    - community_report_summary
    - llm_extracted_relation
```

### 6.2.5 Forbidden Imports

Do not import:

- full GraphRAG runtime as required core;
- graph database as VAKS system of record;
- LLM-extracted relation as reviewed relation;
- community report as evidence support;
- graph rank, report rank, relationship weight, or map-reduce rating as trust;
- prompt tuning as evidence calibration;
- query result as action basis;
- automatic graph/index update as truth mutation.

### 6.2.6 Acceptance Cases

```text
GR-01 TextUnit source anchor helps locate evidence but cannot mark support.
GR-02 Local entity route must emit retrieval receipt and selected authority buckets.
GR-03 Global theme route may include community reports only as orientation.
GR-04 DRIFT follow-up expansion must preserve query lineage and user intent.
GR-05 Graph rank / relationship weight / community rank cannot set confidence.
GR-06 LLM-extracted relation cannot create reviewed relation.
GR-07 Community report cannot satisfy sufficiency without raw/reviewed drilldown.
GR-08 Optional GraphRAG plugin stays read-only/suggest-only until validators exist.
```

### 6.2.7 Final Judgment

Microsoft GraphRAG is a strong supplement to the robust-RAG section.

It should upgrade VAKS' retrieval plan from a generic RAG diagram to a concrete
retrieval-strata design:

```text
TextUnits for source navigation.
Community reports for theme briefing.
Local/global/DRIFT routes for query planning.
Retrieval receipt for traceability.
VAKS gates for support, sufficiency, action, and writeback.
```

This is aligned with VAKS' design philosophy because it keeps retrieval powerful
but authority strict.

### 6.2.8 Companion Reference: Kwipu Local Obsidian Graph RAG

Source:

```text
benmaster82/Kwipu
https://github.com/benmaster82/Kwipu
checked_at: 2026-06-14
upstream HEAD: 908f0e4e300578a22c5fadd4538f75ff7ccfc0b6
local records:
  raw/repos/2026-06-14-benmaster82-Kwipu-source.md
  outputs/review/2026-06-14-benmaster82-Kwipu-strong-distillation.md
  wiki/summaries/2026-06-14-benmaster82-Kwipu-architecture-review.md
  outputs/review/project_lens_overlays/2026-06-14-benmaster82-Kwipu-vaks-local-graph-rag-overlay.md
```

Plain-language judgment:

```text
Kwipu is useful because it is small, local, Obsidian-native, and MCP-readable.
It is a good reference for a VAKS retrieval sidecar.
It is not a VAKS authority layer.
```

#### What Kwipu Adds

Kwipu gives the GraphRAG / robust-RAG section a lighter local implementation
reference:

| Kwipu piece | Meaning | VAKS placement |
|---|---|---|
| Wikilink/frontmatter extraction | Turns Obsidian structure into graph triples | Candidate graph fragments only |
| LlamaIndex PropertyGraphIndex | Local property graph over notes | Derived retrieval cache, not source of record |
| Vector + BM25 + temporal + optional synonym retrieval | Hybrid route for local questions | Bucket-filtered retrieval with receipt |
| File watcher + content hash + incremental update | Keeps derived graph fresh enough for local use | Derived-cache lifecycle manifest |
| Embedding-model storage manifest | Detects graph/model mismatch | Cache integrity warning, not truth confidence |
| FastMCP `query_graph` tool | Agent can ask the vault through one thin tool | Read-only MCP entry for MISA/VAKS context |
| Anti-hallucination prompt | Context-only, cite source files, do not guess | Answer discipline, not evidence support |

#### Why VAKS Still Beats It On Authority

Kwipu does not provide:

- authority bucket filtering;
- retrieval receipts;
- independent evidence support checks;
- evidence sufficiency gate;
- action readiness;
- reviewed relation promotion;
- feedback quarantine;
- operation receipts for agent/tool writes.

So the fused design is:

```text
Kwipu-style sidecar finds local context.
VAKS receipt records how it was found.
VAKS support/sufficiency/action gates decide whether it can be used.
```

#### Minimal VAKS Addition

Add a future P1.5 sandbox slice:

```text
P1.5-RR-KW: Local Obsidian Graph RAG Retrieval Sidecar Sandbox
```

Candidate artifacts:

```text
structural_triples.candidate.yml
derived_cache_manifest.example.yml
retrieval_receipt.hybrid_graph.example.yml
mcp_readonly_query_contract.md
graph_rank_not_support.failure.md
auto_triple_not_reviewed_relation.failure.md
prompt_citation_not_action_basis.failure.md
cache_model_mismatch.failure.md
```

Acceptance cases:

```text
KW-01 Wikilink/frontmatter triples are stored as candidate graph fragments only.
KW-02 Hybrid retrieval emits selected_by for vector/BM25/temporal/synonym routes.
KW-03 Retrieval receipt lists included and excluded authority buckets.
KW-04 Graph rank or retrieval score cannot become support.
KW-05 Cited answer cannot become action basis without support/sufficiency gates.
KW-06 MCP server exposes read-only query only.
KW-07 Derived cache manifest records source state, indexer, model, and rebuild boundary.
KW-08 Cache/model mismatch blocks silent use of stale derived index.
```

#### Forbidden Imports

Do not import:

- graph index as VAKS source of record;
- auto-extracted triple as reviewed relation;
- vector/BM25/temporal rank as confidence/support/action readiness;
- generated answer with file citations as evidence support;
- prompt-only anti-hallucination as review approval;
- MCP reviewed-write tools before operation receipts and permission tiers;
- MD5 content-change cache as VAKS provenance hash;
- default cloud-labelled model configuration without locality review.

#### Final Judgment

Kwipu is the most practical lightweight companion to the GraphRAG plan so far.

Use it to make the future retrieval sandbox concrete:

```text
Obsidian-native structural extraction.
Local hybrid retrieval.
Read-only MCP access.
Derived cache lifecycle.
VAKS receipts and gates around all of it.
```

This stays aligned with VAKS because it improves recall and agent access while
keeping authority outside the retrieval runtime.

## 6.3 OmniParse Strong Distillation Supplement

Source:

```text
adithya-s-k/omniparse
https://github.com/adithya-s-k/omniparse
checked_at: 2026-06-14
upstream HEAD: 9d1ae83c46de777427e67b48f82eaca45ad7994a
local records:
  raw/repos/2026-06-14-adithya-s-k-omniparse-source.md
  outputs/review/2026-06-14-adithya-s-k-omniparse-strong-distillation.md
  wiki/summaries/2026-06-14-adithya-s-k-omniparse-architecture-review.md
  outputs/review/project_lens_overlays/2026-06-14-adithya-s-k-omniparse-vaks-raw-intake-overlay.md
```

Plain-language judgment:

```text
OmniParse can help VAKS organize messy raw materials.
It should sit before VAKS knowledge processing, not inside the truth spine.
```

### 6.3.1 What OmniParse Adds

OmniParse is useful as a raw-material parser router:

```text
documents / PDFs / PPT / Word
images / screenshots
audio / video
public web pages
-> structured markdown-like output
-> images / metadata / chunks
```

Its strongest borrowable idea is not the exact codebase. It is the adapter
shape:

```text
raw input
-> modality classifier
-> parser route
-> retained extraction output
-> VAKS source card
-> candidate distillation
-> review only when needed
```

### 6.3.2 VAKS-owned Extraction Bundle

Do not store OmniParse output directly as knowledge.

Wrap any parser output in a VAKS-owned bundle:

```yaml
original:
  path:
  sha256:
  source_type:
parser:
  adapter_name:
  adapter_version:
  runtime:
  model_flags:
  known_limits:
outputs:
  markdown_path:
  json_path:
  images_dir:
  chunks_path:
anchors:
  page_refs: []
  timestamp_refs: []
  region_refs: []
  url_refs: []
boundary:
  knowledge_status: raw
  action_basis_allowed: false
  truth_mutation_allowed: false
```

This bundle is an intake artifact. It can improve reading, search, and candidate
extraction. It cannot support action by itself.

### 6.3.3 Complement To Existing Parser References

OmniParse should not replace the stronger parser lessons already in the vault.

| Reference | Strongest role | VAKS placement |
|---|---|---|
| PaddleOCR | OCR, scanned documents, visual layout, tables/formulas/images | Specialist parser backend candidate |
| RAG-Anything | Typed multimodal element manifest and heavy-source extraction boundary | Source element manifest reference |
| OmniParse | Unified entrypoint across document/image/audio/video/web | Parser router / adapter shell reference |

Fused posture:

```text
VAKS Raw Intake Adapter
  router: OmniParse-like
  OCR/parser backend: PaddleOCR / MarkItDown / future parser
  element manifest: RAG-Anything-like
  authority: VAKS source card + candidate + review gate
```

### 6.3.4 Strong Borrow Set

P1 borrow:

```text
raw intake parser router
VAKS extraction bundle wrapper
lazy modality routing
```

P2 borrow:

```text
external parser service isolation
text/images/metadata/chunks output concept
public-web parser as strictly bounded source capture
```

P3 borrow:

```text
OmniParse itself as sandbox comparison target
Gradio/API surface as optional workbench inspiration
```

### 6.3.5 Forbidden Imports

Do not import:

- parser Markdown as reviewed knowledge;
- parser confidence as truth confidence;
- parser output as action basis;
- full OmniParse runtime as core dependency;
- GPL/Marker-derived code into product code before license review;
- private/account web crawling without explicit authorization;
- always-on heavy parsing for ordinary capture.

### 6.3.6 Minimal VAKS Addition

Do not add a production parser subsystem now.

Add a future sandbox item:

```text
P1.5-RI-OP: OmniParse-inspired Raw Intake Parser Router Sandbox
```

It should test:

```text
clean PDF
scanned Chinese PDF
screenshot image
short audio/video
public web page
```

Pass condition:

```text
original hash retained
parser config saved
markdown/json/images/chunks retained
page/region/timestamp/url anchors available where relevant
source card points to project-visible artifacts
all generated artifacts have action_basis_allowed: false
```

Fail condition:

```text
keep OmniParse as design-only reference
do not add plugin/runtime dependency
```

### 6.3.7 Final Judgment

OmniParse strengthens the source-intake side of the plan.

It does not change the main VAKS philosophy:

```text
Parser decides how to extract raw material.
VAKS decides whether anything can become knowledge.
Review decides whether anything can support action.
```

## 6.4 mdvs Distillation Supplement

Source:

```text
edochi/mdvs
https://github.com/edochi/mdvs
checked_at: 2026-06-14
upstream HEAD: 66ff5f3cc43e1be7160eacd601ef96de6fa2d6f6
observed crate/release: v0.8.0
local records:
  raw/repos/2026-06-14-edochi-mdvs-source.md
  outputs/review/2026-06-14-edochi-mdvs-candidate-distillation.md
  wiki/summaries/2026-06-14-edochi-mdvs-architecture-review.md
  outputs/review/project_lens_overlays/2026-06-14-edochi-mdvs-vaks-validation-search-overlay.md
```

Plain-language judgment:

```text
mdvs is useful for keeping a Markdown vault structurally clean and searchable.
It is not a truth, review, or action-basis layer.
```

### 6.4.1 What mdvs Adds

mdvs adds two sidecar capabilities:

```text
Validation:
  infer/read mdvs.toml
  validate Markdown frontmatter
  enforce path-scoped allowed/required fields
  emit deterministic JSON/text output and exit codes

Search:
  chunk Markdown body
  build a local LanceDB index under .mdvs/
  support semantic / BM25 / hybrid search
  filter by frontmatter with SQL --where
```

The strongest useful split is:

```text
mdvs.toml = visible contract, can be committed/reviewed
.mdvs/ = derived cache, rebuildable, ignored
```

This matches VAKS' own rule:

```text
Markdown files and reviewed records are source of truth.
Indexes, dashboards, caches, and search hits are not authority.
```

### 6.4.2 VAKS Fit

P1 borrow:

```text
frontmatter/schema drift lint
agent post-write check
deterministic `check --no-update --output json`
```

P2 borrow:

```text
local hybrid search with typed frontmatter filters
JSON Schema export/import as interop
vault health/workbench inputs
```

P3 borrow:

```text
agent skill packaging and CLI UX
incremental cache build strategy
```

### 6.4.3 Forbidden Imports

Do not import:

- `mdvs check` pass as review pass;
- valid frontmatter as evidence support;
- search rank/score as trust or confidence;
- inferred `mdvs.toml` as VAKS schema governance;
- `.mdvs/` as committed truth database;
- auto-update in CI/action-facing flows;
- mdvs as replacement for VAKS custom validators.

### 6.4.4 Minimal VAKS Addition

Do not install mdvs as a required system dependency now.

Add a future sandbox item:

```text
P1.5-MDVS: Markdown Validation/Search Sidecar Sandbox
```

The sandbox should run on a copied subset first:

```text
raw/repos/*.md
outputs/review/*candidate-distillation.md
outputs/feedback/*.md
templates/*.md
```

Pass condition:

```text
no source mutation
no truth mutation
no action basis
no committed .mdvs/
manual review of inferred mdvs.toml
mdvs hits labeled activation_only
VAKS validators still run separately
```

### 6.4.5 Final Judgment

mdvs strengthens the validator/search side of the plan.

It is aligned with VAKS because it keeps authority in visible Markdown while
making structure and retrieval easier to audit:

```text
mdvs validates and finds.
VAKS reviews, supports, and decides.
```

## 6.5 agentmemory Distillation Supplement

Source:

```text
rohitg00/agentmemory
https://github.com/rohitg00/agentmemory
checked_at: 2026-06-14
upstream HEAD: f6f9e3cb1385da31f48036868dc3c7fe342b67ba
observed npm/release: v0.9.27
local records:
  raw/repos/2026-06-14-rohitg00-agentmemory-source.md
  outputs/review/2026-06-14-rohitg00-agentmemory-candidate-distillation.md
  wiki/summaries/2026-06-14-rohitg00-agentmemory-architecture-review.md
  outputs/review/project_lens_overlays/2026-06-14-rohitg00-agentmemory-misa-vaks-bridge-overlay.md
```

Plain-language judgment:

```text
agentmemory is useful for MISA runtime continuity and VAKS context access.
It is not useful as VAKS' truth layer.
```

### 6.5.1 What agentmemory Adds

agentmemory adds a mature runtime-memory plane:

```text
hooks / MCP / REST
-> session observations
-> compressed memories / lessons / slots
-> BM25 + vector + graph-style search
-> budgeted context injection
-> retention / working memory / governance
```

The important MISA-specific reference is its Hermes provider shape:

```text
prefetch()
sync_turn()
on_session_end()
on_pre_compress()
on_memory_write()
system_prompt_block()
```

For VAKS, this is a bridge pattern, not an authority pattern.

### 6.5.2 MISA / VAKS Bridge Split

The safe split:

```text
MISA runtime memory:
  session traces, tool results, user preferences, project guidance, pending work

VAKS context adapter:
  read-only source/candidate/reviewed context through context-pack rules

VAKS writeback:
  feedback_event, candidate_signal, review_due only
```

Forbidden split:

```text
MISA runtime memory
-> reviewed claim / pattern / decision
-> action basis ready
```

MISA can become smarter by remembering process, but VAKS must remain the layer
that decides support, sufficiency, review status, applicability, and action
readiness.

### 6.5.3 Strong Borrow Set

P1 borrow:

```text
MISA runtime memory quarantine
project / agent scoped recall
VAKS context-pack read-only adapter
feedback_event / candidate_signal / review_due writeback path
```

P2 borrow:

```text
Hermes lifecycle hooks
MCP/REST adapter boundary
pinned slots for preferences / tool rules / guidance / pending work
retention/access logs as activation signals
runtime memory provenance with sourceObservationIds-style trace
```

P3 borrow:

```text
viewer / governance / forget / audit UX
plugin/skill packaging after agent gateway validators exist
```

### 6.5.4 Forbidden Imports

Do not import:

- agentmemory as VAKS reviewed knowledge layer;
- runtime memory confidence / strength / rank / graph score / retention score as truth confidence;
- lessons/reflections as reviewed claims;
- `memory_save` or `on_memory_write` as direct VAKS writeback;
- Obsidian export into `H:\Obsidian\资料库` as formal knowledge;
- broad MCP save/delete/export tools before permission tiers and operation receipts;
- context injection without authority bucket, warning, and action-readiness labels.

### 6.5.5 Minimal VAKS/MISA Addition

Do not add a production runtime-memory dependency now.

Add a future sandbox item:

```text
P1.5-MISA-MEM: MISA Runtime Memory / VAKS Bridge Sandbox
```

It should test:

```text
MISA session observation
MISA preference/runtime slot
VAKS context pack read-only fetch
MISA feedback_event writeback
MISA candidate_signal writeback
action readiness block when VAKS support is insufficient
```

Pass condition:

```text
MISA can remember runtime context.
MISA can read VAKS context packs.
MISA cannot write reviewed VAKS knowledge.
MISA feedback/corrections become review pressure, not truth.
All action-facing output still passes VAKS action readiness.
```

Fail condition:

```text
keep agentmemory as design-only reference
do not install broad runtime-memory plugin
do not add reviewed-write integration
```

### 6.5.6 Final Judgment

agentmemory strengthens the MISA integration side of the plan.

It is aligned with VAKS only when placed outside the truth spine:

```text
agentmemory-like runtime memory remembers what happened.
VAKS decides what is reviewed, supported, sufficient, and action-ready.
MISA can bridge the two only through receipts and quarantine.
```

### 6.5.7 Companion Reference: kk-knowledge-agent

Source:

```text
kanna12580/kk-knowledge-agent
https://github.com/kanna12580/kk-knowledge-agent
checked_at: 2026-06-14
upstream HEAD: 713cf3ada1d44b7484157d64a75f61f071caa1bb
local records:
  raw/repos/2026-06-14-kanna12580-kk-knowledge-agent-source.md
  outputs/review/2026-06-14-kanna12580-kk-knowledge-agent-candidate-distillation.md
  wiki/summaries/2026-06-14-kanna12580-kk-knowledge-agent-architecture-review.md
  outputs/review/project_lens_overlays/2026-06-14-kanna12580-kk-knowledge-agent-misa-kb-memory-overlay.md
```

Plain-language judgment:

```text
kk-knowledge-agent helps MISA query an external/local knowledge base.
It does not make MISA truly remember.
It is not a VAKS core architecture reference.
```

The useful split:

```text
kk-like layer:
  MISA -> MCP tool -> backend retrieval API -> context chunks

agentmemory-like layer:
  MISA runtime/session memory, preferences, lessons, continuity

VAKS boundary:
  source/candidate/review/action discipline, receipts, write quarantine
```

Borrow only:

```text
backend owns retrieval core
MCP server stays thin
search/list tools come before write tools
local backend calls use explicit URL, timeout, and proxy isolation
retrieved chunks return with warning labels and receipts
```

Do not borrow:

```text
kk retrieval as evidence support
Chroma score as confidence
add_text_document as reviewed-write path
txt-only ingest as source-intake standard
external KB lookup as MISA's memory brain
```

Minimal future item:

```text
P2-MISA-KB: MISA External Knowledge-Base Bridge Sandbox
```

Pass condition:

```text
MISA can search/list context through a thin tool.
Returned context has authority bucket, warning_code, source/anchor ref, and action_basis_allowed=false.
No tool can write reviewed knowledge.
Candidate/feedback writes require receipts.
```

## 6.6 Product Experience Supplement: Reminds + TimeFriend

Sources:

```text
outputs/review/2026-06-14-reminds-app-sandbox-study/reminds-product-design-study.md
outputs/review/2026-06-14-timefriend-sandbox-study/timefriend-product-design-study.md
```

Plain-language judgment:

```text
Reminds teaches VAKS how to make capture feel easy.
TimeFriend teaches VAKS how to make accumulated activity visible.
VAKS should borrow the product shell, not their truth model.
```

These two products are not architecture replacements:

- Reminds is a personal card-note / second-brain product.
- TimeFriend is a personal time-record / analysis product.
- VAKS is a verified-action knowledge system.

Their value is productization:

```text
make users willing to put things in
make system state visible
make review/action boundaries understandable
make export and handoff feel real
```

### 6.6.1 What Reminds Adds

Reminds adds a mature personal-knowledge product loop:

```text
fleeting thought
-> note/card
-> links/tags/star graph
-> review/recall
-> AI answer / MindPilot / content output
```

Borrowable VAKS ideas:

1. Capability-circle page
   - Explain what VAKS can and cannot do in user language.
   - Product wording: "I can orient you, but this is not action-ready yet."
   - Boundary: explanation page is not schema or policy authority.

2. Quick capture / candidate split
   - Reminds separates fleeting input from durable note.
   - VAKS version:

```text
quick capture
-> raw inbox
-> candidate point
-> review candidate
-> reviewed claim/relation only after gates
```

3. Mobile capture, desktop review
   - Phone/share/voice handles raw/candidate intake.
   - Desktop/workbench handles review, evidence packet, context pack, action basis.

4. Thin MCP / LLM entry
   - Reminds has a constrained tool surface.
   - VAKS version should stay narrower and safer:

```text
create_candidate_input
search_context
get_evidence_packet
get_context_pack
append_feedback_event
```

No direct reviewed write tool.

5. Onboarding in plain language
   - Do not start with `Source / Claim / Relation`.
   - Start with:

```text
save material
turn it into candidate points
check evidence
make a context pack
act only when support is enough
record feedback
```

### 6.6.2 What TimeFriend Adds

TimeFriend adds a strong activity/workbench loop:

```text
low-friction record
-> structured event
-> timeline/calendar/heatmap
-> statistics
-> AI explanation
-> todo/review/export
```

Borrowable VAKS ideas:

1. Activity timeline / activation calendar
   - Show when sources entered, candidates were created, reviews happened, decisions changed, feedback arrived.
   - Boundary: timeline is visibility only, not confidence.

2. Review due / stale calendar
   - Show claims/decisions/context packs that are stale, superseded, blocked, or missing support.
   - Boundary: due status creates review pressure, not truth mutation.

3. AI after data, not before data
   - TimeFriend puts AI analysis after structured records/statistics.
   - VAKS version:

```text
source/context/evidence envelope
-> known support/challenge/gaps
-> AI brief
-> action readiness only after gate
```

4. Export packages
   - TimeFriend exports personal reports.
   - VAKS exports stronger packages:

```text
context pack export
evidence packet export
architecture review package
handoff/recovery package
action basis package
```

Each package should include source anchors, hashes, scope, risk, known gaps, and confidence caps.

5. Cross-entry capture
   - Web/App/voice/WeChat/API Token style entries become a design reference for future VAKS/MISA capture.
   - Boundary: all incoming material lands in raw/candidate/feedback quarantine.

### 6.6.3 Combined Productization Borrow Set

Use both products as a P2 product backlog, not as P0/P1 hardening work:

```text
P2-PX-01 Capability Circle / Boundary Page
P2-PX-02 Quick Capture Inbox
P2-PX-03 Candidate Inbox / Review Funnel
P2-PX-04 Activation Timeline / Activity Calendar
P2-PX-05 Review Due Calendar
P2-PX-06 Context Pack / Evidence Packet Export
P2-PX-07 Mobile Capture Shell
P2-PX-08 Thin MCP / LLM Entry Surface
P2-PX-09 Product Onboarding
P2-PX-10 MISA Read-Only Context Entry
```

Screening rule before implementation:

| Candidate | Adopt when | Reject / park when |
|---|---|---|
| Capability page | It clarifies existing boundaries | It tries to define new schema |
| Quick capture | Output is raw/candidate only | It writes reviewed truth |
| Activity timeline | It shows status and links files | It implies activity = trust |
| Heatmap/calendar | It shows activation/review_due | It changes confidence |
| AI brief | It explains an evidence/context envelope | It becomes reviewer/approver |
| Export package | It includes anchors/hash/scope/gaps | It becomes pretty summary only |
| Mobile shell | It captures raw material | It tries to run full review on phone |
| MCP/LLM entry | Tools are read/candidate/feedback only | It exposes reviewed-write |

### 6.6.4 Forbidden Imports

- Generic card-note model as VAKS core.
- Time management as VAKS product identity.
- Star graph, heatmap, usage count, or activity streak as confidence.
- AI recommendation as reviewed relation.
- AI summary as evidence support.
- SQLite/local app store as source of truth for reviewed knowledge.
- Consumer-style onboarding that hides evidence/action boundaries.
- Subscription/member gating as knowledge authority.
- Admin dashboard before validators can block bad paths.

### 6.6.5 Minimal VAKS Addition

Do not build a full product UI now.

Add a later P2 product-experience screening sandbox:

```text
P2-PX: Product Experience Screening Sandbox

Inputs:
- Reminds sandbox study
- TimeFriend sandbox study
- this architecture upgrade plan

Outputs:
- ranked product backlog
- keep/park/reject table
- boundary-safe wireflow
- no schema changes
- no reviewed knowledge writeback
```

Acceptance:

```text
each product feature candidate maps to one VAKS layer
each candidate has boundary and reject condition
no feature can promote truth or action readiness by UI state alone
P0/P1 validators remain prerequisites for action-facing surfaces
```

### 6.6.6 Final Judgment

Reminds and TimeFriend strengthen the product layer of the plan.

They should be used to make VAKS easier to operate:

```text
capture more easily
see state more clearly
export evidence more cleanly
understand boundaries faster
```

They should not change the VAKS spine:

```text
candidate is still candidate
retrieval is still activation
AI is still assistant
feedback still does not mutate truth
action basis still needs evidence and readiness gates
```

## 7. P0 Engineering Package

P0 target:

```text
Make bad action-facing paths impossible or visibly blocked.
```

### P0-00 Planning Document

Artifact:

```text
outputs/review/vaks-architecture-upgrade-plan-2026-06-13.md
```

Acceptance:

```powershell
Test-Path .\outputs\review\vaks-architecture-upgrade-plan-2026-06-13.md
git diff --name-only
```

Expected diff at this stage:

```text
outputs/review/vaks-architecture-upgrade-plan-2026-06-13.md
```

### P0-01 Retrieval Receipt Template

Artifact:

```text
templates/retrieval-receipt.md
```

Minimum frontmatter:

```yaml
record_kind: retrieval_receipt
query_id:
query_time:
query_mode:
requested_authority_bucket:
included_buckets: []
excluded_buckets: []
rrf_scope: same_authority_bucket_only
retrieval_engines: []
retrieval_filters: {}
selected_items: []
excluded_items: []
support_checks: []
warnings: []
gaps: []
support_boundary:
  selected_by_is_not_support: true
  same_bucket_rrf_only: true
  legacy_raw_metadata_excluded: true
```

### P0-02 Operation Receipt Template

Artifact:

```text
templates/operation-receipt.md
```

Minimum frontmatter:

```yaml
record_kind: operation_receipt
operation_id:
actor:
actor_tier: read_only | suggest_only | candidate_write | reviewed_write | owner_final
operation_mode: read | suggest | propose_write | write | delete | schema_change
intent_confirmation:
  required:
  user_confirmed:
basis:
  context_pack_ref:
  reviewed_support_refs: []
  candidate_refs: []
target_paths: []
proposed_changes: []
approval:
  approved_by:
  checked_body_hash:
rollback:
  possible:
  rollback_plan:
result:
  status:
  performed_at:
```

### P0-03 Body Hash Validator

Artifact:

```text
tools/validate_review_candidate_body_hash.py
```

Must block:

- body hash mismatch
- checked body hash mismatch
- fixed/approved review object with missing body hash
- writeback-ready object with changed body

### P0-04 Support Boundary Validator

Artifact:

```text
tools/validate_support_boundary.py
```

Must block:

- candidate as support
- URL-only as direct support
- rank/score as support or trust
- feedback as support
- source summary self-support
- claim note self-support loop
- legacy metadata support
- background context counted as support

### P0-05 Action Readiness Validator

Artifact:

```text
tools/validate_action_readiness.py
```

Must block:

- insufficient evidence but ready
- out_of_scope but ready
- stale/superseded without replacement basis but ready
- unresolved risk but ready
- hidden warning/gap due to trimming
- missing intent confirmation for significant action

### P0-06 Feedback Validator

Artifact:

```text
tools/validate_feedback_events.py
```

Must block:

- feedback modifies truth confidence
- feedback modifies verification status
- feedback modifies source reliability
- feedback mutates reviewed note/relation
- explicit correction without review_due

### P0-07 Failure Matrix

Artifact:

```text
outputs/review/action-boundary-failure-matrix-*/
```

Minimum cases:

```text
AB-01 body_hash mismatch still approved
AB-02 checked_body_hash mismatch writeback
AB-03 candidate item marked support
AB-04 URL-only citation marked direct_support
AB-05 graph_rank marked trust
AB-06 feedback modifies truth_confidence
AB-07 stale point produces ready action basis
AB-08 budget trimming hides missing evidence
AB-09 read-only actor writes file
AB-10 schema change without owner_final
AB-11 destructive operation without rollback
AB-12 retrieval receipt crosses authority buckets
```

## 8. P1 Runtime And Pilot Package

P1 target:

```text
Prove the read-only query loop can honor P0 boundaries under realistic flow.
```

Artifacts:

- `tools/validate_retrieval_receipts.py`
- `tools/validate_operation_receipts.py`
- read-only query loop pilot
- runtime artifact exclusion test
- semantic anchor support check

Pilot stories:

1. Ordinary question: orientation answer, no full audit required.
2. Action-adjacent question: context pack + support check + action readiness required.
3. Candidate temptation: candidate summary looks useful but cannot support action.
4. Stale decision: historical explanation allowed; ready action blocked.
5. Feedback correction: review_due created; truth unchanged.
6. Agent propose write: operation receipt required; no reviewed write.

## 9. P2 Workbench And Product Package

P2 target:

```text
Make the strict system usable without weakening it.
```

### Use-Surface Reality Check

Current operator experience:

```text
VAKS is stable and boundary-clear, but not yet silky.
It feels like a strong knowledge-engineering base, not a finished product surface.
```

Working well:

- layer boundaries are unusually clear: raw, candidate, overlay, reviewed, and action basis do not collapse into one pool;
- source cards, strong distillation, architecture review, overlays, and the total research plan connect cleanly;
- an agent can act safely after reading the manuals because the forbidden paths are explicit;
- the system is much safer than ordinary Obsidian/RAG setups when handling action-facing knowledge.

Still rough:

- too much manual reading is required before a new window can safely act;
- important docs are long and need navigation, summaries, and status surfaces;
- retrieval is still mostly `rg` plus human/agent judgment, not receipt-backed query flow;
- the worktree can contain many unrelated dirty files, so every action requires extra caution;
- Obsidian sync and hash verification work, but feel like an operator procedure rather than a product action;
- ordinary users would not know which button/path corresponds to raw, candidate, review, context pack, or action basis.

Practical scorecard:

| Area | Current feel | Target |
|---|---:|---:|
| Architecture clarity | 8.5/10 | 9/10 |
| Safety boundary | 9/10 | 9.5/10 |
| Agent operability | 7/10 | 8.5/10 |
| Ordinary-user smoothness | 4.5/10 | 8/10 |
| Productized workflow | early | usable |

Optimization principle:

```text
Do not weaken VAKS to make it easy.
Make the strictness visible, navigable, and low-friction.
```

This means the next productization work should not add a new truth model. It
should make the existing layers easier to operate:

- one entry surface for capture / process / ask / review / act;
- short status pages before long manuals;
- receipt-backed search instead of raw top-k trust;
- clear badges for raw / candidate / reviewed / action-ready;
- worktree/sync health shown as operator state;
- safe defaults that prevent reviewed-write, truth mutation, and action basis by UI accident.

Acceptance:

```text
A new user or agent can answer:
Where do I put this?
What state is it in?
Can I use it only for orientation, review input, or action?
What is blocking promotion/action?
What source/hash/receipt proves the system did not silently mutate authority?
```

### Bases

| Base | Purpose | Key columns | Boundary |
|---|---|---|---|
| `review-candidates.base` | Review queue visibility | review_status, review_object_state, body_hash, promotion_target, missing_evidence, risk_flags | Cannot approve |
| `context-packs.base` | Context/action visibility | query_mode, evidence_sufficiency.state, action_readiness.state, warnings, gaps | Cannot infer ready |
| `feedback-events.base` | Feedback pressure | event_kind, target_ref, project_ref, review_pressure_effect, query_run_ref | Cannot mutate truth |
| `operator-cockpit.base` | Total cockpit | blocked, stale, missing anchor, hash mismatch, action_not_ready | Cannot replace validators |

### Product entries

| Entry | Backend artifact | Boundary |
|---|---|---|
| Add Source | source card | provenance only |
| Process This | candidate distillation | candidate only |
| Ask What Vault Knows | query-run trace | orientation unless action mode |
| Check Vault | lint/maintenance manifest | diagnostic only |
| Make Context Pack | context pack manifest | not action basis by itself |
| Review Candidates | review candidate/Evidence Packet | review input |
| Record Feedback | feedback event | activation/review pressure only |

### Product experience backlog for later screening

These are not approved builds yet. They are productization candidates to screen
after P0/P1 gates exist:

| ID | Candidate | Inspired by | VAKS layer | Boundary |
|---|---|---|---|---|
| P2-PX-01 | Capability Circle / Boundary Page | Reminds | product explanation | Explains existing rules only |
| P2-PX-02 | Quick Capture Inbox | Reminds + TimeFriend | raw/candidate intake | Cannot write reviewed truth |
| P2-PX-03 | Candidate Inbox / Review Funnel | Reminds | candidate/review queue | Cannot imply approval |
| P2-PX-04 | Activation Timeline / Activity Calendar | TimeFriend | activation/workbench | Activity is not confidence |
| P2-PX-05 | Review Due Calendar | TimeFriend | review pressure | Due state is not truth mutation |
| P2-PX-06 | Context Pack / Evidence Packet Export | TimeFriend | context/action prep | Export is not action-ready by itself |
| P2-PX-07 | Mobile Capture Shell | Reminds | capture only | Phone path stops at raw/candidate |
| P2-PX-08 | Thin MCP / LLM Entry Surface | Reminds | read/candidate/feedback bridge | No reviewed-write tool |
| P2-PX-09 | Product Onboarding | Reminds | product education | Must expose candidate/review/action boundaries |
| P2-PX-10 | MISA Read-Only Context Entry | TimeFriend + agentmemory + kk-knowledge-agent | MISA bridge | MISA reads/searches first; writes only candidate/feedback receipts |
| P2-PX-11 | Home / Operator Status Surface | direct VAKS use-surface check | workbench navigation | Shows status only; cannot approve or mutate truth |
| P2-PX-12 | Total Research Map / MOC | direct VAKS use-surface check | research navigation | Navigation is not authority |
| P2-PX-13 | One-Click Sync + Hash Receipt View | direct VAKS use-surface check | source hygiene / operations | Hash match is process integrity, not evidence support |
| P2-PX-14 | Layer Badge System | direct VAKS use-surface check | product explanation | Badge displays boundary; badge cannot promote |
| P2-PX-15 | Worktree / Dirty-State Guardrail | direct VAKS use-surface check | operator safety | Dirty state blocks risky actions; it does not judge knowledge |

Screening output should be:

```text
keep / park / reject
required validators
target layer
boundary warning
source inspiration
minimal wireflow
```

## 10. Risk Register

| ID | Risk | Bad path to block |
|---|---|---|
| R-01 | candidate as support | candidate marked `pack_role: support` |
| R-02 | URL as evidence | URL-only source_ref enters direct_support |
| R-03 | rank as trust | semantic/vector/graph score raises confidence |
| R-04 | body drift | approval remains after candidate body changes |
| R-05 | feedback truth mutation | feedback changes truth_confidence |
| R-06 | stale ready | superseded/out_of_scope point outputs ready |
| R-07 | hidden gaps | budget trimming hides missing evidence/risk |
| R-08 | Base as schema | `.base` fields define canonical schema |
| R-09 | graph edge as reviewed relation | auto relation enters formal graph |
| R-10 | agent direct write | suggest-only actor writes reviewed file |
| R-11 | no rollback | destructive/schema operation lacks rollback |
| R-12 | artifact pollution | runtime/test artifact enters retrieval/support |
| R-13 | shallow approval | "looks good" replaces checked evidence |
| R-14 | cross-bucket rank | raw/candidate/reviewed mixed as equal |
| R-15 | deleted old decision | superseded decision removed instead of linked |
| R-16 | plugin memory as fact | plugin output becomes reviewed knowledge |
| R-17 | lint as approval | test/lint/blind review treated as reviewer approval |
| R-18 | pack as action basis | context pack becomes ready without sufficiency |
| R-19 | summary self-support | source summary supports own claim |
| R-20 | overengineering | graph DB/MCP writes before core gates |
| R-21 | derived graph cache as authority | graph/cache answer or auto triple enters support/reviewed relation without receipt and evidence gate |
| R-22 | strict-but-unusable system | users bypass VAKS or ask agents to shortcut gates because the safe path is too hard to operate |

## 11. Acceptance Stories

1. New source enters as raw source and candidate only.
2. Candidate promotion requires fixed body hash and Evidence Packet.
3. Ordinary query can answer lightly without full audit.
4. Action query requires context pack, support checks, sufficiency, and action readiness.
5. Stale decision is preserved and linked to replacement, not deleted.
6. Negative feedback creates review pressure, not truth mutation.
7. Plugin retrieval can find material but cannot prove it.
8. Agent write must produce operation receipt and pass permission tier.
9. Base view can show review queue state but cannot approve.
10. Failure matrix blocks all listed bad paths.

## 12. Schema Impact Assessment

Current package should not edit `SCHEMA.md`.

Reason:

```text
Receipts, validators, failure matrices, pilots, and Bases are operational controls.
They harden the system around the current schema.
They do not introduce a new truth model.
```

Future schema unlock only after:

- P0 validators exist
- P0 failure matrix passes
- P1 read-only pilot proves loop behavior
- fields prove stable across repeated use
- owner explicitly approves schema unlock

Forbidden future schema fields:

- `retrieval_score_confidence`
- `graph_rank_trust`
- `feedback_truth_delta`
- `plugin_verified`
- `agent_approved`
- `auto_promoted`
- `dashboard_approved`

## 13. Parked Decisions

Park until P0/P1 are stable:

- full graph database
- vector DB as core authority
- MCP write tools
- autonomous agent writeback
- automatic promotion
- automatic reviewed relation extraction
- full desktop UI
- plugin installation as system dependency
- scheduled synthesis
- schema unlock

## 14. Implementation Order

Recommended order:

```text
P0-00 planning document
-> P0-01 retrieval receipt template
-> P0-02 operation receipt template
-> P0-03 body hash validator
-> P0-04 support boundary validator
-> P0-05 action readiness validator
-> P0-06 feedback validator
-> P0-07 failure matrix
-> P1 retrieval/operation receipt validators
-> P1 read-only query loop pilot
-> P1.5 robust RAG retrieval enhancement sandbox
-> P1.5 local Obsidian graph retrieval / read-only MCP sandbox
-> P1.5 raw intake parser router / extraction bundle sandbox
-> P1.5 markdown validation/search sidecar sandbox
-> P1.5 MISA runtime memory / VAKS bridge sandbox
-> P2 use-surface optimization pass
-> P2 Bases cockpit
-> P2 product experience screening sandbox
-> P2 product workflow
-> plugin sandbox
```

Do not start P2 plugin/agent work before P0 validators can block bad paths.

## 15. Completion Audit

This document completes the planning write-down step.

It does not complete implementation.

Still not implemented:

- retrieval receipt template
- operation receipt template
- body hash validator
- support boundary validator
- action readiness validator
- feedback validator
- retrieval receipt validator
- operation receipt validator
- failure matrix
- read-only runtime pilot
- local Obsidian graph retrieval / read-only MCP sandbox
- raw intake parser router / extraction bundle sandbox
- markdown validation/search sidecar sandbox
- MISA runtime memory / VAKS bridge sandbox
- use-surface optimization pass
- Bases cockpit
- product experience screening sandbox
- product workflow

Goal-level completion requires those later artifacts if the scope expands from research/planning into implementation.
