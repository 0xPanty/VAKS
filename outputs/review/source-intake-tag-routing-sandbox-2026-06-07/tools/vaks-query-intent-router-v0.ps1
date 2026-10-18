param(
  [Parameter(Mandatory = $true)]
  [string]$Query,
  [string]$RouterPath = '',
  [switch]$Json
)

$ErrorActionPreference = 'Stop'

if ([string]::IsNullOrWhiteSpace($RouterPath)) {
  $RouterPath = Join-Path (Split-Path -Parent $PSScriptRoot) 'fixtures/query-intent-router-v0.json'
}

if (-not (Test-Path -LiteralPath $RouterPath)) {
  throw "Missing router fixture: $RouterPath"
}

$router = Get-Content -Raw -LiteralPath $RouterPath -Encoding UTF8 | ConvertFrom-Json
$stopWords = @(
  'the','this','that','these','those','can','could','would','should','what',
  'when','where','which','who','why','how','for','with','and','from','show',
  'use','used','using','into','onto','does','did','has','have','had','is',
  'are','was','were','me','my','our','your'
)

function ConvertTo-TermList {
  param($Values)
  $terms = New-Object System.Collections.Generic.List[string]
  foreach ($value in @($Values)) {
    if ($null -eq $value) { continue }
    $text = [string]$value
    foreach ($part in ($text -split '[\s,;|/\\()\[\]{}:]+')) {
      $clean = $part.Trim().Trim('"').Trim("'")
      $lower = $clean.ToLowerInvariant()
      if ($clean.Length -ge 2 -and -not ($stopWords -contains $lower) -and -not $terms.Contains($clean)) {
        $terms.Add($clean) | Out-Null
      }
    }
  }
  return $terms.ToArray()
}

function Test-ContainsPhrase {
  param([string]$Text, [string]$Phrase)
  if ([string]::IsNullOrWhiteSpace($Phrase)) { return $false }
  return $Text.IndexOf($Phrase, [StringComparison]::OrdinalIgnoreCase) -ge 0
}

$queryText = $Query.Trim()
$auditIntent = $queryText -match '(?i)(why|exclude|excluded|audit|check|test|lint|regression|what changed|guardrail|boundary)'
$scored = foreach ($mode in @($router.modes)) {
  $score = 0
  $matched = New-Object System.Collections.Generic.List[string]

  foreach ($keyword in @($mode.keywords)) {
    if (Test-ContainsPhrase -Text $queryText -Phrase $keyword) {
      $score += 4
      if (-not $matched.Contains($keyword)) { $matched.Add($keyword) | Out-Null }
    }
  }

  foreach ($example in @($mode.examples)) {
    foreach ($term in (ConvertTo-TermList -Values @($example))) {
      if ($term.Length -lt 3) { continue }
      if (Test-ContainsPhrase -Text $queryText -Phrase $term) {
        $score += 1
        if (-not $matched.Contains($term)) { $matched.Add($term) | Out-Null }
      }
    }
  }

  # Safety override: if the question smells like decision support, prefer action
  # routing even when it also contains research/source terms.
  if ($mode.mode -eq 'audit' -and $auditIntent) {
    $score += 10
    if (-not $matched.Contains('audit_intent_override')) {
      $matched.Add('audit_intent_override') | Out-Null
    }
  }

  if ($mode.mode -eq 'action' -and -not $auditIntent -and $queryText -match '(?i)(action|decision|basis|support|evidence|should we|can we use|safe to|production|final answer)') {
    $score += 8
    if (-not $matched.Contains('action_safety_override')) {
      $matched.Add('action_safety_override') | Out-Null
    }
  }

  [pscustomobject]@{
    mode = $mode.mode
    score = $score
    matched_terms = @($matched)
    pattern_fragments = @($mode.pattern_fragments)
    warnings = @($mode.warnings)
    route_bias = @($mode.route_bias)
    plain_rule = $mode.plain_rule
  }
}

$selected = @($scored | Sort-Object @{ Expression = { $_.score }; Descending = $true }, mode | Select-Object -First 1)[0]
$fallbackUsed = $false
if ($null -eq $selected -or $selected.score -le 0) {
  $selected = @($scored | Where-Object { $_.mode -eq $router.default_mode } | Select-Object -First 1)[0]
  $fallbackUsed = $true
}

$confidence = 'low'
if ($selected.score -ge 10) {
  $confidence = 'high'
} elseif ($selected.score -ge 4) {
  $confidence = 'medium'
}

$warnings = New-Object System.Collections.Generic.List[string]
foreach ($warning in @($selected.warnings)) {
  if ($warning -and -not $warnings.Contains($warning)) { $warnings.Add($warning) | Out-Null }
}
if ($fallbackUsed) {
  $warnings.Add($router.fallback_warning) | Out-Null
}

$patternParts = New-Object System.Collections.Generic.List[string]
foreach ($fragment in @($selected.pattern_fragments)) {
  if ($fragment -and -not $patternParts.Contains($fragment)) {
    $patternParts.Add($fragment) | Out-Null
  }
}
foreach ($term in (ConvertTo-TermList -Values @($queryText))) {
  if ($term.Length -ge 3 -and -not $patternParts.Contains($term)) {
    $patternParts.Add($term) | Out-Null
  }
}

$result = [pscustomobject]@{
  record_kind = 'query_intent_router_result_candidate'
  query = $queryText
  selected_mode = $selected.mode
  confidence = $confidence
  fallback_used = $fallbackUsed
  score = $selected.score
  matched_terms = @($selected.matched_terms)
  route_bias = @($selected.route_bias)
  pattern = (@($patternParts) -join '|')
  warnings = @($warnings)
  truth_boundary = 'navigation_only_not_truth'
  action_basis_allowed = $false
  plain_rule = $selected.plain_rule
  router_ref = ($RouterPath -replace '\\','/')
}

if ($Json) {
  $result | ConvertTo-Json -Depth 6
} else {
  $result | Format-List
}
