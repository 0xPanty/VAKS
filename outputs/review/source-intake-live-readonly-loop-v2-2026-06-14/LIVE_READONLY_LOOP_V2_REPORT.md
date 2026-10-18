# VAKS Source Intake Live Read-Only Loop v2 Report

## Verdict

This is a no-fallback, adversarial-support-mislabel, canonical-overlay-check, minimal-frozen-replay sandbox package.

It improves on the previous live package by removing silent `force_anchor_hit()` from the mixed-pack case and by adding packaged live-hit misuse cases where candidate, legacy overlay, canonical overlay, and rank-only diagnostic items are intentionally mislabeled as support and then blocked by the support gate.

It still does **not** prove Source Intake P0 passed, live LLM/tool runtime validation, live embedding/vector/graph validation, external blind relevance, or runtime adoption readiness.

## Results

- Live cases: 7
- Expected decisions passed: 7 / 7
- Decisions: {'blocked_or_downgraded': 5, 'allowed_readonly': 2}
- Frozen replay: fail (minimal top-k membership, not exact ranking order)
- Fallback regression scan: pass

## Case Results

- `V2-01-candidate-safe-downgrade`: blocked_or_downgraded / top=`outputs/review/2026-06-11-AxDSan-mnemosyne-candidate-distillation.md` / support_count=0
- `V2-02-real-raw-anchor-natural-allow`: allowed_readonly / top=`raw/articles/2026-06-13-flexnote-docs-source/inspected-pages.md` / support_count=1
- `V2-03-mixed-pack-no-fallback-allow`: allowed_readonly / top=`outputs/review/2026-06-13-flexnote-docs-candidate-distillation.md` / support_count=1
- `V2-04-adversarial-candidate-mislabeled-support`: blocked_or_downgraded / top=`outputs/review/2026-06-11-AxDSan-mnemosyne-candidate-distillation.md` / support_count=0
- `V2-05-adversarial-overlay-mislabeled-support`: blocked_or_downgraded / top=`outputs/review/project_lens_overlays/2026-06-13-flexnote-vaks-visual-knowledge-workbench-overlay.md` / support_count=0
- `V2-06-adversarial-rank-diagnostic-mislabeled-support`: blocked_or_downgraded / top=`outputs/review/2026-06-13-flexnote-docs-candidate-distillation.md` / support_count=0
- `V2-07-adversarial-canonical-overlay-mislabeled-support`: blocked_or_downgraded / top=`outputs/review/project_overlays/_runtime_test_fixtures/2026-06-14-flexnote-canonical-overlay-runtime-fixture.md` / support_count=0

## Boundary

The live retrieval remains local lexical Markdown retrieval. Pack assembly is still scripted, but v2 includes packaged adversarial scripted mislabel cases to test whether the support gate blocks unsafe pack roles. The raw/stable anchor allow cases are structurally resolved, not externally judged for semantic sufficiency. The frozen replay is a minimal top-k membership replay, not exact ranking order and not a full-workspace rerun.
