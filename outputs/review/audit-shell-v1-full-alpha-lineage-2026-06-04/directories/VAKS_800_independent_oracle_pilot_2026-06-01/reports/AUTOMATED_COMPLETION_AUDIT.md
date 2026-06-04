# Automated Completion Audit

Status: patched automated portion complete; human timing and dual-review remain intentionally blank.

## Requirement Audit

| requirement | evidence | status |
| --- | --- | --- |
| new 800-case sandbox | `candidate_cases.json` has 800 cases | complete |
| data fetch | `data/dataset_fetch_log.json` shows 220 rows each for SciFact, AVeriTeC, AmbiFC, FEVER | complete |
| case builder | `build_candidate_cases_800.py`; `data/case_build_manifest.json` | complete |
| frozen gold flow | `gold_oracle_frozen.json`; `gold_oracle_frozen.sha256`; `gold_freeze_manifest.json` | complete, machine-frozen not human-adjudicated |
| four-arm harness | baseline_full, shell_core, shell_core_plus_recurrence, leaky_or_unversioned_control artifacts/checks | complete |
| anchor selector/pointer checks | `checker_800.py` validates source hash, offset, quote, record pointer, evidence pointer | complete |
| real snapshot preflight | `data/clickback_snapshot_manifest.json`; `real_source_snapshots/` | repaired transport: 24 live/immutable representative snapshots, 0 fallback wrappers after retry |
| semantic click-back landing | `data/clickback_semantic_landing_eval.json`; `reports/CLICKBACK_SEMANTIC_LANDING_EVAL.md` | automated proxy repaired: 24/24 semantic selector success, 0 body_window / boilerplate landings |
| front density metrics | `pilot_800_results.json` includes front chars p95 and max line chars p95 | complete |
| resolved view metric | `resolved_default_queue_visible=0`, `resolved_front_line_violations=0` for candidate arms | complete |
| grouping metric repair | `shell_core_plus_recurrence` recalls 8/8 multi-member groups and counts 48 grouped members | complete |
| negative control | `leaky_or_unversioned_control` fails with false-lite, authority leakage, over-grouping, serious folded | complete |
| authority fuzz | `authority_fuzz_results.json` hit_rate 1.0 on canned samples | complete, lint only |
| stratified human packet | `review_packet/packet_summary.json` covers Pro-requested risk faces | complete, not adjudicated |
| human timing packet | timing and dual-review sheets are blank | complete, not fabricated |

## Key Results

`shell_core` passes automated safety gates:

- serious false-lite: 0
- serious full-audit recall: 100%
- serious folded count: 0
- source anchor failures: 0
- record pointer failures: 0
- evidence pointer failures: 0
- authority leakage: 0 on canned/lint checks
- severe over-grouping: 0

`shell_core` performance gates:

- ordinary rendered line reduction: 56.2%
- ordinary rendered char reduction: 63.4%
- ordinary front chars p95: 302
- serious front chars p95: 358
- max front line chars p95: 127
- resolved default queue visible: 0
- resolved front line violations: 0
- threshold audit: pass

`shell_core_plus_recurrence` passes automated safety gates but remains a conditional arm:

- grouping recall: 8/8 multi-member groups
- predicted grouped members: 48
- grouped reduction: 83.3%
- recurrence rendered line reduction: 49.1%
- recurrence rendered char reduction: 53.4%
- severe over-grouping: 0
- serious folded count: 0
- threshold audit: fails/cautions on recurrence line-reduction gate

Negative control fails as required:

- serious false-lite: 376
- state mismatch: 376
- severe over-grouping: 12
- serious folded: 12
- authority leakage: 48

## Human Packet Coverage

Main core packet:

- 120 unique cases, 240 randomized assignments
- resolved cases: 14
- recurrence-capable cases: 22
- non-valid anchor cases: 22
- authority-family cases: 10
- anchor-jumpback-failure layer: 8
- over-grouping-near-miss layer: 10
- serious-folded-violation layer: 8

Side recurrence packet:

- 60 unique recurrence-heavy cases, 120 randomized assignments
- resolved cases: 14
- recurrence-capable cases: 34
- non-valid anchor cases: 6
- over-grouping-near-miss layer: 14
- serious-folded-violation layer: 8

## Non-Completion Boundaries

This does not complete human validation:

- no human timing values were generated
- no dual-review adjudication was fabricated
- frozen gold is machine-derived from explicit overlays
- authority fuzz is canned lint, not semantic firewall proof
- valid anchor checks are package integrity checks, not final UI click-back proof
- latest click-back snapshot preflight has 24 live/immutable representative snapshots and 0 fallback wrappers; automated semantic selector success is 24/24, but final UI/human click-back adjudication remains open

## Next Required Human Step

Use `review_packet/` for at least two reviewers. Fill timing, triage, full-audit
open, anchor click success, state/review_due choice, subjective burden, grouping
helped/hurt, missed serious, and adjudication fields.
