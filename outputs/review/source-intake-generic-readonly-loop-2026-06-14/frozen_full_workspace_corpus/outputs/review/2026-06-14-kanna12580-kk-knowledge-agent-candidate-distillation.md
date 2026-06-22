---
record_kind: candidate_distillation
status: candidate
provisional: true
knowledge_status: candidate
processing_tier: medium
lifecycle_state: candidate_provisional
overlay_state: none
review_pressure: none
source_ref: raw/repos/2026-06-14-kanna12580-kk-knowledge-agent-source.md
derived_from:
  - raw/repos/2026-06-14-kanna12580-kk-knowledge-agent-source.md
  - raw/repos/_snapshots/2026-06-14-kanna12580-kk-knowledge-agent-713cf3a-source.zip
  - wiki/summaries/2026-06-14-kanna12580-kk-knowledge-agent-architecture-review.md
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
  - misa-runtime-memory
  - mcp-agent-access
  - external-knowledge-base
possible_project_refs:
  - misa
point_anchor_refs:
  - "README.md:3"
  - "AGENTS.md:13"
  - "AGENTS.md:154"
  - "docs/PROJECT_HANDOFF.md:85"
  - "docs/PROJECT_HANDOFF.md:98"
  - "backend/app/services/retrieval_service.py:12"
  - "mcp-server/server.py:11"
  - "mcp-server/tools.py:28"
  - "mcp-server/tools.py:94"
borrow_value: medium
borrow_order: P2
dev_context_hint:
  core_when: "MISA external knowledge-base bridge implementation begins."
  support_when: "MISA memory/context design compares external KB lookup with runtime memory."
  risk_when: "Any agent writeback or action-facing answer uses retrieved chunks."
tags:
  - candidate
  - provisional
  - mcp
  - external-knowledge-base
  - misa-memory
---

# 候选蒸馏：kk-knowledge-agent

## Boundary

This note is provisional orientation.

It can help route attention, compare ideas, or suggest project overlays. It is not reviewed knowledge, not a decision, not a formal pattern, and not action basis.

## 一句话结论

`kk-knowledge-agent` 对 MISA 有帮助，但帮助点要说准：

```text
它帮 MISA 接一个外部知识库。
它不负责让 MISA 真正“会记忆”。
```

更准确的定位：

```text
kk-knowledge-agent = MISA external knowledge-base bridge reference
agentmemory = MISA runtime memory reference
VAKS = reviewed/candidate/source boundary and action discipline
```

所以它可以进入 MISA 相关候选材料；不要把它贴成 VAKS 核心能力标签。

## Source

```yaml
derived_from:
  - raw/repos/2026-06-14-kanna12580-kk-knowledge-agent-source.md
  - raw/repos/_snapshots/2026-06-14-kanna12580-kk-knowledge-agent-713cf3a-source.zip
point_anchor_refs:
  - snapshot_ref: raw/repos/_snapshots/2026-06-14-kanna12580-kk-knowledge-agent-713cf3a-source.zip
    selector_type: file_line
    selector_value: README.md:3
  - snapshot_ref: raw/repos/_snapshots/2026-06-14-kanna12580-kk-knowledge-agent-713cf3a-source.zip
    selector_type: file_line
    selector_value: mcp-server/tools.py:28
  - snapshot_ref: raw/repos/_snapshots/2026-06-14-kanna12580-kk-knowledge-agent-713cf3a-source.zip
    selector_type: file_line
    selector_value: mcp-server/tools.py:94
```

## Candidate Points

### Candidate Point 1: Thin MCP adapter is the useful part

The strongest borrow is:

```text
MCP tool -> Backend API -> retrieval core
```

In the repo:

- `mcp-server/server.py` registers `search_knowledge_base`, `list_knowledge_bases`, and `add_text_document`.
- `mcp-server/tools.py` calls backend HTTP endpoints.
- `AGENTS.md` explicitly says MCP Server should call Backend HTTP API and not duplicate retrieval logic.

For MISA:

```text
MISA should not directly parse/search every knowledge store.
MISA should call a small adapter with stable contracts.
```

This is useful.

### Candidate Point 2: External KB lookup is not the same as memory

The repo can help MISA fetch external context:

```text
query -> retrieved chunks -> MISA answer/context
```

But it does not provide:

- episodic memory;
- long-term user preference memory;
- use ledger;
- feedback/reflection loop;
- temporal validity;
- review pressure;
- memory cooling/reactivation.

So the right phrase is:

```text
helps MISA use a knowledge base
does not by itself improve MISA memory architecture
```

If MISA uses it together with `agentmemory`, the split should be:

```text
kk-like layer: external knowledge lookup
agentmemory-like layer: runtime continuity and recall
VAKS-like boundary: source/candidate/review/action discipline
```

### Candidate Point 3: Retrieval results need MISA/VAKS-style safety labels

The repo returns:

```text
document_id
title
chunk
score
chunk_id
chunk_index
```

This is enough for a demo.

It is not enough for our agent context:

```text
authority_bucket: raw/candidate/reviewed
usage_role: activation_only/review_input/support
source_ref
anchor_ref
warning_code
action_basis_allowed
retrieval_receipt
```

MISA must never treat `score` as confidence. It is only a retrieval ranking signal.

### Candidate Point 4: `add_text_document` is useful but dangerous

The repo exposes an optional MCP tool:

```text
add_text_document(knowledge_base_id, title, content)
```

For ordinary demo use, this is fine.

For MISA, direct write tools must be quarantined:

```text
allowed:
  scratch note
  candidate note
  feedback event
  source intake draft

not allowed:
  reviewed claim
  reviewed relation
  architecture decision
  action basis
```

This repo is therefore a good reminder that read tools can come early, but write tools need policy.

### Candidate Point 5: Local MCP reliability notes are genuinely useful

The repo's `docs/DEVELOPMENT_LOG.md` records a real Bad Gateway issue caused by local proxy inheritance, then fixes it with:

```text
httpx.AsyncClient(..., trust_env=False)
```

For MISA, this is practical gold:

- prefer `127.0.0.1` over ambiguous `localhost` when needed;
- set backend timeout explicitly;
- do not inherit proxy env for local backend calls;
- remember MCP child processes may need restart after code/config changes.

This is not architecture theory, but it will save debugging time.

### Candidate Point 6: The mini-stack is fine for prototype, not for final authority

The repo stack:

```text
FastAPI
SQLite
ChromaDB
sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2
React/Vite
FastMCP
```

Good for:

- demo;
- local prototype;
- MISA adapter proof-of-concept;
- small personal KB lookup.

Not enough for:

- VAKS formal source intake;
- evidence-aware review;
- action-basis answers;
- multi-source provenance;
- source anchor preservation;
- long-term memory governance.

## Does It Help MISA?

Yes, but in a bounded way.

| MISA Need | Help Level | Why |
|---|---:|---|
| Query an external/local knowledge base | 8/10 | Clean MCP -> Backend -> retrieval chain. |
| Keep MISA's session/runtime memory | 3/10 | It does not implement real memory lifecycle. |
| Use VAKS material safely | 4/10 | Interface shape helps, but safety labels must be added by us. |
| Agent writeback | 4/10 | Has write tool example, but needs quarantine. |
| Production reliability | 5/10 | Helpful local-call notes, but MVP stack only. |

## Open Questions

- Should MISA's first knowledge tool be read-only?
- Should MISA receive chunks directly, or a VAKS context-pack envelope?
- Should `add_text_document` be disabled until candidate/feedback write receipts exist?
- Should MISA have separate tools for:
  - `search_context`
  - `list_context_sources`
  - `propose_candidate_note`
  - `log_feedback_event`
- Should MISA hide raw vector score from the model and expose only warning labels?

## Routing Hint

Route this source to:

```text
MISA external knowledge-base bridge
MISA MCP tool design
agent access / write boundary discussion
runtime context retrieval
```

Do not route it to:

```text
VAKS core architecture
reviewed knowledge model
truth confidence
evidence support
memory tier replacement
```

## Forbidden

```text
project_borrow_scope as universal decision
decision outcome
formal pattern
action basis
truth confidence
retrieval score as support
VAKS core tag unless a later review confirms direct relevance
```

## Practical Borrow Set

For future MISA work, borrow only:

```text
1. Backend owns retrieval core.
2. MCP tool is thin and small.
3. Search/list can come before write.
4. Write tools require quarantine.
5. Local MCP calls need timeout, backend URL, trust_env=false, restart notes.
6. Returned results need authority/warning labels before MISA uses them.
```

## Final Judgment

```text
Borrow value: medium
Borrow order: P2
Best use: MISA external knowledge-base bridge scaffold
Not best use: MISA memory brain or VAKS core layer
```

说人话：

```text
这个库值得留。
它不高级，但很实用。
它能帮 MISA 先把“查资料库”这条路跑通。
但 MISA 真正的记忆、VAKS 的可信知识边界，不能靠它解决。
```
