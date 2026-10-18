$ErrorActionPreference = "Stop"

$script:Pass = 0
$script:Fail = 0
$script:Rows = New-Object System.Collections.Generic.List[string]

function Add-Result($Name, [bool]$Ok, $Detail = "") {
  if ($Ok) {
    $script:Pass++
    $script:Rows.Add("PASS`t$Name`t$Detail")
  } else {
    $script:Fail++
    $script:Rows.Add("FAIL`t$Name`t$Detail")
  }
}

function Read-Text($Path) {
  return Get-Content -LiteralPath $Path -Raw
}

function Has($Path, $Pattern) {
  return [regex]::IsMatch((Read-Text $Path), $Pattern, "IgnoreCase, Multiline")
}

$sourceIntake = "SOURCE_INTAKE.md"
$sourceTemplate = "templates/source-record.md"
$reviewQueue = "REVIEW_QUEUE.md"
$reviewTemplate = "templates/review-candidate.md"
$feedback = "FEEDBACK.md"
$decisionTemplate = "templates/decision-record.md"
$devContext = "DEV_CONTEXT.md"
$devTemplate = "templates/dev-context-pack.md"
$schema = "SCHEMA.md"

Add-Result "CI-03 SOURCE_INTAKE source_integrity" (Has $sourceIntake "source_integrity:[\s\S]*source_hash:[\s\S]*snapshot_hash:[\s\S]*ingest_state: new \| changed \| unchanged \| deleted \| unknown")
Add-Result "CI-03 source hash is hygiene only" (Has $sourceIntake "source hygiene only[\s\S]*do not decide truth")
Add-Result "CI-03 source template source_integrity" (Has $sourceTemplate "source_integrity:[\s\S]*source_hash:[\s\S]*snapshot_hash:[\s\S]*ingest_state: unknown")

Add-Result "CI-09 SOURCE_INTAKE adapter_ingest" (Has $sourceIntake "adapter_ingest:[\s\S]*adapter_name:[\s\S]*adapter_version:[\s\S]*capture_method:[\s\S]*extraction_trace:[\s\S]*known_limits")
Add-Result "CI-09 adapter blocks reviewed writeback" (Has $sourceIntake "must not directly create reviewed wiki nodes")
Add-Result "CI-09 source template adapter_ingest" (Has $sourceTemplate "adapter_ingest:[\s\S]*adapter_name:[\s\S]*extraction_trace")

Add-Result "CI-02.5 REVIEW_QUEUE candidate_lint" (Has $reviewQueue "candidate_lint:[\s\S]*schema_violations:[\s\S]*provenance_violations")
Add-Result "CI-02.5 lint is review input" (Has $reviewQueue "Candidate lint records[\s\S]*review input")
Add-Result "CI-02.5 template candidate_lint" (Has $reviewTemplate "candidate_lint:[\s\S]*lint_status")

Add-Result "CI-04 feedback precondition" (Has $feedback "recommendation and user choice, or explicit user override")
Add-Result "CI-04 feedback requires rationale/outcome_note" (Has $feedback "confidence_at_decision, rationale, and outcome_note")
Add-Result "CI-04 decision template explicit override" (Has $decisionTemplate "explicit_user_override: false")
Add-Result "CI-04 outcome cannot mutate truth" (Has $decisionTemplate "must not change truth_confidence, verification_status, or\s+source_reliability")

Add-Result "CI-06 DEV_CONTEXT envelope" (Has $devContext "primary\s+neighbors\s+warnings\s+gaps\s+suggested_actions")
Add-Result "CI-06 dev template envelope" (Has $devTemplate "context_pack_envelope:[\s\S]*primary:[\s\S]*neighbors:[\s\S]*warnings:[\s\S]*gaps:[\s\S]*suggested_actions")
Add-Result "CI-06 envelope not truth/action" (Has $devTemplate "cannot create truth,[\s\S]*action readiness")

Add-Result "CI-07 DEV_CONTEXT budget guardrail" (Has $devContext "must not hide critical warnings,[\s\S]*source-window loss")
Add-Result "CI-07 dev template budget guardrails" (Has $devTemplate "budget_guardrails:[\s\S]*trimmed_key_support:[\s\S]*hidden_warnings_or_gaps:[\s\S]*source_window_loss")
Add-Result "CI-07 SCHEMA budget boundary" (Has $schema "Budget trimming may reduce context size[\s\S]*cannot remain action-ready")

Add-Result "CI-08 review template source range handle" (Has $reviewTemplate "Source range / line range / quote selector is a provenance handle")
Add-Result "CI-08 review template evidence_support required" (Has $reviewTemplate "support only after evidence_support checks")
Add-Result "CI-08 SCHEMA source range boundary" (Has $schema "Source ranges, line ranges, quote selectors[\s\S]*only become support when .*evidence_support.* checks")

$schemaDiff = git diff -- SCHEMA.md | Out-String
$schemaAdded = @($schemaDiff -split "`n" | Where-Object { $_ -match '^\+[^+]' })
Add-Result "SCHEMA added exactly two boundary lines" ($schemaAdded.Count -eq 2) ($schemaAdded -join " | ")
Add-Result "SCHEMA has no CI-06 field enum" (-not ($schemaDiff -match "primary, neighbors, warnings, gaps, and suggested actions|suggested_actions|context_pack_envelope"))
Add-Result "SCHEMA diff has no runtime/API/MCP/dashboard" (-not ($schemaDiff -match "(?i)runtime|\bAPI\b|MCP|dashboard|SQLite|auto[- ]?promotion|background rewrite"))

$newBlocks = @(
  (Read-Text $sourceIntake),
  (Read-Text $sourceTemplate),
  (Read-Text $reviewTemplate),
  (Read-Text $feedback),
  (Read-Text $decisionTemplate),
  (Read-Text $devContext),
  (Read-Text $devTemplate),
  $schemaAdded
) -join "`n"
Add-Result "New hardening blocks have no SQLite/dashboard/API runtime additions" (-not ($newBlocks -match "(?i)new sqlite|dashboard truth|MCP write|auto[- ]?promote|scheduled agent|background rewrite"))

$head = git rev-parse --short HEAD
Add-Result "HEAD remains expected commit" ($head -eq "4abb84a") $head

$out = @()
$out += "Two-bucket hardening mainline merge check"
$out += "Pass: $script:Pass"
$out += "Fail: $script:Fail"
$out += ""
$out += $script:Rows
$out -join "`r`n" | Set-Content -LiteralPath "outputs/review/two-bucket-hardening-merge-sandbox-2026-06-08/mainline-merge-check-results.txt" -Encoding UTF8

Write-Output "Pass: $script:Pass"
Write-Output "Fail: $script:Fail"
$script:Rows | ForEach-Object { Write-Output $_ }

if ($script:Fail -gt 0) {
  exit 1
}
