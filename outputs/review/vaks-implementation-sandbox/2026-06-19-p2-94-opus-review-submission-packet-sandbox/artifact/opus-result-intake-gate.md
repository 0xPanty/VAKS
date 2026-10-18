# Opus Result Intake Gate

## Allowed External Conclusions

- `OPUS_PASS_SANDBOX_CLOSEOUT`: Opus accepts the sandbox closeout evidence as externally reviewable and sufficient for sandbox closeout only.
- `OPUS_REVISE_SANDBOX_CLOSEOUT`: stay in the current sandbox review lane and fix the listed blockers before any further claim.
- `OPUS_BLOCKED_NEEDS_USER`: stop and ask the user for missing evidence, scope clarification, or external-state change.

## Not Allowed

- Do not translate Opus pass into mainline merge.
- Do not translate Opus pass into reviewed knowledge, evidence support, or action basis.
- Do not claim Opus approval unless an actual external Opus conclusion is present.
- Do not commit, push, sync, or promote.
- Do not edit root architecture docs, README, tools, templates, wiki truth layers, or Obsidian vault from this gate.

## Required Intake Record If Opus Responds

Create a later sandbox-only slice that stores:

- Opus raw conclusion token;
- Opus reviewed evidence list;
- Opus blockers, if any;
- boundary audit confirming the result is not mainline approval;
- Product Acceptance deciding the next sandbox step.
