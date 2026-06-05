---
type: dual_project_reuse_validation
status: candidate
created_at: 2026-06-05
project: verified-action-knowledge-system
scope: candidate-pattern-cross-project-contextualization
truth_boundary: validation output only; not reviewed knowledge; not architecture decision
write_scope: outputs/review only
projects:
  - VAKS
  - misa-cybernetic-evolution
---

# v0.2.13 Dual Project Reuse Validation

## 说人话结论

这个验证回答一个问题：

```text
同一个通用候选点，能不能在两个项目里得出不同借鉴结论，
但不污染候选点本体？
```

结果：

```text
pass
```

Candidate Pattern Bank 可以继续作为“通用候选知识点库”。
Project Borrowing Ledger / Workspace 应该继续作为“项目开发区 / 借鉴目录”。
不同项目的借鉴姿态不能回写成 pattern 的全局 truth。

## Test Setup

只读参照：

```text
VAKS:
  C:\Users\Administrator\Documents\资料库

Misa:
  C:\Users\Administrator\Documents\New project\misa-cybernetic-evolution
```

Misa 只读证据：

```text
README.md
ARCHITECTURE.md
docs/current/retrieval-lineage-v0.19.md
docs/current/vector-retrieval-ranker-v0.20.md
docs/current/control-boundaries.md
```

No files were written in Misa.

## Candidate Pattern Under Test

```text
retrieval-is-activation-not-truth
```

通用候选点：

```text
retrieval / vector similarity / rerank / GraphRAG / community summary / agentic retrieval
bring material forward, but they are not truth confidence, reviewed relation, or action basis.
```

## Project 1: VAKS

### Borrowing Entry

```yaml
project: VAKS
pattern_id: retrieval-is-activation-not-truth
disposition: adapt
target_locus:
  - MEMORY_TIER
  - context-pack rules
  - review queue wording
why_fit:
  - VAKS explicitly separates retrieval / activation from reviewed support.
  - VAKS needs this boundary to prevent source hits, graph rank, dashboard output, or context pack preparation from becoming truth.
required_gates_before_promotion:
  - wording review before any template patch
  - ordinary query lightweighting check
  - no retrieval score as truth confidence
```

### Meaning

For VAKS, the pattern is directly project-fit because VAKS is a knowledge/review/action-basis system. The boundary belongs near memory tier, context pack, and review wording.

VAKS result:

```text
adapt
```

## Project 2: Misa Cybernetic Evolution

### Read-Only Project Context

Misa describes itself as a control-theoretic sidecar for long-lived AI agents. Its core boundary is:

```text
agents do not get to grade themselves
evidence -> distill -> route -> candidate -> work order variants -> quality eval -> work order -> owner or primary agent
```

Relevant Misa constraints:

```text
candidate and audit records may explain context, but cannot change behavior
vector-memory ranker is dry-run only
same-source context can explain, but cannot outrank a valid primary-kind hit
runtime observations do not become promotion authority
LLMs must not decide route, memory write, winner, provider route, production update, or public posting approval
```

### Borrowing Entry

```yaml
project: misa-cybernetic-evolution
pattern_id: retrieval-is-activation-not-truth
disposition: already_aligned_no_new_borrowing
target_locus:
  - retrieval lineage explanation
  - vector-memory ranker boundary
  - control-boundary wording
why_fit:
  - Misa already implements the same kind of separation: retrieval/audit/candidate records can explain but cannot directly alter behavior.
  - The pattern can be used as a review lens, but not as a new architecture change.
required_gates_before_promotion:
  - none for current architecture; existing docs already carry the core boundary
  - any future live retriever change still needs explicit approval and reversible probe
  - no memory write, route authority, or live behavior change from retrieval hits
```

### Meaning

For Misa, the pattern is not a new project borrowing opportunity. It is already embedded in the control boundary and retrieval-lineage docs. The useful project posture is:

```text
already aligned; do not create a new borrowing action
```

Misa result:

```text
already_aligned_no_new_borrowing
```

## Cross-Project Result

Same candidate pattern, different project dispositions:

| Pattern | VAKS | Misa |
| --- | --- | --- |
| `retrieval-is-activation-not-truth` | `adapt` | `already_aligned_no_new_borrowing` |

This is the desired behavior.

It proves:

```text
candidate pattern = reusable candidate knowledge
project borrowing entry = project-specific contextualization
```

It blocks:

```text
VAKS adapt -> all projects should adapt
Misa already aligned -> pattern is globally adopted
same pattern appears in two projects -> stronger truth support
```

## Second Pattern Spot Check

Pattern:

```text
source-structure-first-rag
```

VAKS posture:

```text
adapt as source intake / context-pack design pressure
```

Misa posture:

```text
watch_only
```

Reason:

```text
Misa already has retrieval lineage and source trace concerns, but it is a runtime/control sidecar,
not a general document/source-intake vault. Requiring VAKS-style source-structure intake
would risk pulling a knowledge-vault pattern into a control-plane repository where it is
not the current bottleneck.
```

This second check also passes:

```text
same reusable pattern
different project fit
no pollution of pattern definition
```

## Validation Verdict

```text
dual_project_reuse_validation: pass
```

What this validates:

```text
Candidate Pattern Bank can hold reusable candidate mechanisms.
Project Borrowing Ledger / Workspace can record project-specific fit.
Different projects can disagree without changing the pattern body.
```

What this does not validate:

```text
mainline promotion
truth confidence
action readiness
stable directory migration
```

## Implication For VAKS

Keep the separation:

```text
Candidate Pattern Bank:
  reusable mechanism, applicability, non-goals, source families

Project Borrowing Workspace:
  project-specific disposition, target locus, why fit/not fit, required gates
```

Do not let one project's borrowing entry rewrite the global candidate pattern.
