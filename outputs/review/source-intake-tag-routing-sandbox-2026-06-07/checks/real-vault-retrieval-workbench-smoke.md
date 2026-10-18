---
type: sandbox_check
status: pass
created_at: 2026-06-07
scope: real-vault retrieval workbench smoke test for source-intake-routing
truth_boundary: sandbox evidence only; not reviewed knowledge; not action basis
---

# Real-Vault Retrieval Workbench Smoke

## Question

Can the source-intake-routing workbench turn a noisy real-vault query into a
clean lane-separated context pack?

## Patch Under Test

```text
16_SOURCE_CARD_VS_CANDIDATE_METADATA_SPLIT.md
17_TOPIC_RETRIEVAL_PACK_MVP.md
tools/vaks-retrieval-mvp.ps1
tools/vaks-context-pack-builder-v0.ps1
tools/vaks-context-pack-lint.ps1
checks/topic-retrieval-pack-source-intake-generated.md
checks/topic-retrieval-pack-source-intake-formal-vault-generated.md
```

## Local Project Repo Run

Command:

```powershell
powershell -ExecutionPolicy Bypass -File .\outputs\review\source-intake-tag-routing-sandbox-2026-06-07\tools\vaks-context-pack-builder-v0.ps1 `
  -Root . `
  -Pattern 'source intake|metadata-routing|context pack|registry-before-recompute|query-run receipt|retrieval_policy' `
  -Mode research `
  -TopicId source-intake-routing `
  -Limit 240 `
  -OutFile .\outputs\review\source-intake-tag-routing-sandbox-2026-06-07\checks\topic-retrieval-pack-source-intake-generated.md `
  -Json
```

Result:

```text
selected_count=32
excluded_count=24
mainline_current total=20 included=0 selected=8
candidate_orientation total=28 included=28 selected=8
active_project_overlay total=18 included=18 selected=8
support_review_output total=100 included=100 selected=8
audit_evidence total=73 included=0 selected=0
feedback_diagnostics total=1 included=0 selected=0
```

Interpretation:

```text
The local repo is dominated by recent outputs/review sandbox and package
material. The pack builder still separates start-here, candidate orientation,
active project overlay, support review output, and audit evidence instead of
letting old sandbox/package matches become default support.
```

## Formal Obsidian Vault Run

Formal vault was used as a read-only retrieval root:

```text
H:\Obsidian\资料库
```

Command:

```powershell
powershell -ExecutionPolicy Bypass -File .\outputs\review\source-intake-tag-routing-sandbox-2026-06-07\tools\vaks-context-pack-builder-v0.ps1 `
  -Root H:\Obsidian\资料库 `
  -Pattern 'source intake|metadata-routing|context pack|registry-before-recompute|query-run receipt|retrieval_policy' `
  -Mode research `
  -TopicId source-intake-routing-formal-vault `
  -Limit 240 `
  -OutFile .\outputs\review\source-intake-tag-routing-sandbox-2026-06-07\checks\topic-retrieval-pack-source-intake-formal-vault-generated.md `
  -Json
```

Result:

```text
selected_count=40
excluded_count=24
mainline_current total=12 included=0 selected=8
raw_drilldown total=51 included=51 selected=8
candidate_orientation total=29 included=29 selected=8
active_project_overlay total=19 included=19 selected=8
support_review_output total=32 included=32 selected=8
audit_evidence total=96 included=0 selected=0
feedback_diagnostics total=1 included=0 selected=0
```

Interpretation:

```text
The formal vault is noisier in exactly the expected way: many audit/sandbox
artifacts match the query. The pack builder keeps those out of the default
research pack and gives the user a lane-labeled working set instead.
```

## Pack Lint

Command:

```powershell
powershell -ExecutionPolicy Bypass -File .\outputs\review\source-intake-tag-routing-sandbox-2026-06-07\tools\vaks-context-pack-lint.ps1 `
  -Root .\outputs\review\source-intake-tag-routing-sandbox-2026-06-07 `
  -Json
```

Result:

```text
files_checked=4
pass=3
fail=1
expected_fail=fixtures/usage-layer-bad-authority-leak.md
```

Interpretation:

```text
Both generated topic packs pass. The intentionally bad fixture still fails
because it lets candidate material look action-ready and omits warnings.
```

## Verdict

```text
status=pass
```

The sandbox now has a minimal "search -> lane separation -> topic/context pack"
workflow. It is still a workbench prototype, not an answer generator and not a
mainline schema change.
