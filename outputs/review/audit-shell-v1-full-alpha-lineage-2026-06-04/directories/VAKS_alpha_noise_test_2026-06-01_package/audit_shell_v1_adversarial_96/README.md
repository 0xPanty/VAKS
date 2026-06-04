# VAKS Audit Shell V1 Adversarial 96 Sandbox

Status:

```text
sandbox only
main vault read-only
no SCHEMA change
adversarial fixture patch
not real-data product proof
```

## Purpose

This sandbox implements Pro's recommended `B, then A` step:

```text
first run a 96-case adversarial fixture patch
then move to a real-data paired pilot only if this patch passes
```

The goal is to break the previous self-confirming test pattern by separating:

```text
gold labels
shell implementation
comparison logic
```

## Run

```powershell
python run_adversarial_patch.py
```

Expected outputs:

```text
shell_outputs.json
comparison_results.json
ADVERSARIAL_PATCH_REPORT.md
```

