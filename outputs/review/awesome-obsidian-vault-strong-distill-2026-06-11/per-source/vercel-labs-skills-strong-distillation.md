---
record_kind: strong_candidate_distillation
status: candidate
provisional: true
knowledge_status: candidate
processing_tier: heavy
lifecycle_state: candidate_provisional
source_family: awesome-obsidian-vault
source_url: "https://github.com/vercel-labs/skills"
repo_key: "vercel-labs/skills"
checked_commit: "be0dd25b4a8665894a56f45ef582cc02ca802c39"
checked_at: 2026-06-11
supersedes_shallow_candidate:
  - outputs/review/awesome-obsidian-vault-full-distill-2026-06-11/per-source/vercel-labs-skills-candidate-distillation.md
derived_from:
  - raw/repos/2026-06-11-awesome-obsidian-vault/vercel-labs-skills-source.md
  - outputs/review/awesome-obsidian-vault-strong-distill-2026-06-11/source-anchor-manifests/vercel-labs-skills-anchor-manifest.json
retrieval_policy:
  policy_kind: orientation_only
  pack_allowed: activation_only
  action_basis_allowed: false
  warning_code: candidate_not_action_basis
promotion_gate: evidence_aware_review_required
action_basis_allowed: false
truth_mutation_allowed: false
borrow_value: strong
borrow_order: P1
routing_hint:
  - agent_skill_runtime_boundary
  - source_parser_safety
fit_layer:
  - agent-boundary
  - skill-registry
  - source-ingest
  - tool-safety
  - source-hygiene
  - risk
not_fit_layer:
  - reviewed-knowledge
  - action-basis
  - automatic-runtime
avoid:
  - "Do not allow a skill runtime, install flow, or prompt output to mutate reviewed knowledge."
  - "Do not execute third-party skills during source review."
  - "Do not copy destructive install/update behavior into the VAKS core path."
dev_context_hint:
  default_layer: support_with_required_risk
  core_only_when: "When designing future VAKS agent-skill intake, parser safety, source locking, or external tool quarantine."
  support_when: "When comparing source parser, lockfile, provider abstraction, or terminal/path sanitization patterns."
  risk_when: "When install/update convenience could blur candidate records, agent runtime state, and reviewed knowledge."
  cold_references:
    - raw/repos/2026-06-11-awesome-obsidian-vault/vercel-labs-skills-source.md
    - outputs/review/awesome-obsidian-vault-strong-distill-2026-06-11/source-anchor-manifests/vercel-labs-skills-anchor-manifest.json
tags:
  - candidate-only
  - strong-distillation
  - awesome-obsidian-vault
  - agent-skills
  - source-safety
---

# Strong Candidate Distillation: vercel-labs / skills

## Boundary

This is a strong candidate distillation. It extracts design mechanisms from a
CLI/runtime for agent skills. It is not reviewed VAKS architecture and cannot be
used as action basis.

## What This Source Actually Is

This repo is a TypeScript CLI for discovering, installing, listing, using,
updating, and removing agent skills across many agent environments. Unlike a
link registry, it contains executable mechanics: source parsing, provider
lookup, install modes, lockfiles, metadata parsing, and safety tests.

For VAKS, the important lesson is not "install skills". The important lesson is
how an external capability runtime keeps source identity, local installation
state, parser safety, and update tracking separate.

## Source / Code Anchors

| Anchor | What exists | Design extraction | Boundary |
|---|---|---|---|
| `README.md` | CLI commands for `add`, `use`, `list`, `find`, `remove`, `update`, plus source formats. | Clear command taxonomy separates discovery, temporary use, installation, and update. | VAKS should not add runtime commands without separate approval gates. |
| `package.json` | Node package with CLI entrypoint, build/test/typecheck scripts, and broad agent keywords. | Shows runtime surface and test discipline around a small CLI. | Package maturity is not VAKS fit proof. |
| `src/source-parser.ts` | Parses local paths, GitHub/GitLab URLs, SSH, shorthand, refs, fragments, and subpaths. | Strong model for normalizing source identity before intake. | Parser output is provenance, not support. |
| `src/source-parser.ts:sanitizeSubpath` | Rejects `..` traversal segments and normalizes slashes. | Borrow directly as a VAKS source-subpath guard concept. | Needs local implementation review before reuse. |
| `src/frontmatter.ts` | Minimal YAML frontmatter parser, explicitly avoiding JS frontmatter execution. | Excellent fit for VAKS source-card parsing: read metadata, do not execute metadata. | YAML parse success is not content review. |
| `src/installer.ts` | Canonical skill dir, agent-specific dirs, symlink/copy modes, path safety, parent symlink resolution. | Strong separation of canonical source and adapter-specific projection. | Install mechanics belong outside reviewed knowledge path. |
| `src/skill-lock.ts` | Lock entries store source, source type, original URL, ref, skillPath, folder hash, timestamps. | Directly relevant to VAKS source integrity and candidate intake traceability. | Lock hash is process evidence, not truth confidence. |
| `tests/subpath-traversal.test.ts` | Tests URL and shorthand traversal rejection. | Good shape for future source-intake fixtures. | Tests diagnose parser safety only. |
| `tests/sanitize-terminal.test.ts` | Strips terminal escape/control sequences from untrusted metadata. | Strong source-hygiene point for displaying external titles/descriptions. | Sanitization does not make content safe to trust. |

## Strong Borrow Points

1. **Source parsing should be an explicit adapter layer.**  
   VAKS should normalize source identity before any candidate record is written:
   host, owner/repo, ref, subpath, original URL, and local path should be
   structured fields. This reduces later ambiguity in provenance and duplicate
   checks.

2. **Subpath safety is a first-class gate.**  
   The traversal tests are directly relevant. VAKS should reject source
   subpaths that can escape a repository/root before snapshotting, converting,
   or syncing retained artifacts.

3. **Frontmatter must be data-only.**  
   The YAML-only parser is a clean pattern for VAKS: metadata is parsed as data,
   never evaluated as code. This fits the current candidate/review boundary and
   prevents note metadata from becoming an execution surface.

4. **Lockfiles should track external-source state, not truth.**  
   `source`, `sourceType`, `sourceUrl`, `ref`, `skillPath`, folder hash, and
   timestamps are valuable for VAKS intake ledgers. The VAKS adaptation should
   call this process integrity, not evidence support.

5. **Canonical copy plus adapter projection is a useful boundary.**  
   The installer separates a canonical skill directory from agent-specific
   paths. VAKS can borrow the same idea for future exports: Markdown source of
   truth remains canonical; Obsidian views, context packs, or agent adapters are
   projections.

6. **Terminal/control-character sanitization belongs in source display.**  
   External repository names, descriptions, README titles, and generated labels
   should be sanitized before being printed into logs, terminals, dashboards, or
   generated Markdown.

## VAKS Layer Mapping

| VAKS layer | Candidate value | Adopt shape |
|---|---|---|
| Capture / Source Ingest | Source parser, subpath guard, source URI normalization. | Strong candidate for future intake helper. |
| Candidate Comprehension | Frontmatter parsing as data-only extraction. | Borrow as metadata hygiene. |
| Review Queue | Lockfile can expose stale refs or changed source hashes. | Review pressure only. |
| Association / Activation | Provider/source type can improve routing. | Candidate routing only. |
| Context Pack | Canonical-source plus projection concept. | Use for context-pack export boundaries. |
| Agent Gateway | Installation/use/update separation and terminal sanitization. | Strong guardrail reference. |
| Action / Use Ledger | No direct action readiness. | Requires separate execution sandbox. |

## Local De-Dup / Collision

The earlier shallow file correctly identified `agent_skill_runtime_boundary`, but
it did not extract the concrete mechanisms. This strong file adds:

- parser safety;
- YAML-only metadata parsing;
- source lock/integrity fields;
- terminal sanitization;
- canonical-vs-agent projection boundary.

These refine existing VAKS ideas: raw provenance, candidate-only external
adapters, and future agent memory quarantine.

## Anti-Borrow

- Do not copy `skills add/use/update` as a VAKS user-facing command without
  separate permission, sandboxing, and audit logs.
- Do not allow skill prompt output into reviewed notes.
- Do not let source hashes become truth confidence.
- Do not treat broad agent compatibility as architecture fit.

## Candidate Tags

```yaml
domain: agent-skill-cli-runtime
problem: safe_external_capability_intake_and_projection
pattern:
  - source-parser-adapter
  - yaml-only-frontmatter
  - source-lockfile
  - canonical-copy-plus-agent-projection
  - terminal-metadata-sanitization
maturity: emerging
problem_fit: 5
reuse_value: 5
implementation_cost: 3
integration_fit: 5
evidence_strength: 4
reversibility: 4
```

## Fusion Judgment

Adapt as a P1 engineering reference for future VAKS agent/source-intake safety.
The strongest near-term borrow is not the CLI; it is the separation of source
normalization, lock integrity, metadata parsing, display sanitization, and
adapter projection.
