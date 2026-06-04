# Pilot Execution Checklist

## Before Running

- Confirm main vault is not being edited for this pilot.
- Use only the prototype CSV files as pilot inputs.
- Do not reinterpret this as formal adoption.
- Do not modify `SCHEMA.md`.
- Do not commit unless explicitly asked.

## Pilot 1: Operator Triage

Input:

```text
C:\Users\Administrator\Documents\VAKS_audit_shell_queue_cockpit_prototype_2026-06-04\OPERATOR_TRIAGE_PILOT_SAMPLE_80.csv
```

Check:

- first action correct,
- high-risk actionability not wrong,
- blocking/regressed/stale not missed,
- authority boundary understood,
- ordinary rows stay light.

## Pilot 2: Semantic Click-Back

Input:

```text
C:\Users\Administrator\Documents\VAKS_audit_shell_queue_cockpit_prototype_2026-06-04\SEMANTIC_CLICKBACK_PILOT_SAMPLE_60.csv
```

Check:

- first correct click,
- wrong semantic landing,
- dead-end click,
- source/claim/context not mistaken for evidence,
- transcript segment not mistaken for reviewed evidence.

## Pilot 3: Source-Family Independence Trap

Input:

```text
C:\Users\Administrator\Documents\VAKS_audit_shell_queue_cockpit_prototype_2026-06-04\SOURCE_FAMILY_INDEPENDENCE_TRAP_SAMPLE.csv
```

Check:

- count not support,
- lineage not support,
- repeated mention not independent support,
- derived summary not reviewed truth,
- source family boundary understood.

## Final Verdict

Use only one:

```text
ready_for_candidate_operation_convention_writeback
continue_sandbox_with_specific_fixes
redesign_required
```

