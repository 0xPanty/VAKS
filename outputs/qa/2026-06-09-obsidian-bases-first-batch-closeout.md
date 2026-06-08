---
type: qa
status: closed
topic: obsidian_bases_first_batch_closeout
created: 2026-06-09
repo_head: 335793a
formal_vault: H:\Obsidian\资料库
confidence: high
---

# Obsidian Bases First Batch Closeout

## Scope

This closeout records the first repo-versioned Obsidian Bases batch and the
formal vault sync state after the C1-C4 metadata/Base work.

The Base files are view/workbench surfaces only. They do not define schema,
truth confidence, reviewed relations, review decisions, or promotion status.

## Repo State

Latest relevant commits:

```text
335793a feat(bases): add claims and patterns Obsidian Bases views
297963b docs(patterns): normalize adoption status values
a3496de docs(metadata): normalize confidence values
39e422a docs(patterns): normalize pattern candidate status
248a0cb fix(bases): align decisions Base serialization
e760fd6 fix(bases): align sources Base serialization
a12907b feat(bases): add sources and decisions Obsidian Bases views
```

Repo Base files now present:

```text
wiki/bases/sources.base
wiki/bases/decisions.base
wiki/bases/claims.base
wiki/bases/patterns.base
```

Tracked content surfaces currently used by the first batch:

```text
wiki/decisions/*.md = 10
wiki/claims/*.md    = 9
wiki/patterns/*.md  = 74
```

## Formal Vault State

Formal vault:

```text
H:\Obsidian\资料库
```

Synchronized files present in the formal vault:

```text
wiki/bases/*.base      = 4
wiki/decisions/*.md    = 10
wiki/claims/*.md       = 9
wiki/patterns/*.md     = 74
```

Base SHA256 alignment, repo vs formal vault:

```text
wiki/bases/sources.base   match=True  8DC0D15E39E8CA7E89946F0B66382A1001B973E1950AF1E10471352DE4E85BCC
wiki/bases/decisions.base match=True  4785B888A80026920D8C44C3780EFF9C2B6A2833199745B4B495E3C5F2C0797D
wiki/bases/claims.base    match=True  6966B9E41EA021333509359D516441CE40DA04C47CF0C83686D1CA353DDE0BF8
wiki/bases/patterns.base  match=True  1C726931A20868C68868E93DE8AA1EA593807F4E06E684D2FBD1645F3A9398DC
```

After the claims/patterns render check, the synced C4 target set still matched:

```text
post_render_missing_count=0
post_render_mismatch_count=0
```

No authorized-content mismatch was observed.

## Render Verification

Obsidian version observed during render smoke test:

```text
Obsidian 1.12.7
```

Formal vault visual smoke checks completed:

```text
claims.base   All claims   rendered 9 results
patterns.base All patterns rendered 74 results
```

Static filter-count checks completed in repo for the new C4 Bases:

```text
claims_all=9
claims_review_due=0
claims_secondary_evidence=5
patterns_all=74
patterns_adoption_focus=29
patterns_candidate_and_draft=56
patterns_review_due=24
```

Earlier source/decision Base work had already established the rendering pattern
for `sources.base` and `decisions.base`; this C5 closeout did not re-run their
visual checks.

## Known Side Effects

Opening Obsidian for visual confirmation wrote normal app state under
`.obsidian`:

```text
.obsidian/app.json
.obsidian/appearance.json
.obsidian/core-plugins.json
.obsidian/workspace.json
```

No recent non-`.obsidian` formal-vault writes outside the authorized Base,
decision, claim, and pattern targets were observed during the C4 sync check.

Temporary screenshots created for visual inspection were deleted.

## Current Dirty Worktree Note

The repo still has unrelated pre-existing dirty/untracked items, including:

```text
M  outputs/review/project_lens_overlays/VAKS.md
?? 00_handoff/2026-06-08-answer-boundary-and-three-window-execution-handoff.md
?? outputs/qa/2026-06-08-obsidian-bases-design-research.md
?? raw/articles|raw/repos|raw/videos and outputs/review intake/sandbox artifacts
```

These were intentionally not staged, committed, deleted, or normalized as part
of the Bases closeout.

## Remaining Gates

Possible next steps, each requiring a separate user decision:

```text
1. Push the completed Base/metadata commits, if a remote is configured later.
2. Add review-candidate / review-queue Base views after review metadata is scoped.
3. Continue light metadata cleanup only if it supports a concrete Base view.
4. Decide whether sources/raw content should be synced more broadly into the formal vault.
```

Do not treat Bases as a truth layer or promotion mechanism. Markdown/YAML source
records and reviewed wiki records remain the durable source of truth.
