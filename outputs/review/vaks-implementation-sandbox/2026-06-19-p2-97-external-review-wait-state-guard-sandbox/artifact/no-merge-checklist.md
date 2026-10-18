# No-Merge Checklist

Do not merge, promote, commit, push, sync, or write truth layers unless every item below is complete.

- [ ] Actual external Opus result exists.
- [ ] Opus result validates against p2-96 schema.
- [ ] Opus result was captured in a later sandbox-only intake slice.
- [ ] Boundary Auditor confirms result is not mainline approval.
- [ ] User separately approves any mainline integration.

Current guard state: `STOP_WAIT_EXTERNAL_OPUS_REVIEW`.
