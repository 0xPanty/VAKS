---
type: sandbox_check
status: completed
created_at: 2026-06-06
truth_boundary: check report only
---

# Retrieval Hygiene Check

## Rule Tested

Do not create a retrieval authority mechanism.

Use one plain default read order:

```text
reviewed core / project decisions / action basis
> candidate experience note / candidate boundary note
> active overlay for current project only
> archived overlay only on explicit historical request
> tombstone never in default semantic retrieval
```

## Live Overlay Behavior

`project_overlays/MISA.md` and `project_overlays/VAKS.md` are active only for
their own project scope.

The live overlay files do not assign confidence, support strength, source count,
or rank.

## Archive Behavior

Archived entries in the closeout note are historical. They are not default
semantic retrieval targets for current project answers.

## Tombstone Behavior

The old duplicate adaptive retrieval entry is retained only as a closeout audit
exception and must not appear in default semantic retrieval.

## Interpretation

This preserves the useful read order without creating a named authority layer.

