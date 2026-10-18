# Formal Vault Execution Request Screening

Slice: 2026-06-15-p2-33-formal-vault-execution-request-screening-sandbox

Purpose: make a request packet inspectable before any later human-controlled
step. This screen is a stop-and-review surface, not a run surface.

Current demo rows:

- Reviewable packet -> SCREENED_REVIEWABLE_NOT_SUBMITTED
- Missing confirmation packet -> SCREENED_BLOCKED_MISSING_CONFIRMATION_NOT_SUBMITTED
- Denied packet -> SCREENED_BLOCKED_BY_DENIAL_NOT_SUBMITTED
