# VAKS Snapshot Manifest v1

Status: draft contract for deterministic observed content identity.

Snapshot manifests describe the logical content observed from a source capture.
They intentionally differ from raw archive byte hashes.

## Files

A structured capture can produce:

```text
capture-envelope.json
snapshot-manifest.jsonl
snapshot-hygiene.intoto.json
```

VAKS v1 bundles always emit `snapshot-manifest.jsonl` for uniform validation.
Tree snapshots use the manifest bytes as identity. Blob or unavailable snapshots
emit a header-only manifest with `state: blob` or `state: unavailable`; that
manifest is a receipt aid and does not define the blob `snapshot_id`.

## JSONL Format

The manifest is UTF-8 JSON Lines with LF newlines. The first line is a header.
Each following line is one entry.

```jsonl
{"profile":"vaks-archive-tree/v1","schema":"urn:vaks:schema:snapshot-manifest:v1","state":"complete"}
{"digest":"sha256:...","mode":"100644","path":"README.md","size":1251,"type":"file"}
{"digest":"sha256:...","mode":"100644","path":"sql/PROJECT_TO_TAG.SQL","size":744,"type":"file"}
{"digest":"sha256:...","mode":"100644","path":"sql/PROJECT_TO_TAG.sql","size":690,"type":"file"}
{"mode":"120000","path":"docs/latest","target":"v1","type":"symlink"}
```

## Determinism Rules

- UTF-8 output.
- LF line endings.
- JSON object keys sorted lexicographically.
- No floating point numbers.
- Explicit hash algorithm in every digest.
- Entries sorted by original path string, not by normalized comparison keys.
- ZIP timestamps, compression method, entry order, UID/GID, and pack metadata do
  not enter logical snapshot identity.
- File entries include `type`, `path`, normalized `mode`, `size`, and content
  `digest`.
- Symlink entries include `type`, `path`, normalized `mode`, and `target`.
- Paths must not be case-folded or Unicode-normalized before identity hashing.
- If every useful archive member is under the same single top-level wrapper
  directory, that wrapper is stripped before manifest identity is computed.
- Empty directory entries do not enter tree identity. They are only used to
  detect ambiguous file/directory conflicts.
- ZIP filenames must reconcile all safety-relevant path representations exposed
  by the scanner, including `filename`, `orig_filename`, local-header name, and
  Unicode path extra fields. NUL, control characters, traversal, backslashes,
  absolute paths, empty segments, or representation conflicts quarantine the
  capture instead of entering tree identity.
- TAR member names must be usable as Unicode strings. Non-UTF-8 or otherwise
  ambiguous names must be reported as partial/failed rather than silently
  normalized into identity.
- Archive directory entries define tree-model constraints but are not emitted as
  manifest entries.
- File modes are normalized to Git-style logical modes: `100644`, `100755`, and
  `120000`; full permission bits do not affect identity.
- Symlink targets must be strict UTF-8 and within the configured target-size
  limit.

Raw paths define identity. Derived comparison keys are only for hygiene checks.
This preserves distinct paths such as:

```text
TAG.SQL
TAG.sql
```

## Snapshot Digest

`snapshot_id` for a tree is the SHA-256 digest of the exact manifest bytes:

```text
vsnap:1:tree:sha256:<manifest-digest>
```

Archive byte identity is separate:

```text
capture_blob_digest: sha256:<raw-archive-digest>
```

The same tree repacked with different ZIP timestamps or compression settings
should produce a different capture blob digest and the same tree snapshot ID.

## Unsafe Or Ambiguous Archives

If an archive contains exact duplicate entries, path traversal, absolute paths,
or members that cannot be interpreted safely, the inspector must not manufacture
a complete tree snapshot.

Expected behavior:

```text
raw blob snapshot retained
tree manifest partial or unavailable
raw handling disposition quarantined
hygiene report records the hazard
```

## Hygiene Reports

Hygiene reports must bind to an immutable subject digest, normally the snapshot
manifest digest. They are facts about a checker run, not trust verdicts.

Missing hygiene means `not_run`, never clean.
Uncompared fidelity means `not_checked`, never matched.
Hygiene statements record the effective scanner limits under
`predicate.parameters`; changing limits can legitimately change findings.
Findings are sorted, deduplicated, and bounded so the same logical input and
same parameters produce stable hygiene bytes.

Source Capture Envelope v1.0-alpha.1 also records:

- `max_input_blob_size`, the raw input copy limit before archive inspection.
- `observation.content_type`, the scanner-selected parser/container
  interpretation, not a filename hint.
- `producer.implementation` and `checker.implementation`, descriptors for the
  pinned scanner/validator/schema/policy implementation manifest.
- `raw_handling.policy.digest`, the canonical digest of the policy that
  actually decided admitted versus quarantined.

The in-toto Statement shape is a local digest-linked receipt shape in v1. It is
not signed and must not be treated as an authenticated attestation.

`raw_handling.disposition = admitted` means the capture may enter the Raw layer.
It does not mean source verified, evidence support, reviewed knowledge, content
truth, completeness, or runtime readiness. `max_severity = none` only means this
checker found no known issue under the recorded parameters.

## Raw To Candidate Pointer

Candidates that use captured source material should preserve a minimum immutable
pointer:

```yaml
source_pointer:
  source_id: "vsrc:1:repo:github.com/linxiv-dev/linXiv"
  capture_id: "urn:uuid:..."
  snapshot_id: "vsnap:1:tree:sha256:..."
  selector:
    path: "README.md"
    lines: "20-48"
  content_digest: "sha256:..."
```

This pointer does not raise the candidate evidence grade and does not create
reviewed knowledge. It only keeps the provenance chain from depending on a
mutable URL or source card.
