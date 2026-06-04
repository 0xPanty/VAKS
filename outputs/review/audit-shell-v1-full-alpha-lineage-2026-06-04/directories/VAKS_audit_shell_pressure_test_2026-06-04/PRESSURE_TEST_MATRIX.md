# Pressure Matrix

| Dimension | Expected shell behavior | Result |
|---|---|---|
| Ordinary source/template/concept | Stay light unless action basis appears | Pass |
| Missing source URL or weak source identity | `for_review` or `blocking` | Pass |
| Flat video transcript | `blocking` before evidence/action use | Pass |
| Timestamped ASR segments | `for_review`; key-entity check before promotion | Pass |
| ASR/acquisition metadata JSON | Stay ordinary diagnostic metadata | Pass |
| Repo/package ZIP snapshot | Block as evidence until code/source anchor is exposed | Pass |
| Feedback records/patterns | Activation or review pressure only, not truth change | Pass |
| Dashboard/test/lint/benchmark/count | Diagnostic only, never authority | Pass |
| Source count / lineage / repeated mention | Not support strength | Pass |
| Draft/candidate pattern | `for_review` before use as rule | Pass |
| Old handoff | `resolved_folded`, route to latest | Pass |
| Stale package manifest | `regressed`, verify latest package/handoff | Pass |
| Completed review output | Folded by default, reopen only for current action use | Pass |
| Derived QA/summary | Review source anchors before action or promotion | Pass |
| Template | Template only, not record facts | Pass |
| Over-heavy risk | Ordinary records should not become paperwork | Pass, 0 over-heavy |
| False-lite risk | Serious risk should not stay light | Pass, 0 false-lite |

## Design Signal

The pressure test supports keeping the full operator shell behavior. It does not support weakening the design into a tiny safe checklist before the operator experience is designed.

