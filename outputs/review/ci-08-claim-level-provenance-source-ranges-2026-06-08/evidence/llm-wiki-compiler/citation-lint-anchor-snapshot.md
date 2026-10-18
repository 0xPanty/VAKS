# llm-wiki-compiler Citation Lint Anchor Snapshot

Source:

```text
raw/repos/_snapshots/llm-wiki-compiler-main-2026-05-26.zip
llm-wiki-compiler-main/src/linter/rules.ts
```

Checked in this sandbox on 2026-06-08.

## Anchors

```text
src/linter/rules.ts:348-446
```

Observed behavior:

- Linter parses both `:start-end` and `#Lstart-Lend` citation suffixes.

```text
src/linter/rules.ts:450-536
```

Observed behavior:

- Linter detects citation markers referencing missing source files.
- Linter detects claim-level spans whose line ranges exceed the source file length.
- The pure-body helper is used by the candidate-lint path before reviewer approval.

```text
src/linter/rules.ts:556-584
```

Observed behavior:

- Linter detects malformed claim-level citations before approval.

## VAKS Extraction

Source ranges should be lintable before approval.

Lint pass means the range is syntactically and locationally valid. It does not
mean the range actually supports the claim.

