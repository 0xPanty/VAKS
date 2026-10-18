param(
  [string]$Pattern = 'source intake|source-intake|retrieval_policy|candidate_not_action_basis',
  [ValidateSet('current-rule','research','action','source-inspection','audit','project-exploration')]
  [string]$Mode = 'current-rule',
  [string]$Root = '.',
  [int]$Limit = 200,
  [switch]$Json
)

$ErrorActionPreference = 'Stop'

$resolvedRoot = (Resolve-Path -LiteralPath $Root).Path
$forbiddenTags = @(
  'reviewed',
  'approved',
  'adopted',
  'use-this',
  'best-practice',
  'truth',
  'safe',
  'action-basis',
  'decision',
  'verified',
  'high-confidence',
  'for-vaks',
  'do-not-borrow-for-vaks',
  'adopt-for-vaks'
)

function Get-RelativePath {
  param([string]$Path)
  $full = (Resolve-Path -LiteralPath $Path).Path
  return $full.Substring($resolvedRoot.Length).TrimStart('\')
}

function Get-FrontMatter {
  param([string]$Text)
  $lines = $Text -split "`r?`n"
  if ($lines.Count -lt 3 -or $lines[0].Trim() -ne '---') {
    return ''
  }
  $buffer = New-Object System.Collections.Generic.List[string]
  for ($i = 1; $i -lt $lines.Count; $i++) {
    if ($lines[$i].Trim() -eq '---') {
      break
    }
    $buffer.Add($lines[$i])
  }
  return ($buffer -join "`n")
}

function Get-ScalarField {
  param(
    [string]$FrontMatter,
    [string]$Name
  )
  $match = [regex]::Match($FrontMatter, "(?m)^\s*$([regex]::Escape($Name)):\s*(.+?)\s*$")
  if ($match.Success) {
    return $match.Groups[1].Value.Trim().Trim('"').Trim("'")
  }
  return ''
}

function Get-YamlList {
  param(
    [string]$FrontMatter,
    [string]$Name
  )
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

function Get-PathRole {
  param(
    [string]$RelativePath,
    [string]$RecordKind,
    [string]$Type
  )
  $p = $RelativePath -replace '/', '\'

  if ($p -like 'outputs\review\source-intake-tag-routing-sandbox-2026-06-07\*') { return 'new_sandbox_package' }
  if ($p -like '00_handoff\*') { return 'handoff' }
  if ($p -eq 'AGENTS.md') { return 'project_guide' }
  if ($p -like 'templates\*') { return 'formal_template' }
  if ($p -like 'wiki\indexes\*') { return 'index' }
  if ($p -in @('SOURCE_INTAKE.md','README.md','purpose.md','SCHEMA.md','ARCHITECTURE_PRINCIPLES.md','IMPLEMENTATION_BLUEPRINT.md','REFERENCE_REVIEW_PROTOCOL.md','DEV_CONTEXT.md','MEMORY_TIER.md','REVIEW_QUEUE.md','FEEDBACK.md','FUSION_ARCHITECTURE_V0_2_DRAFT.md','SECOND_BRAIN_MODEL.md')) { return 'mainline_doc' }
  if ($p -like 'raw\repos\_snapshots\*') { return 'repo_snapshot' }
  if ($p -like 'raw\articles\*' -or $p -like 'raw\videos\*' -or $p -like 'raw\repos\*' -or $p -like 'raw\papers\*') { return 'source_card' }
  if ($p -like 'outputs\feedback\*' -or $RecordKind -eq 'feedback_event') { return 'feedback_event' }
  if ($p -like 'outputs\review\project_overlays\*' -or $RecordKind -eq 'project_overlay') { return 'project_overlay' }
  if ($p -like 'outputs\review\*candidate-distillation.md' -or $RecordKind -eq 'candidate_distillation') { return 'candidate_distillation' }
  if ($p -like 'wiki\projects\*') { return 'project_note' }
  if ($p -like 'wiki\summaries\*') { return 'summary' }
  if ($p -like 'outputs\qa\*') { return 'qa_output' }
  if ($p -like 'wiki\claims\*' -or $p -like 'wiki\patterns\*' -or $p -like 'wiki\anti-patterns\*' -or $p -like 'wiki\decisions\*' -or $p -like 'wiki\concepts\*') { return 'reviewed_knowledge' }
  if ($p -like 'outputs\review\*PRO_*' -or $p -like 'outputs\review\*pro-review*' -or $p -like 'outputs\review\*.zip') { return 'pro_package' }
  if ($p -like 'outputs\review\*sandbox*' -or $p -like 'outputs\review\*checks*' -or $p -like 'outputs\review\*baseline*' -or $p -like 'outputs\review\*package*') { return 'audit_package' }
  if ($p -like 'outputs\review\*') { return 'review_output' }
  return 'legacy_or_unknown'
}

function Get-Lane {
  param([string]$PathRole)
  switch ($PathRole) {
    { $_ -in @('mainline_doc','project_guide','formal_template','handoff','index') } { return 'mainline_current' }
    'candidate_distillation' { return 'candidate_orientation' }
    { $_ -in @('source_card','repo_snapshot') } { return 'raw_drilldown' }
    'project_overlay' { return 'active_project_overlay' }
    { $_ -in @('audit_package','pro_package','new_sandbox_package') } { return 'audit_evidence' }
    'feedback_event' { return 'feedback_diagnostics' }
    'reviewed_knowledge' { return 'reviewed_support' }
    { $_ -in @('review_output','summary','project_note','qa_output') } { return 'support_review_output' }
    default { return 'other_needs_triage' }
  }
}

function Get-LaneOrder {
  param([string]$Lane)
  switch ($Lane) {
    'mainline_current' { return 10 }
    'reviewed_support' { return 20 }
    'raw_drilldown' { return 30 }
    'candidate_orientation' { return 40 }
    'active_project_overlay' { return 50 }
    'support_review_output' { return 60 }
    'audit_evidence' { return 70 }
    'feedback_diagnostics' { return 80 }
    default { return 90 }
  }
}

function Test-IncludedByDefault {
  param(
    [string]$Lane,
    [string]$Mode
  )
  switch ($Mode) {
    'current-rule' { return $Lane -eq 'mainline_current' }
    'research' { return $Lane -in @('reviewed_support','candidate_orientation','raw_drilldown','active_project_overlay','support_review_output') }
    'action' { return $Lane -in @('reviewed_support','mainline_current','raw_drilldown') }
    'source-inspection' { return $Lane -in @('raw_drilldown','candidate_orientation') }
    'audit' { return $Lane -in @('audit_evidence','mainline_current') }
    'project-exploration' { return $Lane -in @('mainline_current','candidate_orientation','raw_drilldown','active_project_overlay','support_review_output') }
  }
}

if ([string]::IsNullOrWhiteSpace($Pattern)) {
  $files = Get-ChildItem -LiteralPath $resolvedRoot -Recurse -Filter '*.md' -File | Select-Object -ExpandProperty FullName
} elseif (Get-Command rg -ErrorAction SilentlyContinue) {
  $files = & rg -l -i --glob '*.md' -- $Pattern $resolvedRoot 2>$null
} else {
  $files = Get-ChildItem -LiteralPath $resolvedRoot -Recurse -Filter '*.md' -File |
    Select-String -Pattern $Pattern -CaseSensitive:$false -List |
    ForEach-Object { $_.Path }
}

$files = @($files |
  Where-Object { $_ -and (Test-Path -LiteralPath $_) } |
  Select-Object -Unique |
  Sort-Object)
$allResults = foreach ($file in $files) {
  $text = Get-Content -Raw -LiteralPath $file
  $fm = Get-FrontMatter -Text $text
  $recordKind = Get-ScalarField -FrontMatter $fm -Name 'record_kind'
  $recordType = Get-ScalarField -FrontMatter $fm -Name 'record_type'
  $type = Get-ScalarField -FrontMatter $fm -Name 'type'
  $knowledgeStatus = Get-ScalarField -FrontMatter $fm -Name 'knowledge_status'
  $warningCode = Get-ScalarField -FrontMatter $fm -Name 'warning_code'
  $tags = Get-YamlList -FrontMatter $fm -Name 'tags'
  $rel = Get-RelativePath -Path $file
  $pathRole = Get-PathRole -RelativePath $rel -RecordKind $recordKind -Type $type
  $lane = Get-Lane -PathRole $pathRole
  $isIntakeSurface = (
    $type -eq 'source' -or
    $recordKind -in @('candidate_distillation','project_overlay','feedback_event','intake_metadata_suggestion') -or
    $recordType -eq 'query-run' -or
    $pathRole -in @('source_card','candidate_distillation','project_overlay','feedback_event')
  )
  $badTags = @()
  if ($isIntakeSurface) {
    $badTags = @($tags | Where-Object { $forbiddenTags -contains $_.ToLowerInvariant() })
  }
  $warnings = New-Object System.Collections.Generic.List[string]
  if ($badTags.Count -gt 0) { $warnings.Add('forbidden_authority_tag') }
  if ($lane -eq 'candidate_orientation') { $warnings.Add('candidate_not_action_basis') }
  if ($lane -eq 'raw_drilldown' -and $knowledgeStatus -eq 'raw') { $warnings.Add('raw_is_provenance_only') }
  if ($lane -eq 'active_project_overlay') { $warnings.Add('overlay_not_authority') }
  if ($lane -eq 'feedback_diagnostics') { $warnings.Add('feedback_not_truth') }
  if ($lane -eq 'other_needs_triage') { $warnings.Add('needs_triage') }

  [pscustomobject]@{
    file = $rel
    path_role = $pathRole
    lane = $lane
    included_by_default = (Test-IncludedByDefault -Lane $lane -Mode $Mode)
    knowledge_status = $knowledgeStatus
    warning_code = $warningCode
    forbidden_tags = @($badTags)
    warnings = @($warnings)
  }
}

$results = @($allResults |
  Sort-Object @{ Expression = { Get-LaneOrder -Lane $_.lane } }, file |
  Select-Object -First $Limit)

$summary = $results | Group-Object lane | Sort-Object Name | ForEach-Object {
  [pscustomobject]@{ lane = $_.Name; count = $_.Count; included_by_default = @($_.Group | Where-Object { $_.included_by_default }).Count }
}

if ($Json) {
  [pscustomobject]@{
    pattern = $Pattern
    mode = $Mode
    total_hits = $results.Count
    summary = @($summary)
    results = @($results)
  } | ConvertTo-Json -Depth 6
} else {
  "pattern=$Pattern"
  "mode=$Mode"
  "total_hits=$($results.Count)"
  ""
  "Lane summary:"
  $summary | Format-Table -AutoSize
  ""
  "First results:"
  $results | Select-Object -First 40 file,lane,path_role,included_by_default,knowledge_status,warning_code,warnings | Format-Table -AutoSize
}
