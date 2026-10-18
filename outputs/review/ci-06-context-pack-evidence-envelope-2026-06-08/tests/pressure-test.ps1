param(
  [string]$RepoRoot = ""
)

if (-not $RepoRoot) {
  $RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot "..\..\..\..")).Path
}

$SandboxRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$ArchitectureRoot = Join-Path $SandboxRoot "architecture"
$FixtureRoot = Join-Path $PSScriptRoot "fixtures\context-pack"
$EvidenceRoot = Join-Path $SandboxRoot "evidence\llm-wiki-compiler"

$script:Pass = 0
$script:Fail = 0
$script:Failures = New-Object System.Collections.Generic.List[string]

function Assert-True {
  param([string]$Name, [bool]$Condition)
  if ($Condition) {
    $script:Pass++
    Write-Output "PASS $Name"
  } else {
    $script:Fail++
    $script:Failures.Add($Name)
    Write-Output "FAIL $Name"
  }
}

function Read-Text {
  param([string]$Path)
  return Get-Content -Path $Path -Raw -Encoding UTF8
}

function Assert-Contains {
  param([string]$Name, [string]$Text, [string]$Pattern)
  Assert-True -Name $Name -Condition ($Text -match [regex]::Escape($Pattern))
}

function Assert-NotRegex {
  param([string]$Name, [string]$Text, [string]$Pattern)
  Assert-True -Name $Name -Condition (-not ($Text -match $Pattern))
}

$patternPath = Join-Path $ArchitectureRoot "wiki\patterns\context-pack-evidence-envelope.md"
$schemaPath = Join-Path $ArchitectureRoot "SCHEMA.md"
$devTemplatePath = Join-Path $ArchitectureRoot "templates\dev-context-pack.md"
$indexPath = Join-Path $ArchitectureRoot "wiki\indexes\knowledge-graph-index.md"
$typesSnapshotPath = Join-Path $EvidenceRoot "context-types-anchor-snapshot.md"
$buildSnapshotPath = Join-Path $EvidenceRoot "context-build-anchor-snapshot.md"

Assert-True "CI-06 pattern exists" (Test-Path $patternPath)
Assert-True "sandbox SCHEMA exists" (Test-Path $schemaPath)
Assert-True "sandbox dev context template exists" (Test-Path $devTemplatePath)
Assert-True "sandbox index exists" (Test-Path $indexPath)
Assert-True "types anchor snapshot exists" (Test-Path $typesSnapshotPath)
Assert-True "build anchor snapshot exists" (Test-Path $buildSnapshotPath)

$pattern = Read-Text $patternPath
$schema = Read-Text $schemaPath
$devTemplate = Read-Text $devTemplatePath
$index = Read-Text $indexPath
$typesSnapshot = Read-Text $typesSnapshotPath
$buildSnapshot = Read-Text $buildSnapshotPath

Assert-Contains "types snapshot has stable v1 anchor" $typesSnapshot "src/context/types.ts:1-11"
Assert-Contains "types snapshot has budget anchor" $typesSnapshot "src/context/types.ts:49-55"
Assert-Contains "types snapshot has source window anchor" $typesSnapshot "src/context/types.ts:93-99"
Assert-Contains "types snapshot has top-level envelope anchor" $typesSnapshot "src/context/types.ts:150-161"
Assert-Contains "types snapshot lists prompt" $typesSnapshot 'version`, `prompt`, `budget`, `project`'
Assert-Contains "types snapshot says source windows explicit" $typesSnapshot "emitted only when"

Assert-Contains "build snapshot has orchestrator anchor" $buildSnapshot "src/context/build.ts:1-20"
Assert-Contains "build snapshot has options anchor" $buildSnapshot "src/context/build.ts:56-76"
Assert-Contains "build snapshot has includeSources anchor" $buildSnapshot "src/context/build.ts:104-119"
Assert-Contains "build snapshot has assemble draft anchor" $buildSnapshot "src/context/build.ts:227-264"
Assert-Contains "build snapshot has budget anchor" $buildSnapshot "src/context/build.ts:449-505"
Assert-Contains "build snapshot has warnings anchor" $buildSnapshot "src/context/build.ts:513-565"

Assert-Contains "pattern sandbox candidate" $pattern "status: sandbox-candidate"
Assert-Contains "pattern references types snapshot" $pattern "context-types-anchor-snapshot.md"
Assert-Contains "pattern references build snapshot" $pattern "context-build-anchor-snapshot.md"
Assert-Contains "pattern says read-only envelope" $pattern "read-only activation and evidence envelope"
Assert-Contains "pattern exposes warnings" $pattern "warnings"
Assert-Contains "pattern exposes gaps" $pattern "gaps"
Assert-Contains "pattern exposes suggested actions" $pattern "suggested actions"
Assert-Contains "pattern exposes source windows explicitly" $pattern "source windows when explicitly requested"
Assert-Contains "pattern forbids truth confidence" $pattern "truth_confidence"
Assert-Contains "pattern forbids reviewed relation" $pattern "reviewed_relation"
Assert-Contains "pattern forbids action basis readiness" $pattern "action_basis_readiness"
Assert-Contains "pattern forbids wiki writeback" $pattern "wiki_writeback"
Assert-Contains "pattern says suggested actions are not auto" $pattern 'suggested_actions` 是建议，不是自动执行'

Assert-Contains "SCHEMA has version field" $schema "version: 1"
Assert-Contains "SCHEMA has primary field" $schema "primary: []"
Assert-Contains "SCHEMA has neighbors field" $schema "neighbors: []"
Assert-Contains "SCHEMA has warnings field" $schema "warnings: []"
Assert-Contains "SCHEMA has gaps field" $schema "gaps: []"
Assert-Contains "SCHEMA has source windows field" $schema "source_windows: []"
Assert-Contains "SCHEMA marks read only" $schema "read_only: true"
Assert-Contains "SCHEMA says envelope read-only" $schema "Context pack evidence envelope is read-only"
Assert-Contains "SCHEMA says source windows default empty" $schema 'source_windows` default to empty'
Assert-Contains "SCHEMA says suggested actions only" $schema "suggestions only"
Assert-Contains "SCHEMA says primary neighbors not support" $schema "do not provide support by relatedness alone"

Assert-Contains "dev template has envelope boundary" $devTemplate "Evidence Envelope Boundary"
Assert-Contains "dev template marks read only" $devTemplate "read_only: true"
Assert-Contains "dev template says source windows empty" $devTemplate "Source windows are empty unless explicitly requested."
Assert-Contains "dev template says warnings gaps visible" $devTemplate "Warnings and gaps must remain visible."
Assert-Contains "dev template says suggested not automatic" $devTemplate "Suggested actions are not automatic actions."

Assert-Contains "index records CI-06 sandbox" $index "CI-06 [[context-pack-evidence-envelope]]"
Assert-Contains "index says source windows default empty" $index "source windows 默认空"
Assert-Contains "index says suggested actions not automatic" $index "suggested actions 不是自动执行"
Assert-Contains "index says retrieval not truth" $index "primary/neighbors/retrieval 不是 truth"

$fixtures = @{
  "pass-read-only-envelope.md" = "expected_result: PASS"
  "pass-include-source-windows.md" = "expected_result: PASS"
  "block-source-windows-default.md" = "expected_result: BLOCK_EXPECTED"
  "block-pack-as-truth.md" = "expected_result: BLOCK_EXPECTED"
  "block-neighbor-as-relation.md" = "expected_result: BLOCK_EXPECTED"
  "block-suggested-action-auto-exec.md" = "expected_result: BLOCK_EXPECTED"
  "block-action-basis-ready.md" = "expected_result: BLOCK_EXPECTED"
  "block-truncated-hides-gaps.md" = "expected_result: BLOCK_EXPECTED"
  "block-wiki-writeback.md" = "expected_result: BLOCK_EXPECTED"
}

foreach ($name in $fixtures.Keys) {
  $path = Join-Path $FixtureRoot $name
  Assert-True "fixture exists $name" (Test-Path $path)
  $text = Read-Text $path
  Assert-Contains "fixture expected marker $name" $text $fixtures[$name]
}

$passEnvelope = Read-Text (Join-Path $FixtureRoot "pass-read-only-envelope.md")
Assert-Contains "pass envelope has budget" $passEnvelope "budget:"
Assert-Contains "pass envelope has project" $passEnvelope "project:"
Assert-Contains "pass envelope has primary" $passEnvelope "primary:"
Assert-Contains "pass envelope has neighbors" $passEnvelope "neighbors:"
Assert-Contains "pass envelope has warnings" $passEnvelope "warnings:"
Assert-Contains "pass envelope has gaps" $passEnvelope "gaps:"
Assert-Contains "pass envelope read only" $passEnvelope "read_only: true"
Assert-Contains "pass envelope not truth" $passEnvelope "not_truth_layer: true"

$includeSources = Read-Text (Join-Path $FixtureRoot "pass-include-source-windows.md")
Assert-Contains "include sources is explicit" $includeSources "include_sources: true"
Assert-Contains "include sources has source window" $includeSources "source_windows:"

$defaultSources = Read-Text (Join-Path $FixtureRoot "block-source-windows-default.md")
Assert-Contains "default source windows blocked" $defaultSources "source_windows must be empty unless include_sources is explicit"

$truth = Read-Text (Join-Path $FixtureRoot "block-pack-as-truth.md")
Assert-Contains "truth misuse blocked" $truth "context pack cannot set truth_confidence"

$neighbor = Read-Text (Join-Path $FixtureRoot "block-neighbor-as-relation.md")
Assert-Contains "neighbor misuse blocked" $neighbor "neighbors explain activation but cannot create reviewed_relation"

$auto = Read-Text (Join-Path $FixtureRoot "block-suggested-action-auto-exec.md")
Assert-Contains "suggested action auto exec blocked" $auto "suggested_actions are suggestions, not automatic actions"

$action = Read-Text (Join-Path $FixtureRoot "block-action-basis-ready.md")
Assert-Contains "action basis misuse blocked" $action "context pack alone cannot create action_basis_readiness"

$truncated = Read-Text (Join-Path $FixtureRoot "block-truncated-hides-gaps.md")
Assert-Contains "truncated pack blocked" $truncated "truncated packs must expose warnings or gaps"

$writeback = Read-Text (Join-Path $FixtureRoot "block-wiki-writeback.md")
Assert-Contains "writeback misuse blocked" $writeback "cannot write wiki or promote candidates"

$reviewQueue = Read-Text (Join-Path $ArchitectureRoot "REVIEW_QUEUE.md")
$reviewCandidate = Read-Text (Join-Path $ArchitectureRoot "templates\review-candidate.md")
$ci03 = Read-Text (Join-Path $ArchitectureRoot "wiki\patterns\source-hash-registry-and-idempotent-ingest.md")
$ci04 = Read-Text (Join-Path $ArchitectureRoot "wiki\patterns\decision-outcome-precondition-before-calibration.md")
$ci05 = Read-Text (Join-Path $ArchitectureRoot "wiki\patterns\scope-dashboard-live-context-surface.md")
Assert-Contains "compat CI-02 still present" $reviewQueue "Review-Gated Compile / Writeback Queue"
Assert-Contains "compat CI-02.5 still present" $reviewQueue "Candidate Lint Before Approval"
Assert-Contains "compat review candidate lint still present" $reviewCandidate "candidate_lint:"
Assert-Contains "compat CI-03 still present" $ci03 "Source Hash Registry and Idempotent Ingest"
Assert-Contains "compat CI-04 still present" $ci04 "Decision Outcome Precondition Before Calibration"
Assert-Contains "compat CI-05 still present" $ci05 "Scope Dashboard Live Context Surface"

$rootPattern = Read-Text (Join-Path $RepoRoot "wiki\patterns\context-pack-evidence-envelope.md")
$rootSchema = Read-Text (Join-Path $RepoRoot "SCHEMA.md")
$rootIndex = Read-Text (Join-Path $RepoRoot "wiki\indexes\knowledge-graph-index.md")
Assert-NotRegex "root CI-06 pattern not polluted with sandbox status" $rootPattern 'status:\s*sandbox-candidate'
Assert-NotRegex "root SCHEMA not polluted with CI-06 read-only sentence" $rootSchema 'Context pack evidence envelope is read-only'
Assert-NotRegex "root index not polluted with CI-06 sandbox line" $rootIndex 'CI-06 \[\[context-pack-evidence-envelope\]\]'

$changedDocs = @($pattern, $schema, $devTemplate, $index)
foreach ($text in $changedDocs) {
  Assert-NotRegex "changed docs do not allow pack as truth" $text 'pack_as_truth|context_pack_as_truth|truth_from_context_pack'
  Assert-NotRegex "changed docs do not allow auto suggested action" $text 'auto_execute_suggested_actions:\s*true|suggested_actions auto'
  Assert-NotRegex "changed docs do not allow writeback" $text 'context_pack_writeback|context pack writes wiki'
}

Write-Output "RESULT pass=$script:Pass fail=$script:Fail"
if ($script:Fail -gt 0) {
  Write-Output "FAILURES:"
  $script:Failures | ForEach-Object { Write-Output $_ }
  exit 1
}
