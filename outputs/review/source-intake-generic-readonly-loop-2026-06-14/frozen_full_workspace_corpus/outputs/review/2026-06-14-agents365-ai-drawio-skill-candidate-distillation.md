---
record_kind: candidate_distillation
status: candidate
provisional: true
knowledge_status: candidate
processing_tier: medium
lifecycle_state: candidate_provisional
overlay_state: none
review_pressure: none
source_ref: raw/repos/2026-06-14-agents365-ai-drawio-skill-source.md
derived_from:
  - raw/repos/2026-06-14-agents365-ai-drawio-skill-source.md
  - raw/repos/_snapshots/2026-06-14-Agents365-ai-drawio-skill-00ed825-source.zip
  - wiki/summaries/2026-06-14-agents365-ai-drawio-skill-architecture-review.md
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
  - architecture-documentation
  - productization
  - generated-artifact-quality
  - misa-codebase-visualization
possible_project_refs:
  - verified-action-knowledge-system
point_anchor_refs:
  - "README.md:17"
  - "skills/drawio-skill/SKILL.md:22"
  - "skills/drawio-skill/SKILL.md:96"
  - "skills/drawio-skill/SKILL.md:113"
  - "skills/drawio-skill/references/autolayout.md:81"
  - "skills/drawio-skill/references/shapes.md:1"
  - "skills/drawio-skill/scripts/validate.py:48"
  - "tests/test_scripts.py:1"
borrow_value: medium
borrow_order: P2
dev_context_hint:
  default_layer: support_with_required_risk
  core_only_when: "An approved task is specifically about generating VAKS/MISA architecture diagrams."
  support_when: "Productization, documentation, onboarding, architecture visual explanation, or codebase visualization work."
  risk_when: "A generated diagram is cited as evidence, review pass, or action basis."
  cold_references:
    - raw/repos/2026-06-14-agents365-ai-drawio-skill-source.md
    - raw/repos/_snapshots/2026-06-14-Agents365-ai-drawio-skill-00ed825-source.zip
avoid:
  - "Do not treat generated diagrams as evidence support."
  - "Do not make draw.io generation part of VAKS core review."
  - "Do not treat visual self-check or script tests as reviewed approval."
  - "Do not replace source anchors with diagrams."
tags:
  - candidate
  - provisional
  - drawio
  - diagram-generation
  - architecture-documentation
---

# 候选蒸馏：drawio-skill

## Boundary

This note is provisional orientation.

It can help route attention, compare ideas, or suggest project overlays. It is not reviewed knowledge, not a decision, not a formal pattern, and not action basis.

## 一句话结论

这个库值得留，但定位要收窄：

```text
drawio-skill = 架构图 / 工作流图 / 代码结构图的生产工具
不是 VAKS 知识逻辑
不是 evidence/review/truth/action 机制
```

对我们最有用的是：

```text
把复杂 VAKS/MISA 逻辑画清楚
把代码结构变成可读图
给生成图加 lint/self-check/feedback loop
```

## Source

```yaml
derived_from:
  - raw/repos/2026-06-14-agents365-ai-drawio-skill-source.md
  - raw/repos/_snapshots/2026-06-14-Agents365-ai-drawio-skill-00ed825-source.zip
point_anchor_refs:
  - snapshot_ref: raw/repos/_snapshots/2026-06-14-Agents365-ai-drawio-skill-00ed825-source.zip
    selector_type: file_line
    selector_value: skills/drawio-skill/SKILL.md:96
  - snapshot_ref: raw/repos/_snapshots/2026-06-14-Agents365-ai-drawio-skill-00ed825-source.zip
    selector_type: file_line
    selector_value: skills/drawio-skill/scripts/validate.py:48
```

## Candidate Points

### Candidate Point 1: Generated diagrams belong to output/view layer

The skill is strong at:

```text
natural language / graph JSON / code imports
-> .drawio XML
-> preview/export
-> visual iteration
```

For VAKS, this maps to:

```text
architecture explanation
onboarding
product documentation
review workflow visualization
```

It does not map to:

```text
truth confidence
evidence support
review pass
action readiness
```

### Candidate Point 2: Lint before visual review is a real pattern

The repo's strongest reusable workflow is:

```text
generate .drawio
-> validate.py structural lint
-> export preview
-> self-check visual issues
-> user feedback loop
-> final export
```

For us, this becomes a general principle:

```text
Generated artifacts should be structurally checked before they are shown or reused.
But checks are diagnostics, not truth or approval.
```

### Candidate Point 3: Codebase visualization can help MISA

The repo has import graph extractors for:

```text
Python
JS/TS
Go
Rust
Python class hierarchy
```

This can help MISA understand a codebase quickly:

```text
repo -> import graph -> autolayout -> editable diagram
```

But the boundary matters:

```text
static import graph != runtime behavior
class hierarchy != architecture decision
diagram != source evidence
```

### Candidate Point 4: Shape search reduces visual hallucination

The skill does not guess cloud/vendor shape strings. It searches a local official draw.io shape index.

This is useful because guessed visual symbols can silently render as blank boxes.

For VAKS product diagrams:

```text
search exact shape/style
embed or cite icon source when needed
avoid fake-looking diagrams
```

But this is only output hygiene.

### Candidate Point 5: Style presets are useful product UX, not knowledge

The style preset flow is useful because it separates:

```text
content structure
visual style
user approval
saved preset
```

For VAKS productization, this could inspire:

```text
consistent visual language for capture/review/action states
diagram style presets for docs
brand/product export style
```

It should not affect knowledge status.

### Candidate Point 6: Browser fallback and editable export are good delivery patterns

The skill has:

```text
.drawio source
PNG/SVG/PDF/JPG exports
embedded editable XML
diagrams.net URL fallback
PNG repair for embedded exports
```

This is useful for publishing and handoff: diagrams remain editable, not dead screenshots.

## What We Should Borrow

Borrow:

```text
P2: diagram/documentation sidecar for VAKS productization
P2: generated artifact lint -> visual check -> feedback loop
P2: codebase visualization for MISA/debugging
P3: style preset idea for product/brand exports
P3: exact shape/icon search for polished architecture diagrams
```

Do not borrow:

```text
diagram output as truth
visual self-check as review approval
script test pass as mainline readiness
draw.io CLI as required VAKS core dependency
diagram generation in ordinary source intake
```

## Does It Help VAKS?

Yes, but only as a sidecar.

| Area | Help Level | Why |
|---|---:|---|
| Architecture explanation | 8/10 | Can make VAKS layers/flows easier to understand. |
| Product onboarding | 7/10 | Can produce polished diagrams and exports. |
| Review logic / evidence | 1/10 | No evidence/review logic. |
| Source intake | 2/10 | Not an intake engine. |
| MISA codebase debugging | 7/10 | Import/class graph visualization is useful. |
| Core VAKS architecture | 2/10 | Only output/view layer. |

## Open Questions

- Should future VAKS docs have a `products/diagrams/` or `outputs/review/diagrams/` area?
- Should every generated architecture diagram include a small footer: `derived view, not evidence`?
- Should MISA use diagrams for codebase orientation only after source files are read?
- Should source prompts and graph JSON be stored next to generated `.drawio` files for traceability?

## Routing Hint

Route this source to:

```text
VAKS productization
architecture documentation
diagram/export workflow
MISA codebase visualization
generated artifact QA
```

Do not route it to:

```text
VAKS truth layer
evidence support
review queue authority
action basis
retrieval/memory design
```

## Forbidden

```text
project_borrow_scope as adoption decision
decision outcome
formal pattern
action basis
truth confidence
diagram-as-evidence
visual-check-as-review-pass
```

## Local Verification

Executed:

```text
python -m unittest discover -s tests -v
```

Result:

```text
Ran 21 tests in 1.597s
OK
```

Not executed:

```text
draw.io desktop CLI export
Graphviz real layout
vision self-check
```

## Final Judgment

```text
borrow_value: medium
borrow_order: P2
best_use: VAKS/MISA diagrams, architecture explanation, generated artifact QA
not_best_use: core knowledge logic, review, evidence, action
```

说人话：

```text
这不是我们架构逻辑的补药。
这是把我们复杂架构讲清楚、画漂亮、可交付的工具。
值得留，别神化。
```
