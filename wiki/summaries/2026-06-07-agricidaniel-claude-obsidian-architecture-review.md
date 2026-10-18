---
type: library_review
record_kind: architecture_review
status: draft
knowledge_status: candidate
processing_tier: heavy
library_name: claude-obsidian
repo_url: https://github.com/AgriciDaniel/claude-obsidian
source_url: https://github.com/AgriciDaniel/claude-obsidian
checked_commit: cb93ff6d82f9c35a08bf6010e7fac36dfddc827b
commit_time: 2026-05-28T00:42:42Z
source_status: active
reviewed_at: 2026-06-07
domain: AI Obsidian wiki / Claude Code skills / second brain
related_projects:
  - verified-action-knowledge-system
current_branch:
  - source-intake
  - activation-tier
  - dev-context
  - agent-write-safety
extracted_patterns:
  - skill catalog as action surface
  - hot index log recovery spine
  - per-file locking for AI writes
  - retrieval cache with egress gate
  - methodology router as filing policy
  - lint verifier as diagnostics
fusion_decision: adapt
confidence: medium
evidence_count: 25
retrieval_policy:
  policy_kind: orientation_only
  pack_allowed: activation_only
  action_basis_allowed: false
  warning_code: candidate_review_not_action_basis
promotion_gate: v0_2_13_required
action_basis_allowed: false
truth_mutation_allowed: false
cross_validated_with:
  - raw/articles/2026-06-06-x-cyrilxbt-claude-obsidian-90-days-source.md
  - wiki/summaries/2026-05-27-kepano-obsidian-architecture-review.md
  - raw/repos/2026-06-04-langchain-miniopenclaw-source.md
negative_evidence:
  - generated wiki pages can be misread as reviewed knowledge
  - auto-research and auto-commit are too strong for VAKS defaults
  - retrieval score and dashboard output are not evidence support
extension_potential: strong for tool/workbench layer, limited for truth/review layer
relations:
  - target: SOURCE_INTAKE.md
    type: refines
    relation_state: candidate
    strength: 3
    confidence: medium
    evidence:
      - raw/repos/2026-06-07-agricidaniel-claude-obsidian-source.md
    rationale: "The repo provides implementation examples for raw/generated split, manifest, and ingest flow, but needs VAKS candidate/review boundaries."
  - target: DEV_CONTEXT.md
    type: refines
    relation_state: candidate
    strength: 4
    confidence: medium
    evidence:
      - raw/repos/2026-06-07-agricidaniel-claude-obsidian-source.md
    rationale: "hot/index/log and skill router are useful for activation and project recovery."
  - target: FEEDBACK.md
    type: refines
    relation_state: candidate
    strength: 3
    confidence: medium
    evidence:
      - raw/repos/2026-06-07-agricidaniel-claude-obsidian-source.md
    rationale: "lint/verifier/GROW outputs are process feedback and review pressure, not truth mutation."
---

# 库分析：AgriciDaniel/claude-obsidian

## 它解决什么问题

它解决的是：

```text
让 Claude Code 能把 Obsidian vault 当成一个会增长的本地 wiki 来维护。
```

具体做法是：

```text
source / URL / session
-> skills
-> generated wiki pages
-> hot cache / index / log
-> query / lint / save / canvas / autoresearch
```

它不是 VAKS 这种 reviewed-action knowledge system。它更像：

```text
Karpathy LLM Wiki
+ Obsidian
+ Claude Code skills
+ locks/hooks/retrieval/mode router
```

## 核心设计

核心结构：

```text
.raw/
  source documents, treated as immutable except manifest.

wiki/
  agent-generated knowledge pages.

wiki/hot.md
  recent context cache.

wiki/index.md
  master catalog.

wiki/log.md
  append-only operation log.

skills/
  action modules for wiki, ingest, query, lint, save, retrieval, mode, canvas, autoresearch.

scripts/
  lock, transport, retrieval, rerank, mode routing, address allocation.

hooks/
  session start, post-tool-use, stop hooks for hot-cache and auto-commit behavior.
```

Architecture judgment:

```text
Great implementation reference for VAKS tool/workbench layer.
Not a replacement for VAKS source/candidate/reviewed/action-basis architecture.
```

## Source / Code Anchors

| Anchor | What exists | Design extraction | Boundary |
|---|---|---|---|
| `README.md:20-27` | 15 skills, multi-writer safety, methodology modes, hybrid retrieval, Obsidian CLI | Implementation-level repo, not just concept | README is self-description |
| `README.md:173-208` | Commands and `/wiki` scaffold | Command-to-skill routing surface | Commands are not permission |
| `README.md:287-315` | Cross-project hot/index read order and generated files | Lightweight activation/recovery spine | hot/index/log are not truth |
| `README.md:325-350` | vault flow, multi-writer locking, hybrid retrieval diagrams | Main architectural zones are explicit | Diagram is not validation |
| `AGENTS.md:29-38` | Trigger map for skills | Skill registry can be simple Markdown/table | VAKS trigger rules remain stricter |
| `AGENTS.md:43-56` | vault root, hot cache, raw source, generated knowledge, manifest, startup | Project-local operating manual pattern | Do not globalize this AGENTS |
| `CLAUDE.md:41-46` | cross-project wiki reading rule and do-not-read-general-coding warning | Context activation gate | Does not encode VAKS authority buckets |
| `CLAUDE.md:67-75` | transport detection, wiki-lock, mode router | Tool selection and write safety | Transport is not authorization |
| `CLAUDE.md:77-79` | verifier agent before non-trivial commits | Non-author review pass | Advisory, not evidence support |
| `WIKI.md:143-185` | `.raw/`, `wiki/`, `index.md`, `hot.md`, `log.md` definitions | Concrete wiki spine | generated wiki still candidate |
| `WIKI.md:423-486` | ingest/query/lint flows | Source workflow with maintenance report | Missing VAKS promotion gates |
| `skills/wiki-ingest/SKILL.md:50-82` | per-file lock, PostToolUse deferral, manifest | AI write safety and duplicate skipping | Not permission to auto-write |
| `skills/wiki-ingest/SKILL.md:163-178` | single-source ingest checklist | Anti-omission ingest flow | Must map to raw/candidate/review in VAKS |
| `skills/wiki-query/SKILL.md:49-73` | quick/standard/deep query tiers | Query depth scales with question | VAKS needs authority-bucket filtering |
| `skills/wiki-lint/SKILL.md:12-18` | lint writes report and asks before fixing | Maintenance manifest analogue | Diagnostic only |
| `skills/wiki-lint/SKILL.md:214-230` | lint error vs assignment responsibility split | Observe vs mutate separation | No truth mutation |
| `skills/wiki-retrieve/SKILL.md:15-24` | egress consent gate for contextual prefix | Privacy-aware retrieval | External API off by default for VAKS |
| `skills/wiki-retrieve/SKILL.md:128-178` | BM25-only, explain mode, manual refresh | Retrieval as derived cache | Retrieval score not support |
| `scripts/wiki-mode.py:2-18` | mode router as single source of truth | Filing policy centralized | Methodology not authority |
| `scripts/wiki-mode.py:146-184` | generic/LYT/PARA/Zettelkasten routes | Supports multiple filing styles | No global default |
| `hooks/hooks.json:3-17` | SessionStart hot-cache load and stale lock clear | Recovery hook | Hook-injected context is not reviewed |
| `hooks/hooks.json:33-50` | PostToolUse auto-commit guarded by locks; Stop hot-cache prompt | Complete automation loop | Too aggressive for VAKS default |
| `PRIVACY.md:25-33` | optional egress table | Explicit consent-gated network behavior | Policy claim needs code/use check for production |
| `Makefile:10-25` | hermetic tests for retrieval/concurrency/mode/contextual | repo has test surface | tests not run in this intake |

## 当前支线价值

当前支线：

```text
VAKS source intake, Obsidian distillation skill, activation/dev-context, and future agent write safety.
```

它对当前支线：

```text
refines / risk_of
```

具体价值：

- Gives concrete skill decomposition for a source-intake tool layer.
- Shows `hot.md + index.md + log.md` as a compact activation and recovery spine.
- Provides lock/hook/manifest patterns for safer AI file writes.
- Shows retrieval as optional cache with privacy/egress gates.
- Shows methodology routing as a filing-policy adapter.

风险：

- Auto-commit and broad wiki writes are too strong for VAKS defaults.
- Auto-research output can look like knowledge before review.
- The repo's `wiki/` does not distinguish candidate/reviewed/action-basis.
- Retrieval and dashboards can be overread as authority.

## 全貌架构价值

| Architecture Zone | Value / Finding | Adopt? |
|---|---|---|
| Karpathy spine | Very strong implementation of `.raw -> wiki -> index/hot/log` | adapt |
| Dusk workbench | Canvas/dashboard/hot cache can inform workbench UX | adapt later |
| source ingest | Manifest, duplicate hash check, full ingest checklist are useful | adapt |
| review queue | Weak: generated wiki lacks VAKS candidate/review separation | do not adopt directly |
| schema / reviewed knowledge | Not enough for VAKS; source pages can blur into claims | reject as truth schema |
| memory / dev context | hot/index/log and cross-project read rules are strong | adapt |
| feedback | lint/verifier/GROW can be feedback/review-pressure inputs | adapt |
| retrieval / cache | BM25/contextual/rerank plus egress gate is useful | adapt with authority buckets |
| API / MCP / agent access | transport detection and CLI/MCP/filesystem fallbacks are useful | adapt cautiously |
| viewer / workbench | Obsidian Bases dashboard and Canvas layer are useful | watch/adapt |
| publishing | Not central here except save/canvas/session filing | watch |
| risk / anti-pattern | auto-research, broad writes, auto-commit, generated-wiki-as-truth | capture as risk |

## 值得提炼的模式

### 1. Skill catalog as action surface

Use a readable skill registry and trigger map as the agent action surface.

VAKS adaptation:

```text
skill trigger
-> explicit user intent check
-> local manuals
-> scoped helper
-> candidate/raw artifact
-> sync/hash
```

### 2. Hot/index/log recovery spine

Use a tiny set of files to restore recent context and navigate without crawling everything.

VAKS adaptation:

```text
hot = activation
index = navigation
log = operation trace
handoff = recovery source
reviewed/action basis remains separate
```

### 3. Per-file locking for AI writes

Before multi-agent write workflows, add:

```text
path validation
per-file lock
stale lock cleanup
hook deferral
hash/sync verification
git status guard
```

### 4. Retrieval cache with egress gate

Borrow local-first retrieval and explicit network consent.

VAKS adaptation:

```text
retrieval finds candidates
authority bucket filters first
scores never become support
egress off by default
```

### 5. Filing policy router

PARA, LYT, Zettelkasten, and generic should be routing policies, not core ontology.

## 标签与量化

- domain: AI Obsidian wiki / Claude Code skills
- problem: file-first AI knowledge workbench and agent-maintained wiki
- pattern: skill-routed wiki operations with recovery/cache/safety helpers
- maturity: emerging
- complexity: high
- problem_fit: 5
- reuse_value: 5
- implementation_cost: 4
- integration_fit: 4
- evidence_strength: 4
- reversibility: 4

## 交叉验证

- 相似设计来源：
  - Karpathy LLM Wiki pattern.
  - Kepano Obsidian / obsidian-skills substrate.
  - CyrilXBT Claude + Obsidian 90-day workflow retrospective.
  - langchain-miniopenclaw local agent workbench.
- 用户历史项目里的相似问题/影子：
  - VAKS explicit distillation trigger.
  - Obsidian sync/hash helper.
  - Source Intake candidate/review/action-basis split.
  - Project Overlay as borrowing sidecar.
- 支持证据：
  - Snapshot captured at commit `cb93ff6d82f9c35a08bf6010e7fac36dfddc827b`.
  - Skills/scripts/hooks/tests inspected by file anchors.
- 反例或失败边界：
  - Auto-research and auto-commit conflict with VAKS ordinary-capture boundaries.
  - Generated wiki pages are too authority-blurry for reviewed knowledge.
- 最小验证方式：
  - Do not install now.
  - If needed later, run lock/retrieval/mode tests in isolated scratch.
  - Implement only one VAKS helper pattern at a time.

## Knowledge Calibration / Point Collision

| Candidate Point | Local Reviewed / Active Project Knowledge | Calibration Output | Review Question |
|---|---|---|---|
| hot/index/log can restore context cheaply | MEMORY_TIER / DEV_CONTEXT treat activation as not truth | candidate_relation | Should VAKS define a formal hot-cache helper or rely on handoff/index files? |
| skills can be action surfaces | Global VAKS skill already uses trigger words | candidate_relation | What metadata fields must a VAKS skill expose for safety and audit? |
| generated wiki pages can accumulate knowledge | SOURCE_INTAKE requires raw/candidate/reviewed/action-basis split | scope_mismatch | How to keep generated notes from being quoted as reviewed knowledge? |
| locks/hooks reduce AI write corruption | VAKS currently uses sync/hash/git discipline, not locks | missing_evidence | Are locks necessary before multi-agent write workflows? |
| retrieval cache improves query depth | SOURCE_INTAKE retrieval bucket policy forbids authority mixing | candidate_relation | How to add retrieval without crossing authority buckets? |
| auto-research files output directly | VAKS forbids automatic truth mutation | risk_of | Should autoresearch be parked until candidate-only pipeline is stronger? |

Boundary:

- Similar is not support.
- Repeated source pattern is not reviewed relation.
- This review is candidate architecture extraction, not promotion.

## Support / Challenge Review

What supports it:

- The repo contains concrete files for skills, hooks, scripts, tests, templates, and docs.
- The implementation addresses known operational risks: concurrency, duplicate ingest, egress, stale caches, mode routing.
- It aligns with already-discussed VAKS directions: file-first, activation cache, project-local manuals, skill helpers, Obsidian workbench.

What challenges it:

- It collapses generated wiki into the product, while VAKS needs candidate/reviewed/action-basis separation.
- Auto-commit and auto-research are powerful but risky defaults.
- Egress gates exist, but production use would require separate verification.
- The repo was inspected, not executed.

Challenge severity:

```text
major for direct adoption
minor for design-only borrowing
```

Scope limits:

```text
Use for tool/workbench/runtime design.
Do not use for truth schema, reviewed relation, or action-basis policy.
```

Known risks:

- source hygiene drift if repo changes after snapshot;
- over-borrowing plugin/runtime complexity;
- confusing hot cache with memory truth;
- letting research/lint/verifier outputs mutate knowledge.

Review again when:

- VAKS designs a multi-agent write pipeline;
- VAKS adds retrieval/cache implementation;
- VAKS builds an Obsidian/Codex workbench;
- someone proposes auto-research or auto-commit.

Action readiness:

```text
not_ready
```

## 关系边 / 关联强度

```yaml
relations:
  - target: "SOURCE_INTAKE.md"
    type: refines
    relation_state: candidate
    strength: 3
    confidence: medium
    evidence:
      - "raw/repos/2026-06-07-agricidaniel-claude-obsidian-source.md"
    rationale: "It provides concrete source ingest mechanics, but VAKS must preserve candidate/review/action-basis boundaries."
    created: 2026-06-07
    last_verified: 2026-06-07
  - target: "DEV_CONTEXT.md"
    type: refines
    relation_state: candidate
    strength: 4
    confidence: medium
    evidence:
      - "raw/repos/2026-06-07-agricidaniel-claude-obsidian-source.md"
    rationale: "hot/index/log and skill router can improve recovery and activation."
    created: 2026-06-07
    last_verified: 2026-06-07
  - target: "generated-wiki-as-truth"
    type: risk_of
    relation_state: candidate
    strength: 4
    confidence: medium
    evidence:
      - "raw/repos/2026-06-07-agricidaniel-claude-obsidian-source.md"
    rationale: "Agent-generated wiki content can be overread as reviewed knowledge if VAKS gates are not preserved."
    created: 2026-06-07
    last_verified: 2026-06-07
```

## 对当前项目的适配点

Use now as:

```text
support reference
risk reference
candidate implementation pattern source
```

Do not use now as:

```text
mainline architecture merge
schema change
reviewed pattern
decision
runtime install
plugin adoption
```

## 可拓展性

- 是否适合作为插件/适配层：yes, design-only; code reuse requires a separate license/security/runtime review.
- 是否会绑定核心结构：yes if copied whole; avoid by borrowing individual primitives.
- 未来替换成本：medium; skill/helper patterns are replaceable if kept behind VAKS contracts.
- 可迁移路径：
  - Start with documentation patterns.
  - Then helper-level lock/sync patterns.
  - Then retrieval/cache experiments.
  - Keep all outputs candidate until review.

## 复杂度和风险

Main risks:

- It is a full plugin/workflow ecosystem, not a small library.
- VAKS could overbuild by copying too much.
- Auto hooks are attractive but can silently mutate repo state.
- Auto-research can become a content flood.
- Retrieval can look scientific while still being only activation.

## 不可行点 / 避坑

- Do not directly install this into the VAKS vault.
- Do not copy its generated `wiki/` authority model.
- Do not turn `/autoresearch` into a default source-intake lane.
- Do not enable `--allow-egress` by default.
- Do not auto-commit VAKS repo changes from hooks.
- Do not treat LYT/PARA/Zettelkasten as VAKS ontology.
- Do not trust lint/verifier as promotion review.

## 融合判断

- 结论：adapt
- 理由：
  - Strong implementation reference for VAKS tool/runtime/workbench layer.
  - Too authority-blurry for VAKS truth/review layer.
  - Best absorption is narrow and reversible.
- 验证方式：
  - If used later, create a sandbox helper prototype and test with temp vault files.
  - No mainline merge without v0.2.13 if it affects action basis or promotion.

## 直接判断

- Direct use: no
- Fork: no
- Design-only: yes
- Reject: no
- Current branch value: strong for skill routing, source intake helper, and Obsidian write safety
- Whole architecture value: strong for activation/workbench/retrieval/tooling, weak for reviewed truth
- Risk: high if copied wholesale; manageable if borrowed as candidate primitives
- Next action: keep as candidate-only and use the VAKS overlay when relevant

## 后续行动

```text
No immediate mainline merge.
No plugin install.
No runtime execution.
No truth-layer mutation.
```

Recommended future reopen:

```text
1. VAKS skill runtime design.
2. Multi-agent or high-rate Obsidian writes.
3. Retrieval/cache implementation.
4. Workbench/dashboard/canvas design.
5. Maintenance lint / verifier workflow.
```
