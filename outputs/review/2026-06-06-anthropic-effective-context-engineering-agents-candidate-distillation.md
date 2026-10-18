---
type: candidate_distillation
status: candidate_only
created_at: 2026-06-06
scope: Anthropic Effective Context Engineering -> VAKS retrieval/query and context-pack contract
truth_boundary: candidate points only; not reviewed knowledge; not architecture decision; not action basis
source_ref: raw/articles/2026-06-06-anthropic-effective-context-engineering-agents-source.md
---

# Anthropic Effective Context Engineering Candidate Distillation

## Chain

This file tests the VAKS flow:

```text
external article
-> source record
-> source extraction
-> candidate points
-> possible general knowledge point candidates
-> tags / indexes / project borrowing view
```

Boundary:

```text
This is candidate distillation.
It does not create reviewed claims, reviewed patterns, or action basis.
```

## General Knowledge Candidate Judgment

Overall judgment:

```text
yes, this source contains reusable general knowledge point candidates.
```

Reason:

```text
The article's ideas apply beyond Anthropic and beyond VAKS: any agent or
knowledge-work system with limited context needs rules for identifiers,
payloads, just-in-time loading, progressive disclosure, compaction, and notes.
```

## Candidate Points

### CP-001: Identifier-First, Payload-Later Context

```yaml
candidate_id: cp-anthropic-identifier-first-payload-later
point_text: "Agent context packs should often carry stable identifiers first and load full payloads only when needed."
candidate_general_knowledge: true
proposed_node_type: pattern
review_route: rationale_check
source_ref: raw/articles/2026-06-06-anthropic-effective-context-engineering-agents-source.md
source_anchor:
  url: https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents
  section: "context engineering / agent context management"
evidence_granularity: article_section
promotion_readiness: not_ready
```

VAKS borrow scope:

```text
Use paths, titles, headings, selectors, item IDs, and drilldown paths as the
front-face of a context pack before loading long payloads.
```

Non-borrow scope:

```text
Do not treat identifier presence as evidence support.
```

Candidate tags:

```text
context-engineering, context-pack, just-in-time-loading, activation
```

### CP-002: Just-In-Time Context Loading

```yaml
candidate_id: cp-anthropic-just-in-time-context-loading
point_text: "Agents should load detailed context just in time rather than preloading every possibly relevant payload."
candidate_general_knowledge: true
proposed_node_type: pattern
review_route: rationale_check
source_ref: raw/articles/2026-06-06-anthropic-effective-context-engineering-agents-source.md
source_anchor:
  url: https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents
  section: "context engineering / tool and context design"
evidence_granularity: article_section
promotion_readiness: not_ready
```

VAKS borrow scope:

```text
Use `drilldown_path` and `citable_status: drilldown_required` so pack items can
point to evidence windows without dumping all source text into the first pack.
```

Non-borrow scope:

```text
Do not hide necessary evidence behind drilldown when an answer is action-facing.
```

Candidate tags:

```text
context-pack, drilldown, agent-workbench, token-budget
```

### CP-003: Progressive Disclosure Context Pack

```yaml
candidate_id: cp-anthropic-progressive-disclosure-pack
point_text: "Context packs should reveal summary and navigation first, then expand to detailed evidence only for the claims that need it."
candidate_general_knowledge: true
proposed_node_type: concept
review_route: rationale_check
source_ref: raw/articles/2026-06-06-anthropic-effective-context-engineering-agents-source.md
source_anchor:
  url: https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents
  section: "context engineering / progressive context management"
evidence_granularity: article_section
promotion_readiness: not_ready
```

VAKS borrow scope:

```text
Use this in the pack compiler:
summary before detail, identifier before payload, drilldown before dump.
```

Non-borrow scope:

```text
Do not let summary-first become summary-only for decisions or action basis.
```

Candidate tags:

```text
context-pack, progressive-disclosure, pack-compiler
```

### CP-004: Context Compaction Is Runtime Hygiene

```yaml
candidate_id: cp-anthropic-context-compaction-runtime-hygiene
point_text: "Compacting long-running agent context is runtime hygiene, not reviewed memory formation."
candidate_general_knowledge: true
proposed_node_type: anti-pattern_boundary
review_route: risk_check
source_ref: raw/articles/2026-06-06-anthropic-effective-context-engineering-agents-source.md
source_anchor:
  url: https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents
  section: "context engineering / compaction and state"
evidence_granularity: article_section
promotion_readiness: not_ready
```

VAKS borrow scope:

```text
Use compaction for long query-runs or agent sessions, but store it as runtime
trace / activation aid.
```

Non-borrow scope:

```text
Do not let compacted summaries become reviewed knowledge or evidence support.
```

Candidate tags:

```text
context-compaction, agent-memory-quarantine, use-ledger, activation
```

### CP-005: Tool Outputs Should Return Compact Useful Context

```yaml
candidate_id: cp-anthropic-tool-output-compact-context
point_text: "Agent tools should return compact, useful, task-relevant context rather than noisy raw dumps."
candidate_general_knowledge: true
proposed_node_type: pattern
review_route: rationale_check
source_ref: raw/articles/2026-06-06-anthropic-effective-context-engineering-agents-source.md
source_anchor:
  url: https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents
  section: "context engineering / tool design"
evidence_granularity: article_section
promotion_readiness: not_ready
```

VAKS borrow scope:

```text
Use in API/MCP read-first layer and retrieval tools: return source_ref,
selector, short context, citable_status, warnings, and drilldown path instead of
unbounded text.
```

Non-borrow scope:

```text
Do not omit provenance or selector-grade target in the name of compactness.
```

Candidate tags:

```text
agent-tools, mcp-read-layer, context-pack, provenance
```

## Proposed General Knowledge Point Candidates

| Candidate slug | Proposed type | Why general |
|---|---|---|
| `identifier-first-payload-later` | pattern | Applies to agent context and knowledge work systems with limited context windows. |
| `just-in-time-context-loading` | pattern | Applies to retrieval, context pack, and tool response design. |
| `progressive-disclosure-context-pack` | concept | Names a pack-compiler style beyond VAKS. |
| `context-compaction-is-runtime-hygiene` | anti-pattern boundary | Prevents compaction / memory summaries from becoming truth. |
| `tool-output-compact-context` | pattern | Applies to MCP/API/tool response design. |

Current status:

```text
candidate_only
```

Do not create `wiki/patterns/`, `wiki/concepts/`, or `wiki/anti-patterns/`
entries until reviewed.

## Tags Are Navigation Only

Candidate tags:

```yaml
tags:
  - context-engineering
  - agent
  - retrieval
  - context-pack
  - just-in-time-loading
  - progressive-disclosure
  - compaction
  - mcp-read-layer
  - activation
  - evidence-boundary
```

Rule:

```text
Tags help retrieval and dashboards.
Tags do not prove generality, adoption, truth, or action readiness.
```

## VAKS Project Borrowing View

This is a usage-layer borrowing view, not Project Overlay mainline.

```yaml
kp_candidate_ref: identifier-first-payload-later
borrow_scope: "Use path/title/heading/selector/item ID as pack skeleton before loading full payload."
non_borrow_scope: "Do not treat identifier presence as evidence support."
target_hint: "future retrieval/query contract; pack compiler; API/MCP read resources"
stance: partial
```

```yaml
kp_candidate_ref: just-in-time-context-loading
borrow_scope: "Use drilldown_path and citable_status to delay payload expansion until needed."
non_borrow_scope: "Do not hide action-facing evidence behind drilldown-only records."
target_hint: "future pack item contract; claim-to-evidence binding"
stance: partial
```

```yaml
kp_candidate_ref: progressive-disclosure-context-pack
borrow_scope: "Use summary before detail, identifier before payload, drilldown before dump."
non_borrow_scope: "Do not let summary-first become summary-only."
target_hint: "future pack compiler design"
stance: partial
```

```yaml
kp_candidate_ref: context-compaction-is-runtime-hygiene
borrow_scope: "Use compaction for long-running query/agent sessions as trace and activation aid."
non_borrow_scope: "Do not treat compacted agent context as reviewed knowledge."
target_hint: "future query-run trace; agent memory quarantine"
stance: watch
```

```yaml
kp_candidate_ref: tool-output-compact-context
borrow_scope: "Make retrieval/API/MCP read tools return compact but provenance-rich context."
non_borrow_scope: "Do not remove selector/target/provenance in the name of compactness."
target_hint: "future API/MCP read-first layer"
stance: partial
```

## Review / Promotion Requirements

Before any candidate becomes reviewed pattern/concept:

```text
1. Compare against at least one or two other agent/context engineering sources:
   OpenAI Agents SDK / Anthropic tool design / MemGPT / LlamaIndex / Haystack.

2. Check VAKS need:
   pack compiler and Codex skill design yes; implementation later.

3. Preserve boundary:
   context engineering improves activation and operational focus.
   it does not create evidence support or reviewed knowledge.

4. Decide destination:
   pattern for repeatable pack/tool behavior.
   concept for field/contract naming.
   anti-pattern boundary for compaction-as-truth risk.
```

