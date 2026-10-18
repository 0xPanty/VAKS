# R1.5 Supervised Trial Adapter Preflight

This sandbox tests the real trial adapter risks that remain after R1.4:

- server-constructed trusted request envelope;
- user payload and trusted runtime context type validation before guarded path;
- user payload allowlist: only query, query_sha256, and client_request_id are
  accepted;
- user query hash must be valid and match the user query when supplied;
- trusted runtime context allowlist and feature flag mode enum validation before
  guarded path;
- trusted runtime context values are restricted to the one-account low-risk
  supervised trial allowlist;
- user query, trusted query, trusted query hash, and feature flag mode must bind
  consistently before guarded path;
- adapter rejection reason codes are stable categories and do not include raw
  rejected field values;
- non-standard JSON values such as NaN and Infinity in fixtures are rejected by
  the adapter and recorded with safe audit markers rather than emitted as
  non-standard JSON;
- non-string object keys in fixtures are rejected by the adapter and recorded
  as typed audit entries so key collisions cannot hide input evidence;
- non-string keys whose repr fails are still rejected and recorded with safe
  repr-unavailable metadata rather than crashing validation;
- non-JSON values such as bytes, sets, and arbitrary objects are rejected by
  the adapter and recorded with safe metadata rather than raw repr/body text;
- JSONL audit artifacts redact synthetic sensitive test strings while keeping
  explicit redaction markers for reviewability;
- JSONL audit artifacts redact sensitive dictionary keys and convert
  redaction-induced key collisions into typed entries instead of overwriting;
- bytes/bytearray audit metadata uses a structural fingerprint derived from
  type, length, and a sensitive-hint flag, never a raw payload SHA256, so
  encoded sensitive values cannot become enumerable audit fingerprints;
- non-string key repr and custom object type names are recorded only as safe
  metadata, not as raw repr/type strings;
- JSONL audit serialization has explicit depth, node, item-count, long-string,
  and cycle markers so malicious fixture structure cannot crash bundle
  generation or expand without bound;
- oversized strings are represented without storing a raw leading text fragment,
  preventing truncation records from leaking unknown sensitive text;
- feature flag off / error behavior;
- adapter-level ReleaseSink after relevance and before user-visible release;
- write-once / sealed adapter ReleaseSink after the first successful commit;
- direct adversarial self-test for same-sink concurrent candidate commits,
  post-commit candidate/fallback/fact write attempts, copied committed-final
  mutation, extra visible claim rejection, and candidate hash mismatch;
- direct adversarial self-test for audit serialization cycles, deep nesting,
  long sensitive strings, and non-finite floats;
- direct adversarial self-test for ZIP entry name safety, including traversal,
  absolute path, Windows drive path, backslash, dot-segment, empty-segment, and
  control-character cases;
- public sink state is exposed as read-only properties, not mutable release state;
- Guard and relevance commit gates require strict boolean `true`, not truthy
  strings or numbers;
- answer relevance gate on the exact candidate final before the adapter release commit;
- R1.4 final/user-visible coherence before adapter commit;
- candidate final envelopes must use the allowlisted final-answer fields only;
  extra debug/trace fields fail closed and are not copied into audit artifacts;
- exact visible claim-set matching for the fixture contract;
- malformed candidate final text is structurally rejected, not released;
- malformed relevance contract fields such as non-list claim ids, unhashable
  claim ids, invalid marker groups, or non-object candidate finals are
  structurally rejected, not released;
- duplicate, control-character, or whitespace-padded claim ids are
  structurally rejected, not released;
- no fact text before Guard through the same adapter sink;
- fallback is generated from adapter-owned allowlisted templates only;
- user-visible output is read only from the adapter sink buffer;
- logs do not contain sensitive raw text, unsalted principal/tenant SHA256,
  raw query SHA256, or raw final-answer SHA256; sandbox logs use HMAC-shaped
  identifiers;
- append-only package generation treats pre-existing directories, ZIPs,
  sidecars, artifacts, and symlinks as blockers;
- output directory enforcement rejects raw, wiki, Obsidian, sibling-prefix,
  bad-name, and control-character output targets before creating directories;
- local stress self-test repeatedly exercises adapter rejection, feature-flag
  off, guarded release, relevance failure, Guard error fallback, and parallel
  pure-gate paths;
- stress temporary workspaces must be removed before packaging and must not
  appear in the review directory or ZIP;
- source import audit checks this runner and frozen local dependencies for
  allowlisted stdlib imports and banned network/DB/LLM/client imports;
- local adapter latency is measured.

It supports only a one-account, low-risk, supervised internal enforce trial.
It does not approve Canary or production rollout.
