param(
  [string]$Root = 'outputs/review/source-intake-tag-routing-sandbox-2026-06-07/fixtures',
  [switch]$Json
)

$ErrorActionPreference = 'Stop'
$resolvedRoot = (Resolve-Path -LiteralPath $Root).Path
$forbiddenTagWords = @(
  'reviewed','approved','adopted','use-this','best-practice','truth','safe',
  'action-basis','decision','verified','high-confidence','for-vaks',
  'do-not-borrow-for-vaks','adopt-for-vaks'
)

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

function Get-YamlList {
  param([string]$FrontMatter, [string]$Name)
  $lines = $FrontMatter -split "`n"
  $values = New-Object System.Collections.Generic.List[string]
  $inList = $false
  foreach ($line in $lines) {
    if ($line -match "^$([regex]::Escape($Name)):\s*\[(.*)\]\s*$") {
      $inline = $Matches[1].Trim()
      if ($inline.Length -gt 0) {
        foreach ($part in ($inline -split ',')) {
          $values.Add($part.Trim().Trim('"').Trim("'"))
        }
      }
      $inList = $false
      continue
    }
    if ($line -match "^$([regex]::Escape($Name)):\s*$") {
      $inList = $true
      continue
    }
    if ($inList -and $line -match '^\S[^:]*:\s*') {
      $inList = $false
    }
    if ($inList -and $line -match '^\s*-\s*(.+?)\s*$') {
      $values.Add($Matches[1].Trim().Trim('"').Trim("'"))
    }
  }
  return @($values)
}

function Add-Issue {
  param(
    [System.Collections.Generic.List[string]]$Issues,
    [string]$Issue
  )
  $Issues.Add($Issue) | Out-Null
}

$files = Get-ChildItem -LiteralPath $resolvedRoot -Recurse -Filter '*.md' -File
$results = foreach ($file in $files) {
  $text = Get-Content -Raw -LiteralPath $file.FullName
  $fm = Get-FrontMatter -Text $text
  $recordKind = Get-ScalarField -FrontMatter $fm -Name 'record_kind'
  $truthBoundary = Get-ScalarField -FrontMatter $fm -Name 'truth_boundary'
  $allowedUse = Get-YamlList -FrontMatter $fm -Name 'allowed_use'
  $forbiddenUse = Get-YamlList -FrontMatter $fm -Name 'forbidden_use'
  $defaultExclude = Get-YamlList -FrontMatter $fm -Name 'default_exclude_lanes'
  $issues = New-Object System.Collections.Generic.List[string]

  foreach ($word in $forbiddenTagWords) {
    if ($allowedUse | Where-Object { $_.ToLowerInvariant() -eq $word }) {
      Add-Issue -Issues $issues -Issue "forbidden_allowed_use:$word"
    }
  }

  if ($recordKind -in @('artifact_registry_candidate','context_pack_manifest_candidate','obsidian_workbench_entrypoint_candidate')) {
    if ($truthBoundary -match '(?i)reviewed|truth_source|action_basis') {
      Add-Issue -Issues $issues -Issue 'usage_layer_truth_boundary_leak'
    }
  }

  if ($recordKind -eq 'artifact_registry_candidate') {
    foreach ($required in @('truth','reviewed_relation','action_basis')) {
      if (-not ($forbiddenUse | Where-Object { $_ -eq $required })) {
        Add-Issue -Issues $issues -Issue "registry_missing_forbidden_use:$required"
      }
    }
    if ($text -match '(?i)artifact exists\s*->\s*artifact is true') {
      Add-Issue -Issues $issues -Issue 'registry_truth_inference_phrase'
    }
  }

  if ($recordKind -eq 'context_pack_manifest_candidate') {
    foreach ($requiredText in @('coverage_overview','context_pack_trace')) {
      if ($text -notmatch [regex]::Escape($requiredText)) {
        Add-Issue -Issues $issues -Issue "context_pack_missing:$requiredText"
      }
    }
    $candidateActionLeak = [regex]::IsMatch(
      $text,
      '(?is)lane:\s*candidate_orientation.*?(citable_status:\s*span_ready|action_basis_allowed:\s*true)'
    )
    if ($candidateActionLeak) {
      Add-Issue -Issues $issues -Issue 'candidate_item_action_leak'
    }
  }

  if ($recordKind -eq 'obsidian_workbench_entrypoint_candidate') {
    foreach ($required in @('truth','reviewed_relation','action_basis','ontology')) {
      if (-not ($forbiddenUse | Where-Object { $_ -eq $required })) {
        Add-Issue -Issues $issues -Issue "entrypoint_missing_forbidden_use:$required"
      }
    }
    foreach ($requiredExclusion in @('old_sandbox','package_copy','baseline_copy','archived_overlay')) {
      if (-not ($defaultExclude | Where-Object { $_ -eq $requiredExclusion })) {
        Add-Issue -Issues $issues -Issue "entrypoint_missing_default_exclusion:$requiredExclusion"
      }
    }
  }

  [pscustomobject]@{
    file = $file.FullName.Substring($resolvedRoot.Length).TrimStart('\')
    record_kind = $recordKind
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
