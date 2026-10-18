# Limits

- Offline, stdlib-only, sandbox-only.
- No live IAM, live feature flag service, live LLM, live retrieval, DB, API,
  service, network call, Obsidian write, wiki write, raw write, or Truth Core write.
- Trusted runtime context must carry `trusted_context_origin=server_adapter`,
  `iam_subject_verified=true`, and `feature_flag_resolved_by=server_flag_resolver`.
- User payload must be an object and may only contain query, query_sha256, and
  client_request_id. Those fields must be strings when present. Trusted runtime
  context must be an object with only allowlisted fields, and principal/tenant/
  mode/risk/domain/flag fields must be strings where applicable.
- User query, client request id, and trusted runtime fields must be within
  bounded lengths and must not contain control, surrogate, or format
  characters. User-provided query_sha256 must be valid SHA256 hex and match the
  query.
- The bounded trial allowlist is one internal principal and tenant, low risk,
  orientation/source_inspection, and general/source_lookup domains. Action and
  high-risk requests fail closed at the adapter preflight.
- Feature flag mode must be either `off` or `enforce`.
- Answer relevance is checked with frozen alignment id, expected claim ids, and
  marker groups against the exact candidate final. This is not a general
  semantic relevance model.
- Adapter safe fallback text is generated internally from allowlisted templates;
  callers cannot pass arbitrary fallback bodies.
- Adapter candidate commit accepts only a narrow final-answer envelope. Unknown
  candidate final fields are treated as a schema failure, not as metadata to
  preserve.
- Adapter rejection reason codes should be treated as categories; raw rejected
  values are not embedded in the reason code.
- Trial logs use deterministic HMAC-shaped identifiers with a sandbox key so
  this bundle can be reproduced. Production must use secret runtime key
  material; this sandbox does not prove production log-key management.
- JSONL audit artifacts redact synthetic sensitive test strings while retaining
  explicit redaction markers. The provenance source copy remains executable
  review evidence and may contain synthetic test-token construction logic.
- JSONL audit artifact keys are also redacted. If redaction would make two keys
  collide, the object is recorded as typed entries rather than a normal JSON
  object so evidence is not silently overwritten.
- JSONL audit artifacts must not store raw `repr()` output or raw custom object
  type names. They record a safe type category, repr length, and a sensitive
  hint flag instead.
- If an object's `repr()` is unavailable or raises, the audit record must stay
  structured and fail closed without emitting object text.
- JSONL audit serialization is bounded. Cycles, deep nesting, oversized
  collections, and oversized strings are represented by explicit resource-limit
  or truncation markers rather than by unbounded recursion or full expansion.
- The direct adversarial self-test exercises JSON serialization edge cases
  independently of the fixed trial fixtures.
- The local stress self-test is still an in-process sandbox test. It does not
  represent real IAM, network, live retrieval, live LLM, or production load.
- Source import audit is static and import-level. It can catch direct banned
  imports, but it is not a runtime firewall or production egress control.
- Stress workspaces are temporary scratch and must not become review evidence;
  bundle verification fails if `_stress_workspace` artifacts or ZIP entries are
  present.
- Oversized string markers store length and a structural fingerprint only; they
  do not store raw leading text fragments.
- JSONL artifact writing converts non-standard floats such as NaN and Infinity
  into explicit audit markers. They remain invalid request values and must not
  enter guarded release.
- JSONL artifact candidates are strict-parsed before summary pass is granted,
  rejecting non-standard JSON constants such as raw NaN or Infinity.
- JSONL artifact writing converts objects with non-string keys or converted-key
  collisions into explicit typed entries. They remain invalid request values
  and must not enter guarded release.
- JSONL artifact writing records bytes/bytearray by length, a
  payload_sensitive_hint flag, and a structural fingerprint that does not hash
  raw payload bytes. It must not store raw sensitive-token SHA256 values as an
  audit side channel. Sets are recorded as typed entries, and arbitrary objects
  by type only. Raw object repr/body text must not be emitted.
- The strict JSONL parse gate covers the generated trial case, result, and log
  audit rows. It is an artifact integrity gate, not a production API contract.
- The adapter sink buffer is the sole user-visible output source in this
  sandbox.
- The adapter sink is write-once: after a successful candidate or fallback
  commit, later candidate/fallback commits and fact-text writes must not change
  the buffer.
- The direct adversarial self-test is still a local method-level test. It
  exercises concurrent calls inside one Python process, not distributed
  cross-process release coordination.
- Candidate commit requires `guard_passed is true` and
  `relevance_passed is true`; truthy non-boolean values must fail closed.
- Public sink state and event snapshots are read-only views in this sandbox;
  mutating a returned event snapshot must not change internal sink state.
- Candidate final text must be a string and must match its SHA256 before release.
- Candidate final, visible claim ids, expected claim ids, and marker groups must
  be structurally valid before relevance can pass.
- Claim ids must be unique, trimmed, non-empty strings without control
  characters.
- Latency is local adapter path latency, not production end-to-end latency.
- Review bundle output paths, ZIP paths, SHA256 sidecar paths, and individual
  artifact paths are append-only; pre-existing symlinks are treated as
  pre-existing paths.
- Bundle output must stay under `outputs/review` with an allowlisted bundle
  name. The append-only self-test probes forbidden raw/wiki/Obsidian and
  sibling-prefix paths and requires rejection before directory creation.
- Bundle self-test verifies ZIP sidecar SHA256, ZIP integrity, duplicate entry
  count, unsafe entry names, fixed ZIP timestamps/compression, entry set
  equality with the output directory, and entry hash equality with directory
  artifacts.
- Append-only self-test also runs tamper negative controls for artifact hash
  modification, missing artifact, extra artifact, ZIP SHA256 sidecar
  modification, sidecar format mismatch, unsafe ZIP entry injection, duplicate
  ZIP entry injection, and ZIP entry content mismatch.
- ZIP entry name safety is also tested with explicit negative controls for
  traversal, absolute, Windows-drive, backslash, dot-segment, empty-segment, and
  control-character forms.
- Trial approval is limited to one allowlisted internal account and low-risk
  orientation/source_inspection.
