param(
  [Parameter(Mandatory = $true)]
  [string]$AnswerReadyPackPath,
  [string]$Root = '.',
  [string]$OutFile = '',
  [switch]$Json
)

$ErrorActionPreference = 'Stop'

$resolvedRoot = (Resolve-Path -LiteralPath $Root).Path
$resolvedAnswerReadyPath = (Resolve-Path -LiteralPath $AnswerReadyPackPath).Path
$createdAt = Get-Date -Format 'yyyy-MM-ddTHH:mm:ssK'

function ConvertTo-Ref {
  param([string]$Path)
  return ($Path -replace '\\','/').TrimStart('./')
}

function Get-DisplayRef {
  param([string]$Path)
  if ([string]::IsNullOrWhiteSpace($Path) -or -not (Test-Path -LiteralPath $Path)) {
    return ''
  }
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

function ConvertTo-PackText {
  param([string]$Value, [int]$MaxLength = 260)
  if ([string]::IsNullOrWhiteSpace($Value)) { return '' }
  $text = ($Value -replace '\s+', ' ').Trim()
  $text = $text -replace '"', "'"
  if ($text.Length -gt $MaxLength) {
    $text = $text.Substring(0, $MaxLength - 3).TrimEnd() + '...'
  }
  return $text
}

function Read-InlineList {
  param([string]$Value)
  if ([string]::IsNullOrWhiteSpace($Value)) { return @() }
  $text = $Value.Trim()
  if ($text -eq '[]') { return @() }
  $matches = [regex]::Matches($text, '"([^"]*)"')
  if ($matches.Count -gt 0) {
    return @($matches | ForEach-Object { $_.Groups[1].Value })
  }
  $text = $text.Trim('[', ']')
  if ([string]::IsNullOrWhiteSpace($text)) { return @() }
  return @($text -split ',' | ForEach-Object { $_.Trim().Trim('"').Trim("'") } | Where-Object { $_ })
}

function Format-ListInline {
  param($Values)
  $items = @($Values | Where-Object { $_ } | Select-Object -Unique)
  if ($items.Count -eq 0) { return '[]' }
  return '[' + (($items | ForEach-Object { '"' + ($_ -replace '"','\"') + '"' }) -join ', ') + ']'
}

function Read-ClaimEvidenceMap {
  param([string]$Text)
  $items = New-Object System.Collections.Generic.List[object]
  $current = $null
  $inMap = $false

  foreach ($line in ($Text -split "`r?`n")) {
    if ($line -match '^claim_evidence_map:\s*$') {
      $inMap = $true
      continue
    }
    if (-not $inMap) { continue }

    if ($line -match '^\S' -and $line -notmatch '^claim_evidence_map:\s*$') {
      if ($null -ne $current) { $items.Add([pscustomobject]$current) | Out-Null }
      break
    }

    if ($line -match '^\s*-\s+claim_id:\s*(\S+)\s*$') {
      if ($null -ne $current) { $items.Add([pscustomobject]$current) | Out-Null }
      $current = [ordered]@{ claim_id = $Matches[1] }
      continue
    }

    if ($null -eq $current) { continue }
    if ($line -match '^\s+([A-Za-z0-9_]+):\s*(.*?)\s*$') {
      $name = $Matches[1]
      $value = $Matches[2].Trim()
      $current[$name] = $value
    }
  }

  return $items.ToArray()
}

$packText = Get-Content -Raw -LiteralPath $resolvedAnswerReadyPath -Encoding UTF8
$frontMatter = Get-FrontMatter -Text $packText
$answerReadyRef = Get-DisplayRef -Path $resolvedAnswerReadyPath
$topicId = Get-ScalarField -FrontMatter $frontMatter -Name 'topic_id'
if ([string]::IsNullOrWhiteSpace($topicId)) { $topicId = 'unknown' }

$inputActionBasis = Get-ScalarField -FrontMatter $frontMatter -Name 'action_basis_allowed'
$inputTruthMutation = Get-ScalarField -FrontMatter $frontMatter -Name 'truth_mutation_allowed'
$sourcePackRef = Get-ScalarField -FrontMatter $frontMatter -Name 'source_pack_ref'
$supportCheckRef = Get-ScalarField -FrontMatter $frontMatter -Name 'evidence_support_check_ref'
$inputReady = [regex]::IsMatch($packText, '(?ms)answer_readiness:\s*\r?\n\s*state:\s*ready_for_answer_draft')
$finalSupportAnswerOnly = [regex]::IsMatch(
  $packText,
  '(?ms)final_support:\s*\r?\n\s*state:\s*checked\s*\r?\n\s*scope:\s*answer_draft_only\s*\r?\n\s*not_action_basis:\s*true'
)

$claims = @(Read-ClaimEvidenceMap -Text $packText)
$unsupportedClaims = @($claims | Where-Object { $_.support_status -ne 'supported' })
$hasClaimMap = ($claims.Count -gt 0)
$canEmitDraft = (
  $inputReady -and
  $finalSupportAnswerOnly -and
  $inputActionBasis -eq 'false' -and
  $inputTruthMutation -eq 'false' -and
  $hasClaimMap -and
  $unsupportedClaims.Count -eq 0
)
$draftState = if ($canEmitDraft) { 'ready_for_human_draft' } else { 'blocked_not_ready' }
$emittedCount = if ($canEmitDraft) { $claims.Count } else { 0 }

$blockReasons = New-Object System.Collections.Generic.List[string]
if (-not $inputReady) { $blockReasons.Add('input_answer_readiness_not_ready_for_answer_draft') | Out-Null }
if (-not $finalSupportAnswerOnly) { $blockReasons.Add('final_support_not_answer_draft_only') | Out-Null }
if ($inputActionBasis -ne 'false') { $blockReasons.Add('input_action_basis_boundary_not_false') | Out-Null }
if ($inputTruthMutation -ne 'false') { $blockReasons.Add('input_truth_mutation_boundary_not_false') | Out-Null }
if (-not $hasClaimMap) { $blockReasons.Add('claim_evidence_map_missing') | Out-Null }
if ($unsupportedClaims.Count -gt 0) { $blockReasons.Add('claim_evidence_map_contains_non_supported_claim') | Out-Null }

$lines = New-Object System.Collections.Generic.List[string]
$lines.Add('---') | Out-Null
$lines.Add('record_kind: answer_draft_skeleton_candidate') | Out-Null
$lines.Add('status: candidate') | Out-Null
$lines.Add("created_at: $createdAt") | Out-Null
$lines.Add("topic_id: $topicId") | Out-Null
$lines.Add('truth_boundary: answer_draft_skeleton_not_truth') | Out-Null
$lines.Add('action_basis_allowed: false') | Out-Null
$lines.Add('truth_mutation_allowed: false') | Out-Null
$lines.Add("source_answer_ready_pack_ref: $answerReadyRef") | Out-Null
$lines.Add('---') | Out-Null
$lines.Add('') | Out-Null
$lines.Add("# Answer Draft Skeleton v0: $topicId") | Out-Null
$lines.Add('') | Out-Null
$lines.Add('## Gate') | Out-Null
$lines.Add('') | Out-Null
$lines.Add('```yaml') | Out-Null
$lines.Add("source_answer_ready_pack_ref: ""$answerReadyRef""") | Out-Null
$lines.Add("source_pack_ref: ""$sourcePackRef""") | Out-Null
$lines.Add("evidence_support_check_ref: ""$supportCheckRef""") | Out-Null
$lines.Add("input_answer_readiness: $(if ($inputReady) { 'ready_for_answer_draft' } else { 'not_ready' })") | Out-Null
$lines.Add("draft_skeleton_state: $draftState") | Out-Null
$lines.Add("claims_seen: $($claims.Count)") | Out-Null
$lines.Add("draft_claims_emitted: $emittedCount") | Out-Null
$lines.Add('source_refs_policy: claim_evidence_map_only') | Out-Null
$lines.Add('action_basis_allowed: false') | Out-Null
$lines.Add('truth_mutation_allowed: false') | Out-Null
$lines.Add('final_support:') | Out-Null
$lines.Add("  state: $(if ($canEmitDraft) { 'checked_for_draft' } else { 'blocked' })") | Out-Null
$lines.Add('  scope: answer_draft_only') | Out-Null
$lines.Add('  not_action_basis: true') | Out-Null
$lines.Add("  input_final_support_answer_only: $($finalSupportAnswerOnly.ToString().ToLowerInvariant())") | Out-Null
$lines.Add('forbidden_use: ["truth", "reviewed_relation", "action_basis", "agent_action"]') | Out-Null
$lines.Add("block_reasons: $(Format-ListInline -Values $blockReasons)") | Out-Null
$lines.Add('```') | Out-Null
$lines.Add('') | Out-Null

if ($canEmitDraft) {
  $lines.Add('## Draft Spine') | Out-Null
  $lines.Add('') | Out-Null
  foreach ($claim in $claims) {
    $sentence = ConvertTo-PackText -Value ($claim.answer_sentence.Trim('"'))
    $sourceRefs = Read-InlineList -Value $claim.source_refs
    $selectors = Read-InlineList -Value $claim.selectors
    $supportChannels = Read-InlineList -Value $claim.support_channels
    $requiredChannels = Read-InlineList -Value $claim.required_support_channels
    $warrant = ConvertTo-PackText -Value ($claim.warrant.Trim('"'))

    $lines.Add("- claim_id: $($claim.claim_id)") | Out-Null
    $lines.Add("  answer_sentence: ""$sentence""") | Out-Null
    $lines.Add("  support_status: $($claim.support_status)") | Out-Null
    $lines.Add("  required_support_channels: $(Format-ListInline -Values $requiredChannels)") | Out-Null
    $lines.Add("  support_channels: $(Format-ListInline -Values $supportChannels)") | Out-Null
    $lines.Add("  source_refs: $(Format-ListInline -Values $sourceRefs)") | Out-Null
    $lines.Add("  selectors: $(Format-ListInline -Values $selectors)") | Out-Null
    $lines.Add("  warrant: ""$warrant""") | Out-Null
  }
} else {
  $lines.Add('## Draft Spine') | Out-Null
  $lines.Add('') | Out-Null
  $lines.Add('```text') | Out-Null
  $lines.Add('blocked: input is not ready_for_answer_draft or contains non-supported claims') | Out-Null
  $lines.Add('draft_claims_emitted: 0') | Out-Null
  $lines.Add('```') | Out-Null
}

$lines.Add('') | Out-Null
$lines.Add('## Guardrails') | Out-Null
$lines.Add('') | Out-Null
$lines.Add('```text') | Out-Null
$lines.Add('This skeleton is only a drafting aid.') | Out-Null
$lines.Add('It must not introduce claims outside claim_evidence_map.') | Out-Null
$lines.Add('It must not convert answer readiness into action basis.') | Out-Null
$lines.Add('Human review is still required before action-facing use.') | Out-Null
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
    record_kind = 'answer_draft_skeleton_result_candidate'
    answer_ready_pack_ref = $answerReadyRef
    out_file = $OutFile
    draft_skeleton_state = $draftState
    claims_seen = $claims.Count
    draft_claims_emitted = $emittedCount
    source_refs_policy = 'claim_evidence_map_only'
    action_basis_allowed = $false
    truth_mutation_allowed = $false
    block_reasons = @($blockReasons)
  } | ConvertTo-Json -Depth 5
} elseif ([string]::IsNullOrWhiteSpace($OutFile)) {
  $outputText
}
