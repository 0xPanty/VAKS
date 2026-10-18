# Source Capture Store v1

Status: v1.0-alpha.1 follow-up contract for Source Capture Envelope artifacts.

The Source Capture Store is a local persistence layer for validated Raw Capture
artifacts. It is not a knowledge truth source, review database, evidence-support
judge, or action authorization layer.

It stores:

- the three Source Capture Envelope artifacts under `bundle/`;
- the raw input blob in a SHA256 content-addressed store when provided;
- the implementation manifest and raw-intake policy used during storage-time
  validation;
- a local `capture-storage-receipt.json` proving retention and fixity in this
  store instance.

It never writes candidate, reviewed, action, or feedback objects.

## Layout

```text
source-capture-store/
├── store.json
├── blobs/
│   └── sha256/
│       └── ab/
│           └── <full-sha256>
├── captures/
│   └── <capture-uuid>/
│       ├── bundle/
│       │   ├── capture-envelope.json
│       │   ├── snapshot-manifest.jsonl
│       │   └── snapshot-hygiene.intoto.json
│       ├── validation-context/
│       │   ├── source-capture-implementation-manifest.json
│       │   └── raw-intake-policy.json
│       └── capture-storage-receipt.json
├── indexes/
│   └── source-snapshot-index.jsonl
└── .staging/
```

`<capture-uuid>` is the UUID portion of `capture_id`; the receipt preserves the
full `urn:uuid:...` value.

## Store Identity

`store.json` identifies one concrete filesystem store:

```json
{
  "schema": "urn:vaks:schema:source-capture-store:v1",
  "layout_version": "1",
  "store_instance_id": "urn:uuid:00000000-0000-4000-8000-000000000000",
  "created_at": "2026-06-25T08:00:00Z",
  "content_addressing": {
    "algorithm": "sha256",
    "layout": "prefix-2/v1"
  }
}
```

`layout_version` describes the store format. `store_instance_id` distinguishes
this concrete store from another store using the same layout.

## Bundle Identity

The bundle digest is not a hash of a directory or a ZIP. It is the SHA256 digest
of a canonical JSON identity payload:

```json
{
  "schema": "urn:vaks:identity:capture-bundle:v1",
  "artifacts": [
    {
      "digest": "sha256:...",
      "media_type": "application/vnd.vaks.source-capture.v1+json",
      "name": "capture-envelope.json",
      "size": 3201
    },
    {
      "digest": "sha256:...",
      "media_type": "application/vnd.in-toto+json",
      "name": "snapshot-hygiene.intoto.json",
      "size": 5012
    },
    {
      "digest": "sha256:...",
      "media_type": "application/vnd.vaks.snapshot-manifest.v1+jsonl",
      "name": "snapshot-manifest.jsonl",
      "size": 90123
    }
  ]
}
```

The profile is `vaks-capture-bundle-id/v1`. The JSON profile is the narrow VAKS
canonical JSON used by Source Capture tooling: UTF-8, sorted keys, compact
separators, no NaN/Infinity, and no floating point values in this payload.

## Storage Receipt

`capture-storage-receipt.json` proves that this store retained the capture
bundle and, when supplied, the raw blob:

```json
{
  "schema": "urn:vaks:schema:capture-storage-receipt:v1",
  "capture_id": "urn:uuid:00000000-0000-4000-8000-000000000000",
  "stored_at": "2026-06-25T08:15:00Z",
  "store": {
    "instance_id": "urn:uuid:00000000-0000-4000-8000-000000000001",
    "layout": "vaks-source-capture-store/v1"
  },
  "bundle": {
    "digest_profile": "vaks-capture-bundle-id/v1",
    "digest": "sha256:...",
    "artifacts": []
  },
  "raw_blob": {
    "retention_state": "retained",
    "media_type": "application/zip",
    "size": 123,
    "digest": "sha256:...",
    "store_path": "blobs/sha256/ab/abcdef..."
  },
  "validation_context": {
    "implementation": {
      "size": 1450,
      "digest": "sha256:...",
      "store_path": "captures/<uuid>/validation-context/source-capture-implementation-manifest.json"
    },
    "policy": {
      "size": 928,
      "digest": "sha256:...",
      "store_path": "captures/<uuid>/validation-context/raw-intake-policy.json"
    }
  },
  "storage_state": "retained"
}
```

If no raw blob was supplied, `raw_blob.retention_state` is `not_retained` and the
receipt records the expected digest and size from the capture envelope.

Do not use `disposition` in the receipt. `raw_handling.disposition` belongs to
the Source Capture Envelope and records Raw Intake handling. The store receipt
uses `storage_state` and `retention_state` only.

## Commands

```powershell
python tools/store_source_capture.py init `
  --store-root source-capture-store

python tools/store_source_capture.py put `
  --store-root source-capture-store `
  --bundle-dir outputs/capture-demo `
  --raw-blob raw/repos/_snapshots/source.zip `
  --implementation-manifest tools/source_capture_implementation_manifest.json `
  --policy-file policies/source-capture/raw-intake-default-v1.json

python tools/store_source_capture.py verify-capture `
  --store-root source-capture-store `
  --capture-id urn:uuid:00000000-0000-4000-8000-000000000000

python tools/verify_source_capture_store.py `
  --store-root source-capture-store

python tools/rebuild_source_snapshot_index.py `
  --store-root source-capture-store

python tools/rebuild_source_snapshot_index.py `
  --store-root source-capture-store `
  --check
```

## Put Rules

`put` must:

- validate the input bundle using `enterprise-alpha1` before final retention;
- copy the bundle, raw blob, implementation manifest, and policy into private
  staging and compute size/digest from the staged bytes;
- validate the staged bundle before capture commit;
- require raw blob size and digest to match `observation.blob`;
- store retained raw blobs under `blobs/sha256/<prefix>/<digest>`;
- reject existing CAS objects whose bytes do not match the digest path;
- write `bundle/`, `validation-context/`, and the receipt under a staging capture
  directory before renaming into `captures/<uuid>/`;
- never modify the three bundle artifacts;
- never overwrite an existing capture.

Duplicate handling:

- same `capture_id`, same `bundle.digest`, and same raw-blob retention: return
  `already_retained`;
- same `capture_id` with different bundle or raw retention: fail with
  `CAPTURE_ID_CONFLICT`.

## Boundaries

This receipt attests only to local retention and fixity. It does not establish
source authenticity, evidentiary support, review status, or action
authorization.

The store index is intentionally out of scope for PR-B1. Future indexes must be
rebuildable from `captures/` and must not become the source of truth.

## Full Store Verification

`tools/verify_source_capture_store.py` verifies one Store instance without
modifying it. It reuses the same historical capture verification used by
`verify-capture`; every retained capture must pass receipt, bundle, validation
context, implementation manifest, policy replay, and raw blob fixity checks.
The report is emitted to stdout; B2.1 intentionally does not write report files.

The report schema is
`urn:vaks:schema:source-capture-store-verification-report:v1`.

Status meanings:

- `pass`: every capture and referenced CAS blob verified, with no warnings.
- `pass_with_warnings`: every capture verified, but non-authoritative issues
  such as a valid orphan CAS blob were found.
- `fail`: at least one capture, receipt, context, referenced blob, or CAS object
  failed verification.
- `indeterminate`: the Store was not stable enough to verify, for example
  `.staging/` was non-empty or the inventory changed during scanning.

Rules:

- the verifier is read-only and performs no repair;
- all reported paths are Store-relative POSIX paths; unsafe bytes are UTF-8
  percent-encoded;
- orphan CAS blobs are warnings if their bytes match their digest path;
- missing blobs referenced by retained receipts are errors;
- `.staging/` residue or concurrent Store changes are indeterminate, not proof
  of source corruption;
- the report's `assurance_scope` states that it attests only to local retention
  and fixity.

The verification report must not be interpreted as source authenticity,
evidentiary support, review status, action authorization, or mainline readiness.

## Deterministic Source Snapshot Index

`tools/rebuild_source_snapshot_index.py` rebuilds
`indexes/source-snapshot-index.jsonl` from verified captures. The index is a
derived projection for lookup and deduplication. It is not a source of truth and
must be deletable and rebuildable from `captures/`.

Before generating bytes, the tool runs full Store verification. If any capture,
referenced raw blob, receipt, validation context, or Store layout check fails,
the rebuild fails and an existing index is left unchanged. Valid orphan CAS blobs
remain verification warnings and are not written as index entries.

The JSONL file uses:

- one deterministic header record;
- one entry per verified capture;
- canonical JSON, UTF-8, LF line endings;
- no `generated_at`, local absolute paths, or filesystem-order-dependent fields;
- entry sorting by UTF-8 bytes of `source_id`, `snapshot_id`, then `capture_id`.

`--check` is read-only. It regenerates the expected bytes in memory and compares
them with the existing index. It does not create `indexes/`, write reports, or
repair drift.

Write rules:

- `indexes/` is created lazily only during rebuild, never during `--check`;
- `indexes/` and `source-snapshot-index.jsonl` must not be symlinks or reparse
  points;
- output is staged and atomically replaces the old index only after the Store
  remains stable through verification and projection;
- after staging the new index bytes, the tool performs a final Store truth
  inventory check before `os.replace`; index temp files do not count as Store
  truth changes;
- if the Store changes during rebuild, the result is indeterminate and the old
  index remains untouched.

The index schema is `urn:vaks:index:source-snapshot:v1`. It records source,
snapshot, capture, bundle digest, and raw-blob retention pointers only. It does
not create candidate, reviewed, evidence-support, feedback, or action objects.
