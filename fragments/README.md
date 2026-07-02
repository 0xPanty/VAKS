# Fragment Candidates

This directory is the VAKS inbox for source-missing fragments.

Fragment candidates preserve useful ideas and weak leads without granting them
source, evidence, review, or action authority.

Allowed:

- orientation
- activation
- source recovery tasks
- pointer-only context pack references

Forbidden:

- evidence support
- reviewed knowledge
- action basis
- Source Capture Store input
- Source Annotation target
- exact quote output without a recovered source

Use `templates/fragment-candidate.md` for new records and validate them with:

```powershell
python tools/validate_fragment_candidate.py fragments
```
