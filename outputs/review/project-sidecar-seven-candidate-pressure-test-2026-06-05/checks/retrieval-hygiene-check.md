---
type: sandbox_check
status: completed
created_at: 2026-06-05
scope: retrieval-hygiene-and-default-precedence
truth_boundary: test report only; not reviewed knowledge; not action basis
---

# Retrieval Hygiene Check

## Terms Tested

Old risky term:

```text
retrieval priority
```

Safer terms:

```text
default retrieval precedence
default search inclusion order
default read order
```

## Default Inclusion Rule

```text
reviewed core / decision / action basis
> candidate experience / boundary snapshots
> active sidecar overlay for the current project only
> archived overlay only when explicitly requested
> tombstone never in semantic retrieval
```

## Misa Scenario

Query:

```text
Can Misa use component-health diagnostic candidates to repair itself?
```

Expected retrieval:

| Layer | Include by default? | Role |
|---|---:|---|
| Misa docs/code/tests on component health and control boundaries | yes | primary evidence/context |
| Candidate boundary snapshot: retrieval hints not authority | yes, as warning candidate | risk warning |
| Active Misa overlay entry | yes, only because current project is Misa | navigation hint |
| Archived adaptive-retrieval-depth entry | no | historical only |
| Tombstone for duplicate vector priority entry | no | audit only |

## Pass / Fail

Pass:

```text
The retrieval order is expressed as inclusion/read order.
No layer is described as more true because it appears earlier.
Tombstone is explicitly excluded from semantic retrieval.
Archived overlay requires explicit historical query.
```

Fail risk found:

```text
The phrase retrieval priority is already present elsewhere in FUSION as
"graph rank is retrieval priority, not trust." That older wording is not from
this Project Lens test, but it confirms the term can be ambiguous.
```

## Recommendation

Use `default retrieval precedence` in sandbox artifacts. Avoid `retrieval
priority` for the sidecar lifecycle mechanism.
