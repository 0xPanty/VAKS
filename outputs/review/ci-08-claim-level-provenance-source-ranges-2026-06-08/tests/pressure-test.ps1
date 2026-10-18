param(
  [string]$Root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
)

$ErrorActionPreference = 'Stop'

$checks = New-Object System.Collections.Generic.List[object]

function Add-Check {
  param(
    [string]$Name,
    [bool]$Ok,
    [string]$Detail
  )
  $script:checks.Add([pscustomobject]@{
    name = $Name
    ok = $Ok
    detail = $Detail
  })
}

function Read-Text {
  param([string]$Path)
  return Get-Content -LiteralPath $Path -Raw
}

function Assert-Contains {
  param([string]$Name, [string]$Text, [string]$Needle)
  Add-Check $Name ($Text.Contains($Needle)) $Needle
}

function Assert-NotContains {
  param([string]$Name, [string]$Text, [string]$Needle)
  Add-Check $Name (-not $Text.Contains($Needle)) $Needle
}

$sandbox = Resolve-Path (Join-Path $PSScriptRoot '..')
$repo = Resolve-Path (Join-Path $sandbox '..\..\..')
$architecture = Join-Path $sandbox 'architecture'
$patternPath = Join-Path $architecture 'wiki\patterns\claim-level-provenance-source-ranges.md'
$schemaPath = Join-Path $architecture 'SCHEMA.md'
$claimTemplatePath = Join-Path $architecture 'templates\claim-record.md'
$indexPath = Join-Path $architecture 'wiki\indexes\knowledge-graph-index.md'
$fixtureDir = Join-Path $sandbox 'tests\fixtures\claim-provenance'

$pattern = Read-Text $patternPath
$schema = Read-Text $schemaPath
$claimTemplate = Read-Text $claimTemplatePath
$index = Read-Text $indexPath

$evidenceFiles = @(
  'claim-citation-parser-anchor-snapshot.md',
  'citation-lint-anchor-snapshot.md',
  'citation-render-and-context-anchor-snapshot.md'
)

foreach ($fileName in $evidenceFiles) {
  $path = Join-Path $sandbox ("evidence\llm-wiki-compiler\" + $fileName)
  Add-Check "evidence exists: $fileName" (Test-Path -LiteralPath $path) $path
}

foreach ($needle in @(
  'src/utils/markdown.ts:18-25',
  'src/utils/markdown.ts:117-190',
  'src/utils/markdown.ts:195-230',
  'src/linter/rules.ts:348-446',
  'src/linter/rules.ts:450-536',
  'src/linter/rules.ts:556-584',
  'src/viewer/citation-rule.ts:1-16',
  'src/viewer/citation-rule.ts:88-115',
  'src/viewer/citation-rule.ts:162-190',
  'src/context/provenance.ts:67-91',
  'src/context/provenance.ts:116-149',
  'src/context/provenance.ts:170-198',
  'src/context/provenance.ts:222-246'
)) {
  Assert-Contains "pattern records anchor: $needle" $pattern $needle
}

Assert-Contains 'pattern sandbox status' $pattern 'status: sandbox-candidate'
Assert-Contains 'pattern has VAKS boundary' $pattern '## VAKS Boundary'
Assert-Contains 'pattern blocks truth confidence' $pattern 'truth confidence'
Assert-Contains 'pattern blocks verification status' $pattern 'verification status'
Assert-Contains 'pattern blocks reviewed relation' $pattern 'reviewed relation'
Assert-Contains 'pattern blocks action readiness' $pattern 'action readiness'
Assert-Contains 'pattern requires target claim' $pattern 'target_claim'
Assert-Contains 'pattern requires span support judgment' $pattern 'span_supports_target'
Assert-Contains 'pattern requires evidence role' $pattern 'evidence_role'
Assert-Contains 'pattern requires warrant' $pattern 'warrant'
Assert-Contains 'pattern requires scope' $pattern 'scope'
Assert-Contains 'pattern blocks URL-only' $pattern 'URL-only reference as support'
Assert-Contains 'pattern blocks summary-only' $pattern 'summary-only reference as support'
Assert-Contains 'pattern blocks background context' $pattern '`background_context` as support'
Assert-Contains 'pattern blocks malformed range' $pattern 'malformed, missing-source, or out-of-bounds source range as support'
Assert-NotContains 'pattern does not allow range as truth' $pattern 'source_range_as_truth'
Assert-NotContains 'pattern does not allow range as support shortcut' $pattern 'range_as_support_without_warrant'

Assert-Contains 'claim template has CI-08 boundary' $claimTemplate 'CI-08 Source Range Boundary'
Assert-Contains 'claim template examples colon' $claimTemplate 'file.md:42-58'
Assert-Contains 'claim template examples hash lines' $claimTemplate 'file.md#L42-L58'
Assert-Contains 'claim template says provenance until check' $claimTemplate 'is provenance until the target-specific support check is filled'
Assert-Contains 'claim template blocks range without warrant' $claimTemplate 'range-without-warrant cannot support'

Assert-Contains 'schema has CI-08 sandbox rule' $schema 'CI-08 sandbox rule'
Assert-Contains 'schema has source-range-only provenance rule' $schema 'Source-range-only reference is provenance, not evidence support'
Assert-Contains 'schema keeps URL-only provenance rule' $schema 'URL-only source reference 是 provenance'
Assert-Contains 'schema keeps evidence support no confidence mutation' $schema 'evidence support 不自动改变 confidence'

Assert-Contains 'index records CI-08 sandbox line' $index 'CI-08 [[claim-level-provenance-source-ranges]]'
Assert-Contains 'index records citation parser lint viewer-context' $index 'citation parser / lint / viewer-context anchors'
Assert-Contains 'index blocks source range as truth' $index 'source range 本身不是 evidence support'

$fixtureExpectations = @{
  'pass-direct-source-range-support.md' = @('expected: PASS', 'target_claim:', 'source_range:', 'span_supports_target: supported', 'evidence_role: direct_support', 'warrant:', 'scope:')
  'pass-counterexample-range.md' = @('expected: PASS', 'evidence_role: counterexample', 'challenge_refs or risk_refs')
  'block-url-only-support.md' = @('expected: BLOCK', 'source_access: url_only')
  'block-summary-only-support.md' = @('expected: BLOCK', 'source_access: summary_only')
  'block-background-context-support.md' = @('expected: BLOCK', 'evidence_role: background_context')
  'block-range-without-target.md' = @('expected: BLOCK', 'target_claim:')
  'block-range-without-warrant.md' = @('expected: BLOCK', 'warrant:', 'scope:')
  'block-malformed-citation.md' = @('expected: BLOCK', 'src/utils/markdown.ts:0-5')
  'block-out-of-bounds-citation.md' = @('expected: BLOCK', 'src/utils/markdown.ts:999-1000')
  'block-missing-source.md' = @('expected: BLOCK', 'src/missing/file.ts:1-5')
  'block-range-as-truth-confidence.md' = @('expected: BLOCK', 'truth_confidence: high', 'verification_status: cross-checked')
}

foreach ($entry in $fixtureExpectations.GetEnumerator()) {
  $path = Join-Path $fixtureDir $entry.Key
  Add-Check "fixture exists: $($entry.Key)" (Test-Path -LiteralPath $path) $path
  if (Test-Path -LiteralPath $path) {
    $text = Read-Text $path
    foreach ($needle in $entry.Value) {
      Assert-Contains "fixture $($entry.Key) contains $needle" $text $needle
    }
  }
}

$compatPaths = @{
  'CI-02 review queue exists' = 'REVIEW_QUEUE.md'
  'CI-02.5 candidate lint template exists' = 'templates\review-candidate.md'
  'CI-03 source hash pattern exists' = 'wiki\patterns\source-hash-registry-and-idempotent-ingest.md'
  'CI-04 decision outcome pattern exists' = 'wiki\patterns\decision-outcome-precondition-before-calibration.md'
  'CI-05 scope dashboard pattern exists' = 'wiki\patterns\scope-dashboard-live-context-surface.md'
  'CI-06 context pack pattern exists' = 'wiki\patterns\context-pack-evidence-envelope.md'
}

foreach ($entry in $compatPaths.GetEnumerator()) {
  Add-Check $entry.Key (Test-Path -LiteralPath (Join-Path $architecture $entry.Value)) $entry.Value
}

$rootPattern = Read-Text (Join-Path $repo 'wiki\patterns\claim-level-provenance-source-ranges.md')
$rootClaimTemplate = Read-Text (Join-Path $repo 'templates\claim-record.md')
$rootSchema = Read-Text (Join-Path $repo 'SCHEMA.md')
$rootIndex = Read-Text (Join-Path $repo 'wiki\indexes\knowledge-graph-index.md')

Assert-NotContains 'root pattern not sandbox-mutated' $rootPattern 'status: sandbox-candidate'
Assert-NotContains 'root claim template not sandbox-mutated' $rootClaimTemplate 'CI-08 Source Range Boundary'
Assert-NotContains 'root schema not sandbox-mutated' $rootSchema 'CI-08 sandbox rule'
Assert-NotContains 'root index not sandbox-mutated' $rootIndex 'CI-08 [[claim-level-provenance-source-ranges]]'

$failed = $checks | Where-Object { -not $_.ok }
$passedCount = ($checks | Where-Object { $_.ok }).Count
$failedCount = $failed.Count

foreach ($checkItem in $checks) {
  $status = if ($checkItem.ok) { 'PASS' } else { 'FAIL' }
  Write-Host ("[$status] " + $checkItem.name + " :: " + $checkItem.detail)
}

Write-Host ("TOTAL passed=$passedCount failed=$failedCount")

if ($failedCount -gt 0) {
  exit 1
}
