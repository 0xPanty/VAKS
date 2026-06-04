# 800-Case Automated Patch Report

Status: sandbox patch complete. No main-vault writeback, no schema change, no human timing fabricated.

## Why This Patch Exists

Pro's review of the first 800-case package found that the automated scaffold was
mostly complete, but several pre-human-stage gaps remained:

- human review packet missed the actual risk faces that humans need to inspect.
- grouping metrics failed to count folded recurrence members.
- resolved folding was measured with the wrong target.
- click-back checks were still too close to local wrapper integrity.
- authority fuzz needed to stay labeled as lint only.

## Changes Made

1. Human packet was rebuilt as two stratified packets.
   - `main_core_*`: baseline_full vs shell_core, 120 cases.
   - `side_recurrence_*`: shell_core vs shell_core_plus_recurrence, 60 cases.
   - Timing and adjudication fields are blank.

2. Grouping metric was repaired.
   - Folded recurrence members now carry a parseable `group_id`.
   - `shell_core_plus_recurrence` now reports 8/8 multi-member group recall,
     48 predicted grouped members, and 83.3% grouped reduction.

3. Resolved folding metric was retargeted.
   - Old target: opened resolved record must show 95% line reduction.
   - New target: resolved records must be absent from default unresolved-first
     queue surface and must not violate front discipline when opened.
   - Candidate arms report `resolved_default_queue_visible=0`.

4. Click-back snapshot preflight was added and later repaired.
   - 24 representative full-anchor cases were materialized to
     `real_source_snapshots/`.
   - Initial patched run: 4 live fetched real snapshots, 20 fallback
     source-wrapper snapshots.
   - Latest retry run: 24 live/immutable representative snapshots, 0 fallback
     wrappers, using urllib retry plus PowerShell fallback retry.
   - This repairs the wrapper-heavy subset, but still does not claim final
     UI/human product click-back adjudication.

5. Click-back semantic landing was split from transport success.
   - `data/clickback_snapshot_manifest.json` reports transport fetch status.
   - `data/clickback_semantic_landing_eval.json` reports claim-relevant
     selector landing.
   - Initial semantic selector success was 7/24.
   - A conservative claim-keyword window fallback was added after exact
     evidence / exact claim matching.
   - Current semantic selector success is 24/24.
   - `body_window` and Wayback / Archive boilerplate landing are 0/24.
   - Landing class is now explicit: evidence landing, claim landing, or weaker
     claim-relevant context landing.

6. Authority fuzz language remains downgraded.
   - 16/16 canned samples are caught.
   - This remains lint coverage, not semantic authority safety proof.

## Current Design Readout

`shell_core` remains the only default-core candidate:

- available automated proxy gates largely pass, while source-anchor exactness
  and human/product gates must still be read separately
- ordinary line reduction: 56.2%
- ordinary char reduction: 63.4%
- resolved default queue visible: 0
- negative control fails when core protections are removed

`shell_core_plus_recurrence` remains conditional:

- safety gates pass
- grouping recall is repaired
- recurrence line reduction is 49.1%, below the >=50% continuation gate
- it should be tested only in recurrence-heavy human timing/review slices

## What Still Cannot Be Claimed

- This is not an independent human oracle.
- This is not product-grade click-back validation.
- Authority lint is not a semantic firewall.
- Recurrence grouping is not truth/support strength.
- Frozen gold is not human adjudication.

## Recommended Next Step

Do not proceed directly to the 120-case main packet yet. Claim-relevant selector
landing now passes the automated semantic proxy, but the right next step is to
rerun the narrow operator adjudication and keep recurrence closed until
human/product click-back is checked.
