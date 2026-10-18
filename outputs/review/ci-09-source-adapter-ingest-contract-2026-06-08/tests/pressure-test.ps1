param(
  [string]$Root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
)

$ErrorActionPreference = 'Stop'
$checks = New-Object System.Collections.Generic.List[object]

function Add-Check {
  param([string]$Name, [bool]$Ok, [string]$Detail)
  $script:checks.Add([pscustomobject]@{ name = $Name; ok = $Ok; detail = $Detail })
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
$patternPath = Join-Path $architecture 'wiki\patterns\source-adapter-ingest-contract.md'
$sourceIntakePath = Join-Path $architecture 'SOURCE_INTAKE.md'
$sourceTemplatePath = Join-Path $architecture 'templates\source-record.md'
$indexPath = Join-Path $architecture 'wiki\indexes\knowledge-graph-index.md'
$fixtureDir = Join-Path $sandbox 'tests\fixtures\source-adapter'

$pattern = Read-Text $patternPath
$sourceIntake = Read-Text $sourceIntakePath
$sourceTemplate = Read-Text $sourceTemplatePath
$index = Read-Text $indexPath

foreach ($fileName in @(
  'source-adapter-core-anchor-snapshot.md',
  'source-adapter-types-anchor-snapshot.md',
  'source-writer-session-anchor-snapshot.md'
)) {
  $path = Join-Path $sandbox ("evidence\llm-wiki-compiler\" + $fileName)
  Add-Check "evidence exists: $fileName" (Test-Path -LiteralPath $path) $path
}

foreach ($needle in @(
  'src/ingest/shared.ts:11-15',
  'src/ingest/shared.ts:140-176',
  'src/commands/ingest.ts:190-205',
  'src/commands/ingest.ts:207-229',
  'src/commands/ingest.ts:231-275',
  'src/ingest/web.ts:14-63',
  'src/ingest/pdf.ts:18-57',
  'src/ingest/file.ts:12-40',
  'src/ingest/image.ts:82-114',
  'src/ingest/transcript.ts:58-73',
  'src/ingest/transcript.ts:141-156',
  'src/utils/source-writer.ts:1-95',
  'src/adapters/types.ts:19-52',
  'src/commands/ingest-session.ts:27-54',
  'src/commands/ingest-session.ts:95-133'
)) {
  Assert-Contains "pattern records anchor: $needle" $pattern $needle
}

Assert-Contains 'pattern sandbox status' $pattern 'status: sandbox-candidate'
Assert-Contains 'pattern has VAKS boundary' $pattern '## VAKS Boundary'
Assert-Contains 'pattern allows source record' $pattern 'source record'
Assert-Contains 'pattern allows raw artifact' $pattern 'raw source artifact'
Assert-Contains 'pattern allows candidate extraction' $pattern 'candidate extraction input'
Assert-Contains 'pattern blocks reviewed claim' $pattern 'reviewed claim'
Assert-Contains 'pattern blocks truth confidence' $pattern 'truth confidence'
Assert-Contains 'pattern blocks verification upgrade' $pattern 'verification status upgrade'
Assert-Contains 'pattern blocks reviewed relation' $pattern 'reviewed relation'
Assert-Contains 'pattern blocks action basis' $pattern 'action basis'
Assert-Contains 'pattern keeps contract light' $pattern 'The contract must stay light'
Assert-Contains 'pattern has required adapter block' $pattern 'adapter_status: ok | partial | failed | blocked'
Assert-Contains 'pattern has source boundary' $pattern 'source_boundary:'
Assert-Contains 'pattern blocks bulk old-record rewrite' $pattern 'v0.2 不批量改旧 source records'

Assert-Contains 'SOURCE_INTAKE has CI-09 rule' $sourceIntake 'CI-09 sandbox rule'
Assert-Contains 'SOURCE_INTAKE blocks reviewed claims' $sourceIntake 'reviewed claims'
Assert-Contains 'SOURCE_INTAKE has adapter status' $sourceIntake 'adapter_status: ok | partial | failed | blocked'
Assert-Contains 'source template has adapter boundary' $sourceTemplate '## Adapter Ingest Boundary'
Assert-Contains 'source template says manual may omit' $sourceTemplate 'Manual source cards may omit it'
Assert-Contains 'source template blocks promotion approval' $sourceTemplate 'promotion approval'
Assert-Contains 'source template blocks project adoption' $sourceTemplate 'project adoption verdicts'
Assert-Contains 'index records CI-09' $index 'CI-09 [[source-adapter-ingest-contract]]'
Assert-Contains 'index records lightweight contract' $index 'lightweight source adapter contract'
Assert-Contains 'index blocks action basis' $index 'action basis'

$fixtureExpectations = @{
  'pass-web-source-record.md' = @('expected: PASS', 'adapter_status: ok', 'knowledge_status: raw', 'action_basis_allowed: false')
  'pass-partial-pdf-source-record.md' = @('expected: PASS', 'adapter_status: partial', 'truncated: true', 'known_gaps:')
  'pass-session-source-record.md' = @('expected: PASS', 'source_type: session', 'participant_identity')
  'block-adapter-as-reviewed-claim.md' = @('expected: BLOCK', 'reviewed_claim:', 'truth_confidence: high')
  'block-adapter-reviewed-relation.md' = @('expected: BLOCK', 'relation_state: reviewed')
  'block-adapter-action-basis.md' = @('expected: BLOCK', 'action_basis_allowed: true')
  'block-empty-content-success.md' = @('expected: BLOCK', 'content: ""')
  'block-silent-title-collision.md' = @('expected: BLOCK', 'collision_handling: silent_overwrite')
  'block-zero-success-batch.md' = @('expected: BLOCK', 'imported: 0')
  'block-heavy-schema-required-for-light-source.md' = @('expected: BLOCK', 'full_prov_ontology: true')
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
  'CI-08 source range pattern exists' = 'wiki\patterns\claim-level-provenance-source-ranges.md'
}

foreach ($entry in $compatPaths.GetEnumerator()) {
  Add-Check $entry.Key (Test-Path -LiteralPath (Join-Path $architecture $entry.Value)) $entry.Value
}

$rootPattern = Read-Text (Join-Path $repo 'wiki\patterns\source-adapter-ingest-contract.md')
$rootSourceIntake = Read-Text (Join-Path $repo 'SOURCE_INTAKE.md')
$rootSourceTemplate = Read-Text (Join-Path $repo 'templates\source-record.md')
$rootIndex = Read-Text (Join-Path $repo 'wiki\indexes\knowledge-graph-index.md')

Assert-NotContains 'root pattern not sandbox-mutated' $rootPattern 'status: sandbox-candidate'
Assert-NotContains 'root SOURCE_INTAKE not sandbox-mutated' $rootSourceIntake 'CI-09 sandbox rule'
Assert-NotContains 'root source template not sandbox-mutated' $rootSourceTemplate '## Adapter Ingest Boundary'
Assert-NotContains 'root index not sandbox-mutated' $rootIndex 'CI-09 [[source-adapter-ingest-contract]]'

Assert-NotContains 'pattern does not allow adapter truth shortcut' $pattern 'adapter_truth_confidence'
Assert-NotContains 'pattern does not allow adapter reviewed relation shortcut' $pattern 'adapter_reviewed_relation'
Assert-NotContains 'pattern does not allow adapter action shortcut' $pattern 'adapter_action_basis_ready'

$failed = @($checks | Where-Object { -not $_.ok })
$passedCount = @($checks | Where-Object { $_.ok }).Count
$failedCount = @($failed).Count

foreach ($checkItem in $checks) {
  $status = if ($checkItem.ok) { 'PASS' } else { 'FAIL' }
  Write-Host ("[$status] " + $checkItem.name + " :: " + $checkItem.detail)
}

Write-Host ("TOTAL passed=$passedCount failed=$failedCount")

if ($failedCount -gt 0) {
  exit 1
}
