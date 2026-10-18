param(
  [string]$Root = 'outputs/review/source-intake-tag-routing-sandbox-2026-06-07/fixtures',
  [switch]$Json
)

$ErrorActionPreference = 'Stop'
$resolvedRoot = (Resolve-Path -LiteralPath $Root).Path
$authorityPattern = '(reviewed|approved|adopt|action|truth|safe|decision|best)'

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

$files = Get-ChildItem -LiteralPath $resolvedRoot -Recurse -Filter '*.md' -File
$results = foreach ($file in $files) {
  $text = Get-Content -Raw -LiteralPath $file.FullName
  $fm = Get-FrontMatter -Text $text
  $recordKind = Get-ScalarField -FrontMatter $fm -Name 'record_kind'
  $isCandidateDistillation = ($recordKind -eq 'candidate_distillation' -or $file.Name -like '*candidate-distillation*.md')
  if (-not $isCandidateDistillation) { continue }

  $kpRefs = @([regex]::Matches($text, '(?m)^\s*-\s*kp_ref:\s*(\S+)\s*$') | ForEach-Object { $_.Groups[1].Value.Trim() })
  $issues = New-Object System.Collections.Generic.List[string]

  if ($text -match '(?m)^\s*candidate_points:\s*$' -and $kpRefs.Count -eq 0) {
    $issues.Add('candidate_points_without_kp_ref')
  }
  foreach ($kp in $kpRefs) {
    if ($kp -notmatch '^KP-\d{3}$') {
      $issues.Add("kp_ref_bad_format:$kp")
    }
    if ($kp -match $authorityPattern) {
      $issues.Add("kp_ref_authority_word:$kp")
    }
  }
  $duplicates = @($kpRefs | Group-Object | Where-Object { $_.Count -gt 1 } | Select-Object -ExpandProperty Name)
  foreach ($dup in $duplicates) {
    $issues.Add("duplicate_kp_ref:$dup")
  }

  [pscustomobject]@{
    file = $file.FullName.Substring($resolvedRoot.Length).TrimStart('\')
    kp_ref_count = $kpRefs.Count
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
  } | ConvertTo-Json -Depth 5
} else {
  $summary | Format-List
  $results | Format-Table -AutoSize
}
