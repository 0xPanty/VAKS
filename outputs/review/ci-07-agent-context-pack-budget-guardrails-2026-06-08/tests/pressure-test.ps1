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
$patternPath = Join-Path $architecture 'wiki\patterns\agent-context-pack-budget-guardrails.md'
$schemaPath = Join-Path $architecture 'SCHEMA.md'
$devTemplatePath = Join-Path $architecture 'templates\dev-context-pack.md'
$indexPath = Join-Path $architecture 'wiki\indexes\knowledge-graph-index.md'
$fixtureDir = Join-Path $sandbox 'tests\fixtures\context-budget'

$pattern = Read-Text $patternPath
$schema = Read-Text $schemaPath
$devTemplate = Read-Text $devTemplatePath
$index = Read-Text $indexPath

foreach ($fileName in @(
  'context-budget-anchor-snapshot.md',
  'source-window-budget-anchor-snapshot.md',
  'retrieval-warning-anchor-snapshot.md'
)) {
  $path = Join-Path $sandbox ("evidence\llm-wiki-compiler\" + $fileName)
  Add-Check "evidence exists: $fileName" (Test-Path -LiteralPath $path) $path
}

foreach ($needle in @(
  'src/context/budget.ts:1-24',
  'src/context/budget.ts:31-43',
  'src/context/budget.ts:56-69',
  'src/context/budget.ts:77-103',
  'src/context/budget.ts:116-173',
  'src/context/build.ts:449-505',
  'src/context/provenance.ts:101-137',
  'src/context/provenance.ts:139-149',
  'src/context/provenance.ts:152-198',
  'src/context/provenance.ts:222-246',
  'src/context/build.ts:513-565',
  'src/context/retrieval.ts:38-70',
  'src/context/retrieval.ts:72-108',
  'src/context/retrieval.ts:115-147',
  'src/context/retrieval.ts:149-175',
  'src/context/types.ts:44-55',
  'src/context/types.ts:150-161'
)) {
  Assert-Contains "pattern records anchor: $needle" $pattern $needle
}

Assert-Contains 'pattern sandbox status' $pattern 'status: sandbox-candidate'
Assert-Contains 'pattern has VAKS boundary' $pattern '## VAKS Boundary'
Assert-Contains 'pattern preserves warnings' $pattern 'warnings'
Assert-Contains 'pattern preserves gaps' $pattern 'gaps'
Assert-Contains 'pattern blocks action-ready when support trimmed' $pattern 'cannot be marked action-ready'
Assert-Contains 'pattern has trim order' $pattern 'neighbors'
Assert-Contains 'pattern has sourceWindows trim section' $pattern 'sourceWindows'
Assert-Contains 'pattern has chunks trim section' $pattern 'chunks'
Assert-Contains 'pattern has primary trim section' $pattern 'primary'
Assert-Contains 'pattern says fields are warnings' $pattern 'Budget fields are warnings about context loss'
Assert-Contains 'pattern has budget guardrails block' $pattern 'budget_guardrails:'

Assert-Contains 'schema has CI-07 rule' $schema 'CI-07 sandbox rule'
Assert-Contains 'schema says preserve warnings/gaps' $schema 'preserve warnings/gaps'
Assert-Contains 'schema blocks action-ready after key support trimmed' $schema 'must not let a pack remain action-ready'
Assert-Contains 'dev template has Budget Guardrails section' $devTemplate '## Budget Guardrails'
Assert-Contains 'dev template blocks hidden evidence insufficiency' $devTemplate 'evidence insufficiency'
Assert-Contains 'dev template blocks key support trimmed ready' $devTemplate 'If key support is trimmed'
Assert-Contains 'index records CI-07' $index 'CI-07 [[agent-context-pack-budget-guardrails]]'
Assert-Contains 'index records trim order' $index 'neighbors -> sourceWindows -> chunks -> primary'
Assert-Contains 'index blocks action-ready' $index 'cannot remain action-ready'

$fixtureExpectations = @{
  'pass-trimmed-with-visible-warnings.md' = @('expected: PASS', 'truncated: true', 'trimmed_sections:', 'warnings:', 'gaps:', 'state: needs_review')
  'pass-semantic-fallback-warning.md' = @('expected: PASS', 'embedding-store-missing', 'lexical_fallback_used: true')
  'pass-source-windows-opt-in-bounded.md' = @('expected: PASS', 'include_sources: true', 'max_windows: 20', 'path_confined_to: sources/')
  'block-hidden-gaps-after-trim.md' = @('expected: BLOCK', 'known_before_trim:', 'gaps: []')
  'block-key-support-trimmed-ready.md' = @('expected: BLOCK', 'key_support_trimmed: true', 'state: ready')
  'block-source-windows-default-on.md' = @('expected: BLOCK', 'default: on', '../private.txt')
  'block-path-escape-window.md' = @('expected: BLOCK', '../outside.md')
  'block-semantic-fallback-silent.md' = @('expected: BLOCK', 'semantic_hits: []', 'warnings: []')
  'block-invalid-trim-section.md' = @('expected: BLOCK', 'trimmed_sections:', 'warnings')
  'block-json-string-sliced.md' = @('expected: BLOCK', 'trim_method: slice_serialized_json')
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
  'CI-09 source adapter pattern exists' = 'wiki\patterns\source-adapter-ingest-contract.md'
}

foreach ($entry in $compatPaths.GetEnumerator()) {
  Add-Check $entry.Key (Test-Path -LiteralPath (Join-Path $architecture $entry.Value)) $entry.Value
}

$rootPattern = Read-Text (Join-Path $repo 'wiki\patterns\agent-context-pack-budget-guardrails.md')
$rootSchema = Read-Text (Join-Path $repo 'SCHEMA.md')
$rootDevTemplate = Read-Text (Join-Path $repo 'templates\dev-context-pack.md')
$rootIndex = Read-Text (Join-Path $repo 'wiki\indexes\knowledge-graph-index.md')

Assert-NotContains 'root pattern not sandbox-mutated' $rootPattern 'status: sandbox-candidate'
Assert-NotContains 'root schema not sandbox-mutated' $rootSchema 'CI-07 sandbox rule'
Assert-NotContains 'root dev template not sandbox-mutated' $rootDevTemplate '## Budget Guardrails'
Assert-NotContains 'root index not sandbox-mutated' $rootIndex 'CI-07 [[agent-context-pack-budget-guardrails]]'

Assert-NotContains 'pattern does not allow warning trim section' $pattern 'trimmed_sections: [warnings]'
Assert-NotContains 'pattern does not allow gaps trim section' $pattern 'trimmed_sections: [gaps]'
Assert-NotContains 'pattern does not allow action ready shortcut' $pattern 'budget_trimmed_but_action_ready'

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
