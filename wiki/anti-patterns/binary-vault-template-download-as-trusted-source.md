---
type: anti-pattern
status: draft
created: 2026-05-27
updated: 2026-05-27
domain: source-hygiene
failure_mode: "Treating a downloadable vault archive with executable payloads as a trusted knowledge source"
severity: 5
likelihood: 3
complexity_cost: 2
cross_validated_with:
  - "[[source-hash-registry-and-idempotent-ingest]]"
  - "[[source-adapter-ingest-contract]]"
related_projects:
  - verified-action-knowledge-system
replacement:
  - "[[source-adapter-ingest-contract]]"
  - "[[hierarchical-index-context-routing]]"
verification_status: single-source
evidence_level: primary
confidence: high
last_verified: 2026-05-27
next_review: 2026-06-03
epistemic_type: take
gaps:
  - "Only zip listing and small text sample were inspected; executable was not executed."
evidence_timeline:
  - date: 2026-05-27
    source: "[[2026-05-27-kagantic-vault-structure-source]]"
    observation: "The advertised vault zip contains Application.cmd, package.txt, and unit.exe instead of Markdown vault files."
    effect: supports
    confidence: high
relations:
  - target: "[[SCHEMA]]"
    type: supports
    strength: 5
    confidence: high
    evidence:
      - "[[2026-05-27-kagantic-vault-structure-source]]"
    rationale: "The finding reinforces traceability-first source capture and source hygiene before ingest."
    created: 2026-05-27
    last_verified: 2026-05-27
decision: avoid
tags:
  - anti-pattern
  - source-hygiene
  - vault-template
  - binary-artifact
---

# Anti-pattern: Binary Vault Template Download As Trusted Source

## AI-readable preamble

Do not treat a downloadable "vault template" archive as trusted just because the repository says it is a vault.

Inspect archive contents first. Never execute binary payloads from a knowledge-template source.

## Problem

Knowledge-template repos can include download links or bundled archives.

If an agent or user blindly opens the archive, a vault review can turn into an execution risk.

## Source evidence

In `Asim00740/Kagantic-vault-structure`, the README points to:

```text
example vault/Operations/vault_Kagantic_structure_3.4.zip
```

Zip listing observed:

```text
Application.cmd
package.txt
unit.exe
```

`Application.cmd` content:

```text
start unit.exe package.txt
```

`package.txt` begins with obfuscated code-like text.

No executable was run.

## Why it fails

A vault template should normally contain:

```text
Markdown files
attachments
Obsidian config
templates
```

An archive that launches an executable is not a safe Markdown source.

## Failure conditions

- Treating GitHub download links as safe by default.
- Extracting and running a vault archive before inspecting contents.
- Letting agent automation ingest binaries as trusted source material.
- Confusing README marketing with actual source evidence.

## Replacement

Use this source hygiene rule:

```text
inspect archive listing
prefer git-tracked Markdown
hash source artifacts
never execute unknown binaries
record suspicious artifacts as risk
```

## Boundary

The Markdown files in the repo can still be reviewed for design ideas.

The binary zip artifact should not be trusted or executed.
