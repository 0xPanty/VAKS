# VAKS Source ID v1

Status: draft contract for Source Capture Envelope v1.

This document defines stable source identity for raw capture and provenance.
It does not define trust, evidence support, reviewed knowledge, or action
readiness.

## Object Split

VAKS source capture keeps four objects separate:

```text
Source    stable upstream identity
Revision  upstream version claim
Snapshot  intrinsic observed content identity
Capture   one observation/capture event
```

Do not collapse these into a single `source_id` or commit string.

## Stable Source ID

`source_id` identifies the stable logical upstream source. It is extrinsic
identity, not content identity.

Format:

```text
vsrc:1:<kind>:<provider-or-namespace>:<provider-native-id>
```

Examples:

```text
vsrc:1:repo:github.com/linxiv-dev/linXiv
vsrc:1:repo:gitlab.example.com/group/name
vsrc:1:doi:10.xxxx/xxxxx
vsrc:1:arxiv:2204.12985
vsrc:1:openalex:W3123456789
vsrc:1:video:youtube:<video-id>
vsrc:1:video:bilibili:<bv-id>
vsrc:1:opaque:<uuid>
vsrc:1:content:sha256:<digest>
```

Rules:

- Provider or host must be explicit when a provider-native ID exists.
- Repo IDs must not be cross-provider. Use `repo:github.com/...`,
  `repo:gitlab.com/...`, or the concrete self-hosted Git host.
- The global layer must not lowercase owner/name or normalize provider IDs.
  Provider adapters own provider-specific casing rules.
- arXiv revision such as `v2` belongs in `revision`, not in stable
  `source_id`.
- Ordinary web pages and local files without stable native IDs should use
  `vsrc:1:opaque:<uuid>`. URLs are locators and aliases, not global identity.
- `vsrc:1:content:sha256:<digest>` is allowed only as a content-addressed
  fallback when source continuity is not needed.
- For repo, web, and video captures, tools must require an explicit stable
  `source_id` unless the caller explicitly opts into content-addressed fallback.

## Revision

`revision` records the upstream version claim.

```yaml
revision:
  kind: git_commit | git_tag | git_ref | version | arxiv_version | timestamp | content_hash | provider_revision | doi_version | web_capture_time
  value: "..."
```

A revision is not proof of the actual captured content. Submodules, Git LFS,
provider archives, and capture method can all make the observed snapshot differ
from the revision claim.

If there is no upstream revision claim, omit `revision`; do not serialize a
blank or arbitrary revision kind.

## Snapshot ID

`snapshot_id` identifies the observed immutable content.

Examples:

```text
vsnap:1:tree:sha256:<manifest-digest>
vsnap:1:blob:sha256:<blob-digest>
```

Tree snapshots are derived from deterministic snapshot manifests. Blob
snapshots are for single files or archives that cannot safely produce a complete
tree manifest.

## Capture ID

`capture_id` identifies one capture event.

```text
urn:uuid:<uuid>
```

The same snapshot can have multiple capture receipts. Snapshot storage may
deduplicate by `snapshot_id`, but capture history must preserve separate
observations unless an explicit idempotency key says they are the same retry.

Capture envelopes should default `change.state` to `unknown`, not `first_seen`,
unless they have compared against prior capture history.

## Aliases And Legacy IDs

Use typed aliases rather than a single legacy field:

```yaml
aliases:
  - kind: legacy
    value: "repo:owner/name@commit"
  - kind: locator
    value: "https://example.com/source"
  - kind: provider_object_id
    value: "github.com:repository:R_kgDO..."
```

Redirects and canonical links are observations. They must not automatically
merge source identity.

`provider_object_id` is optional continuity metadata supplied by a provider
adapter, not by the offline scanner. Its format is:

```text
<provider-host>:<object-type>:<opaque-provider-id>
```

Rules:

- Provider host and object type are lowercase.
- The opaque provider ID is case-sensitive.
- It is not trust, ownership, authority, or evidence support.
- Same provider object ID with a new locator means the same source may have
  been renamed or moved.
- Same locator with a different provider object ID is a rebound risk and must
  not silently overwrite the old source identity.

## Boundary

Source IDs, revisions, snapshots, captures, and aliases are provenance facts.
They do not create trust, verification, evidence support, reviewed relations,
truth confidence, or action basis.
