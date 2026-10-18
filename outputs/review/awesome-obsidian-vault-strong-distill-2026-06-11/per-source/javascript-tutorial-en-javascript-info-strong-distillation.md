---
record_kind: strong_candidate_distillation
status: candidate
provisional: true
knowledge_status: candidate
processing_tier: heavy
lifecycle_state: candidate_provisional
source_family: awesome-obsidian-vault
source_url: "https://github.com/javascript-tutorial/en.javascript.info"
repo_key: "javascript-tutorial/en.javascript.info"
checked_commit: "52c1e61915bc8970a950a3f59bd845827e49b4bf"
checked_at: 2026-06-11
derived_from:
  - outputs/review/awesome-obsidian-vault-strong-distill-2026-06-11/source-anchor-manifests/javascript-tutorial-en-javascript-info-anchor-manifest.json
retrieval_policy:
  policy_kind: orientation_only
  pack_allowed: activation_only
  action_basis_allowed: false
  warning_code: candidate_not_action_basis
promotion_gate: evidence_aware_review_required
action_basis_allowed: false
truth_mutation_allowed: false
borrow_value: high
borrow_order: P3
routing_hint:
  - authoring-contract
  - exercise-solution-pairing
  - executable-markdown
fit_layer:
  - capture-provenance
  - candidate-comprehension
  - publishing
  - maintenance
  - activation
not_fit_layer:
  - reviewed-knowledge
  - action-basis
  - automatic-truth-update
avoid:
  - "Do not import JavaScript tutorial content as local VAKS knowledge."
  - "Do not make executable code fences an evidence-support mechanism."
  - "Do not copy the whole publishing stack when only authoring contracts are needed."
dev_context_hint:
  default_layer: support
  core_only_when: "When designing VAKS authoring conventions for ordered lessons, tasks, solutions, and renderable examples."
  support_when: "When comparing structured tutorial repositories and link-stability rules."
  risk_when: "When executable examples could be mistaken for reviewed evidence or action readiness."
  cold_references:
    - outputs/review/awesome-obsidian-vault-strong-distill-2026-06-11/source-anchor-manifests/javascript-tutorial-en-javascript-info-anchor-manifest.json
tags:
  - candidate-only
  - strong-distillation
  - awesome-obsidian-vault
  - tutorial-authoring
  - executable-markdown
---

# Strong Candidate Distillation: javascript-tutorial / en.javascript.info

## Boundary

This file extracts authoring and publishing mechanisms from JavaScript.info. It
does not import JavaScript teaching content into VAKS, and it does not treat
executable demos or tests as evidence review.

## What This Source Actually Is

This repository is the English source content for the Modern JavaScript
Tutorial. It is not a loose note vault. It is a structured tutorial corpus with
chapter/article/task folders, enhanced Markdown syntax, task/solution pairs,
viewable examples, tests, translation rules, and authoring conventions.

For VAKS, its best value is in durable source organization and authoring
contracts.

## Source / Code Anchors

| Anchor | What exists | Design extraction | Boundary |
|---|---|---|---|
| `README.md` | Explains English tutorial source, translations, enhanced Markdown, and local server. | Source repo separate from rendered tutorial. | Tutorial content not imported. |
| `AUTHORING.md` | Root-relative link rule and `info:` scheme with auto-inserted title. | Prevent title drift and hardcoded domain drift. | Link convention is support tooling only. |
| `1-js/.../article.md` | Article content under ordered path. | Folder order encodes curriculum sequence. | Article facts still external. |
| `.../task.md` + `solution.md` | Exercise and solution paired in same task folder. | Atomic exercise units with answer boundary. | Solution is not evidence review. |
| `*.view/index.html` and `*.view/test.js` | Executable demos and tests. | Render/test artifacts can sit beside source. | Execution proves demo behavior only. |

## Strong Borrow Points

1. **Path order can encode curriculum order without external metadata.**  
   Numbered folder names (`1-js`, `02-first-steps`, etc.) make the reading path
   visible in the filesystem. VAKS can borrow this for training packs or
   project-local manuals, while keeping reviewed knowledge separate.

2. **File names declare semantic role.**  
   `article.md`, `task.md`, and `solution.md` are simple but strong contracts.
   VAKS can use this pattern for future learning/candidate lanes where a source
   explanation, prompt, and answer need clean boundaries.

3. **Link rules reduce long-term maintenance drift.**  
   `AUTHORING.md` forbids hardcoded absolute tutorial URLs and supports an
   `info:` scheme that derives titles from the target article. VAKS can borrow
   the principle: links should preserve source identity while minimizing stale
   duplicate titles.

4. **Executable examples should be sidecars, not canonical claims.**  
   `.view` folders keep runnable HTML/tests beside lessons. For VAKS, code
   demos or query examples should remain sidecar verification artifacts, not
   truth-bearing Markdown.

5. **Translation/source separation is a governance asset.**  
   The repo explicitly links translations to separate repositories. VAKS should
   similarly separate source intake, derived summaries, and rendered projection.

## VAKS Layer Mapping

| VAKS layer | Candidate value | Adopt shape |
|---|---|---|
| Capture / Provenance | Source repo and translation boundaries. | Source identity preserved. |
| Candidate Comprehension | Ordered article/task/solution corpus. | Candidate learning path. |
| Activation | Ordered folders and semantic file names. | Context-pack assembly hints. |
| Publishing | Enhanced Markdown render semantics. | Downstream renderer only. |
| Maintenance | Link rules and executable sidecars. | Lint and tests, not truth. |

## Local De-Dup / Collision

This overlaps with OSSU and DevCookbook:

- OSSU is a route map across external courses.
- DevCookbook is a small Markdown-to-object compiler.
- JavaScript.info is a full tutorial source tree with strong authoring
  contracts and adjacent exercises.

The unique borrow is the combination of ordered path, role-specific file names,
and link-stability rules.

## Anti-Borrow

- Do not turn VAKS into a tutorial engine by default.
- Do not import copyrighted tutorial prose or code wholesale.
- Do not treat runnable examples as evidence support for unrelated claims.
- Do not use folder order as truth priority.

## Candidate Tags

```yaml
domain: tutorial_source_authoring
problem: maintaining_large_ordered_learning_corpus_with_tasks_and_demos
pattern:
  - numbered-folder-order
  - semantic-file-role-contract
  - task-solution-pair
  - root-relative-link-rule
  - executable-demo-sidecars
maturity: production-tutorial-source
problem_fit: 4
reuse_value: 5
implementation_cost: 3
integration_fit: 4
evidence_strength: 4
reversibility: 4
```

## Fusion Judgment

Borrow strongly for authoring contracts and sidecar demo boundaries. Do not
borrow the JavaScript content itself.
