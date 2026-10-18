param(
  [Parameter(Mandatory = $true)]
  [string]$SkeletonPath,
  [Parameter(Mandatory = $true)]
  [string]$DraftPath,
  [string]$Root = '.',
  [string]$OutFile = '',
  [switch]$Json
)

$ErrorActionPreference = 'Stop'

$resolvedRoot = (Resolve-Path -LiteralPath $Root).Path
$resolvedSkeletonPath = (Resolve-Path -LiteralPath $SkeletonPath).Path
$resolvedDraftPath = (Resolve-Path -LiteralPath $DraftPath).Path
$createdAt = Get-Date -Format 'yyyy-MM-ddTHH:mm:ssK'

function ConvertTo-Ref {
  param([string]$Path)
  return ($Path -replace '\\','/').TrimStart('./')
}

function Get-DisplayRef {
  param([string]$Path)
  $full = (Resolve-Path -LiteralPath $Path).Path
  $rootPrefix = $resolvedRoot.TrimEnd('\') + '\'
  if ($full.StartsWith($rootPrefix, [StringComparison]::OrdinalIgnoreCase)) {
    return ConvertTo-Ref -Path $full.Substring($rootPrefix.Length)
  }
  return ConvertTo-Ref -Path $full
}

function Get-FrontMatter {
  param([string]$Text)
  $lines = $Text -split "`r?`n"
  if ($lines.Count -lt 3 -or $lines[0].Trim() -ne '---') { return '' }
  $buffer = New-Object System.Collections.Generic.List[string]
  for ($i = 1; $i -lt $lines.Count; $i++) {
    if ($lines[$i].Trim() -eq '---') { break }
    $buffer.Add($lines[$i]) | Out-Null
  }
  return ($buffer -join "`n")
}

function Get-ScalarField {
  param([string]$FrontMatter, [string]$Name)
  $escaped = [regex]::Escape($Name)
  $match = [regex]::Match($FrontMatter, "(?m)^\s*$escaped\s*:\s*(.+?)\s*$")
  if ($match.Success) { return $match.Groups[1].Value.Trim().Trim('"').Trim("'") }
  return ''
}

function Format-ListInline {
  param($Values)
  $items = @($Values | Where-Object { $_ } | Select-Object -Unique)
  if ($items.Count -eq 0) { return '[]' }
  return '[' + (($items | ForEach-Object { '"' + ($_ -replace '"','\"') + '"' }) -join ', ') + ']'
}

function Read-SkeletonClaimIds {
  param([string]$Text)
  $ids = New-Object System.Collections.Generic.List[string]
  foreach ($match in [regex]::Matches($Text, '(?m)^\s*-\s+claim_id:\s*(\S+)\s*$')) {
    $id = $match.Groups[1].Value.Trim()
    if (-not $ids.Contains($id)) { $ids.Add($id) | Out-Null }
  }
  return $ids.ToArray()
}

function Read-ClaimRefs {
  param([string]$Text)
  $refs = New-Object System.Collections.Generic.List[string]
  foreach ($match in [regex]::Matches($Text, '\[claim_refs:\s*([^\]]+)\]')) {
    foreach ($id in ($match.Groups[1].Value -split ',')) {
      $clean = $id.Trim()
      if ($clean -and -not $refs.Contains($clean)) { $refs.Add($clean) | Out-Null }
    }
  }
  return $refs.ToArray()
}

function Read-EmptyClaimRefTags {
  param([string]$Text)
  $tags = New-Object System.Collections.Generic.List[string]
  foreach ($match in [regex]::Matches($Text, '\[claim_refs:\s*\]')) {
    $tags.Add($match.Value) | Out-Null
  }
  return $tags.ToArray()
}

function Read-DraftAnswerLines {
  param([string]$Text)
  $lines = $Text -split "`r?`n"
  $inSection = $false
  $inFence = $false
  $items = New-Object System.Collections.Generic.List[string]
  foreach ($line in $lines) {
    if ($line -match '^#{2,6}\s+Draft Answer\b.*$') {
      $inSection = $true
      continue
    }
    if (-not $inSection) { continue }

    if ($line -match '^\s*```') {
      $inFence = -not $inFence
      continue
    }
    if ($inFence) { continue }
    if ($line -match '^#{1,6}\s+') { break }

    $trimmed = $line.Trim()
    if ([string]::IsNullOrWhiteSpace($trimmed)) { continue }
    if ($trimmed -match '^#{1,6}\s+') { continue }
    $items.Add($trimmed) | Out-Null
  }
  return $items.ToArray()
}

function Read-DraftAnswerBulletLines {
  param([string[]]$DraftAnswerLines)
  $items = New-Object System.Collections.Generic.List[string]
  foreach ($line in @($DraftAnswerLines)) {
    if ($line -match '^\s*-\s+') {
      $items.Add($line) | Out-Null
    }
  }
  return $items.ToArray()
}

$skeletonText = Get-Content -Raw -LiteralPath $resolvedSkeletonPath -Encoding UTF8
$draftText = Get-Content -Raw -LiteralPath $resolvedDraftPath -Encoding UTF8
$skeletonFm = Get-FrontMatter -Text $skeletonText
$draftFm = Get-FrontMatter -Text $draftText
$skeletonRef = Get-DisplayRef -Path $resolvedSkeletonPath
$draftRef = Get-DisplayRef -Path $resolvedDraftPath

$skeletonStateMatch = [regex]::Match($skeletonText, '(?m)^\s*draft_skeleton_state:\s*(\S+)\s*$')
$skeletonState = if ($skeletonStateMatch.Success) { $skeletonStateMatch.Groups[1].Value.Trim() } else { '' }
$draftEmittedMatch = [regex]::Match($draftText, '(?m)^\s*draft_answer_emitted:\s*(true|false)\s*$')
$draftAnswerEmitted = if ($draftEmittedMatch.Success) { $draftEmittedMatch.Groups[1].Value.Trim() } else { '' }

$skeletonClaimIds = @(Read-SkeletonClaimIds -Text $skeletonText)
$claimRefs = @(Read-ClaimRefs -Text $draftText)
$emptyClaimRefTags = @(Read-EmptyClaimRefTags -Text $draftText)
$draftAnswerLines = @(Read-DraftAnswerLines -Text $draftText)
$draftBullets = @(Read-DraftAnswerBulletLines -DraftAnswerLines $draftAnswerLines)
$untaggedDraftLines = @($draftAnswerLines | Where-Object { $_ -notmatch '\[claim_refs:\s*[^\]]+\]' })
$unknownClaimRefs = @($claimRefs | Where-Object { $skeletonClaimIds -notcontains $_ })

$issues = New-Object System.Collections.Generic.List[string]

if ((Get-ScalarField -FrontMatter $draftFm -Name 'action_basis_allowed') -ne 'false') {
  $issues.Add('draft_action_basis_boundary_not_false') | Out-Null
}
if ((Get-ScalarField -FrontMatter $draftFm -Name 'truth_mutation_allowed') -ne 'false') {
  $issues.Add('draft_truth_mutation_boundary_not_false') | Out-Null
}
if ($draftText -notmatch '(?m)^\s*source_refs_policy:\s*claim_evidence_map_only\s*$') {
  $issues.Add('missing_claim_evidence_map_only_policy') | Out-Null
}
if ($draftText -match 'action_basis_allowed:\s*true\b|truth_mutation_allowed:\s*true\b|citation_faithfulness_checked:\s*true\b|support_score_used=true|llm_judge_used=true|external_api_used=true|agent_execution_used=true') {
  $issues.Add('forbidden_true_flag_present') | Out-Null
}

if ($skeletonState -eq 'ready_for_human_draft') {
  if ($draftAnswerEmitted -ne 'true') { $issues.Add('ready_skeleton_did_not_emit_draft') | Out-Null }
  if ($claimRefs.Count -eq 0) { $issues.Add('ready_draft_has_no_claim_refs') | Out-Null }
  if ($emptyClaimRefTags.Count -gt 0) { $issues.Add('ready_draft_has_empty_claim_refs') | Out-Null }
  if ($untaggedDraftLines.Count -gt 0) { $issues.Add('ready_draft_has_untagged_answer_lines') | Out-Null }
  if ($unknownClaimRefs.Count -gt 0) { $issues.Add('ready_draft_has_unknown_claim_refs') | Out-Null }
} else {
  if ($draftAnswerEmitted -ne 'false') { $issues.Add('blocked_skeleton_emitted_draft') | Out-Null }
  if ($claimRefs.Count -gt 0) { $issues.Add('blocked_draft_has_claim_refs') | Out-Null }
  if ($draftAnswerLines.Count -gt 0) { $issues.Add('blocked_draft_has_answer_text') | Out-Null }
}

$status = if ($issues.Count -eq 0) { 'pass' } else { 'fail' }

$lines = New-Object System.Collections.Generic.List[string]
$lines.Add('---') | Out-Null
$lines.Add('record_kind: answer_draft_smoke_lint_candidate') | Out-Null
$lines.Add("status: $status") | Out-Null
$lines.Add("created_at: $createdAt") | Out-Null
$lines.Add('topic_id: source-intake-routing') | Out-Null
$lines.Add('truth_boundary: smoke_lint_not_truth') | Out-Null
$lines.Add('action_basis_allowed: false') | Out-Null
$lines.Add('truth_mutation_allowed: false') | Out-Null
$lines.Add("source_skeleton_ref: $skeletonRef") | Out-Null
$lines.Add("draft_ref: $draftRef") | Out-Null
$lines.Add('---') | Out-Null
$lines.Add('') | Out-Null
$lines.Add('# Answer Draft Smoke Lint v0') | Out-Null
$lines.Add('') | Out-Null
$lines.Add('```yaml') | Out-Null
$lines.Add("status: $status") | Out-Null
$lines.Add("skeleton_state: $skeletonState") | Out-Null
$lines.Add("draft_answer_emitted: $draftAnswerEmitted") | Out-Null
$lines.Add("skeleton_claim_ids: $(Format-ListInline -Values $skeletonClaimIds)") | Out-Null
$lines.Add("draft_claim_refs: $(Format-ListInline -Values $claimRefs)") | Out-Null
$lines.Add("draft_answer_lines: $($draftAnswerLines.Count)") | Out-Null
$lines.Add("draft_answer_bullets: $($draftBullets.Count)") | Out-Null
$lines.Add("untagged_draft_lines: $($untaggedDraftLines.Count)") | Out-Null
$lines.Add("empty_claim_ref_tags: $($emptyClaimRefTags.Count)") | Out-Null
$lines.Add("unknown_claim_refs: $(Format-ListInline -Values $unknownClaimRefs)") | Out-Null
$lines.Add("issues: $(Format-ListInline -Values $issues)") | Out-Null
$lines.Add('action_basis_allowed: false') | Out-Null
$lines.Add('truth_mutation_allowed: false') | Out-Null
$lines.Add('```') | Out-Null

$outputText = $lines -join "`n"
if (-not [string]::IsNullOrWhiteSpace($OutFile)) {
  $outDir = Split-Path -Parent $OutFile
  if (-not [string]::IsNullOrWhiteSpace($outDir) -and -not (Test-Path -LiteralPath $outDir)) {
    New-Item -ItemType Directory -Path $outDir -Force | Out-Null
  }
  Set-Content -LiteralPath $OutFile -Value $outputText -Encoding UTF8
}

if ($Json) {
  [pscustomobject]@{
    record_kind = 'answer_draft_smoke_lint_result_candidate'
    status = $status
    skeleton_ref = $skeletonRef
    draft_ref = $draftRef
    skeleton_state = $skeletonState
    draft_answer_emitted = $draftAnswerEmitted
    skeleton_claim_ids = @($skeletonClaimIds)
    draft_claim_refs = @($claimRefs)
    draft_answer_lines = $draftAnswerLines.Count
    draft_answer_bullets = $draftBullets.Count
    untagged_draft_lines = $untaggedDraftLines.Count
    empty_claim_ref_tags = $emptyClaimRefTags.Count
    unknown_claim_refs = @($unknownClaimRefs)
    issues = @($issues)
    action_basis_allowed = $false
    truth_mutation_allowed = $false
  } | ConvertTo-Json -Depth 5
} elseif ([string]::IsNullOrWhiteSpace($OutFile)) {
  $outputText
}
