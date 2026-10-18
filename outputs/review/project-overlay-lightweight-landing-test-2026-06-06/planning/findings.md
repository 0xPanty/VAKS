# Findings

## Prior Sandbox Shape

The previous seven-candidate package proved sandbox usefulness but also showed
why the object model should not be promoted.

Observed heavy/fragile parts:

- `Project Lens` reads like a formal object name.
- YAML entry blocks make the note look schema-like.
- `park` is less clear than `defer`.
- `reason_1liner` duplicates `borrow_scope`.
- Manual target health belongs in checker output, not live entries.
- Snapshot wording can read like best practice or universal ban.
- Retrieval priority wording can read like authority or confidence.

## Current Lightweight Direction

Use one project file as a borrowing list:

```text
project_overlays/MISA.md
project_overlays/VAKS.md
```

Knowledge points stay clean. Project tags live only on project overlay files.

## Mainline Boundary

Current scan shows no diff in:

```text
ARCHITECTURE_PRINCIPLES.md
FUSION_ARCHITECTURE_V0_2_DRAFT.md
SCHEMA.md
REVIEW_QUEUE.md
templates/
```

This sandbox should preserve that.

