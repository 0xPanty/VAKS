---
type: library_review
status: draft
library_name: "drawio-skill"
repo_url: "https://github.com/Agents365-ai/drawio-skill"
source_url: "raw/repos/2026-06-14-agents365-ai-drawio-skill-source.md"
checked_commit: 00ed825c4aec623a5838a16d1ad6b7a2c603dfa6
commit_time: 2026-06-04T00:53:31+08:00
source_status: active
reviewed_at: 2026-06-14
domain:
  - diagram-generation
  - architecture-documentation
  - agent-skill
  - codebase-visualization
related_projects:
  - verified-action-knowledge-system
current_branch: "VAKS architecture/product documentation and future MISA codebase visualization"
extracted_patterns:
  - generated-diagram-as-derived-view
  - deterministic-artifact-lint-before-visual-review
  - codebase-graph-to-editable-diagram
  - shape-search-before-style-string
fusion_decision: adapt
confidence: medium
evidence_count: 20
cross_validated_with:
  - "VAKS output/view/dashboard not truth boundary"
  - "test and visual checks are diagnostics, not approval"
negative_evidence:
  - "No knowledge review/evidence/action-basis model."
  - "Requires draw.io desktop CLI for full export workflow."
  - "Generated diagrams can mislead if treated as source evidence."
extension_potential: "Useful as VAKS product/documentation sidecar and MISA codebase visualization helper; not useful as VAKS core logic."
relations: []
tags:
  - architecture-review
  - drawio
  - diagram-generation
  - architecture-documentation
---

# 库分析：drawio-skill

## 它解决什么问题

它解决的不是“怎么让知识可靠”，而是：

```text
自然语言 / 代码结构 / 图表需求
-> 规划图表
-> 生成 .drawio XML
-> 校验结构
-> 导出 PNG/SVG/PDF/JPG
-> 视觉自检和用户反馈迭代
```

说人话：它帮 agent 产出更专业、可编辑、可导出的 draw.io 图。对我们有用，但它属于表达层 / 文档层 / 工作流可视化层。

## 核心设计

```text
SKILL.md as orchestration manual
references/ as on-demand submanuals
scripts/ as deterministic helpers
data/ as local shape/icon index
styles/ as visual presets
assets/ and docs/ as examples and user-facing docs
tests/ as dependency-free regression suite
```

关键流水线：

```text
resolve style preset
-> check draw.io CLI
-> choose diagram preset/resources
-> generate .drawio XML
-> validate.py lint
-> export preview PNG
-> vision self-check / auto-fix
-> user feedback loop
-> final export with embedded editable XML
```

## Source / Code Anchors

| Anchor | What exists | Design extraction | Boundary |
|---|---|---|---|
| `README.md:17` | States natural language to `.drawio` XML and export via native draw.io CLI. | Confirms core product path. | Diagram output is not evidence. |
| `README.md:26-30` | Highlights codebase visualization, shape search, AI logos, self-check, iteration. | Strong output/product workflow ideas. | README claims still need code anchors. |
| `skills/drawio-skill/SKILL.md:3-7` | Version 1.14.0, scope, dependencies, platform metadata. | Skill packaging and dependency contract. | Runtime dependency is not VAKS dependency. |
| `skills/drawio-skill/SKILL.md:22-29` | When to use / not use routing guidance. | Good tool-selection boundary. | Routing guidance is not architectural adoption. |
| `skills/drawio-skill/SKILL.md:31-49` | Bundled resources table with references/scripts loaded on demand. | Good progressive-disclosure skill design. | This is agent instruction structure, not knowledge schema. |
| `skills/drawio-skill/SKILL.md:96-107` | Generate step uses hand placement for small diagrams, autolayout for large/code graphs, validate before export. | Excellent generated-artifact workflow. | Generated artifact remains derived view. |
| `skills/drawio-skill/SKILL.md:113-128` | Vision self-check catches overlap, clipped labels, missing connections, edge-shape overlap, stacked edges. | Useful UI/artifact QA checklist. | Visual QA is diagnostic, not review. |
| `skills/drawio-skill/SKILL.md:133-149` | Feedback loop applies targeted XML edits and caps iteration at 5 rounds. | Good human-in-loop artifact refinement. | Feedback improves artifact, not truth. |
| `skills/drawio-skill/references/autolayout.md:1-17` | Graphviz autolayout for large/layout-heavy diagrams. | Good scale strategy for architecture/code diagrams. | Graphviz layout is aesthetic/topological, not semantic truth. |
| `skills/drawio-skill/references/autolayout.md:81-114` | Importers for Python, JS/TS, Go, Rust, Python class hierarchy and transitive reduction. | Useful MISA codebase visualization. | Static import graph is partial. |
| `skills/drawio-skill/references/shapes.md:1-16` | Local official shape index search. | Avoid hallucinated `shape=mxgraph.*` strings. | Shape match quality is output hygiene. |
| `skills/drawio-skill/references/shapes.md:48-67` | AI/LLM brand logo lookup; CDN default, embed option. | Useful for LLM/RAG diagrams. | CDN icons are not archival evidence unless embedded. |
| `skills/drawio-skill/scripts/autolayout.py:51-66` | Loads palette from built-in style file. | Single source of visual style. | Style is presentation. |
| `skills/drawio-skill/scripts/autolayout.py:108-155` | Builds Graphviz dot and runs `dot -Tplain`. | Real autolayout implementation. | Requires Graphviz. |
| `skills/drawio-skill/scripts/autolayout.py:179-312` | Emits draw.io XML with containers, relative geometry, edge waypoints. | Converts graph/layout into editable diagram. | XML correctness still needs validation/export check. |
| `skills/drawio-skill/scripts/validate.py:24-97` | Parses geometry, checks dangling endpoints, duplicate/reserved ids, parent refs, overlap warnings. | Deterministic artifact lint pattern. | Lint pass is not approval. |
| `skills/drawio-skill/scripts/shapesearch.py:27-139` | Loads shape index, builds tag map, searches styles. | Local shape search helper. | Search rank is heuristic. |
| `skills/drawio-skill/scripts/aiicons.py:33-127` | Loads lobe-icons manifest, groups variants, searches and picks logo variant. | AI/RAG brand diagram support. | External CDN use needs caution. |
| `tests/test_scripts.py:1-271` | Dependency-free regression tests across shape search, icons, URL encoding, autolayout, validator, importers. | Good project hygiene. | Tests are diagnostic, not VAKS truth. |

## 当前支线价值

当前支线：

```text
VAKS architecture/product documentation and future MISA codebase visualization.
```

它对当前支线：

```text
refines
```

具体价值：

- Can help produce readable VAKS architecture diagrams, review workflow diagrams, context-pack flow diagrams, and product onboarding diagrams.
- Can help MISA visualize code/module structure when debugging architecture.
- Provides a good generated-artifact quality pattern: deterministic lint first, visual self-check second, human feedback loop last.

风险：

- The pretty diagram can create false confidence.
- Generated diagram might omit hard evidence, risks, counterevidence, or scope limitations.
- Static code import graphs may be mistaken for runtime architecture.
- Visual self-check or unit tests may be mistaken for review approval.

## 全貌架构价值

| Architecture Zone | Value / Finding | Adopt? |
|---|---|---|
| Karpathy spine | Can make simple public story diagrams clearer. | adapt as output |
| Dusk workbench | Can support dashboards/workbench visuals and onboarding. | adapt |
| source ingest | Not a source-intake engine. | no |
| review queue | Can visualize review funnel, but cannot review. | adapt as view only |
| schema / reviewed knowledge | No reviewed knowledge schema. | no |
| memory / dev context | Can visualize dev-context packs or code graphs. | support only |
| feedback | Feedback loop is artifact-editing loop, not knowledge feedback. | borrow boundary wording |
| retrieval / cache | No retrieval model. | no |
| API / MCP / agent access | Skill packaging and on-demand references are useful instruction design. | watch/adapt |
| viewer / workbench | Strong: editable diagrams, exports, style presets. | adapt |
| publishing | Strong: PNG/SVG/PDF/JPG export, embedded editable XML. | adapt |
| risk / anti-pattern | Risk: diagram-as-truth / test-as-approval. | keep as warning |

## 值得提炼的模式

### Pattern 1: Generated Diagram Is A Derived View

```text
source / architecture notes / code graph
-> generated diagram
-> human-readable explanation
```

The diagram can explain. It cannot prove.

### Pattern 2: Deterministic Artifact Lint Before Visual Review

For diagram generation:

```text
validate.py
-> export preview
-> visual self-check
-> user feedback
```

For VAKS product/export surfaces, this maps to:

```text
machine structural check
-> human visual/usefulness check
-> no automatic truth promotion
```

### Pattern 3: Codebase Graph As MISA Debug View

The import/class graph extractors can help agents understand code topology:

```text
pyimports / jsimports / goimports / rustimports / pyclasses
-> graph JSON
-> autolayout
-> editable .drawio
```

Useful for MISA debugging, but:

```text
static graph != runtime behavior
diagram != verified architecture
```

### Pattern 4: Search Before Guessing Vendor Shapes

The shape search pattern is a concrete anti-hallucination move for visual outputs:

```text
do not guess shape=mxgraph.*
search official local index
copy exact style
```

This is an output-quality idea, not a knowledge-quality idea.

## 标签与量化

- domain: diagram generation / documentation / agent skill
- problem: agents produce poor or non-editable architecture diagrams without a structured workflow
- pattern: generated-diagram-as-derived-view
- maturity: emerging
- complexity: medium
- problem_fit: 4/5 for VAKS documentation/productization
- reuse_value: 4/5 for diagrams, 2/5 for core architecture
- implementation_cost: 2/5 if used as external skill, 4/5 if reimplemented
- integration_fit: 3/5
- evidence_strength: 3/5
- reversibility: 5/5

## 交叉验证

- 相似设计来源：Mermaid/PlantUML/Excalidraw/Tldraw-style diagram tools; draw.io desktop CLI.
- 用户历史项目里的相似问题/影子：VAKS needs architecture and workflow explanation; MISA may need codebase maps.
- 支持证据：Repo includes SKILL.md, references, scripts, shape/icon data, docs, tests, and examples.
- 反例或失败边界：Diagram aesthetics may hide unsupported assumptions.
- 最小验证方式：Use it on a sandbox copy to draw VAKS intake/review/action flow; ensure each diagram carries "derived view, not evidence" label.

## Knowledge Calibration / Point Collision

| Candidate Point | Local Reviewed Knowledge | Calibration Output | Review Question |
|---|---|---|---|
| Generated diagrams can improve architecture explanation. | Dashboard/view/output is not truth. | candidate_relation | Where should generated diagrams live: products/, outputs/review/, or docs assets? |
| Visual self-check can catch artifact errors. | Tests/LLM-judge/benchmarks are diagnostic, not review approval. | supports as warning | How should diagram QA be labeled so it cannot become review pass? |
| Code import graph can help MISA understand projects. | Dev Context uses Core/Support/Risk/Cold and activation is not truth. | refines | Should code graphs enter dev context as Support, never Core by themselves? |
| Shape search reduces visual hallucination. | Source/extraction tools do not create reviewed knowledge. | candidate_relation | Should output tools record their source shape/icon provenance? |

## Support / Challenge Review

- What supports it:
  - Code and docs show concrete scripts for autolayout, validation, shape search, AI icons, and import graph extraction.
  - Local regression tests passed: `21 tests OK`.
- What challenges it:
  - No draw.io CLI export was run in this intake.
  - It is a visual artifact tool, not a knowledge validation tool.
  - Some icon paths default to CDN references.
- Challenge severity: minor for documentation use; major if misused as evidence/review.
- Scope limits:
  - Use as diagram/documentation/productization sidecar.
  - Do not use as VAKS truth/review/action layer.
- Known risks:
  - diagram-as-truth
  - static-code-graph-as-runtime-architecture
  - visual-QA-as-review-pass
  - CDN logo dependency for archival outputs
- Review again when:
  - VAKS starts publishing diagrams.
  - MISA uses code graphs for debugging.
  - Generated diagrams are cited in action-facing decisions.
- Action readiness: not_ready

## 对当前项目的适配点

Potential VAKS uses:

```text
public five-layer story diagram
internal loop diagram
source intake state machine diagram
review queue / evidence packet diagram
MISA bridge diagram
product onboarding visuals
```

Potential MISA uses:

```text
module/import graph for codebase understanding
class hierarchy diagram for backend/runtime components
architecture map for handoff/debug
```

Required label on generated diagrams:

```text
derived_view_only: true
action_basis_allowed: false
source_notes_required: true
```

## 可拓展性

- 是否适合作为插件/适配层：yes, as external skill/tool.
- 是否会绑定核心结构：no, if kept in output/product layer.
- 未来替换成本：low; Mermaid/PlantUML/Figma/Excalidraw can replace per use case.
- 可迁移路径：
  1. Keep generated diagrams under outputs/products/docs assets.
  2. Store source prompt/spec next to diagram.
  3. Label diagram as derived view.
  4. Link back to source docs/anchors.
  5. Never count diagram as support.

## 复杂度和风险

Complexity is moderate because draw.io CLI, optional Graphviz, and visual review can fail depending on environment.

For VAKS, this is acceptable only as a sidecar. Reimplementing the whole tool would be overdesign.

## 不可行点 / 避坑

- Do not import as a VAKS core module.
- Do not use generated diagrams as evidence support.
- Do not treat visual self-check as human review.
- Do not make diagram generation mandatory in ordinary intake.
- Do not let a diagram replace the source anchors it summarizes.
- Do not rely on CDN icons for archival/offline diagrams unless embedded.

## 融合判断

- 结论：adapt
- 理由：Very useful for architecture/documentation/productization, weak for core VAKS logic.
- 验证方式：Run one sandbox diagram for a VAKS workflow and check whether it improves comprehension without hiding boundaries.

## 直接判断

- Direct use: maybe, as external skill when diagrams are needed.
- Fork: no.
- Design-only: yes for workflow and boundaries.
- Reject: no.
- Current branch value: medium for productization/docs; low for knowledge logic.
- Whole architecture value: support layer only.
- Risk: diagram-as-truth / test-as-approval.
- Next action: keep candidate-only; use later in a diagram/productization sandbox.

## 后续行动

- Add to a future product/documentation screening batch, not P0 architecture.
- If used, pair every generated diagram with source prompt, source docs, and "derived view only" label.
