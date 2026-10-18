param(
  [string]$RepoRoot = ""
)

if (-not $RepoRoot) {
  $RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot "..\..\..\..")).Path
}

$SandboxRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$ArchitectureRoot = Join-Path $SandboxRoot "architecture"
$FixtureRoot = Join-Path $PSScriptRoot "fixtures"

$script:Pass = 0
$script:Fail = 0
$script:Failures = New-Object System.Collections.Generic.List[string]

function Assert-True {
  param(
    [string]$Name,
    [bool]$Condition
  )
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
  param(
    [string]$Name,
    [string]$Text,
    [string]$Pattern
  )
  Assert-True -Name $Name -Condition ($Text -match [regex]::Escape($Pattern))
}

function Assert-Regex {
  param(
    [string]$Name,
    [string]$Text,
    [string]$Pattern
  )
  Assert-True -Name $Name -Condition ($Text -match $Pattern)
}

function Assert-NotRegex {
  param(
    [string]$Name,
    [string]$Text,
    [string]$Pattern
  )
  Assert-True -Name $Name -Condition (-not ($Text -match $Pattern))
}

function Get-ZipEntryText {
  param(
    [string]$ZipPath,
    [string]$EntryName
  )
  Add-Type -AssemblyName System.IO.Compression.FileSystem
  $zip = [System.IO.Compression.ZipFile]::OpenRead((Resolve-Path $ZipPath))
  try {
    $entry = $zip.GetEntry($EntryName)
    if ($null -eq $entry) { return "" }
    $reader = New-Object System.IO.StreamReader($entry.Open())
    try {
      return $reader.ReadToEnd()
    } finally {
      $reader.Dispose()
    }
  } finally {
    $zip.Dispose()
  }
}

$patternPath = Join-Path $ArchitectureRoot "wiki\patterns\source-hash-registry-and-idempotent-ingest.md"
$sourceIntakePath = Join-Path $ArchitectureRoot "SOURCE_INTAKE.md"
$reviewQueuePath = Join-Path $ArchitectureRoot "REVIEW_QUEUE.md"
$candidateTemplatePath = Join-Path $ArchitectureRoot "templates\review-candidate.md"
$indexPath = Join-Path $ArchitectureRoot "wiki\indexes\knowledge-graph-index.md"
$registryPath = Join-Path $FixtureRoot "derived-registry\source-registry.expected.json"

Assert-True "sandbox pattern exists" (Test-Path $patternPath)
Assert-True "sandbox SOURCE_INTAKE exists" (Test-Path $sourceIntakePath)
Assert-True "sandbox REVIEW_QUEUE exists" (Test-Path $reviewQueuePath)
Assert-True "sandbox review candidate template exists" (Test-Path $candidateTemplatePath)
Assert-True "sandbox index exists" (Test-Path $indexPath)

$pattern = Read-Text $patternPath
$sourceIntake = Read-Text $sourceIntakePath
$reviewQueue = Read-Text $reviewQueuePath
$candidateTemplate = Read-Text $candidateTemplatePath
$index = Read-Text $indexPath

Assert-Contains "pattern names markdown source record primary" $pattern "Markdown source record 是主记录"
Assert-Contains "pattern names derived registry" $pattern "JSON registry 是加速索引"
Assert-Contains "pattern says registry rebuilds from markdown" $pattern "registry 需要重建"
Assert-Contains "pattern blocks truth confidence from hash" $pattern "source hash 不增加 truth confidence"
Assert-Contains "pattern blocks evidence support from hash" $pattern "source hash 不算 evidence support"
Assert-Contains "pattern blocks reviewed relation from hash" $pattern "source hash 不创建 reviewed relation"
Assert-Contains "pattern blocks review queue bypass" $pattern "source hash 不允许绕过 review queue 写入正式 wiki"
Assert-Contains "pattern blocks obsidian sync as approval" $pattern "source hash 不允许把 Obsidian 同步当成审批或入库完成"
Assert-Contains "pattern includes idempotent skip" $pattern "idempotent_skip"
Assert-Contains "pattern includes preserve new origin" $pattern "preserve_new_origin"
Assert-Contains "pattern includes replacement candidate" $pattern "replacement_candidate"
Assert-Contains "pattern includes orphan review due" $pattern "orphan_review_due"
Assert-Contains "pattern includes no registry commit" $pattern "no_registry_commit"
Assert-Contains "pattern records OpenKB state anchor" $pattern "OpenKB-main/openkb/state.py:8-25"
Assert-Contains "pattern records OpenKB converter anchor" $pattern "OpenKB-main/openkb/converter.py:36-61"
Assert-Contains "pattern records OpenKB cli anchor" $pattern "OpenKB-main/openkb/cli.py:348-361"

Assert-Contains "SOURCE_INTAKE has source identity block" $sourceIntake "source_identity:"
Assert-Contains "SOURCE_INTAKE keeps markdown primary" $sourceIntake "Markdown source record is primary."
Assert-Contains "SOURCE_INTAKE keeps registry derived" $sourceIntake "The hash registry is derived and rebuildable."
Assert-Contains "SOURCE_INTAKE preserves different origin" $sourceIntake "Same hash + different origin must preserve the new origin/provenance."
Assert-Contains "SOURCE_INTAKE routes changed hash" $sourceIntake "Same origin + changed hash creates a replacement/recompile candidate."
Assert-Contains "SOURCE_INTAKE routes missing raw as review due" $sourceIntake "Missing raw source that is already referenced becomes orphan/review_due, not silent deletion."
Assert-Contains "SOURCE_INTAKE says hash is not evidence support" $sourceIntake "Source hash is not evidence support, truth confidence, approval, or action readiness."

Assert-Contains "CI-02 review gate still present" $reviewQueue "Review-Gated Compile / Writeback Queue"
Assert-Contains "CI-02.5 candidate lint still present" $reviewQueue "Candidate Lint Before Approval"
Assert-Contains "template still has candidate_lint" $candidateTemplate "candidate_lint:"
Assert-Contains "index marks CI-03 sandbox scope" $index "CI-03 [[source-hash-registry-and-idempotent-ingest]] 只作为 source 生命周期卫生规则测试"

$fixtures = @{
  "new-source.md" = "expected_ingest_decision: new_source"
  "repeat-same-origin-same-hash.md" = "expected_ingest_decision: idempotent_skip"
  "same-hash-different-origin.md" = "expected_ingest_decision: preserve_new_origin"
  "same-origin-changed-hash.md" = "expected_ingest_decision: replacement_candidate"
  "deleted-source-still-referenced.md" = "expected_ingest_decision: orphan_review_due"
  "compile-failure-no-registry-commit.md" = "expected_registry_action: no_registry_commit"
  "block-hash-as-truth.md" = "expected_test_result: BLOCK_EXPECTED"
}

foreach ($name in $fixtures.Keys) {
  $path = Join-Path $FixtureRoot "source-records\$name"
  Assert-True "fixture exists $name" (Test-Path $path)
  $text = Read-Text $path
  Assert-Contains "fixture expected marker $name" $text $fixtures[$name]
}

$sameHashDifferentOrigin = Read-Text (Join-Path $FixtureRoot "source-records\same-hash-different-origin.md")
Assert-Contains "same hash different origin keeps mirror origin" $sameHashDifferentOrigin "https://mirror.example.test/source-a"
Assert-NotRegex "same hash different origin does not skip provenance" $sameHashDifferentOrigin "expected_ingest_decision:\s*idempotent_skip"

$changedHash = Read-Text (Join-Path $FixtureRoot "source-records\same-origin-changed-hash.md")
Assert-Contains "changed hash records previous hash" $changedHash "previous_content_hash: sha256:1111111111111111111111111111111111111111111111111111111111111111"
Assert-Contains "changed hash routes recompile" $changedHash "expected_registry_action: route_recompile_candidate"

$deletedSource = Read-Text (Join-Path $FixtureRoot "source-records\deleted-source-still-referenced.md")
Assert-Contains "deleted source preserves downstream evidence packet" $deletedSource "outputs/review/evidence-packets/source-b-evidence.md"
Assert-Contains "deleted source preserves reviewed node reference" $deletedSource "wiki/patterns/example-reviewed-pattern.md"
Assert-NotRegex "deleted source fixture does not allow reviewed evidence delete" $deletedSource "delete_reviewed_evidence|silent_delete|purge_downstream"

$failure = Read-Text (Join-Path $FixtureRoot "source-records\compile-failure-no-registry-commit.md")
Assert-Contains "compile failure has failed result" $failure "compile_result: failed"
Assert-Contains "compile failure blocks registry commit" $failure "expected_registry_action: no_registry_commit"

$badTruth = Read-Text (Join-Path $FixtureRoot "source-records\block-hash-as-truth.md")
Assert-Contains "bad truth fixture is blocked" $badTruth "expected_test_result: BLOCK_EXPECTED"
Assert-Contains "bad truth fixture names violation" $badTruth "source hash cannot provide truth confidence"

Assert-True "derived registry fixture exists" (Test-Path $registryPath)
$registry = Get-Content -Path $registryPath -Raw -Encoding UTF8 | ConvertFrom-Json
$hashOne = $registry."sha256:1111111111111111111111111111111111111111111111111111111111111111"
Assert-True "derived registry keeps two source records for same hash" ($hashOne.source_records.Count -eq 2)
Assert-True "derived registry keeps two origins for same hash" ($hashOne.origins.Count -eq 2)
Assert-True "derived registry is not a truth record" (-not ($registryPath -match "truth"))

$zipPath = Join-Path $RepoRoot "raw\repos\_snapshots\openkb-main-2026-05-27.zip"
Assert-True "OpenKB source snapshot exists" (Test-Path $zipPath)
$statePy = Get-ZipEntryText $zipPath "OpenKB-main/openkb/state.py"
$converterPy = Get-ZipEntryText $zipPath "OpenKB-main/openkb/converter.py"
$cliPy = Get-ZipEntryText $zipPath "OpenKB-main/openkb/cli.py"
Assert-Regex "OpenKB state defines HashRegistry" $statePy "class\s+HashRegistry"
Assert-Regex "OpenKB state has is_known lookup" $statePy "def\s+is_known"
Assert-Regex "OpenKB state persists add" $statePy "def\s+add"
Assert-Regex "OpenKB state hashes files with sha256" $statePy "hashlib\.sha256"
Assert-Regex "OpenKB converter hashes before skip" $converterPy "file_hash\s*=\s*HashRegistry\.hash_file"
Assert-Regex "OpenKB converter skips known file" $converterPy "Skipping already-known file"
Assert-Regex "OpenKB cli registers after success comment" $cliPy "Register hash only after successful compilation"
Assert-Regex "OpenKB cli registry add" $cliPy "registry\.add"

$rootSourceIntake = Read-Text (Join-Path $RepoRoot "SOURCE_INTAKE.md")
$rootPatternPath = Join-Path $RepoRoot "wiki\patterns\source-hash-registry-and-idempotent-ingest.md"
$rootPattern = Read-Text $rootPatternPath
Assert-NotRegex "root SOURCE_INTAKE not polluted with CI-03 new decision field" $rootSourceIntake 'ingest_decision:\s*new_source\s*\|'
Assert-NotRegex "root CI-03 pattern not polluted with sandbox orphan decision table" $rootPattern 'orphan_review_due'

$changedSandboxFiles = @($pattern, $sourceIntake, $index)
foreach ($text in $changedSandboxFiles) {
  Assert-NotRegex "changed sandbox docs do not allow hash as approval" $text 'hash_as_approval|registry_as_approval|approval_from_hash'
  Assert-NotRegex "changed sandbox docs do not allow direct truth from hash" $text 'truth_confidence_from_hash|registry_as_truth|hash_confidence'
  Assert-NotRegex "changed sandbox docs do not allow direct action basis from hash" $text 'action_basis_from_hash|hash_action_ready'
}

Write-Output "RESULT pass=$script:Pass fail=$script:Fail"
if ($script:Fail -gt 0) {
  Write-Output "FAILURES:"
  $script:Failures | ForEach-Object { Write-Output $_ }
  exit 1
}
