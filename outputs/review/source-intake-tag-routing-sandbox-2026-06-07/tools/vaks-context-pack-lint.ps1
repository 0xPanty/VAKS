param(
  [string]$Root = 'outputs/review/source-intake-tag-routing-sandbox-2026-06-07',
  [switch]$Json
)

$ErrorActionPreference = 'Stop'
$resolvedRoot = (Resolve-Path -LiteralPath $Root).Path

function Get-FrontMatter {
  param([string]$Text)
  $lines = $Text -split "`r?`n"
  if ($lines.Count -lt 3 -or $lines[0].Trim() -ne '---') { return '' }
  $buffer = New-Object System.Collections.Generic.List[string]
  for ($i = 1; $i -lt $lines.Count; $i++) {
    if ($lines[$i].Trim() -eq '---') { break }
    $buffer.Add($lines[$i])
  }
  return ($buffer -join "`n")
}

function Get-ScalarField {
  param([string]$FrontMatter, [string]$Name)
  $match = [regex]::Match($FrontMatter, "(?m)^\s*$([regex]::Escape($Name)):\s*(.+?)\s*$")
  if ($match.Success) { return $match.Groups[1].Value.Trim().Trim('"').Trim("'") }
  return ''
}

function Add-Issue {
  param([System.Collections.Generic.List[string]]$Issues, [string]$Issue)
  $Issues.Add($Issue) | Out-Null
}

$files = Get-ChildItem -LiteralPath $resolvedRoot -Recurse -Filter '*.md' -File
$results = foreach ($file in $files) {
  $text = Get-Content -Raw -LiteralPath $file.FullName
  $fm = Get-FrontMatter -Text $text
  $recordKind = Get-ScalarField -FrontMatter $fm -Name 'record_kind'
  if ($recordKind -ne 'context_pack_manifest_candidate') { continue }

  $issues = New-Object System.Collections.Generic.List[string]
  $truthBoundary = Get-ScalarField -FrontMatter $fm -Name 'truth_boundary'
  if ($truthBoundary -ne 'activation_pack_not_truth') {
    Add-Issue -Issues $issues -Issue 'context_pack_truth_boundary_not_activation_only'
  }

  $candidateLeak = [regex]::IsMatch(
    $text,
    '(?is)lane:\s*candidate_orientation.*?(citable_status:\s*span_ready|action_basis_allowed:\s*true)'
  )
  if ($candidateLeak) {
    Add-Issue -Issues $issues -Issue 'candidate_item_action_leak'
  }

  $nonAnchorLeak = [regex]::IsMatch(
    $text,
    '(?is)lane:\s*(active_project_overlay|audit_evidence|feedback_diagnostics|support_review_output).*?action_basis_allowed:\s*true'
  )
  if ($nonAnchorLeak) {
    Add-Issue -Issues $issues -Issue 'non_anchor_lane_action_leak'
  }

  if ($text -match '\$\(@\{' -or $text -match '\$\([A-Za-z_]') {
    Add-Issue -Issues $issues -Issue 'unrendered_powershell_interpolation'
  }

  $mentionsRrf = $text -match '(?i)fusion_method:\s*.*(rrf|reciprocal)'
  $hasBucketGuard = $text -match '(?i)(same_authority_bucket|no_cross_lane_rrf|lane_grouping_only_no_cross_lane_rrf)'
  if ($mentionsRrf -and -not $hasBucketGuard) {
    Add-Issue -Issues $issues -Issue 'cross_lane_rrf_phrase_without_bucket_guard'
  }

  if ($text -notmatch 'evidence_support_check_not_run') {
    Add-Issue -Issues $issues -Issue 'missing_evidence_support_check_warning'
  }

  if ($text -match 'selector_or_offset:\s*""') {
    Add-Issue -Issues $issues -Issue 'missing_selector_or_offset'
  }

  if ($text -match '## Pack Items' -and $text -notmatch 'snippet_status:\s*navigation_snippet_not_evidence') {
    Add-Issue -Issues $issues -Issue 'missing_navigation_snippet_boundary'
  }

  $mode = Get-ScalarField -FrontMatter $fm -Name 'mode'
  if ($mode -eq 'action') {
    if ($text -notmatch 'final_support:\s*\r?\n\s*state:\s*none') {
      Add-Issue -Issues $issues -Issue 'action_pack_missing_final_support_none'
    }
    if ($text -notmatch 'anchor_queue:') {
      Add-Issue -Issues $issues -Issue 'action_pack_missing_anchor_queue'
    }
    if ($text -match 'action_role:\s*support') {
      Add-Issue -Issues $issues -Issue 'action_role_mislabels_anchor_as_support'
    }
  }

  if ($text -notmatch 'Excluded Or Not Default' -and $text -notmatch 'ignored_sources') {
    Add-Issue -Issues $issues -Issue 'missing_exclusion_or_noise_section'
  }

  [pscustomobject]@{
    file = $file.FullName.Substring($resolvedRoot.Length).TrimStart('\')
    status = if ($issues.Count -eq 0) { 'pass' } else { 'fail' }
    issues = @($issues)
  }
}

$summary = [pscustomobject]@{
  files_checked = @($results).Count
  pass = @($results | Where-Object { $_.status -eq 'pass' }).Count
  fail = @($results | Where-Object { $_.status -eq 'fail' }).Count
}

if ($Json) {
  [pscustomobject]@{
    summary = $summary
    results = @($results)
  } | ConvertTo-Json -Depth 6
} else {
  $summary | Format-List
  $results | Format-Table -AutoSize
}
