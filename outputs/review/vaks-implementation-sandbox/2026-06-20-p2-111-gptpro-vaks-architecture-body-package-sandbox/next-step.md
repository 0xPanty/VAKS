---
slice_id: 2026-06-20-p2-111-gptpro-vaks-architecture-body-package-sandbox
status: ready_for_external_review
---

# Next Step

Give GPT Pro:

```text
artifact/gptpro-architecture-body-reading-guide.md
artifact/gptpro-architecture-body-upload-prompt.md
artifact/source-docs/
```

Ask it first to answer:

```text
Does the VAKS architecture body support a lightweight VAKS Guard tool layer that executes existing boundaries?
```

Do not ask it to approve a merge yet.

## After Pro Replies

If Pro returns:

- `BODY_SUPPORTS_TOOL_LAYER_DIRECTION`: proceed to a future sandbox absorption-design package.
- `BODY_SUPPORTS_WITH_REVISIONS`: adjust positioning/context package first.
- `BODY_DOES_NOT_SUPPORT_TOOL_LAYER`: stop and revisit architecture/tool split before any implementation.

