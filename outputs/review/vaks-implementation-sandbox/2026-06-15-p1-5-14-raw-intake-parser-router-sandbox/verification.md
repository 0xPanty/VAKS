---
record_kind: sandbox_verification
slice_id: 2026-06-15-p1-5-14-raw-intake-parser-router-sandbox
status: local_verification_passed
truth_boundary: sandbox_verification_only
---

# Verification

## Baseline

Start-of-slice baseline:

```text
git status --short count: 253
target path existed before slice: False
target path status before slice: empty
```

The dirty tree is treated as pre-existing baseline per user instruction. Final
audit only checks whether this slice wrote outside the allowed sandbox path.

P1.5-13 prerequisite:

```text
Product Acceptance conclusion: PASS_PRODUCT_GRADE
```

## Commands

No-bytecode syntax check:

```powershell
python -B -c "import ast, pathlib; [ast.parse(pathlib.Path(p).read_text(encoding='utf-8'), filename=p) for p in ['outputs/review/vaks-implementation-sandbox/2026-06-15-p1-5-14-raw-intake-parser-router-sandbox/artifact/raw_intake_parser_router_sandbox.py','outputs/review/vaks-implementation-sandbox/2026-06-15-p1-5-14-raw-intake-parser-router-sandbox/artifact/verify_raw_intake_parser_router_sandbox.py']]; print('syntax_ok')"
```

Observed:

```text
syntax_ok
```

Suite:

```powershell
python -B outputs/review/vaks-implementation-sandbox/2026-06-15-p1-5-14-raw-intake-parser-router-sandbox/artifact/verify_raw_intake_parser_router_sandbox.py
```

Observed summary:

```text
positive_fixtures: 4
failure_cases: 37
passed: true
failures: []
```

Target `__pycache__` check:

```text
no target __pycache__ found
```

## Adversarial Probe

An in-memory probe against the valid public-web fixture also confirmed:

```text
parser_markdown_bool -> valid: false, issue_codes: [RP_AUTHORITY_CONFUSION]
crawler_text_support -> valid: false, issue_codes: [RP_AUTHORITY_CONFUSION]
source_card_wiki_claims -> valid: false, issue_codes: [RP_PROTECTED_PATH_TARGET]
obsidian_exact -> valid: false, issue_codes: [RP_PROTECTED_PATH_TARGET]
candidate_action_basis -> valid: false, issue_codes: [RP_ACTION_BASIS_FORBIDDEN, RP_AUTHORITY_CONFUSION]
claim_action_basis -> valid: false, issue_codes: [RP_AUTHORITY_CLAIM_FORBIDDEN]
```

## Reviewer Repair

Initial Reviewer returned:

```text
REVIEW_BLOCKERS_FOUND
```

The blocker was a direct-field authority bypass. Claim arrays and named boolean
fields were blocked, but direct fields such as `evidence_support: true`,
`reviewed_knowledge: true`, `action_basis: true`, `mainline_readiness: true`,
and `truth_confidence: 0.91` could pass on retained output, parser, router,
source card, candidate distillation, and anchor objects.

Builder repaired this by blocking direct authority field names when they carry a
truthy value or non-boolean value, while preserving explicit negative boundary
fields such as `promotion_ready: false`.

Added failure cases:

- `retained-output-direct-authority-field.json`
- `parser-truth-confidence-direct-field.json`
- `router-truth-confidence-direct-field.json`
- `source-card-direct-evidence-support.json`
- `candidate-direct-reviewed-knowledge.json`
- `anchor-direct-evidence-support.json`

Post-repair suite result:

```text
positive_fixtures: 4
failure_cases: 36
passed: true
failures: []
```

Reviewer direct-field probes were rerun in memory:

```text
retained_evidence_support -> valid: false, issue_codes: [RP_AUTHORITY_CLAIM_FORBIDDEN]
retained_reviewed_knowledge -> valid: false, issue_codes: [RP_AUTHORITY_CLAIM_FORBIDDEN]
retained_action_basis -> valid: false, issue_codes: [RP_AUTHORITY_CLAIM_FORBIDDEN]
retained_mainline_readiness -> valid: false, issue_codes: [RP_AUTHORITY_CLAIM_FORBIDDEN]
parser_truth_confidence -> valid: false, issue_codes: [RP_AUTHORITY_CLAIM_FORBIDDEN]
router_truth_confidence -> valid: false, issue_codes: [RP_AUTHORITY_CLAIM_FORBIDDEN]
source_card_evidence_support -> valid: false, issue_codes: [RP_AUTHORITY_CLAIM_FORBIDDEN]
candidate_reviewed_knowledge -> valid: false, issue_codes: [RP_AUTHORITY_CLAIM_FORBIDDEN]
anchor_evidence_support -> valid: false, issue_codes: [RP_AUTHORITY_CLAIM_FORBIDDEN]
```

## Boundary Repair

Boundary Auditor later returned:

```text
BOUNDARY_BLOCKERS_FOUND
```

The blocker was that the direct field `promotion: true` could pass even though
promotion is explicitly forbidden for raw parser routing artifacts. Builder
added `promotion` to the direct authority denylist and added:

- `promotion-direct-authority-field.json`

Post-boundary-repair suite result:

```text
positive_fixtures: 4
failure_cases: 37
passed: true
failures: []
```

Boundary direct `promotion: true` probe was rerun in memory:

```text
promotion -> valid: false, issue_codes: [RP_AUTHORITY_CLAIM_FORBIDDEN]
```

## Positive Fixtures

- `valid-document-extraction-bundle.json`
- `valid-image-ocr-extraction-bundle.json`
- `valid-video-transcript-extraction-bundle.json`
- `valid-public-web-extraction-bundle.json`

## Failure Cases

- `missing-original-hash.json`
- `weak-md5-original-hash.json`
- `unknown-source-type.json`
- `route-modality-mismatch.json`
- `lazy-routing-missing.json`
- `heavy-parser-always-on.json`
- `router-confidence-as-truth.json`
- `router-truth-confidence-direct-field.json`
- `parser-config-hash-missing.json`
- `dependency-install-requested.json`
- `full-runtime-core-dependency.json`
- `gpl-license-unreviewed.json`
- `cloud-model-locality-unreviewed.json`
- `parser-confidence-as-truth.json`
- `parser-truth-confidence-direct-field.json`
- `retained-outputs-missing.json`
- `retained-output-hash-missing.json`
- `retained-output-direct-authority-field.json`
- `scratch-only-output.json`
- `protected-output-path.json`
- `obsidian-vault-output-path.json`
- `anchors-missing.json`
- `anchor-source-hash-missing.json`
- `anchor-direct-evidence-support.json`
- `parser-output-reviewed-status.json`
- `parser-markdown-reviewed-knowledge.json`
- `action-basis-allowed.json`
- `truth-mutation-allowed.json`
- `promotion-direct-authority-field.json`
- `private-web-no-auth.json`
- `account-cookies-used.json`
- `source-card-reviewed.json`
- `source-card-relations-top-level.json`
- `source-card-protected-target.json`
- `source-card-direct-evidence-support.json`
- `candidate-not-provisional.json`
- `candidate-direct-reviewed-knowledge.json`

## Non-Claims

The suite passing does not approve real parser execution, dependency
installation, Obsidian sync, reviewed knowledge, evidence support, reviewed
relations, reviewer approval, action basis, promotion, mainline readiness,
commit, or push.
