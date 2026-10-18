param(
  [Parameter(Mandatory = $true)]
  [string]$PackPath,
  [Parameter(Mandatory = $true)]
  [string]$ClaimSpecPath,
  [string]$Root = '.',
  [string]$OutFile = '',
  [string]$AnswerReadyOutFile = '',
  [switch]$Json
)

$ErrorActionPreference = 'Stop'

$resolvedRoot = (Resolve-Path -LiteralPath $Root).Path
$resolvedPackPath = (Resolve-Path -LiteralPath $PackPath).Path
$resolvedClaimSpecPath = (Resolve-Path -LiteralPath $ClaimSpecPath).Path
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

function ConvertTo-WorkspacePath {
  param([string]$Ref)
  $clean = ($Ref -replace '/', '\').TrimStart('.\')
  return Join-Path $resolvedRoot $clean
}

function ConvertTo-PackText {
  param([string]$Value, [int]$MaxLength = 220)
  if ([string]::IsNullOrWhiteSpace($Value)) { return '' }
  $text = ($Value -replace '\s+', ' ').Trim()
  $text = $text -replace '"', "'"
  if ($text.Length -gt $MaxLength) {
    $text = $text.Substring(0, $MaxLength - 3).TrimEnd() + '...'
  }
  return $text
}

function Format-ListInline {
  param($Values)
  $items = @($Values | Where-Object { $_ } | Select-Object -Unique)
  if ($items.Count -eq 0) { return '[]' }
  return '[' + (($items | ForEach-Object { '"' + ($_ -replace '"','\"') + '"' }) -join ', ') + ']'
}

function Test-NegatedLine {
  param([string]$Line)
  if ([string]::IsNullOrWhiteSpace($Line)) { return $false }
  $text = $Line.Trim()
  return [regex]::IsMatch(
    $text,
    '(?i)(^|\b)(no|not|never|cannot|can not|must not|should not|does not|do not|is not|are not|non-goals?|forbidden|forbidden_use)\b|!='
  )
}

function Test-ExcludedSupportContext {
  param(
    [string[]]$Lines,
    [int]$Index
  )
  if ($Index -lt 0 -or $Index -ge $Lines.Count) { return $false }
  if (Test-NegatedLine -Line $Lines[$Index]) { return $true }

  $windowStart = [Math]::Max(0, $Index - 8)
  $context = New-Object System.Collections.Generic.List[string]
  for ($j = $windowStart; $j -le $Index; $j++) {
    $context.Add(([string]$Lines[$j]).Trim()) | Out-Null
  }
  $text = ($context -join ' ')
  return [regex]::IsMatch(
    $text,
    '(?i)(supported\s+does\s+not\s+mean|non-goals?|must\s+not\s+become|not\s+an\s+automatic\s+evaluator|forbidden_use|forbidden\s+use|negative\s+fixture|bad\s+claims?|deliberately\s+checks|unsupported\s+and\s+scope-mismatched)'
  )
}

function Read-ContextPackItems {
  param([string]$Text)
  $items = New-Object System.Collections.Generic.List[object]
  $current = $null
  foreach ($line in ($Text -split "`r?`n")) {
    if ($line -match '^\s*-\s+item_id:\s*(\S+)\s*$') {
      if ($null -ne $current) { $items.Add([pscustomobject]$current) | Out-Null }
      $current = [ordered]@{ item_id = $Matches[1] }
      continue
    }
    if ($null -eq $current) { continue }
    if ($line -match '^\s+([A-Za-z0-9_]+):\s*"?(.+?)"?\s*$') {
      $name = $Matches[1]
      $value = $Matches[2].Trim().Trim('"')
      $current[$name] = $value
    }
  }
  if ($null -ne $current) { $items.Add([pscustomobject]$current) | Out-Null }
  return $items.ToArray()
}

function Find-FirstSupportMatch {
  param(
    [string]$SourceRef,
    $Patterns
  )
  $path = ConvertTo-WorkspacePath -Ref $SourceRef
  if (-not (Test-Path -LiteralPath $path)) { return $null }

  $lines = Get-Content -LiteralPath $path -Encoding UTF8
  for ($i = 0; $i -lt $lines.Count; $i++) {
    $line = [string]$lines[$i]
    foreach ($pattern in @($Patterns)) {
      if ([string]::IsNullOrWhiteSpace($pattern)) { continue }
      if ($line -match $pattern) {
        if (Test-ExcludedSupportContext -Lines $lines -Index $i) {
          continue
        }
        return [pscustomobject]@{
          source_ref = ConvertTo-Ref -Path $SourceRef
          selector_or_offset = "line:$($i + 1)"
          snippet = ConvertTo-PackText -Value $line
          matched_pattern = $pattern
        }
      }
    }
  }
  return $null
}

function Normalize-Ref {
  param([string]$Ref)
  return (ConvertTo-Ref -Path $Ref).ToLowerInvariant()
}

$packText = Get-Content -Raw -LiteralPath $resolvedPackPath -Encoding UTF8
$claimSpec = Get-Content -Raw -LiteralPath $resolvedClaimSpecPath -Encoding UTF8 | ConvertFrom-Json
$packItems = @(Read-ContextPackItems -Text $packText)
$anchorItems = @($packItems | Where-Object { $_.action_role -like 'anchor_queue*' })
$anchorRefs = @($anchorItems | ForEach-Object { ConvertTo-Ref -Path $_.source_ref } | Select-Object -Unique)
$packRef = Get-DisplayRef -Path $resolvedPackPath
$claimSpecRef = Get-DisplayRef -Path $resolvedClaimSpecPath
$anchorLookup = @{}
foreach ($ref in $anchorRefs) {
  $anchorLookup[(Normalize-Ref -Ref $ref)] = $true
}

$claimResults = foreach ($claim in @($claimSpec.claims)) {
  $preferred = @($claim.preferred_refs | ForEach-Object { ConvertTo-Ref -Path $_ })
  $configuredFailureOrigin = @($claim.failure_origin_if_missing | Where-Object {
    -not [string]::IsNullOrWhiteSpace([string]$_)
  })
  $requiredSupportChannels = @($claim.required_support_channels | Where-Object {
    -not [string]::IsNullOrWhiteSpace([string]$_)
  })
  $preferredLookup = @{}
  foreach ($ref in $preferred) { $preferredLookup[(Normalize-Ref -Ref $ref)] = $true }
  $requiredSupportChannelLookup = @{}
  foreach ($channel in $requiredSupportChannels) {
    $requiredSupportChannelLookup[[string]$channel] = $true
  }

  $candidateRefs = New-Object System.Collections.Generic.List[string]
  foreach ($ref in $preferred) {
    if (-not $candidateRefs.Contains($ref)) { $candidateRefs.Add($ref) | Out-Null }
  }
  foreach ($ref in $anchorRefs) {
    if (-not $candidateRefs.Contains($ref)) { $candidateRefs.Add($ref) | Out-Null }
  }

  $supportMatches = New-Object System.Collections.Generic.List[object]
  foreach ($ref in @($candidateRefs)) {
    $match = Find-FirstSupportMatch -SourceRef $ref -Patterns $claim.must_match_any
    if ($null -ne $match) {
      $normalizedRef = Normalize-Ref -Ref $match.source_ref
      $supportChannel = if ($anchorLookup.ContainsKey($normalizedRef)) {
        'anchor_queue'
      } elseif ($normalizedRef -eq (Normalize-Ref -Ref $packRef)) {
        'context_pack_metadata'
      } else {
        'explicit_fixture_ref'
      }
      $match | Add-Member -NotePropertyName support_channel -NotePropertyValue $supportChannel
      $supportMatches.Add($match) | Out-Null
    }
  }

  $preferredMatchCount = @($supportMatches | Where-Object {
    $preferredLookup.ContainsKey((Normalize-Ref -Ref $_.source_ref))
  }).Count
  $preferredRequiredChannelMatchCount = @($supportMatches | Where-Object {
    $preferredLookup.ContainsKey((Normalize-Ref -Ref $_.source_ref)) -and
    ($requiredSupportChannels.Count -eq 0 -or $requiredSupportChannelLookup.ContainsKey([string]$_.support_channel))
  }).Count

  $status = 'unsupported'
  $failureOrigin = @()
  if (-not $claim.grounding_check_required) {
    $status = 'not_checked'
  } elseif ($requiredSupportChannels.Count -gt 0 -and $preferredRequiredChannelMatchCount -gt 0) {
    $status = 'supported'
  } elseif ($requiredSupportChannels.Count -gt 0 -and $supportMatches.Count -gt 0) {
    $status = 'weakly_supported'
    $failureOrigin = @('matched_outside_required_support_channel')
  } elseif ($preferredMatchCount -gt 0) {
    $status = 'supported'
  } elseif ($supportMatches.Count -gt 0) {
    $status = 'weakly_supported'
    $failureOrigin = @('matched_non_preferred_anchor')
  } else {
    $status = 'missing_evidence'
    $failureOrigin = if ($configuredFailureOrigin.Count -gt 0) {
      $configuredFailureOrigin
    } else {
      @('retrieval_gap_or_pattern_miss')
    }
  }

  [pscustomobject]@{
    claim_id = $claim.claim_id
    claim_text = $claim.claim_text
    grounding_check_required = [bool]$claim.grounding_check_required
    support_status = $status
    support_kind = 'source_span_support'
    required_support_channels = @($requiredSupportChannels)
    citation_correctness_checked = ($status -in @('supported','weakly_supported'))
    citation_faithfulness_checked = $false
    supporting_anchors = @($supportMatches | Select-Object -First 3)
    warrant = [string]$claim.warrant
    failure_origin = @($failureOrigin)
  }
}

$supportedCount = @($claimResults | Where-Object { $_.support_status -eq 'supported' }).Count
$weakCount = @($claimResults | Where-Object { $_.support_status -eq 'weakly_supported' }).Count
$missingCount = @($claimResults | Where-Object { $_.support_status -eq 'missing_evidence' }).Count
$unsupportedCount = @($claimResults | Where-Object { $_.support_status -eq 'unsupported' }).Count
$notCheckedCount = @($claimResults | Where-Object { $_.support_status -eq 'not_checked' }).Count
$checkedClaims = @($claimResults | Where-Object { $_.grounding_check_required })
$readyForDraft = ($checkedClaims.Count -gt 0 -and $missingCount -eq 0 -and $unsupportedCount -eq 0 -and $weakCount -eq 0)
$answerReadiness = if ($readyForDraft) { 'ready_for_answer_draft' } else { 'not_ready' }
$readinessReason = if ($readyForDraft) {
  'All grounding-required claims have at least source-span support in this sandbox check.'
} else {
  'One or more grounding-required claims lack required source-span support or only have weak support.'
}

$lines = New-Object System.Collections.Generic.List[string]
$lines.Add('---') | Out-Null
$lines.Add('record_kind: evidence_support_check_candidate') | Out-Null
$lines.Add('status: candidate') | Out-Null
$lines.Add("created_at: $createdAt") | Out-Null
$lines.Add("topic_id: $($claimSpec.topic_id)") | Out-Null
$lines.Add('truth_boundary: support_check_review_input_not_truth') | Out-Null
$lines.Add('action_basis_allowed: false') | Out-Null
$lines.Add('truth_mutation_allowed: false') | Out-Null
$lines.Add("context_pack_ref: $packRef") | Out-Null
$lines.Add("claim_spec_ref: $claimSpecRef") | Out-Null
$lines.Add('---') | Out-Null
$lines.Add('') | Out-Null
$lines.Add("# Evidence Support Check v0: $($claimSpec.topic_id)") | Out-Null
$lines.Add('') | Out-Null
$lines.Add('## Query') | Out-Null
$lines.Add('') | Out-Null
$lines.Add('```yaml') | Out-Null
$lines.Add("query: `"$($claimSpec.query -replace '"', "'")`"") | Out-Null
$lines.Add("context_pack_ref: `"$packRef`"") | Out-Null
$lines.Add("claim_spec_ref: `"$claimSpecRef`"") | Out-Null
$lines.Add("anchor_queue_total: $($anchorItems.Count)") | Out-Null
$lines.Add('truth_boundary: support_check_review_input_not_truth') | Out-Null
$lines.Add('action_basis_allowed: false') | Out-Null
$lines.Add('citation_faithfulness_checked: false') | Out-Null
$lines.Add('```') | Out-Null
$lines.Add('') | Out-Null
$lines.Add('## Answer Candidate') | Out-Null
$lines.Add('') | Out-Null
foreach ($sentence in @($claimSpec.answer_candidate)) {
  $lines.Add('- ' + $sentence) | Out-Null
}
$lines.Add('') | Out-Null
$lines.Add('## Claim Support Map') | Out-Null
$lines.Add('') | Out-Null
$lines.Add('```yaml') | Out-Null
$lines.Add('claims:') | Out-Null
foreach ($claim in @($claimResults)) {
  $lines.Add("  - claim_id: $($claim.claim_id)") | Out-Null
  $lines.Add("    claim_text: `"$($claim.claim_text -replace '"', "'")`"") | Out-Null
  $lines.Add(('    grounding_check_required: ' + ($(if ($claim.grounding_check_required) { 'true' } else { 'false' })))) | Out-Null
  $lines.Add("    support_status: $($claim.support_status)") | Out-Null
  $lines.Add("    support_kind: $($claim.support_kind)") | Out-Null
  $lines.Add("    required_support_channels: $(Format-ListInline -Values $claim.required_support_channels)") | Out-Null
  $lines.Add(('    citation_correctness_checked: ' + ($(if ($claim.citation_correctness_checked) { 'true' } else { 'false' })))) | Out-Null
  $lines.Add('    citation_faithfulness_checked: false') | Out-Null
  $lines.Add("    warrant: `"$($claim.warrant -replace '"', "'")`"") | Out-Null
  $lines.Add("    failure_origin: $(Format-ListInline -Values $claim.failure_origin)") | Out-Null
  $lines.Add('    supporting_anchors:') | Out-Null
  foreach ($anchor in @($claim.supporting_anchors)) {
    $lines.Add("      - source_ref: `"$($anchor.source_ref)`"") | Out-Null
    $lines.Add("        selector_or_offset: `"$($anchor.selector_or_offset)`"") | Out-Null
    $lines.Add("        snippet: `"$($anchor.snippet)`"") | Out-Null
    $lines.Add("        support_channel: `"$($anchor.support_channel)`"") | Out-Null
    $lines.Add("        matched_pattern: `"$($anchor.matched_pattern -replace '"', "'")`"") | Out-Null
  }
  if (@($claim.supporting_anchors).Count -eq 0) {
    $lines.Add('      - none') | Out-Null
  }
}
$lines.Add('```') | Out-Null
$lines.Add('') | Out-Null
$lines.Add('## Coverage Overview') | Out-Null
$lines.Add('') | Out-Null
$lines.Add('```yaml') | Out-Null
$lines.Add('coverage_overview:') | Out-Null
$lines.Add("  supported: $supportedCount") | Out-Null
$lines.Add("  weakly_supported: $weakCount") | Out-Null
$lines.Add("  unsupported: $unsupportedCount") | Out-Null
$lines.Add("  missing_evidence: $missingCount") | Out-Null
$lines.Add("  not_checked: $notCheckedCount") | Out-Null
$lines.Add('  known_omissions: []') | Out-Null
$lines.Add("  support_channels: $(Format-ListInline -Values @($claimResults.supporting_anchors | ForEach-Object { $_.support_channel }))") | Out-Null
$lines.Add('answer_readiness:') | Out-Null
$lines.Add("  state: $answerReadiness") | Out-Null
$lines.Add("  reason: `"$readinessReason`"") | Out-Null
$lines.Add('final_support:') | Out-Null
$lines.Add('  state: checked') | Out-Null
$lines.Add('  scope: answer_draft_only') | Out-Null
$lines.Add('  not_action_basis: true') | Out-Null
$lines.Add('warnings:') | Out-Null
$lines.Add('  - citation_faithfulness_not_checked') | Out-Null
$lines.Add('  - scores_are_diagnostic_only') | Out-Null
$lines.Add('  - answer_ready_is_not_action_basis') | Out-Null
$lines.Add('```') | Out-Null
$supportMarkdown = $lines -join "`n"

if ($OutFile) {
  $outDir = Split-Path -Parent $OutFile
  if ($outDir -and -not (Test-Path -LiteralPath $outDir)) {
    New-Item -ItemType Directory -Path $outDir | Out-Null
  }
  Set-Content -LiteralPath $OutFile -Value $supportMarkdown -Encoding UTF8
}

$answerReadyMarkdown = ''
if ($AnswerReadyOutFile) {
  $readyLines = New-Object System.Collections.Generic.List[string]
  $readyLines.Add('---') | Out-Null
  $readyLines.Add('record_kind: answer_ready_context_pack_candidate') | Out-Null
  $readyLines.Add('status: candidate') | Out-Null
  $readyLines.Add("created_at: $createdAt") | Out-Null
  $readyLines.Add("topic_id: $($claimSpec.topic_id)") | Out-Null
  $readyLines.Add('truth_boundary: answer_preparation_not_truth') | Out-Null
  $readyLines.Add('action_basis_allowed: false') | Out-Null
  $readyLines.Add('truth_mutation_allowed: false') | Out-Null
  $readyLines.Add("source_pack_ref: $packRef") | Out-Null
  $readyLines.Add("evidence_support_check_ref: $(Get-DisplayRef -Path $OutFile)") | Out-Null
  $readyLines.Add('---') | Out-Null
  $readyLines.Add('') | Out-Null
  $readyLines.Add("# Answer-Ready Context Pack v0: $($claimSpec.topic_id)") | Out-Null
  $readyLines.Add('') | Out-Null
  $readyLines.Add('```yaml') | Out-Null
  $readyLines.Add('final_support:') | Out-Null
  $readyLines.Add('  state: checked') | Out-Null
  $readyLines.Add('  scope: answer_draft_only') | Out-Null
  $readyLines.Add('  not_action_basis: true') | Out-Null
  $readyLines.Add('claim_evidence_map:') | Out-Null
  foreach ($claim in @($claimResults)) {
    $readyLines.Add("  - claim_id: $($claim.claim_id)") | Out-Null
    $readyLines.Add("    answer_sentence: `"$($claim.claim_text -replace '"', "'")`"") | Out-Null
    $readyLines.Add("    support_status: $($claim.support_status)") | Out-Null
    $readyLines.Add("    required_support_channels: $(Format-ListInline -Values $claim.required_support_channels)") | Out-Null
    $readyLines.Add("    source_refs: $(Format-ListInline -Values @($claim.supporting_anchors | ForEach-Object { $_.source_ref }))") | Out-Null
    $readyLines.Add("    selectors: $(Format-ListInline -Values @($claim.supporting_anchors | ForEach-Object { $_.selector_or_offset }))") | Out-Null
    $readyLines.Add("    support_channels: $(Format-ListInline -Values @($claim.supporting_anchors | ForEach-Object { $_.support_channel }))") | Out-Null
    $readyLines.Add("    failure_origin: $(Format-ListInline -Values $claim.failure_origin)") | Out-Null
    $readyLines.Add("    warrant: `"$($claim.warrant -replace '"', "'")`"") | Out-Null
  }
  $readyLines.Add('coverage_overview:') | Out-Null
  $readyLines.Add("  supported: $supportedCount") | Out-Null
  $readyLines.Add("  weakly_supported: $weakCount") | Out-Null
  $readyLines.Add("  unsupported: $unsupportedCount") | Out-Null
  $readyLines.Add("  missing_evidence: $missingCount") | Out-Null
  $readyLines.Add('answer_readiness:') | Out-Null
  $readyLines.Add("  state: $answerReadiness") | Out-Null
  $readyLines.Add('  required_next_step: human review before action-facing use') | Out-Null
  $readyLines.Add('warnings:') | Out-Null
  $readyLines.Add('  - answer_ready_is_not_action_basis') | Out-Null
  $readyLines.Add('  - support_check_is_review_input_not_truth') | Out-Null
  $readyLines.Add('```') | Out-Null
  $answerReadyMarkdown = $readyLines -join "`n"
  $readyOutDir = Split-Path -Parent $AnswerReadyOutFile
  if ($readyOutDir -and -not (Test-Path -LiteralPath $readyOutDir)) {
    New-Item -ItemType Directory -Path $readyOutDir | Out-Null
  }
  Set-Content -LiteralPath $AnswerReadyOutFile -Value $answerReadyMarkdown -Encoding UTF8
}

$result = [pscustomobject]@{
  record_kind = 'evidence_support_check_result_candidate'
  context_pack_ref = $packRef
  claim_spec_ref = $claimSpecRef
  out_file = $OutFile
  answer_ready_out_file = $AnswerReadyOutFile
  anchor_queue_total = $anchorItems.Count
  claims_checked = $claimResults.Count
  supported = $supportedCount
  weakly_supported = $weakCount
  unsupported = $unsupportedCount
  missing_evidence = $missingCount
  answer_readiness = $answerReadiness
  action_basis_allowed = $false
  citation_faithfulness_checked = $false
}

if ($Json) {
  $result | ConvertTo-Json -Depth 5
} elseif ($OutFile -or $AnswerReadyOutFile) {
  $result | Format-List
} else {
  $supportMarkdown
}
