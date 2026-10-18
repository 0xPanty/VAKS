param(
  [string]$Root = 'outputs/review/source-intake-tag-routing-sandbox-2026-06-07/fixtures',
  [switch]$Json
)

$ErrorActionPreference = 'Stop'
$resolvedRoot = (Resolve-Path -LiteralPath $Root).Path
$allowedTopics = @(
  'source-intake',
  'metadata-routing',
  'retrieval',
  'context-pack',
  'candidate-distillation',
  'project-overlay',
  'evidence-support',
  'rag-evaluation',
  'agent-memory',
  'obsidian-workbench',
  'entity-routing',
  'feedback-cache'
)
$authorityWords = @(
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
  param([System.Collections.Generic.List[string]]$Issues, [string]$Issue)
  $Issues.Add($Issue) | Out-Null
}

function Test-AuthorityWord {
  param([string]$Value)
  $lower = $Value.ToLowerInvariant()
  foreach ($word in $authorityWords) {
    if ($lower -eq $word -or $lower -like "*$word*") { return $true }
  }
  return $false
}

$files = Get-ChildItem -LiteralPath $resolvedRoot -Recurse -Filter '*.md' -File
$results = foreach ($file in $files) {
  $text = Get-Content -Raw -LiteralPath $file.FullName
  $fm = Get-FrontMatter -Text $text
  $type = Get-ScalarField -FrontMatter $fm -Name 'type'
  $recordKind = Get-ScalarField -FrontMatter $fm -Name 'record_kind'
  $actionBasisAllowed = Get-ScalarField -FrontMatter $fm -Name 'action_basis_allowed'
  $issues = New-Object System.Collections.Generic.List[string]

  if ($type -eq 'source') {
    $topics = Get-YamlList -FrontMatter $fm -Name 'topics'
    $entities = Get-YamlList -FrontMatter $fm -Name 'entities'
    $aliases = Get-YamlList -FrontMatter $fm -Name 'aliases'
    $tags = Get-YamlList -FrontMatter $fm -Name 'tags'

    if ($topics.Count -gt 2) { Add-Issue -Issues $issues -Issue "too_many_topics:$($topics.Count)" }
    foreach ($topic in $topics) {
      if ($allowedTopics -notcontains $topic) { Add-Issue -Issues $issues -Issue "topic_not_in_candidate_registry:$topic" }
      if (Test-AuthorityWord -Value $topic) { Add-Issue -Issues $issues -Issue "authority_topic:$topic" }
    }
    foreach ($value in @($entities + $aliases + $tags)) {
      if (Test-AuthorityWord -Value $value) { Add-Issue -Issues $issues -Issue "authority_metadata:$value" }
    }
    if ($actionBasisAllowed -eq 'true') {
      Add-Issue -Issues $issues -Issue 'source_metadata_sets_action_basis'
    }
  }

  if ($recordKind -eq 'intake_metadata_suggestion') {
    $persistent = Get-ScalarField -FrontMatter $fm -Name 'persistent_main_note_allowed'
    $defaultRetrieval = Get-ScalarField -FrontMatter $fm -Name 'default_retrieval_allowed'
    $suggestedTopics = Get-YamlList -FrontMatter $fm -Name 'suggested_topics'
    $suggestedEntities = Get-YamlList -FrontMatter $fm -Name 'suggested_entities'
    $routingHints = Get-YamlList -FrontMatter $fm -Name 'suggested_routing_hint'
    $queryFilters = Get-YamlList -FrontMatter $fm -Name 'suggested_query_time_filters'
    $confirmationRequired = Get-YamlList -FrontMatter $fm -Name 'confirmation_required_for'

    if ($persistent -ne 'false') { Add-Issue -Issues $issues -Issue 'suggestion_persistent_main_note_allowed_not_false' }
    if ($defaultRetrieval -ne 'false') { Add-Issue -Issues $issues -Issue 'suggestion_default_retrieval_allowed_not_false' }
    foreach ($topic in $suggestedTopics) {
      if ($allowedTopics -notcontains $topic) { Add-Issue -Issues $issues -Issue "suggested_topic_not_in_candidate_registry:$topic" }
      if (Test-AuthorityWord -Value $topic) { Add-Issue -Issues $issues -Issue "suggested_authority_topic:$topic" }
    }
    foreach ($value in @($suggestedEntities + $routingHints + $queryFilters)) {
      if (Test-AuthorityWord -Value $value) { Add-Issue -Issues $issues -Issue "suggested_authority_metadata:$value" }
    }
    foreach ($required in @('write_to_source_card','reviewed_or_action_use')) {
      if (-not ($confirmationRequired | Where-Object { $_ -eq $required })) {
        Add-Issue -Issues $issues -Issue "suggestion_missing_confirmation_required_for:$required"
      }
    }
  }

  if ($issues.Count -eq 0 -and $type -ne 'source' -and $recordKind -ne 'intake_metadata_suggestion') {
    continue
  }

  [pscustomobject]@{
    file = $file.FullName.Substring($resolvedRoot.Length).TrimStart('\')
    record_kind = if ($recordKind) { $recordKind } else { $type }
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
