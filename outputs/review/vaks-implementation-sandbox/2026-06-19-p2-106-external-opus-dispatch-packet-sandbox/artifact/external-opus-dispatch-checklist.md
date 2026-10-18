# External Opus Dispatch Checklist

- Verify the ZIP exists before upload.
- Verify ZIP path: `outputs/review/vaks-implementation-sandbox/2026-06-19-p2-100-opus-review-transfer-package-sandbox/artifact/opus-review-transfer-package.zip`
- Verify ZIP SHA256: `2fa20d453406757c0e53abc2c2ad9842264c35359d1e12b203ea5113273b2640`
- Send `external-opus-dispatch-message.md` as the message body.
- Attach the ZIP file to the external Opus review surface.
- Require exactly one conclusion token in the response.
- Preserve the raw Opus response in a later sandbox-only intake slice.
- Validate the raw response with p2-102 before any user approval or merge discussion.
- Do not edit old slices, main architecture docs, wiki truth layers, templates, tools, or Obsidian vault during dispatch.

