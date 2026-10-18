---
type: sandbox_protocol
status: test_candidate
created_at: 2026-06-06
truth_boundary: sandbox protocol only; not schema; not reviewed knowledge; not action basis
---

# Project Overlay One-Page Protocol

## Plain Rule

```text
Project Overlay = 当前项目的借鉴清单。
```

It tells Codex what a project may borrow from reusable knowledge points. It does
not change those knowledge points.

## Ten Rules

1. Project Overlay is a current-project navigation note. It is not truth, not
   ADR, and not action basis.
2. Each live entry must have four fields: `kp_ref`, `stance`, `borrow_scope`,
   and `updated_at`.
3. `target_hint` is optional. It is only a path, symbol, command, or module
   hint. It is not evidence.
4. Live stance words are only `watch`, `partial`, `avoid`, and `defer`.
5. Live entries must not use outcome, approval, confidence, or review-verdict
   wording.
6. If an entry is about to support action, promotion, architecture absorption,
   project control, or a risk-sensitive answer, stop using the overlay and switch
   to v0.2.13.
7. Default read order is:

```text
reviewed core / project decisions / action basis
> candidate experience note / candidate boundary note
> active overlay for current project only
> archived overlay only on explicit historical request
> tombstone never in default semantic retrieval
```

8. Project closeout must drain live entries into a candidate experience note,
   candidate boundary note, archive, or delete + tombstone exception.
9. A live `watch`, `partial`, `avoid`, or `defer` entry must not stay live after
   project closeout.
10. If an entry no longer reduces judgment cost, remove it from live overlay.

## Minimal Fields

Required:

```text
kp_ref
stance
borrow_scope
updated_at
```

Optional:

```text
non_borrow_scope
target_hint
outcome_ref
```

Do not make these into a mainline schema yet.

## Field Notes

`kp_ref` points back to a reusable knowledge point.

`stance` says how the current project temporarily treats that point.

`borrow_scope` says what can be borrowed here.

`non_borrow_scope` says what must not be borrowed here.

`target_hint` says where to look in the current project. It should not include
health labels or support claims.

`outcome_ref` is only for closeout or post-closeout notes.

## File Tags

Use tags only at the project overlay file level, for discovery:

```text
#project-overlay
#project-misa
#sandbox
```

Do not add project tags to the reusable knowledge point itself.

