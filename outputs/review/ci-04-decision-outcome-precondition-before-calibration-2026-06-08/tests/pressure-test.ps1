param(
  [string]$RepoRoot = ""
)

if (-not $RepoRoot) {
  $RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot "..\..\..\..")).Path
}

$SandboxRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$ArchitectureRoot = Join-Path $SandboxRoot "architecture"
$FixtureRoot = Join-Path $PSScriptRoot "fixtures\decision-outcomes"

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

$patternPath = Join-Path $ArchitectureRoot "wiki\patterns\decision-outcome-precondition-before-calibration.md"
$feedbackPath = Join-Path $ArchitectureRoot "FEEDBACK.md"
$decisionTemplatePath = Join-Path $ArchitectureRoot "templates\decision-record.md"
$indexPath = Join-Path $ArchitectureRoot "wiki\indexes\knowledge-graph-index.md"
$reviewQueuePath = Join-Path $ArchitectureRoot "REVIEW_QUEUE.md"
$candidateTemplatePath = Join-Path $ArchitectureRoot "templates\review-candidate.md"
$ci03PatternPath = Join-Path $ArchitectureRoot "wiki\patterns\source-hash-registry-and-idempotent-ingest.md"

Assert-True "CI-04 pattern exists" (Test-Path $patternPath)
Assert-True "sandbox FEEDBACK exists" (Test-Path $feedbackPath)
Assert-True "sandbox decision template exists" (Test-Path $decisionTemplatePath)
Assert-True "sandbox index exists" (Test-Path $indexPath)

$pattern = Read-Text $patternPath
$feedback = Read-Text $feedbackPath
$decisionTemplate = Read-Text $decisionTemplatePath
$index = Read-Text $indexPath
$reviewQueue = Read-Text $reviewQueuePath
$candidateTemplate = Read-Text $candidateTemplatePath
$ci03Pattern = Read-Text $ci03PatternPath

Assert-Contains "pattern requires original recommendation" $pattern "original recommendation"
Assert-Contains "pattern requires user choice or explicit override" $pattern "user_choice OR explicit_user_override"
Assert-Contains "pattern requires outcome note" $pattern "outcome_note"
Assert-Contains "pattern allows future recommendation" $pattern "future_recommendation"
Assert-Contains "pattern allows risk calibration" $pattern "risk_calibration"
Assert-Contains "pattern forbids truth confidence" $pattern "truth_confidence"
Assert-Contains "pattern forbids verification status" $pattern "verification_status"
Assert-Contains "pattern forbids source reliability" $pattern "source_reliability"
Assert-Contains "pattern forbids review verdict" $pattern "review_verdict"
Assert-Contains "pattern forbids reviewed relation" $pattern "reviewed_relation"
Assert-Contains "pattern forbids action basis readiness" $pattern "action_basis_readiness"
Assert-Contains "pattern blocks RKA runtime" $pattern "RKA runtime"
Assert-Contains "pattern blocks RKA SQLite" $pattern "RKA SQLite database"
Assert-Contains "pattern has exact RKA decision option anchor" $pattern "decision_option.py#L121-L130"
Assert-Contains "pattern has exact RKA service anchor" $pattern "decision_options.py#L234-L280"
Assert-Contains "pattern has exact RKA route anchor" $pattern "api/routes/decisions.py#L227-L243"

Assert-Contains "FEEDBACK has explicit override field" $feedback "explicit_user_override:"
Assert-Contains "FEEDBACK has override rationale field" $feedback "override_rationale:"
Assert-Contains "FEEDBACK requires confidence at decision" $feedback "confidence_at_decision_recorded"
Assert-Contains "FEEDBACK requires outcome note" $feedback "outcome_note_recorded"
Assert-Contains "FEEDBACK forbids truth confidence target" $feedback "truth_confidence"
Assert-Contains "FEEDBACK forbids reviewed relation target" $feedback "reviewed_relation"
Assert-Contains "FEEDBACK blocks RKA runtime import" $feedback "Do not import RKA runtime"

Assert-Contains "decision template has explicit override" $decisionTemplate "explicit user override"
Assert-Contains "decision template has outcome precondition" $decisionTemplate "outcome precondition"
Assert-Contains "decision template blocks reviewed relation" $decisionTemplate "reviewed_relation"
Assert-Contains "decision template blocks RKA runtime" $decisionTemplate "RKA runtime"

Assert-Contains "index records CI-04 sandbox candidate" $index "CI-04 [[decision-outcome-precondition-before-calibration]]"
Assert-Contains "index says not metrics as truth" $index "metrics-as-truth"

Assert-Contains "compat CI-02 review gate still present" $reviewQueue "Review-Gated Compile / Writeback Queue"
Assert-Contains "compat CI-02.5 candidate lint still present" $reviewQueue "Candidate Lint Before Approval"
Assert-Contains "compat review candidate template still has lint" $candidateTemplate "candidate_lint:"
Assert-Contains "compat CI-03 source hash still present" $ci03Pattern "Source Hash Registry and Idempotent Ingest"
Assert-Contains "compat CI-03 still blocks hash as truth" $ci03Pattern "source hash 不增加 truth confidence"

$fixtures = @{
  "pass-user-choice.md" = "expected_result: PASS"
  "pass-explicit-override.md" = "expected_result: PASS"
  "block-outcome-only.md" = "expected_result: BLOCK_EXPECTED"
  "block-no-user-choice.md" = "expected_result: BLOCK_EXPECTED"
  "block-casual-approval.md" = "expected_result: BLOCK_EXPECTED"
  "block-truth-confidence-mutation.md" = "expected_result: BLOCK_EXPECTED"
  "block-verification-status-mutation.md" = "expected_result: BLOCK_EXPECTED"
  "block-reviewed-relation-creation.md" = "expected_result: BLOCK_EXPECTED"
  "block-rka-runtime-import.md" = "expected_result: BLOCK_EXPECTED"
}

foreach ($name in $fixtures.Keys) {
  $path = Join-Path $FixtureRoot $name
  Assert-True "fixture exists $name" (Test-Path $path)
  $text = Read-Text $path
  Assert-Contains "fixture expected marker $name" $text $fixtures[$name]
}

$passChoice = Read-Text (Join-Path $FixtureRoot "pass-user-choice.md")
Assert-Contains "pass choice has recommendation" $passChoice "recommendation: choose option A"
Assert-Contains "pass choice has confidence" $passChoice "confidence_at_decision: medium"
Assert-Contains "pass choice has user choice" $passChoice "user_choice: option A"
Assert-Contains "pass choice has outcome note" $passChoice "outcome_note: The chosen option worked"

$passOverride = Read-Text (Join-Path $FixtureRoot "pass-explicit-override.md")
Assert-Contains "pass override has explicit override" $passOverride "explicit_user_override: chose option B"
Assert-Contains "pass override has rationale" $passOverride "override_rationale:"
Assert-Contains "pass override has outcome note" $passOverride "outcome_note:"

$outcomeOnly = Read-Text (Join-Path $FixtureRoot "block-outcome-only.md")
Assert-Contains "outcome only missing recommendation violation" $outcomeOnly "missing recommendation"
Assert-Contains "outcome only missing choice violation" $outcomeOnly "missing user_choice_or_explicit_override"

$noChoice = Read-Text (Join-Path $FixtureRoot "block-no-user-choice.md")
Assert-Contains "no choice has missing choice violation" $noChoice "missing user_choice_or_explicit_override"

$casual = Read-Text (Join-Path $FixtureRoot "block-casual-approval.md")
Assert-Contains "casual approval is blocked" $casual "casual approval is not a recorded choice"

$truthMutation = Read-Text (Join-Path $FixtureRoot "block-truth-confidence-mutation.md")
Assert-Contains "truth mutation proposes truth_confidence" $truthMutation "truth_confidence: high"
Assert-Contains "truth mutation is blocked" $truthMutation "decision outcome cannot mutate truth_confidence"

$verificationMutation = Read-Text (Join-Path $FixtureRoot "block-verification-status-mutation.md")
Assert-Contains "verification mutation proposes verified" $verificationMutation "verification_status: verified"
Assert-Contains "verification mutation is blocked" $verificationMutation "decision outcome cannot mutate verification_status"

$relationMutation = Read-Text (Join-Path $FixtureRoot "block-reviewed-relation-creation.md")
Assert-Contains "relation mutation proposes reviewed relation" $relationMutation "reviewed_relation: creates_supports_relation"
Assert-Contains "relation mutation is blocked" $relationMutation "decision outcome cannot create reviewed_relation"

$runtimeImport = Read-Text (Join-Path $FixtureRoot "block-rka-runtime-import.md")
Assert-Contains "runtime import names MCP" $runtimeImport "RKA MCP"
Assert-Contains "runtime import names SQLite" $runtimeImport "RKA SQLite database"
Assert-Contains "runtime import is blocked" $runtimeImport "not the runtime"

$rootFeedback = Read-Text (Join-Path $RepoRoot "FEEDBACK.md")
$rootDecisionTemplate = Read-Text (Join-Path $RepoRoot "templates\decision-record.md")
$rootIndex = Read-Text (Join-Path $RepoRoot "wiki\indexes\knowledge-graph-index.md")
Assert-NotRegex "root FEEDBACK not polluted with CI-04 explicit override field" $rootFeedback 'explicit_user_override:'
Assert-NotRegex "root decision template not polluted with CI-04 RKA runtime line" $rootDecisionTemplate '不吸收 RKA runtime'
Assert-NotRegex "root index not polluted with CI-04 sandbox line" $rootIndex 'CI-04 \[\[decision-outcome-precondition-before-calibration\]\]'

$changedSandboxDocs = @($pattern, $feedback, $decisionTemplate, $index)
foreach ($text in $changedSandboxDocs) {
  Assert-NotRegex "changed docs do not allow outcome as truth" $text 'outcome_as_truth|calibration_as_truth|truth_from_outcome'
  Assert-NotRegex "changed docs do not allow outcome as review verdict" $text 'outcome_as_review_verdict|reviewed_by_outcome'
  Assert-NotRegex "changed docs do not allow RKA runtime adoption" $text 'adopt RKA runtime|copy RKA runtime|RKA runtime is required|use RKA runtime'
}

Write-Output "RESULT pass=$script:Pass fail=$script:Fail"
if ($script:Fail -gt 0) {
  Write-Output "FAILURES:"
  $script:Failures | ForEach-Object { Write-Output $_ }
  exit 1
}
