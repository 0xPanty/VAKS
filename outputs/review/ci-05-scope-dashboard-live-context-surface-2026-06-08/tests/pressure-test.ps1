param(
  [string]$RepoRoot = ""
)

if (-not $RepoRoot) {
  $RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot "..\..\..\..")).Path
}

$SandboxRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$ArchitectureRoot = Join-Path $SandboxRoot "architecture"
$FixtureRoot = Join-Path $PSScriptRoot "fixtures\scope-dashboard"
$EvidenceRoot = Join-Path $SandboxRoot "evidence\dusk"

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

function Assert-Regex {
  param([string]$Name, [string]$Text, [string]$Pattern)
  Assert-True -Name $Name -Condition ($Text -match $Pattern)
}

function Assert-NotRegex {
  param([string]$Name, [string]$Text, [string]$Pattern)
  Assert-True -Name $Name -Condition (-not ($Text -match $Pattern))
}

$patternPath = Join-Path $ArchitectureRoot "wiki\patterns\scope-dashboard-live-context-surface.md"
$devContextPath = Join-Path $ArchitectureRoot "DEV_CONTEXT.md"
$indexPath = Join-Path $ArchitectureRoot "wiki\indexes\knowledge-graph-index.md"
$reviewQueuePath = Join-Path $ArchitectureRoot "REVIEW_QUEUE.md"
$reviewCandidatePath = Join-Path $ArchitectureRoot "templates\review-candidate.md"
$ci03Path = Join-Path $ArchitectureRoot "wiki\patterns\source-hash-registry-and-idempotent-ingest.md"
$ci04Path = Join-Path $ArchitectureRoot "wiki\patterns\decision-outcome-precondition-before-calibration.md"
$templateSnapshotPath = Join-Path $EvidenceRoot "template-area-anchor-snapshot.md"
$onboardingSnapshotPath = Join-Path $EvidenceRoot "onboarding-part-3-anchor-snapshot.md"

Assert-True "CI-05 pattern exists" (Test-Path $patternPath)
Assert-True "sandbox DEV_CONTEXT exists" (Test-Path $devContextPath)
Assert-True "sandbox index exists" (Test-Path $indexPath)
Assert-True "Dusk template snapshot exists" (Test-Path $templateSnapshotPath)
Assert-True "Dusk onboarding snapshot exists" (Test-Path $onboardingSnapshotPath)

$pattern = Read-Text $patternPath
$devContext = Read-Text $devContextPath
$index = Read-Text $indexPath
$templateSnapshot = Read-Text $templateSnapshotPath
$onboardingSnapshot = Read-Text $onboardingSnapshotPath
$reviewQueue = Read-Text $reviewQueuePath
$reviewCandidate = Read-Text $reviewCandidatePath
$ci03 = Read-Text $ci03Path
$ci04 = Read-Text $ci04Path

Assert-Contains "template snapshot anchors 13-38" $templateSnapshot "template_area.md:13-38"
Assert-Contains "template snapshot anchors 40-66" $templateSnapshot "template_area.md:40-66"
Assert-Contains "template snapshot names components" $templateSnapshot "Components"
Assert-Contains "template snapshot names projects" $templateSnapshot "Projects"
Assert-Contains "template snapshot names meetings" $templateSnapshot "Scheduled Meetings"
Assert-Contains "template snapshot names ongoing tasks" $templateSnapshot "Ongoing Task"
Assert-Contains "onboarding snapshot anchors 72-83" $onboardingSnapshot "Vault Onboarding Part 3 - Main Features.md:72-83"
Assert-Contains "onboarding snapshot names area family" $onboardingSnapshot "area_family"
Assert-Contains "onboarding snapshot says MOC" $onboardingSnapshot "MOC"

Assert-Contains "pattern has sandbox trial status" $pattern "verification_status: sandbox-trial"
Assert-Contains "pattern references template snapshot" $pattern "template-area-anchor-snapshot.md"
Assert-Contains "pattern references onboarding snapshot" $pattern "onboarding-part-3-anchor-snapshot.md"
Assert-Contains "pattern includes dashboard to briefing to pack" $pattern "scope dashboard -> compact briefing -> selected dev context pack"
Assert-Contains "pattern marks not truth layer" $pattern "not_truth_layer: true"
Assert-Contains "pattern marks not evidence support" $pattern "not_evidence_support: true"
Assert-Contains "pattern marks not action basis" $pattern "not_action_basis: true"
Assert-Contains "pattern says candidate only" $pattern "selection_status: candidate_only"
Assert-Contains "pattern blocks reviewed relations" $pattern "Creating reviewed relations"
Assert-Contains "pattern blocks permanent activation" $pattern "Changing activation tier permanently"

Assert-Contains "DEV_CONTEXT trial boundary exists" $devContext "Scope Dashboard Trial Boundary"
Assert-Contains "DEV_CONTEXT allows candidate surfacing" $devContext "surface core/support/risk/task/cold candidates"
Assert-Contains "DEV_CONTEXT allows compact briefing" $devContext "create a compact briefing"
Assert-Contains "DEV_CONTEXT forbids dashboard truth" $devContext "dashboard state as truth"
Assert-Contains "DEV_CONTEXT forbids plugin authority" $devContext "plugin output as authority"
Assert-Contains "DEV_CONTEXT forbids auto selection" $devContext "automatic dev context pack selection without recorded selection rationale"
Assert-Contains "DEV_CONTEXT forbids permanent activation" $devContext "permanent activation-tier mutation from dashboard appearance alone"

Assert-Contains "index records CI-05 sandbox" $index "CI-05 [[scope-dashboard-live-context-surface]]"
Assert-Contains "index says dashboard not truth" $index "dashboard 可帮助选 Core / Support / Risk / Cold 候选，但不是 truth"
Assert-Contains "index says not plugin authority" $index "Obsidian plugin authority"

Assert-Contains "compat CI-02 review gate still present" $reviewQueue "Review-Gated Compile / Writeback Queue"
Assert-Contains "compat CI-02.5 candidate lint still present" $reviewQueue "Candidate Lint Before Approval"
Assert-Contains "compat review candidate lint template still present" $reviewCandidate "candidate_lint:"
Assert-Contains "compat CI-03 still present" $ci03 "Source Hash Registry and Idempotent Ingest"
Assert-Contains "compat CI-04 still present" $ci04 "Decision Outcome Precondition Before Calibration"

$fixtures = @{
  "pass-scope-dashboard.md" = "expected_result: PASS"
  "pass-compact-briefing.md" = "expected_result: PASS"
  "pass-dev-context-pack-selection.md" = "expected_result: PASS"
  "block-dashboard-as-truth.md" = "expected_result: BLOCK_EXPECTED"
  "block-plugin-output-authority.md" = "expected_result: BLOCK_EXPECTED"
  "block-auto-context-pack.md" = "expected_result: BLOCK_EXPECTED"
  "block-action-basis-ready.md" = "expected_result: BLOCK_EXPECTED"
  "block-reviewed-relation.md" = "expected_result: BLOCK_EXPECTED"
  "block-permanent-activation.md" = "expected_result: BLOCK_EXPECTED"
}

foreach ($name in $fixtures.Keys) {
  $path = Join-Path $FixtureRoot $name
  Assert-True "fixture exists $name" (Test-Path $path)
  $text = Read-Text $path
  Assert-Contains "fixture expected marker $name" $text $fixtures[$name]
}

$dashboard = Read-Text (Join-Path $FixtureRoot "pass-scope-dashboard.md")
Assert-Contains "dashboard marks not truth" $dashboard "not_truth_layer: true"
Assert-Contains "dashboard marks candidate only" $dashboard "selection_status: candidate_only"
Assert-Contains "dashboard has core candidate" $dashboard "core_candidates:"
Assert-Contains "dashboard has support candidate" $dashboard "support_candidates:"
Assert-Contains "dashboard has risk candidate" $dashboard "risk_candidates:"
Assert-Contains "dashboard has task candidate" $dashboard "task_candidates:"
Assert-Contains "dashboard has cold candidate" $dashboard "cold_reference_candidates:"

$briefing = Read-Text (Join-Path $FixtureRoot "pass-compact-briefing.md")
Assert-Contains "briefing derived from dashboard" $briefing "source_dashboard: pass-scope-dashboard.md"
Assert-Contains "briefing records rationale" $briefing "selection_rationale_recorded: true"
Assert-Contains "briefing still not truth" $briefing "not_truth_layer: true"

$pack = Read-Text (Join-Path $FixtureRoot "pass-dev-context-pack-selection.md")
Assert-Contains "pack is temporary" $pack "pack_status: temporary"
Assert-Contains "pack derived from briefing" $pack "derived_from_briefing: pass-compact-briefing.md"
Assert-Contains "pack records no truth change" $pack "truth_status_changed: false"
Assert-Contains "pack records no permanent activation" $pack "activation_tier_changed_permanently: false"
Assert-Contains "pack records not action ready" $pack "action_basis_ready: false"

$badTruth = Read-Text (Join-Path $FixtureRoot "block-dashboard-as-truth.md")
Assert-Contains "bad truth fixture blocked" $badTruth "dashboard cannot decide truth_confidence"

$badPlugin = Read-Text (Join-Path $FixtureRoot "block-plugin-output-authority.md")
Assert-Contains "bad plugin fixture blocked" $badPlugin "plugin output can surface candidates but cannot act as authority"

$badAuto = Read-Text (Join-Path $FixtureRoot "block-auto-context-pack.md")
Assert-Contains "bad auto fixture blocked" $badAuto "dashboard appearance alone cannot auto-select"

$badAction = Read-Text (Join-Path $FixtureRoot "block-action-basis-ready.md")
Assert-Contains "bad action fixture blocked" $badAction "dashboard cannot create action_basis_readiness"

$badRelation = Read-Text (Join-Path $FixtureRoot "block-reviewed-relation.md")
Assert-Contains "bad relation fixture blocked" $badRelation "dashboard cannot create reviewed relations"

$badActivation = Read-Text (Join-Path $FixtureRoot "block-permanent-activation.md")
Assert-Contains "bad activation fixture blocked" $badActivation "dashboard appearance alone cannot permanently change activation tier"

$rootPattern = Read-Text (Join-Path $RepoRoot "wiki\patterns\scope-dashboard-live-context-surface.md")
$rootDevContext = Read-Text (Join-Path $RepoRoot "DEV_CONTEXT.md")
$rootIndex = Read-Text (Join-Path $RepoRoot "wiki\indexes\knowledge-graph-index.md")
Assert-NotRegex "root CI-05 pattern not polluted with sandbox trial status" $rootPattern 'verification_status:\s*sandbox-trial'
Assert-NotRegex "root DEV_CONTEXT not polluted with CI-05 trial boundary" $rootDevContext 'Scope Dashboard Trial Boundary'
Assert-NotRegex "root index not polluted with CI-05 sandbox line" $rootIndex 'CI-05 \[\[scope-dashboard-live-context-surface\]\]'

$changedDocs = @($pattern, $devContext, $index)
foreach ($text in $changedDocs) {
  Assert-NotRegex "changed docs do not allow dashboard as truth" $text 'dashboard_as_truth|dashboard state decides truth|dashboard.*truth_confidence: high'
  Assert-NotRegex "changed docs do not allow plugin authority" $text 'plugin_output_authority|plugin output is authority|plugin output as reviewed'
  Assert-NotRegex "changed docs do not allow auto action basis" $text 'dashboard_as_action_basis|action_basis_ready: true'
}

Write-Output "RESULT pass=$script:Pass fail=$script:Fail"
if ($script:Fail -gt 0) {
  Write-Output "FAILURES:"
  $script:Failures | ForEach-Object { Write-Output $_ }
  exit 1
}
