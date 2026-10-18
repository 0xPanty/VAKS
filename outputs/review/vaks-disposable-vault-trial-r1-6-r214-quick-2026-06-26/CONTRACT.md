# R1.6 Disposable Vault Trial Contract

This sandbox checks the file-output boundary after R1.5 adapter commit.

Allowed behavior:

- Create one disposable Obsidian-like vault under the current review output.
- Write committed guarded answers only under `.vaks_runtime/released/`.
- Exercise Obsidian-shaped paths and note content in that disposable vault:
  `.obsidian` config/plugin/snippet writes, attachments, templates, daily notes,
  Canvas/Base files, frontmatter, properties, wiki links, transclusions,
  Dataview/Tasks syntax, callouts, block IDs, tags, and active file URIs must be
  rejected, while plain released/fallback answers must still write.
- After all attack and concurrency cases, scan the disposable vault tree. The
  only tolerated final structure is `.obsidian/app.json`, the two runtime lock
  files, and safe Markdown files under `.vaks_runtime/released/` or
  `.vaks_runtime/fallback/`; plugin state, attachments, templates, daily notes,
  raw/wiki roots, staging residue, links/reparse points, and non-Markdown
  runtime files are violations.
- Re-read final allowed files before cleanup. `.obsidian/app.json` and runtime
  lock files must match their exact expected contents, and every final runtime
  Markdown note must still pass the safe Markdown subset validator. Temporary
  integrity probes deliberately tamper app config, lock content, runtime
  Markdown content, and UTF-8 validity; each probe must be detected and cleaned
  before the final scan.
- Recompute every committed release file against the commit-time HMAC ledger
  before cleanup. A dedicated probe rewrites a released answer with different
  safe-looking Markdown text; the ledger check must detect that the content is
  no longer the committed output and must restore the original bytes before the
  final scan.
- Final tree scan also checks casefold/NFC canonical path collisions and
  Windows file attributes. Read-only, hidden, system, temporary, device,
  compressed, offline, not-content-indexed, encrypted, integrity-stream,
  no-scrub-data, recall, pinned/unpinned, or reparse-point residue is
  forbidden. Dedicated hidden-attribute and read-only-attribute probes must be
  detected and cleaned before the final scan.
- On Windows, final tree scan enumerates NTFS alternate data streams on every
  retained file. Non-default streams or stream-enumeration errors are
  violations. A dedicated ADS probe writes and removes a hidden stream to prove
  the scanner catches this residue class.
- Final retained files must not keep hardlink aliases. A dedicated hardlink
  probe creates an outside alias for a runtime note, verifies that the final
  tree scanner catches the elevated link count, and removes both names before
  the final scan.
- Block pre-Guard writes, non-released answers, traversal paths, encoded paths,
  Unicode format-character filename tricks, non-ASCII separator tricks, raw/wiki
  prefixes, `.obsidian` config writes, Windows-invalid filename characters,
  malformed or literal percent escapes, URI fragment/query/parameter-looking
  suffixes, NTFS alternate-data-stream suffixes, case-insensitive duplicate
  targets, Windows device-name aliases including CONIN$/CONOUT$/CLOCK$ and
  COM/LPT superscript digits, Unicode path-separator / colon / percent
  confusables, symlink escapes, and formal Obsidian vault writes.
- Release paths must be exactly one file under `.vaks_runtime/released/` or
  `.vaks_runtime/fallback/`; nested release subdirectories and overlong names
  are rejected before filesystem writes. Internal release filenames must use a
  conservative ASCII allowlist: letters, digits, dot, underscore, and hyphen,
  ending in `.md`.
- Release file bodies are constrained to a safe plain-text Markdown subset.
  Runtime release/fallback bodies must not contain YAML/TOML frontmatter, raw
  excessive line counts, overlong single lines, excessive combining-mark runs,
  HTML, HTML comments, ASCII angle brackets, Markdown links/images,
  reference-style links, raw active URI schemes, generic URI schemes, Obsidian
  wiki links or transclusions, Obsidian comments, ASCII or Unicode tags,
  inline fields, property-like metadata lines including ASCII key/value lines,
  block IDs, footnotes, footnote references, reference-style link
  definitions, raw or decoded Unicode format / Bidi / zero-width characters,
  raw or decoded Unicode separator characters, raw or decoded control characters, multi-line
  bracket/link constructs, unclosed link-like constructs, spaced path-link forms, HTML angle confusables,
  visual homograph scripts, right-to-left scripts / Arabic-number bidi classes,
  variation selectors, combining marks, status/check/bullet-like symbols,
  visual separator lines, approval/status badges, system/Guard/VAKS/action-basis
  authority claims, compliance/legal/security release language, no-review /
  direct-execute language, combining-mark-obfuscated path/URI variants, domain-dot / path-slash / tag-marker confusables, path/URI
  confusables, HTML angle entities, NUL/control characters, bare `www.` links,
  bare domain autolink candidates including
  local/internal LAN domains, bare IPv4 / IPv6 / variant IP / localhost
  references, plain email autolink candidates, protocol-relative URLs, Windows
  drive paths, Windows environment-variable paths, UNC paths, backslash
  relative paths, Windows root-relative paths, POSIX / tilde / relative path
  strings, vault-relative paths wrapped in ASCII/CJK quote or bracket forms,
  vault-relative paths with fragment/query suffixes, vault-relative paths split
  with whitespace, whitespace/backslash-split
  or entity-encoded URI schemes, Obsidian
  callouts, encoded active syntax, fenced code blocks, or indented code blocks. Rich
  Marker, percent-encoding, and HTML-entity floods are rejected before expensive
  decode / regex scanning.
  render-only Markdown constructs that can hide, restyle, or structurally
  transform the final answer are also rejected, including inline math, math blocks / risky
  LaTeX commands, tables, headings, highlights, emphasis, inline backticks,
  horizontal rules including spaced variants, Setext heading underlines,
  strikethrough, definition lists, and abbreviation definitions. Interactive
  task-list checkboxes, including ordered-list parenthesis markers and
  Unicode/symbol checkbox forms, visual bullet glyph list markers, and callouts
  hidden behind list / quote prefixes are rejected. Leading-indented lines,
  nested list items, and indented list continuation blocks are rejected. Plain
  paragraphs and simple non-nested ordered/unordered lists remain allowed. The scanner
  checks raw, iteratively percent-decoded, HTML-entity-decoded, NFKC-normalized,
  and combined decoded variants before any filesystem write.
- A deterministic path-fuzz matrix must show that generated invalid paths never
  write and generated valid paths do write inside the disposable vault.
- Release file creation uses staged temp + no-clobber hardlink publish. A fault
  injected after staging must leave no target file, no staging temp, and no
  staging directory.
- If bundle generation itself fails after creating its output directory, the
  partial output directory, ZIP, and sidecar must be removed before returning
  the error.
- Concurrent writes to the same target must be one-winner only; pre-existing
  targets must not be overwritten; parallel writes to distinct valid targets
  must all succeed.
- The same collision rules must hold across local child processes, not only
  threads in one Python process.
- If an allowed release directory is swapped to a junction after path
  validation, the final write must fail closed and create no external file.
- If an allowed release directory is swapped to a junction immediately before
  hardlink publish, the final pre-link check must fail closed and create no
  external file.
- During the final check -> hardlink window, Windows runs must hold parent
  directory and directory-lock-file handles without delete sharing. A
  post-final-check directory swap attempt must be blocked before it can replace
  the release directory.
- Internal junction aliases such as `fallback -> released` must not be accepted:
  resolved-inside-vault is not enough when the policy path is semantically
  different from the real target directory.
- Directory lock files may be recreated when missing, but malformed lock entries
  such as directories, symlinks, or junctions must fail closed.
- Delete the disposable vault workspace before packaging and verify a workspace
  external junction target sentinel survives workspace cleanup before it is
  removed by the test harness.
- The review bundle must hash-manage every non-manifest artifact and the
  manifest must carry a canonical self-hash checked by self-test.
- `CONTRACT.md` and `LIMITS.md` must byte-match the canonical bounded text
  generated by this runner. A self-consistent hash update cannot append
  production-ready, formal-vault-write, or action-ready language to the
  human-readable boundary documents.
- Runner provenance must bind to the current local runner file. `runner_sha256`,
  `runner_provenance_sha256`, the managed provenance artifact hash, and the
  local `tools/vaks_disposable_vault_trial_r1_6.py` SHA256 must all match; a
  self-consistent forged provenance copy is not enough.
- Bundle verification must fail closed with structured results when core JSON
  artifacts are malformed or have the wrong top-level type. A corrupt
  `run_manifest.json` or `summary.json` must not crash the verifier or look
  like a tool failure.
- Core JSON artifacts must not contain duplicate object keys. Python's default
  parser keeps the last duplicate key, but other tools may interpret or report
  duplicates differently; duplicate keys are therefore rejected before schema
  checks.
- Managed JSON artifact files must also be UTF-8, LF-terminated, CR-free,
  duplicate-key-free JSON objects. Hash consistency alone must not allow
  malformed or ambiguous evidence JSON to remain in a review bundle.
- Managed JSONL ledger artifacts must be UTF-8, LF-terminated, CR-free, and
  line-delimited JSON objects parsed with the same duplicate-key rejection. A
  self-consistent hash update cannot hide malformed, non-object, or
  duplicate-key ledger rows.
- High-coverage detail ledgers are not allowed to self-classify their own
  safety or silently shrink coverage. Path adversarial rows must retain the
  fixed case matrix; path fuzz rows are replay-checked against the deterministic
  fuzz seed and formal/quick row counts; Markdown content rows are checked
  against canonical safe/unsafe case naming and exact case counts; disposable
  Obsidian shadow rows, atomic fault rows, swap rows, directory-lock rows, and
  thread/process collision rows are checked against fixed case matrices. A
  self-consistent metrics rewrite cannot wash or delete adversarial rows into
  positive coverage.
- Pre-Guard write-attempt rows must exist one-for-one with release results and
  retain the exact `pre-guard-N.md` path sequence plus fail-closed write state.
  A self-consistent metrics rewrite cannot replace the pre-Guard blocking
  ledger with a single harmless-looking row.
- Committed-release integrity rows must bind back to the release result rows
  that actually created files: same request ID, release path, and committed
  text HMAC. Count-only integrity ledgers are not sufficient.
- Integrity probe ledgers must retain their exact tamper case matrix. A
  self-consistent metrics rewrite cannot replace probe evidence with fake
  `detected: true` rows.
- Disposable vault structure and cleanup metadata must be internally bound:
  runtime-note and scanned-file counts are derived from release, Markdown,
  fuzz, and shadow ledgers; cleanup file counts must match the structure scan.
  Cleanup and structure ledgers are not free-form summary claims.
- Bundle verification must enforce a required/allowed artifact set. Mandatory
  evidence files, runner provenance, summary, metrics, workspace cleanup, and
  release/fault/fuzz result ledgers must be present; optional self-test
  artifacts are required when their summary status is `pass` or `fail`; managed
  extra artifacts fail closed even when their hashes and ZIP bytes are
  self-consistent.
- Formal closeout evidence must not be downgraded to a quick/partial evidence
  profile. A bundle whose directory name is the formal `run_id` must carry
  `evidence_profile: formal`, all four self-test statuses must be `pass`, and
  formal-scale coverage floors for request count, released writes, path fuzz,
  Markdown adversarial cases, and retained runtime-note revalidation must be
  met. Quick or partial evidence may still be generated for internal probes,
  but it cannot masquerade as formal closeout evidence.
- `summary.json` must pass a minimal schema gate: pass summaries must keep
  `hard_zero_pass` and `positive_gate_pass` true, all listed hard-zero metrics
  must be integer zero, optional self-test statuses must not be `fail`, the
  recommendation must remain bounded to the supervised low-risk trial wording,
  the required `not_proven` boundary list must not be weakened, and unknown
  top-level fields must fail closed so hidden overclaim fields cannot be added.
- Bundle verification must recompute `hard_zero_keys`, `hard_zero_pass`,
  `positive_gate_pass`, and `status` from the metrics ledger and self-test
  statuses. A summary cannot delete a required hard-zero metric, add a fake
  zero metric, or claim positive coverage when the underlying metrics do not
  satisfy the gate. Malformed metric values must fail closed as structured
  verification errors instead of crashing the verifier.
- `summary.metrics` and `quality_metrics.json` must be the same metrics ledger.
  A self-consistent package cannot make the summary prettier than the detailed
  quality metrics or make the detailed metrics disagree with the summary.
- `quality_metrics.json` must be recomputable from the managed detail ledgers
  and JSON evidence artifacts. Release-result, path-fuzz, integrity-probe,
  concurrency, process, cleanup, and vault-structure detail files cannot be
  self-consistently rewritten while leaving the summary metrics unchanged.
  `processed_case_count` must derive from `vault_release_results.jsonl`, and
  `released_candidate_count` must derive from released adapter-allowed rows; a
  summary cannot inflate sample scale or released-candidate coverage by self-report.
- Coverage-style, fault-injection, vault-shape, directory-lock, and concurrency
  detail ledgers must not fake breadth by repeating a small number of cases.
  Managed detail ledgers that use `case_id` for scenario identity require
  non-empty unique `case_id` values; a self-consistent metrics and hash update
  cannot turn duplicated rows into formal coverage evidence.
- Release result and write-attempt ledgers must be cross-checked. Every release
  result must have exactly one matching attempt by release path, matching HMAC,
  allowed / created state, and successful created writes must be covered by the
  committed-release integrity checked count.
- Release write attempts must also be internally coherent. An allowed / created
  attempt requires valid path, valid text, valid Markdown content, zero content
  errors, `commit_allowed_input: true`, the adapter-committed reason, the
  staged-temp hardlink strategy, no write error, a created staging temp, no
  leftover staging temp, and matching text/file HMACs. A self-consistent bundle
  cannot claim a successful write while its own attempt row says the path,
  content, commit input, reason, or atomic strategy was invalid.
- Release result rows must also be semantically valid. A released row requires
  `guard_status: pass`, a direct or qualified answer policy, adapter approval,
  successful vault write, and a true HMAC match. Guard block / error / timeout
  rows must remain withheld or review-only and must not write. Release-result
  rows must match the frozen R1.5 adapter result fingerprint for this bundle
  profile: request ID, release path, category, guard status, adapter decision,
  release state, answer policy, write state, text HMAC, and HMAC-match flag. A
  self-consistent bundle cannot fake coverage by repeating requests, replacing
  real request IDs with unique invented IDs, or turning withheld cases into
  released cases after the fact.
- `run_manifest.json` must also pass a minimal schema gate: critical fields
  have the expected primitive types, SHA256 fields are lowercase 64-character
  hex strings, artifact hashes are an object of safe relative paths to SHA256
  strings, sandbox boundary booleans keep their expected values, and unknown
  top-level fields fail closed. Schema drift or wrong-type fields fail closed
  instead of crashing verification.
- Manifest identity fields are bound to this runner and slice. `run_id`,
  `created_at`, and `tool` cannot be self-consistently rewritten to make the
  package look like a different run, different tool, or different release line.
- Bundle verification must enforce resource limits before reading core files:
  `run_manifest.json`, `summary.json`, the ZIP SHA256 sidecar, managed
  directory file count, per-file bytes, and total managed directory bytes.
  Oversized or over-count bundles fail closed without deep reads.
- The review bundle directory and ZIP creation must reject symlink / junction
  / reparse entries instead of following them into external content.
- The review bundle directory must also reject hardlinked files. An artifact
  path must own its own regular file content inside the bundle tree, not be a
  second directory entry for another filesystem object outside the bundle.
- Optional integrity-tamper self-test must prove that artifact, manifest, ZIP,
  sidecar, unsafe-entry, duplicate-entry, safe-extra-entry, missing-entry,
  global-comment, entry-comment, entry-extra, entry-timestamp,
  entry-compression, entry-attribute, directory/core-file/ZIP resource-limit
  violations, prefix-stub, trailing-junk, local-header-extra, link-entry, and
  unmanaged-file tampering are detected.
- Optional self-test artifacts must also pass semantic validation, not only hash
  validation. Empty `pass` files, missing required tamper scenarios, falsified
  append-only collisions, falsified reproducibility matches, and falsified
  failed-cleanup results fail closed even when the package hashes and ZIP are
  self-consistent.
- Optional append-only, failed-cleanup, reproducibility, and integrity-tamper
  artifacts must match locally recomputed self-test results for this runner.
  A self-consistent bundle cannot replace those artifacts with perfect-looking
  hand-written success reports.
- The ZIP SHA256 sidecar must be an exact single LF-terminated line:
  lowercase hex digest, two spaces, and the exact ZIP file name. Wrong file
  names, uppercase digests, missing newline, trailing whitespace, CRLF, and
  extra sidecar lines must fail verification.
- ZIP package metadata must be clean: no global comment, no per-entry comments,
  and no per-entry extra fields. ZIP entry metadata must also be canonical:
  fixed timestamp, deflated compression, fixed create-system, fixed external /
  internal attributes, and fixed flag bits.
- The ZIP file must byte-match a freshly regenerated canonical ZIP from the
  managed output directory, so prefix stubs, trailing bytes, local-header-only
  data, and other unmodeled ZIP byte drift fail closed.
- ZIP verification must enforce resource limits before decompression: maximum
  compressed package bytes, entry count, per-entry uncompressed bytes, total
  uncompressed bytes, and per-entry compression ratio. Violations fail closed
  and skip deep entry reads / testzip-style decompression.
- Optional reproducibility self-test must show two independent quick bundles
  produce identical path-independent evidence artifacts, and the comparison
  matrix must retain the full fixed artifact list. A self-consistent package
  cannot shrink reproducibility evidence to only a few easy core files or fill
  the complete matrix with forged equal digests; the artifact must match a
  locally recomputed reproducibility matrix for this runner.
- Optional append-only self-test must reject reruns when only the output
  directory, only the ZIP, or only the ZIP SHA256 sidecar already exists.
- Optional failed-bundle-cleanup self-test must inject an early run failure and
  prove no partial directory, ZIP, or sidecar remains.

It does not write to the real Obsidian vault, raw sources, wiki notes, Truth
Core, production runtime, service endpoints, databases, network, LLMs, or live
retrieval. On Windows, the junction escape fixture uses a local WinAPI reparse
point helper inside the disposable workspace; its use is recorded in metrics.
The junction target is outside the disposable vault/workspace but still inside
the sandbox output tree, so cleanup-follow bugs are detectable without touching
the real vault.
