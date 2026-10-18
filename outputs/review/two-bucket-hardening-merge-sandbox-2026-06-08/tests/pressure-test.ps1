$ErrorActionPreference = "Stop"

$Root = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
$Arch = Join-Path $Root "architecture"
$SchemaLocked = Join-Path $Arch "SCHEMA.md"
$SchemaBaseline = Join-Path $Root "tests/fixtures/SCHEMA.locked.baseline.md"
$SchemaUnlocked = Join-Path $Root "schema-unlocked-candidate/SCHEMA.md"

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

function Hash-File($Path) {
  return (Get-FileHash -Algorithm SHA256 -LiteralPath $Path).Hash
}

function Has($Path, $Pattern) {
  return [regex]::IsMatch((Read-Text $Path), $Pattern, "IgnoreCase, Multiline")
}

function NotHasNear($Path, $Anchor, $Forbidden) {
  $txt = Read-Text $Path
  $idx = $txt.IndexOf($Anchor)
  if ($idx -lt 0) { return $false }
  $len = [Math]::Min(900, $txt.Length - $idx)
  $slice = $txt.Substring($idx, $len)
  return -not [regex]::IsMatch($slice, $Forbidden, "IgnoreCase")
}

$reviewQueue = Join-Path $Arch "REVIEW_QUEUE.md"
$reviewTemplate = Join-Path $Arch "templates/review-candidate.md"
$sourceIntake = Join-Path $Arch "SOURCE_INTAKE.md"
$sourceTemplate = Join-Path $Arch "templates/source-record.md"
$feedback = Join-Path $Arch "FEEDBACK.md"
$decisionTemplate = Join-Path $Arch "templates/decision-record.md"
$devContext = Join-Path $Arch "DEV_CONTEXT.md"
$devTemplate = Join-Path $Arch "templates/dev-context-pack.md"

Add-Result "SCHEMA locked architecture unchanged" ((Hash-File $SchemaLocked) -eq (Hash-File $SchemaBaseline)) "architecture/SCHEMA.md equals baseline"
Add-Result "Schema-unlocked candidate exists" (Test-Path $SchemaUnlocked) "separate review candidate only"
Add-Result "Schema-unlocked candidate has source-range line" (Has $SchemaUnlocked "Source ranges, line ranges, quote selectors")
Add-Result "Schema-unlocked candidate has envelope line" (Has $SchemaUnlocked "primary, neighbors, warnings, gaps, and suggested actions")
Add-Result "Schema-unlocked candidate has budget line" (Has $SchemaUnlocked "Budget trimming may reduce context size")

Add-Result "CI-02.5 queue lint block present" (Has $reviewQueue "candidate_lint:[\s\S]*schema_violations:[\s\S]*provenance_violations")
Add-Result "CI-02.5 template lint block present" (Has $reviewTemplate "candidate_lint:[\s\S]*lint_status")
Add-Result "CI-02.5 lint not verdict" (Has $reviewQueue "review input, not[\s\S]*rejection verdict")
Add-Result "CI-02.5 lint does not auto-promote near block" (NotHasNear $reviewQueue "Candidate lint before approval" "automatic promotion decision: true|auto[_ -]?promote")

Add-Result "CI-03 source hash fields present" (Has $sourceIntake "source_hash:[\s\S]*snapshot_hash:[\s\S]*ingest_state")
Add-Result "CI-03 hash hygiene boundary present" (Has $sourceIntake "Hashes and adapter records are source hygiene")
Add-Result "CI-03 template source integrity present" (Has $sourceTemplate "source_integrity:[\s\S]*source_hash")
Add-Result "CI-03 hash does not decide truth" (Has $sourceIntake "They do not decide truth")

Add-Result "CI-09 adapter fields present" (Has $sourceIntake "adapter_ingest:[\s\S]*adapter_name:[\s\S]*capture_method:[\s\S]*known_limits")
Add-Result "CI-09 source template adapter fields present" (Has $sourceTemplate "adapter_ingest:[\s\S]*extraction_trace")
Add-Result "CI-09 adapter no action readiness" (Has $sourceTemplate "do not create evidence support, verification status, or action\s+readiness")

Add-Result "CI-04 feedback precondition present" (Has $feedback "recommendation and user choice, or explicit user override")
Add-Result "CI-04 confidence rationale note present" (Has $feedback "confidence_at_decision, rationale, and outcome_note")
Add-Result "CI-04 decision template override present" (Has $decisionTemplate "explicit_user_override: false")
Add-Result "CI-04 decision template rationale present" (Has $decisionTemplate "rationale:")
Add-Result "CI-04 outcome cannot mutate truth" (Has $decisionTemplate "must not change truth_confidence, verification_status, or\s+source_reliability")

Add-Result "CI-06 DEV_CONTEXT envelope present" (Has $devContext "primary\s+neighbors\s+warnings\s+gaps\s+suggested_actions")
Add-Result "CI-06 dev template envelope present" (Has $devTemplate "context_pack_envelope:[\s\S]*primary:[\s\S]*neighbors:[\s\S]*warnings:[\s\S]*gaps:[\s\S]*suggested_actions")
Add-Result "CI-06 envelope not truth" (Has $devTemplate "cannot create truth")

Add-Result "CI-07 budget guardrails present" (Has $devTemplate "budget_guardrails:[\s\S]*trimmed_key_support:[\s\S]*hidden_warnings_or_gaps")
Add-Result "CI-07 budget cannot hide risk" (Has $devContext "must not hide critical warnings")
Add-Result "CI-07 trimmed support blocks action-ready" (Has $devContext "key support is\s+trimmed out, the pack cannot remain action-ready")

Add-Result "CI-08 source range handle in template" (Has $reviewTemplate "Source range / line range / quote selector is a provenance handle")
Add-Result "CI-08 evidence support still required" (Has $reviewTemplate "support only after evidence_support checks")
Add-Result "CI-08 source range not support by itself" (Has $reviewTemplate "not\s+support by themselves")

Add-Result "Decision PASS fixture has required fields" (Has (Join-Path $Root "tests/fixtures/pass-decision-outcome-with-choice.yml") "recommendation:[\s\S]*user_choice:[\s\S]*rationale:[\s\S]*outcome_note")
Add-Result "Decision BLOCK fixture missing user choice" (-not (Has (Join-Path $Root "tests/fixtures/block-decision-outcome-without-choice.yml") "user_choice|explicit_user_override:\s*true"))

$firstBucketFiles = @($reviewQueue, $reviewTemplate, $sourceIntake, $sourceTemplate, $feedback, $decisionTemplate)
foreach ($file in $firstBucketFiles) {
  Add-Result "First-bucket file exists: $(Split-Path -Leaf $file)" (Test-Path $file)
}

$forbiddenRuntime = "new sqlite|dashboard truth|mcp write|auto-promote|scheduled agent|background rewrite"
Add-Result "No forbidden runtime near lint block" (NotHasNear $reviewQueue "Candidate lint before approval" $forbiddenRuntime)
Add-Result "No forbidden runtime near ingest block" (NotHasNear $sourceIntake "Minimal ingest hardening" $forbiddenRuntime)
Add-Result "No forbidden runtime near outcome block" (NotHasNear $feedback "MVP rule:" $forbiddenRuntime)
Add-Result "No forbidden runtime near envelope block" (NotHasNear $devContext "For important or agent-facing packs" $forbiddenRuntime)
Add-Result "No forbidden runtime near dev template envelope" (NotHasNear $devTemplate "Envelope and budget fields" $forbiddenRuntime)

$out = @()
$out += "Two-bucket hardening sandbox pressure test"
$out += "Root: $Root"
$out += "Pass: $script:Pass"
$out += "Fail: $script:Fail"
$out += ""
$out += $script:Rows
$out -join "`r`n" | Set-Content -LiteralPath (Join-Path $Root "tests/pressure-test-results.txt") -Encoding UTF8

Write-Output "Pass: $script:Pass"
Write-Output "Fail: $script:Fail"
$script:Rows | ForEach-Object { Write-Output $_ }

if ($script:Fail -gt 0) {
  exit 1
}
