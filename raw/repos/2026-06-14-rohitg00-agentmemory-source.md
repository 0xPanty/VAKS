---
type: source
record_kind: source_card
status: source-captured
title: "agentmemory - Persistent memory for AI coding agents"
source_id: "repo:rohitg00/agentmemory@f6f9e3cb1385da31f48036868dc3c7fe342b67ba"
source_uri: "github:rohitg00/agentmemory@f6f9e3cb1385da31f48036868dc3c7fe342b67ba"
source_url: "https://github.com/rohitg00/agentmemory"
source_type: repository
author: "rohitg00"
publisher: GitHub / npm
published_at: "2026-02-25T07:32:52Z"
updated_at: "2026-06-13T17:57:21Z"
captured_at: "2026-06-14"
captured_by: Codex
version_or_commit: "f6f9e3cb1385da31f48036868dc3c7fe342b67ba"
observed_version: "0.9.27"
source_integrity:
  source_hash: null
  snapshot_hash: "sha256:F894BF00ECE2ED84B476B436ED7FDEFDC54E064132E25F1A43630ED4DAE09055"
  ingest_state: new
adapter_ingest:
  adapter_name: "manual-github-review"
  adapter_version: "2026-06-14"
  capture_method: "GitHub API metadata, npm metadata, git ls-remote, shallow clone/source inspection, and commit zip snapshot"
  extraction_trace:
    - "GitHub repo metadata API"
    - "git ls-remote HEAD"
    - "npm view @agentmemory/agentmemory and @agentmemory/mcp"
    - "local shallow clone for README/source/integration/security inspection"
    - "GitHub commit zip snapshot"
  known_limits:
    - "Repository was inspected but not executed locally."
    - "Upstream benchmark claims were recorded as upstream-reported and were not reproduced."
    - "Hermes integration was inspected from source; it was not installed into MISA/Hermes."
    - "MCP, hook, Obsidian export, memory-write, and governance surfaces were not security-audited locally."
    - "The repo includes security advisory drafts for earlier versions; patched status was inferred from upstream docs, not independently tested."
source_status: active
raw_location: "raw/repos/_snapshots/2026-06-14-rohitg00-agentmemory-f6f9e3c-source.zip"
processing_tier: heavy
knowledge_status: raw
overlay_state: none
review_pressure: review_due
retrieval_policy:
  policy_kind: source_identity_only
  pack_allowed: drilldown_required
  action_basis_allowed: false
  warning_code: raw_is_provenance_only
promotion_gate: none
action_basis_allowed: false
truth_mutation_allowed: false
review_priority: normal
review_owner: Codex
formalization_status: raw-only
why_saved: "User asked to distill rohitg00/agentmemory and judge whether it helps MISA use the VAKS vault."
topics:
  - agent-memory
  - runtime-memory
  - mcp
  - hermes
  - codex
  - context-injection
  - activation
  - memory-quarantine
  - misa-vaks-bridge
projects:
  - verified-action-knowledge-system
  - misa
source_family:
  - agent-runtime-memory
  - mcp-server
  - hook-integration
  - context-pack-adapter-reference
upstream_sources:
  - "https://github.com/rohitg00/agentmemory"
  - "https://www.npmjs.com/package/@agentmemory/agentmemory"
  - "https://www.npmjs.com/package/@agentmemory/mcp"
  - "https://agent-memory.dev"
verification_status: source_identity_checked
candidate_relation_suggestions:
  - target: "outputs/review/2026-06-14-rohitg00-agentmemory-candidate-distillation.md"
    relation_type: derived_from
    relation_state: candidate
    why_suggested: "Candidate distillation extracts the runtime-memory and MISA/VAKS bridge lessons."
    suggested_at: "2026-06-14"
tags:
  - source
  - repository
  - candidate-only
  - agentmemory
  - mcp
  - hermes
  - misa
---

# 来源记录：agentmemory

## 为什么收录

用户给出：

```text
https://github.com/rohitg00/agentmemory
```

并要求：

```text
蒸馏这个 到时候对misa使用我们的资料库有没有帮助
```

这个仓库与 VAKS/MISA 的交叉点很明确：

```text
MISA 需要跨会话记住工作过程、偏好、历史决策、工具结果。
VAKS 需要保持 reviewed knowledge / action basis 的权威边界。
agentmemory 提供运行时记忆、MCP、hooks、Hermes 集成形状。
```

所以本次收录重点不是“把 agentmemory 接进资料库当真值层”，而是判断：

```text
能否借鉴它的 runtime memory / MCP / Hermes adapter 形状，
让 MISA 更好地读取 VAKS context pack，
同时把 MISA 写回严格隔离在 feedback / candidate / review_due。
```

## 来源信息

- 作者/组织：rohitg00
- 仓库：https://github.com/rohitg00/agentmemory
- 官网：https://agent-memory.dev
- npm package：`@agentmemory/agentmemory`
- npm MCP package：`@agentmemory/mcp`
- 语言：TypeScript
- License：Apache-2.0
- 当前上游 HEAD：`f6f9e3cb1385da31f48036868dc3c7fe342b67ba`
- HEAD commit 时间：`2026-06-11T09:48:24Z`
- HEAD commit message：`fix(website): portal mobile nav sheet to body and close breakpoint gap (#670)`
- GitHub API metadata：stars `22659`，forks `1861`，open issues `295`
- observed npm version：`0.9.27`
- latest release：`v0.9.27`，published `2026-06-07T08:58:35Z`
- package runtime：Node `>=20.0.0`
- production deps observed：Anthropic SDKs, `iii-sdk`, `zod`, `dotenv`, `@clack/prompts`
- optional deps observed：local embeddings / ONNX / CJK segmentation packages
- source snapshot：`raw/repos/_snapshots/2026-06-14-rohitg00-agentmemory-f6f9e3c-source.zip`
- snapshot SHA256：`F894BF00ECE2ED84B476B436ED7FDEFDC54E064132E25F1A43630ED4DAE09055`

## Intake Boundary

```yaml
processing_tier: heavy
knowledge_status: raw
overlay_state: none
review_pressure: review_due
retrieval_policy:
  policy_kind: source_identity_only
  pack_allowed: drilldown_required
  action_basis_allowed: false
  warning_code: raw_is_provenance_only
promotion_gate: none
action_basis_allowed: false
truth_mutation_allowed: false
```

This source card is provenance only. It does not approve installing agentmemory, does not approve MISA runtime changes, does not allow MISA to write reviewed VAKS knowledge, and does not make upstream benchmark claims local evidence.

## Inspected Repository Areas

| Anchor | What exists | Design extraction | Boundary |
|---|---|---|---|
| `README.md` | Positions agentmemory as persistent memory for Claude Code, Codex CLI, Hermes, and MCP clients. | Direct relevance to MISA/Hermes and multi-agent runtime memory. | Marketing/support matrix is not local integration proof. |
| `README.md` | Describes shared server, hooks/MCP/REST, capture/compress/search/context injection, viewer, and benchmarks. | Strong runtime-memory plane reference. | Context injection must not become VAKS action basis. |
| `README.md` | Reports retrieval/token metrics and a competitor table with methodology caveat. | Useful evaluation framing. | Upstream-reported benchmark, not reproduced locally. |
| `README.md` | Codex plugin path registers MCP, lifecycle hooks, invocable skills, and notes a Codex Desktop hook limitation. | Useful plugin-boundary lesson. | Do not install or assume hook availability without sandbox. |
| `package.json` | `@agentmemory/agentmemory` v0.9.27, Apache-2.0, TypeScript, Node >=20, iii-sdk dependency, optional local embeddings. | Runtime/dependency map. | Dependency/security posture not audited locally. |
| `src/types.ts` | Defines Session, RawObservation, CompressedObservation, Memory, ContextBlock, MemorySlot, MemoryRelation, HybridSearchResult. | Good schema for runtime memory vs session observations. | Its `confidence` / `strength` fields must not map to VAKS truth confidence. |
| `src/functions/observe.ts` | Hook payload capture, privacy redaction, dedup, session-scoped observations, live stream, optional image handling. | Good MISA event capture reference. | Captured tool/conversation events are raw runtime observations only. |
| `src/functions/remember.ts` | Explicit memory save with type, concepts, files, TTL, sourceObservationIds, agentId, project, supersession, search indexing. | Useful explicit memory API and source-observation trace. | Direct `remember` is not reviewed knowledge writeback. |
| `src/functions/search.ts` and `src/functions/smart-search.ts` | BM25/hybrid search, project filtering, agent isolation fail-closed mode, follow-up diagnostic. | Strong adapter boundary reference for MISA multi-agent memory. | Retrieval results are activation, not evidence support. |
| `src/state/hybrid-search.ts` | BM25 + vector + graph RRF-style fusion, session diversification, optional rerank. | Useful activation/search design. | Ranks/scores/graph context are not trust. |
| `src/functions/context.ts` | Builds budgeted context from slots, profile, lessons, recent sessions, summaries, observations. | Closest analog to VAKS dev context/context pack preparation. | Generated context is not action basis by itself. |
| `src/functions/verify.ts` | Verifies memory by linking to source observation IDs and session metadata. | Useful provenance-check pattern for runtime memory. | Citation count is not evidence sufficiency. |
| `src/functions/retention.ts` and `src/functions/working-memory.ts` | Access-count, decay, hot/warm/cold retention, core vs archival working context. | Strong Activation Tier analogy. | Activation score is not truth confidence. |
| `src/functions/slots.ts` | Pinned slots for persona, user preferences, tool guidelines, project context, guidance, pending items. | Useful MISA runtime prompt-memory slots. | Slots must be outside VAKS reviewed truth. |
| `src/functions/lessons.ts` and `src/functions/reflect.ts` | Lessons, confidence, reinforcement, reflection, insight extraction. | Useful feedback/learning UX reference. | Reinforcement/confidence cannot mutate VAKS truth. |
| `src/mcp/tools-registry.ts` | Tools such as recall, save, file history, smart search, timeline, profile, export, relations, commits, governance. | Strong MCP surface reference. | Write/delete/export tools require strict permission tiering if copied. |
| `src/functions/governance.ts` and `src/functions/privacy.ts` | Delete/bulk/audit query plus secret redaction. | Useful minimum governance/privacy floor. | Redaction is incomplete by nature; sensitive memory still needs sandbox/auth. |
| `src/functions/obsidian-export.ts` | Exports memories/lessons/crystals/sessions to Markdown under a constrained export root. | Relevant to VAKS/Obsidian boundary warning. | Do not export runtime memory into formal VAKS vault as reviewed knowledge. |
| `integrations/hermes/README.md` | MCP config plus deeper Hermes plugin: prefetch, sync_turn, session_end, pre_compress, memory_write, system_prompt_block. | Most directly useful to MISA/Hermes bridge design. | `on_memory_write` mirroring must be quarantined, not VAKS reviewed writeback. |
| `integrations/hermes/__init__.py` | Python provider calls REST endpoints for context, smart-search, remember, observe, session/end. | Concrete adapter shape for MISA. | It currently saves memory without VAKS review gate. |
| `src/cli/connect/hermes.ts` | Hermes CLI adapter detects config but automated merge is not implemented; returns manual stub. | Maturity caveat. | Do not assume production-ready Hermes installer. |
| `SECURITY.md` and `.github/security-advisories/` | Security policy and advisory drafts for prior `curl|sh`, default network bind, mesh auth, Obsidian export traversal, redaction gaps. | Important risk lessons for any runtime memory service. | Current local safety not independently verified. |

## 初步看点

agentmemory is a serious reference for:

```text
agent session capture
runtime memory persistence
cross-agent MCP/REST access
Hermes/Codex hook integration
context injection
memory provenance back to observations
retention / working memory / slots
governance / forget / audit
```

For VAKS/MISA, the useful position is:

```text
MISA runtime memory and context adapter reference
```

not:

```text
VAKS reviewed knowledge layer
VAKS truth engine
VAKS action basis generator
formal Obsidian vault writer
```

## 明显疑点

- `DESIGN.md` in the repo appears unrelated to agentmemory architecture and should be ignored as a source anchor.
- Hermes install adapter in `src/cli/connect/hermes.ts` is still manual/stub-like even though the integration folder exists.
- The Hermes plugin's `on_memory_write` mirrors memory writes into agentmemory; this is useful for runtime continuity but dangerous if copied into VAKS without quarantine.
- Upstream benchmarks were not reproduced locally.
- MCP and REST surfaces are powerful enough to read/export/delete/remember data; any adoption needs auth, loopback-only defaults, permission tiers, and operation receipts.
- Security advisory drafts show this class of tool has real supply-chain, network exposure, and filesystem-write risks.

## 可抽取 Candidate Points

1. agentmemory is a strong reference for MISA runtime memory, especially session observation capture and project/agent-scoped recall.
2. Its Hermes integration gives a concrete bridge shape: prefetch context before LLM, sync turns, inject session-start context, and persist session end.
3. Its `sourceObservationIds` / verify path is worth borrowing as runtime provenance, but not as VAKS evidence support.
4. Its slots/retention/working-context model maps well to VAKS Activation Tier, not truth.
5. The key VAKS upgrade is a stricter bridge: MISA may read VAKS context packs and write feedback/candidate signals, but cannot write reviewed knowledge.

## 当前处理等级

```text
heavy source review, candidate only
```

升级到 sandbox 的条件：

- User explicitly asks to design or pilot MISA/VAKS runtime bridge.
- MISA runtime is inspected in its own workspace first.
- Agentmemory-like memory is run in a sandbox or design-only adapter, not attached to formal VAKS vault.
- VAKS writes are limited to candidate/feedback/review_due records through operation receipts.
- No reviewed knowledge, schema, or action-basis mutation is allowed.

## 下一步

Read:

- `outputs/review/2026-06-14-rohitg00-agentmemory-candidate-distillation.md`
- `wiki/summaries/2026-06-14-rohitg00-agentmemory-architecture-review.md`
- `outputs/review/project_lens_overlays/2026-06-14-rohitg00-agentmemory-misa-vaks-bridge-overlay.md`
