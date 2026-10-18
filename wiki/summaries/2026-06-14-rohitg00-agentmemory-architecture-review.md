---
type: summary
status: draft
title: "agentmemory architecture review for MISA runtime memory and VAKS bridge"
created: "2026-06-14"
library_name: "agentmemory"
repo_url: "https://github.com/rohitg00/agentmemory"
source_url: "raw/repos/2026-06-14-rohitg00-agentmemory-source.md"
checked_commit: "f6f9e3cb1385da31f48036868dc3c7fe342b67ba"
commit_time: "2026-06-11T09:48:24Z"
observed_version: "0.9.27"
source_status: active
reviewed_at: "2026-06-14"
domain: "Agent runtime memory / MCP / Hermes integration / context injection"
related_projects:
  - verified-action-knowledge-system
  - misa
current_branch: "MISA runtime memory / VAKS context-pack adapter / agent memory quarantine"
extracted_patterns:
  - "session observation capture"
  - "project and agent scoped memory"
  - "MCP and hook integration"
  - "budgeted context injection"
  - "runtime memory provenance"
  - "retention and pinned slots"
fusion_decision: adapt-design-after-sandbox
inspection_confidence: medium
evidence_count: 19
cross_validated_with:
  - "SCHEMA.md"
  - "MEMORY_TIER.md"
  - "DEV_CONTEXT.md"
  - "FEEDBACK.md"
  - "outputs/review/vaks-architecture-upgrade-plan-2026-06-13.md"
negative_evidence:
  - "No local runtime install/test was run."
  - "Hermes connect adapter is manual/stub-like."
  - "Upstream benchmark claims were not reproduced."
  - "Runtime memory write/export/delete surfaces are too broad for direct VAKS adoption."
  - "Security advisory drafts show prior high-impact issues in this class of tool."
extension_potential: "High for MISA runtime memory and bridge design; low for VAKS truth authority."
knowledge_status: candidate
action_basis_allowed: false
truth_mutation_allowed: false
tags:
  - summary
  - architecture-review
  - agentmemory
  - misa
  - hermes
  - mcp
  - runtime-memory
  - candidate-only
---

# agentmemory 架构评审：MISA runtime memory / VAKS bridge 候选

## 一句话判断

agentmemory 对 MISA 有明显帮助，但必须放在正确位置：

```text
MISA runtime memory and VAKS bridge reference.
Not VAKS reviewed knowledge authority.
```

正确吸收方式：

```text
Use agentmemory-like mechanics to help MISA remember and fetch context.
Use VAKS gates to decide what can be believed, reviewed, and acted on.
```

## 它解决什么问题

agentmemory 解决的是 agent 跨会话连续性：

```text
session history
tool outcomes
project conventions
user preferences
previous decisions
common errors
pending work
```

它做了：

```text
hooks / MCP / REST capture
session and observation storage
explicit memory save
BM25 / vector / graph-style hybrid search
context generation
slots / working memory / retention
Hermes/Codex/Claude integration
viewer / governance / forget / export
```

这与 MISA 的需求重合：

```text
MISA needs continuity.
MISA needs to read VAKS without rereading the whole vault.
MISA needs to write back corrections safely.
```

但它与 VAKS 的核心差异也很大：

```text
agentmemory optimizes recall and continuity.
VAKS optimizes authority and action safety.
```

## 核心设计

The architecture has four planes:

```text
Capture plane:
  hooks / MCP / REST / Hermes provider
  raw observations
  session metadata

Memory plane:
  explicit memories
  lessons
  slots
  summaries
  retention scores

Retrieval plane:
  BM25
  vector
  graph-style expansion
  smart search
  project / agent filters

Injection plane:
  context block
  system prompt block
  prefetch
  pre-compress reinjection
```

The key reusable split for MISA:

```text
runtime memory = remembers work
VAKS context pack = supplies bounded knowledge
operation receipt = records action/writeback
```

## Source / Code Anchors

| Anchor | What exists | Design extraction | Boundary |
|---|---|---|---|
| `README.md` | Agentmemory supports multiple coding agents and MCP clients including Hermes and Codex. | Confirms target-surface relevance. | Support claim is not local integration proof. |
| `README.md` | Describes capture, compression, search, context injection, viewer, and cross-agent sharing. | Full runtime-memory loop. | Context injection is not action readiness. |
| `README.md` | Reports retrieval and token metrics with a benchmark caveat. | Useful benchmark reporting discipline. | Upstream-reported only. |
| `package.json` | TypeScript package v0.9.27, Node >=20, Apache-2.0, iii-sdk, optional local embedding dependencies. | Runtime and deployment map. | Dependency posture not audited. |
| `src/types.ts` | Session, observation, compressed observation, memory, context block, slots, relations. | Good runtime schema reference. | Its confidence/strength fields are not VAKS truth confidence. |
| `src/functions/observe.ts` | Captures hook payloads, redacts secrets, dedups, stores observations, streams live events. | Good MISA observation capture pattern. | Raw observation remains raw runtime trace. |
| `src/functions/remember.ts` | Explicit save with type/concepts/files/TTL/sourceObservationIds/project/agentId/supersession. | Good memory API shape. | Cannot write VAKS reviewed nodes. |
| `src/functions/search.ts` | Search validates query, filters project/cwd/agent, fail-closes isolated agent mode. | Important multi-agent isolation pattern. | Search result remains activation. |
| `src/functions/smart-search.ts` | Hybrid search with compact/expand flow, lessons, follow-up diagnostic. | Useful progressive disclosure and diagnostic idea. | Follow-up rate is a diagnostic, not evidence. |
| `src/state/hybrid-search.ts` | BM25/vector/graph streams combined with RRF-like scoring and session diversification. | Useful retrieval stack pattern. | Graph/rank/score is not support. |
| `src/functions/context.ts` | Builds budgeted context from pinned slots, project profile, lessons, summaries, observations. | Strong context-pack UX reference. | Needs VAKS receipts and action readiness. |
| `src/functions/verify.ts` | Links memory back to source observations and session metadata. | Runtime provenance pattern. | Not evidence sufficiency. |
| `src/functions/retention.ts` | Decay/access scoring and hot/warm/cold thresholds. | Activation Tier analogy. | Hot/warm/cold is not belief/truth. |
| `src/functions/working-memory.ts` | Core vs archival memory, pinned entries, budgeted working context. | Useful memory paging reference. | Working memory is prompt support, not authority. |
| `src/functions/slots.ts` | Default slots for persona, preferences, tool guidelines, project context, guidance, pending items. | Excellent MISA runtime slot candidates. | Slots must be quarantined from VAKS reviewed knowledge. |
| `src/functions/lessons.ts` and `reflect.ts` | Lessons/reflection with confidence/reinforcement/decay. | Useful feedback and improvement loop reference. | Reinforcement cannot mutate VAKS truth. |
| `src/mcp/tools-registry.ts` | MCP tools for recall, save, smart search, timeline, profile, export, relations, governance. | Strong MCP surface map. | Write/delete/export tools need permission tiers. |
| `integrations/hermes/README.md` | Hermes MCP setup and deeper provider hooks. | Most directly useful to MISA/Hermes. | Must be adapted, not copied blindly. |
| `integrations/hermes/__init__.py` | Provider calls REST for context, smart-search, remember, observe, session end. | Concrete adapter design. | `memory_save` and `on_memory_write` must not touch VAKS reviewed layer. |
| `.github/security-advisories/` | Prior risks: remote shell startup, exposed REST, unauth mesh, Obsidian path traversal, redaction gaps. | Strong safety lessons for any runtime memory service. | Patched status not locally verified. |

## 当前支线价值

Current local concern:

```text
MISA reading VAKS without breaking VAKS boundaries.
MISA remembering runtime work without pretending it is reviewed knowledge.
```

agentmemory supports:

- MISA session memory.
- Hermes provider lifecycle inspiration.
- Context injection UX.
- Project/agent-scoped recall.
- Runtime memory provenance.
- Access/retention as activation signal.
- Governance/forget/audit concepts.

Risks:

- Runtime memory can look authoritative.
- Context injection can hide source/action boundaries.
- `memory_save` can be abused as direct writeback.
- Obsidian export can pollute formal vaults.
- MCP tools can create broad write/delete/export surfaces.

## 全貌架构价值

| Architecture Zone | Value / Finding | Adopt? |
|---|---|---|
| Karpathy spine | Good runtime memory for agent sessions; not a knowledge authority spine. | adapt |
| source ingest | Not a source parser; useful for runtime observations. | limited |
| candidate distillation | Can produce candidate signals from runtime discoveries. | adapt with quarantine |
| review queue | Corrections can create review_due. | adapt |
| schema / reviewed knowledge | No direct authority. | reject as authority |
| memory / dev context | Very strong reference. | adapt |
| feedback | Useful feedback/lesson loop. | adapt with truth quarantine |
| retrieval / cache | Strong activation search reference. | adapt |
| API / MCP / agent access | Strong but dangerous surface. | sandbox only |
| viewer / workbench | Useful runtime visibility reference. | watch |
| publishing / Obsidian | Export idea is risky for VAKS formal vault. | reject for reviewed vault |
| risk / anti-pattern | Main risk is runtime memory becoming truth. | adopt guardrail |

## 值得提炼的模式

### 1. Runtime memory is a separate plane

VAKS should not try to make reviewed knowledge do runtime work.

Better split:

```text
MISA runtime memory:
  session traces, preferences, pending work, tool outcomes

VAKS:
  source records, candidates, reviewed nodes, relations, context packs, action basis
```

### 2. Project and agent scope must fail closed

Agentmemory's agent-scope isolation is valuable because cross-agent memory leaks are a real risk.

VAKS/MISA version:

```text
No implicit wildcard.
No cross-project read unless explicitly requested.
No VAKS writeback without actor tier and operation receipt.
```

### 3. Context injection needs boundary labels

Agentmemory's context UX is good, but VAKS needs more structure:

```yaml
context_source: VAKS_context_pack | MISA_runtime_memory | user_preference
authority_bucket:
support_boundary:
action_readiness:
warnings:
```

### 4. Source observation trace is useful but insufficient

Source observations answer:

```text
Where did this runtime memory come from?
```

VAKS evidence answers:

```text
Does this evidence support this point under this scope strongly enough for this action?
```

Do not collapse the two.

## 标签与量化

- domain: agent runtime memory
- problem: cross-session agent continuity and context recall
- pattern: memory quarantine + context-pack bridge
- maturity: active / broad feature surface
- complexity: high
- problem_fit_for_misa: 5/5
- problem_fit_for_vaks_core: 1/5
- reuse_value: 5/5 for design, 2/5 for direct dependency
- implementation_cost: 4/5 if adopted, 2/5 as design reference
- evidence_strength: 4/5 for source inspection, 1/5 for local runtime proof
- reversibility: high if design-only, medium if installed

## Knowledge Calibration / Point Collision

| Candidate Point | Local Reviewed / Candidate Knowledge | Calibration Output | Review Question |
|---|---|---|---|
| MISA needs runtime memory. | VAKS already has Activation Tier and Dev Context, but not MISA runtime store. | supports | Should MISA memory live outside VAKS repo/vault? |
| Agent can inject context before LLM. | Context Pack is not action basis by itself. | refines | What receipt must accompany injected VAKS context? |
| Memory can save lessons/reflections. | Feedback does not mutate truth. | risk | How to map MISA lessons to feedback/review_due only? |
| MCP tools expose recall/save/delete/export. | Agent Gateway restricts write tiers. | challenge | Which tools are allowed before P0 validators exist? |
| Hermes provider can mirror memory writes. | MISA/Hermes boundary must not write VAKS reviewed knowledge. | challenge | Should `on_memory_write` be disabled or quarantined for VAKS? |

## Support / Challenge Review

What supports it:

- The repo explicitly targets Hermes, Codex, MCP, and coding-agent memory.
- Source code includes concrete observation, memory, context, search, verify, retention, slots, and Hermes provider surfaces.
- It has active public adoption signal and current releases.
- Its design addresses a real gap for MISA: runtime continuity.

What challenges it:

- No local MISA/Hermes integration was run.
- Runtime write/delete/export surfaces are too broad for VAKS without gates.
- Security advisory drafts show prior high-impact attack surfaces.
- Upstream benchmark claims are not local proof.
- Some integration maturity details are mixed: Hermes docs exist, CLI connect is manual/stub-like.

Challenge severity:

```text
minor for design borrowing
major for direct dependency adoption
critical for direct VAKS reviewed-vault writeback
```

Scope limits:

```text
Use as MISA runtime memory / bridge design reference.
Do not use as VAKS truth/review/action authority.
```

Action readiness:

```text
not_ready
```

## 可拓展性

- 适合作为插件/适配层参考：yes.
- 适合作为直接 VAKS dependency：not now.
- 适合作为 MISA runtime sidecar sandbox：yes, after reading MISA current runtime.
- 未来替换成本：low if adapter interface is VAKS-owned.
- 可迁移路径：design adapter first, run sandbox, keep VAKS writes quarantined.

## 复杂度和风险

- High feature-surface complexity.
- Medium deployment complexity: iii-engine, Node, MCP, hooks, optional embeddings.
- High security sensitivity: memory can contain secrets, tool outputs, prompts, source context.
- High authority-confusion risk if runtime memory is presented as reviewed knowledge.
- Medium lock-in risk if MISA depends directly on agentmemory's schema instead of a VAKS-owned adapter contract.

## 不可行点 / 避坑

- Do not install broad MCP write/delete/export tools into MISA before permission gates.
- Do not treat runtime memory as VAKS reviewed note.
- Do not use memory confidence, strength, retention, rank, or lesson reinforcement as truth confidence.
- Do not export runtime memory into formal Obsidian vault as reviewed knowledge.
- Do not let memory provider auto-write VAKS reviewed nodes.
- Do not let MISA context injection hide source bucket, warning, or action readiness.

## 融合判断

- 结论：adapt-design-after-sandbox.
- 理由：The design strongly fits MISA runtime memory and VAKS bridge needs, but direct adoption is unsafe before permission gates and current MISA runtime inspection.
- 验证方式：Create a small MISA/VAKS bridge sandbox with read-only VAKS context pack reads and candidate/feedback-only writeback.

## 直接判断

- Direct use in VAKS: no.
- Direct use in MISA production: not yet.
- Fork: no.
- Design-only: yes, strong.
- Sandbox: yes, recommended.
- Reject: reject as reviewed truth/action basis.
- Current branch value: very strong for MISA memory bridge design.
- Whole architecture value: high as complement to VAKS, not replacement.
- Risk: runtime memory authority confusion.
- Next action: add to architecture plan as `P1.5-MISA-MEM` sandbox candidate.

## 后续行动

Possible future sandbox:

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

and require:

```text
no reviewed knowledge write
no truth mutation
no action basis from runtime memory
project/agent scope explicit
operation receipt for any writeback
all VAKS context labeled with authority bucket and warnings
```
