param(
  [string]$Pattern = 'source intake|metadata-routing|context pack|registry-before-recompute|query-run receipt|retrieval_policy',
  [string]$Query = '',
  [ValidateSet('current-rule','research','action','source-inspection','audit','project-exploration')]
  [string]$Mode = 'research',
  [string]$Root = '.',
  [string]$TopicId = 'source-intake-routing',
  [int]$Limit = 120,
  [int]$MaxStartHere = 8,
  [int]$MaxItemsPerLane = 8,
  [int]$MaxExcluded = 24,
  [string]$RouteMapPath = '',
  [string]$IntentRouterPath = '',
  [string]$OutFile = '',
  [switch]$Json
)

$ErrorActionPreference = 'Stop'

$retrievalScript = Join-Path $PSScriptRoot 'vaks-retrieval-mvp.ps1'
if (-not (Test-Path -LiteralPath $retrievalScript)) {
  throw "Missing retrieval script: $retrievalScript"
}

$resolvedRoot = (Resolve-Path -LiteralPath $Root).Path
$createdAt = Get-Date -Format 'yyyy-MM-ddTHH:mm:ssK'
$originalMode = $Mode
$originalPattern = $Pattern
$intentRouter = $null
$intentRouterRef = ''

if ([string]::IsNullOrWhiteSpace($RouteMapPath)) {
  $RouteMapPath = Join-Path (Split-Path -Parent $PSScriptRoot) 'fixtures/source-intake-route-map.json'
}

if ([string]::IsNullOrWhiteSpace($IntentRouterPath)) {
  $IntentRouterPath = Join-Path (Split-Path -Parent $PSScriptRoot) 'fixtures/query-intent-router-v0.json'
}

if (-not [string]::IsNullOrWhiteSpace($Query)) {
  $intentRouterScript = Join-Path $PSScriptRoot 'vaks-query-intent-router-v0.ps1'
  if (-not (Test-Path -LiteralPath $intentRouterScript)) {
    throw "Missing intent router script: $intentRouterScript"
  }
  if (-not (Test-Path -LiteralPath $IntentRouterPath)) {
    throw "Missing intent router fixture: $IntentRouterPath"
  }
  $intentRouterRaw = & $intentRouterScript -Query $Query -RouterPath $IntentRouterPath -Json
  $intentRouter = ((@($intentRouterRaw) -join "`n") | ConvertFrom-Json)
  $Mode = $intentRouter.selected_mode
  if (-not [string]::IsNullOrWhiteSpace($intentRouter.pattern)) {
    $Pattern = $intentRouter.pattern
  }
  $intentRouterRef = ''
}

$packId = "CPACK-$TopicId-$Mode-$(Get-Date -Format 'yyyyMMddHHmmss')"

function ConvertTo-Ref {
  param([string]$Path)
  return ($Path -replace '\\','/').TrimStart('./')
}

function Read-RouteMap {
  param([string]$Path)
  if ([string]::IsNullOrWhiteSpace($Path) -or -not (Test-Path -LiteralPath $Path)) {
    return $null
  }
  $raw = Get-Content -Raw -LiteralPath $Path -Encoding UTF8
  return $raw | ConvertFrom-Json
}

function Test-RouteMatch {
  param($Route, [string]$Text)
  foreach ($trigger in @($Route.query_triggers)) {
    if ($Text -match [regex]::Escape($trigger)) { return $true }
  }
  return $false
}

function Join-List {
  param($Values)
  $items = @($Values | Where-Object { $_ })
  if ($items.Count -eq 0) { return '' }
  return ($items -join ', ')
}

function Add-RefList {
  param(
    [System.Collections.Generic.List[string]]$Lines,
    [string]$Header,
    $Refs
  )
  $Lines.Add("## $Header") | Out-Null
  $Lines.Add('') | Out-Null
  foreach ($ref in @($Refs)) {
    $Lines.Add('- `' + $ref + '`') | Out-Null
  }
  if (@($Refs).Count -eq 0) {
    $Lines.Add('- none') | Out-Null
  }
  $Lines.Add('') | Out-Null
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
  $cwd = (Get-Location).Path
  $cwdPrefix = $cwd.TrimEnd('\') + '\'
  if ($full.StartsWith($cwdPrefix, [StringComparison]::OrdinalIgnoreCase)) {
    return ConvertTo-Ref -Path $full.Substring($cwdPrefix.Length)
  }
  return ConvertTo-Ref -Path $full
}

function Invoke-RetrievalJson {
  param([string]$RunMode)
  $raw = & $retrievalScript -Root $resolvedRoot -Pattern $Pattern -Mode $RunMode -Limit $Limit -Json
  $jsonText = @($raw) -join "`n"
  return $jsonText | ConvertFrom-Json
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

function Get-CitableStatus {
  param([string]$Lane)
  switch ($Lane) {
    { $_ -in @('mainline_current','reviewed_support','raw_drilldown') } { return 'drilldown_required' }
    default { return 'activation_only' }
  }
}

function Get-LaneWarning {
  param([string]$Lane)
  switch ($Lane) {
    'candidate_orientation' { return 'candidate_not_action_basis' }
    'raw_drilldown' { return 'raw_is_provenance_only' }
    'active_project_overlay' { return 'overlay_not_authority' }
    'audit_evidence' { return 'audit_evidence_not_current_rule' }
    'feedback_diagnostics' { return 'feedback_not_truth' }
    'support_review_output' { return 'review_output_needs_anchor_before_action' }
    default { return '' }
  }
}

function Get-PinnedPathRole {
  param([string]$Ref)
  $p = $Ref -replace '/', '\'
  if ($p -like '00_handoff\*') { return 'handoff' }
  if ($p -like 'templates\*') { return 'formal_template' }
  if ($p -in @('SOURCE_INTAKE.md','README.md','purpose.md','SCHEMA.md','ARCHITECTURE_PRINCIPLES.md','IMPLEMENTATION_BLUEPRINT.md','REFERENCE_REVIEW_PROTOCOL.md','DEV_CONTEXT.md','MEMORY_TIER.md','REVIEW_QUEUE.md','FEEDBACK.md','FUSION_ARCHITECTURE_V0_2_DRAFT.md','SECOND_BRAIN_MODEL.md')) { return 'mainline_doc' }
  if ($p -like 'raw\repos\_snapshots\*') { return 'repo_snapshot' }
  if ($p -like 'raw\articles\*' -or $p -like 'raw\videos\*' -or $p -like 'raw\repos\*' -or $p -like 'raw\papers\*') { return 'source_card' }
  if ($p -like 'outputs\review\project_overlays\*') { return 'project_overlay' }
  if ($p -like 'outputs\review\*candidate-distillation.md') { return 'candidate_distillation' }
  if ($p -like 'outputs\review\source-intake-tag-routing-sandbox-2026-06-07\*') { return 'new_sandbox_package' }
  if ($p -like 'outputs\review\*') { return 'review_output' }
  return 'legacy_or_unknown'
}

function Get-LaneFromPathRole {
  param([string]$PathRole)
  switch ($PathRole) {
    { $_ -in @('mainline_doc','formal_template','handoff') } { return 'mainline_current' }
    { $_ -in @('source_card','repo_snapshot') } { return 'raw_drilldown' }
    'candidate_distillation' { return 'candidate_orientation' }
    'project_overlay' { return 'active_project_overlay' }
    'new_sandbox_package' { return 'audit_evidence' }
    'review_output' { return 'support_review_output' }
    default { return 'other_needs_triage' }
  }
}

function New-PinnedResult {
  param([string]$Ref)
  $role = Get-PinnedPathRole -Ref $Ref
  $lane = Get-LaneFromPathRole -PathRole $role
  [pscustomobject]@{
    file = ($Ref -replace '/', '\')
    path_role = $role
    lane = $lane
    included_by_default = $true
    knowledge_status = ''
    warning_code = ''
    forbidden_tags = @()
    warnings = @('pinned_by_route_map')
  }
}

function Format-WarningList {
  param($Warnings)
  $items = @($Warnings | Where-Object { $_ } | Select-Object -Unique)
  if ($items.Count -eq 0) { return '[]' }
  return '[' + (($items | ForEach-Object { '"' + ($_ -replace '"','\"') + '"' }) -join ', ') + ']'
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

function ConvertTo-TermList {
  param($Values)
  $stopWords = @(
    'the','this','that','these','those','can','could','would','should','what',
    'when','where','which','who','why','how','for','with','and','from','show',
    'use','used','using','into','onto','does','did','has','have','had','is',
    'are','was','were','me','my','our','your','true','false','none','only'
  )
  $terms = New-Object System.Collections.Generic.List[string]
  foreach ($value in @($Values)) {
    if ($null -eq $value) { continue }
    foreach ($part in (([string]$value) -split '[\s,;|/\\()\[\]{}:"]+')) {
      $clean = $part.Trim().Trim("'").Trim('.')
      $lower = $clean.ToLowerInvariant()
      if ($clean.Length -ge 3 -and -not ($stopWords -contains $lower) -and -not $terms.Contains($clean)) {
        $terms.Add($clean) | Out-Null
      }
    }
  }
  return $terms.ToArray()
}

function Test-TextContainsAny {
  param([string]$Text, $Terms)
  if ([string]::IsNullOrWhiteSpace($Text)) { return $false }
  foreach ($term in @($Terms)) {
    if ([string]::IsNullOrWhiteSpace($term)) { continue }
    if ($Text.IndexOf([string]$term, [StringComparison]::OrdinalIgnoreCase) -ge 0) {
      return $true
    }
  }
  return $false
}

function Get-ResultFullPath {
  param($Result)
  if ($null -eq $Result -or [string]::IsNullOrWhiteSpace($Result.file)) { return '' }
  $joined = Join-Path $resolvedRoot $Result.file
  if (Test-Path -LiteralPath $joined) {
    return (Resolve-Path -LiteralPath $joined).Path
  }
  return ''
}

function Get-ResultPreviewText {
  param($Result, [int]$MaxChars = 6000)
  $path = Get-ResultFullPath -Result $Result
  if ([string]::IsNullOrWhiteSpace($path)) { return '' }
  try {
    $text = Get-Content -Raw -LiteralPath $path -Encoding UTF8 -ErrorAction Stop
    if ($text.Length -gt $MaxChars) { return $text.Substring(0, $MaxChars) }
    return $text
  } catch {
    return ''
  }
}

function Get-SnippetForResult {
  param($Result, $Terms)
  $path = Get-ResultFullPath -Result $Result
  if ([string]::IsNullOrWhiteSpace($path)) {
    return [pscustomobject]@{ selector = ''; snippet = ''; line = 0 }
  }
  try {
    $lines = Get-Content -LiteralPath $path -Encoding UTF8 -ErrorAction Stop
  } catch {
    return [pscustomobject]@{ selector = ''; snippet = ''; line = 0 }
  }

  $fallbackLine = 0
  $fallbackText = ''
  for ($i = 0; $i -lt $lines.Count; $i++) {
    $line = [string]$lines[$i]
    if ($fallbackLine -eq 0 -and -not [string]::IsNullOrWhiteSpace($line)) {
      $fallbackLine = $i + 1
      $fallbackText = $line
    }
    foreach ($term in @($Terms)) {
      if ([string]::IsNullOrWhiteSpace($term)) { continue }
      if ($line.IndexOf([string]$term, [StringComparison]::OrdinalIgnoreCase) -ge 0) {
        return [pscustomobject]@{
          selector = ('line:{0}' -f ($i + 1))
          snippet = ConvertTo-PackText -Value $line
          line = $i + 1
        }
      }
    }
  }

  if ($fallbackLine -gt 0) {
    return [pscustomobject]@{
      selector = ('line:{0}' -f $fallbackLine)
      snippet = ConvertTo-PackText -Value $fallbackText
      line = $fallbackLine
    }
  }
  return [pscustomobject]@{ selector = ''; snippet = ''; line = 0 }
}

function Get-ActionRole {
  param([string]$Lane)
  if ($Mode -ne 'action') { return 'navigation_only' }
  switch ($Lane) {
    'mainline_current' { return 'anchor_queue_rule_or_template' }
    'reviewed_support' { return 'anchor_queue_reviewed_or_review_ready' }
    'raw_drilldown' { return 'anchor_queue_raw_provenance' }
    default { return 'excluded_from_action_support' }
  }
}

function Get-SelectionProfile {
  param($Result)
  $ref = ConvertTo-Ref -Path $Result.file
  $preview = Get-ResultPreviewText -Result $Result
  $rankText = ($ref + "`n" + $preview)
  $priority = 10
  $reasons = New-Object System.Collections.Generic.List[string]
  $reasons.Add('ordinary_match') | Out-Null

  if ($script:PinnedRankRefs -contains $ref) {
    $priority += 10000
    $reasons.Add('pinned_ref') | Out-Null
  }
  if (Test-TextContainsAny -Text $rankText -Terms $script:TopicRankTerms) {
    $priority += 3000
    $reasons.Add('exact_topic_match') | Out-Null
  }
  if (Test-TextContainsAny -Text $rankText -Terms $script:EntityRankTerms) {
    $priority += 1000
    $reasons.Add('entity_match') | Out-Null
  }
  if ($ref -match '2026-06-07' -or $ref -match 'github-scout|source-intake-routing') {
    $priority += 500
    $reasons.Add('recent_scout_or_current_sandbox') | Out-Null
  }

  [pscustomobject]@{
    priority = $priority
    reason = (@($reasons | Select-Object -Unique) -join ' > ')
  }
}

function Add-SelectionProfileToResult {
  param($Result)
  $profile = Get-SelectionProfile -Result $Result
  $Result | Add-Member -NotePropertyName selection_priority -NotePropertyValue $profile.priority -Force
  $Result | Add-Member -NotePropertyName selection_reason -NotePropertyValue $profile.reason -Force
  return $Result
}

$routeMap = Read-RouteMap -Path $RouteMapPath
$routeMapRef = if ($routeMap) {
  Get-DisplayRef -Path $RouteMapPath
} else {
  ''
}
$intentRouterRef = if (-not [string]::IsNullOrWhiteSpace($Query) -and (Test-Path -LiteralPath $IntentRouterPath)) {
  Get-DisplayRef -Path $IntentRouterPath
} else {
  ''
}

function ConvertTo-PackItem {
  param($Result, [int]$Index)
  $laneWarning = Get-LaneWarning -Lane $Result.lane
  $warnings = @($Result.warnings) + @($laneWarning, 'pack_builder_not_evidence_check')
  $snippet = Get-SnippetForResult -Result $Result -Terms $script:SnippetTerms
  $selectionPriority = if ($null -ne $Result.selection_priority) { $Result.selection_priority } else { (Get-SelectionProfile -Result $Result).priority }
  $selectionReason = if ($Result.selection_reason) { $Result.selection_reason } else { (Get-SelectionProfile -Result $Result).reason }
  [pscustomobject]@{
    item_id = ('PI-{0:D3}' -f $Index)
    display_label = [IO.Path]::GetFileNameWithoutExtension($Result.file)
    lane = $Result.lane
    path_role = $Result.path_role
    source_ref = $Result.file
    selector_or_offset = $snippet.selector
    snippet = $snippet.snippet
    snippet_status = 'navigation_snippet_not_evidence'
    selection_priority = $selectionPriority
    selection_reason = $selectionReason
    citable_status = Get-CitableStatus -Lane $Result.lane
    action_basis_allowed = $false
    action_anchor_candidate = ($Mode -eq 'action' -and $Result.lane -in @('mainline_current','reviewed_support','raw_drilldown'))
    action_role = Get-ActionRole -Lane $Result.lane
    matched_channels = @('path_or_text_match')
    why_included = "Matched query pattern inside allowed lane for mode '$Mode'; ranked as $selectionReason."
    warnings = @($warnings | Where-Object { $_ } | Select-Object -Unique)
  }
}

function Select-TopByLane {
  param($Items, [int]$PerLane)
  $selected = New-Object System.Collections.ArrayList
  foreach ($group in (@($Items) | Sort-Object @{ Expression = { Get-LaneOrder -Lane $_.lane } }, file | Group-Object lane)) {
    foreach ($item in (@($group.Group) | Sort-Object @{ Expression = { $_.selection_priority }; Descending = $true }, file | Select-Object -First $PerLane)) {
      $selected.Add($item) | Out-Null
    }
  }
  return $selected.ToArray()
}

$startRun = Invoke-RetrievalJson -RunMode 'current-rule'
$modeRun = Invoke-RetrievalJson -RunMode $Mode

$routeStartRefs = @()
if ($routeMap) {
  $routeStartRefs = @($routeMap.start_here_refs | ForEach-Object { ConvertTo-Ref -Path $_ })
}

if ($routeStartRefs.Count -gt 0) {
  $startHere = @($routeStartRefs |
    Where-Object { Test-Path -LiteralPath (Join-Path $resolvedRoot $_) } |
    Select-Object -First $MaxStartHere |
    ForEach-Object { New-PinnedResult -Ref $_ })
} else {
  $startHere = @($startRun.results | Where-Object { $_.included_by_default } | Select-Object -First $MaxStartHere)
}

$pinnedRouteRefs = @()
if ($routeMap -and $Mode -in @('research','source-inspection','project-exploration')) {
  $pinnedRouteRefs = @($routeMap.external_scout_refs | ForEach-Object { ConvertTo-Ref -Path $_ })
}

$routeTermValues = New-Object System.Collections.Generic.List[string]
if ($routeMap) {
  foreach ($route in @($routeMap.route_cards)) {
    foreach ($value in @($route.route_id, $route.label, $route.borrowed_from, $route.query_triggers)) {
      foreach ($item in @($value)) {
        if ($item) { $routeTermValues.Add([string]$item) | Out-Null }
      }
    }
  }
}
$script:PinnedRankRefs = @($routeStartRefs + $pinnedRouteRefs | Select-Object -Unique)
$script:TopicRankTerms = ConvertTo-TermList -Values @($TopicId, ($TopicId -replace '-', ' '), $Query, $Pattern)
$script:EntityRankTerms = ConvertTo-TermList -Values @($routeTermValues)
$script:SnippetTerms = ConvertTo-TermList -Values @($Query, $Pattern, $TopicId, ($routeTermValues | Select-Object -First 24))

$pinnedRouteItems = @($pinnedRouteRefs |
  Where-Object { Test-Path -LiteralPath (Join-Path $resolvedRoot $_) } |
  ForEach-Object { Add-SelectionProfileToResult -Result (New-PinnedResult -Ref $_) })
$startHere = @($startHere | ForEach-Object { Add-SelectionProfileToResult -Result $_ })
$modeIncluded = @($modeRun.results | Where-Object { $_.included_by_default } | ForEach-Object { Add-SelectionProfileToResult -Result $_ })
$knownFiles = @{}
foreach ($item in @($startHere + $pinnedRouteItems + $modeIncluded)) {
  if (-not $knownFiles.ContainsKey($item.file)) { $knownFiles[$item.file] = $true }
}

$pinnedFiles = @($startHere + $pinnedRouteItems).file
$modeIncluded = @($modeIncluded | Where-Object { -not ($pinnedFiles -contains $_.file) })
$selectedModeItems = Select-TopByLane -Items $modeIncluded -PerLane $MaxItemsPerLane
$packItems = New-Object System.Collections.Generic.List[object]
$index = 1
foreach ($item in @($startHere + $pinnedRouteItems + $selectedModeItems)) {
  $packItems.Add((ConvertTo-PackItem -Result $item -Index $index)) | Out-Null
  $index++
}

$excluded = @($modeRun.results |
  Where-Object { -not $_.included_by_default -and -not $knownFiles.ContainsKey($_.file) } |
  Sort-Object @{ Expression = { Get-LaneOrder -Lane $_.lane } }, file |
  Select-Object -First $MaxExcluded)

$summaryRows = @($modeRun.summary | Sort-Object @{ Expression = { Get-LaneOrder -Lane $_.lane } })
$selectedByLane = @($packItems | Group-Object lane | Sort-Object @{ Expression = { Get-LaneOrder -Lane $_.Name } } | ForEach-Object {
  [pscustomobject]@{ lane = $_.Name; count = $_.Count }
})
$anchorQueueItems = @($packItems | Where-Object { $_.action_role -like 'anchor_queue*' })
$rawAnchorQueueCount = @($anchorQueueItems | Where-Object { $_.lane -eq 'raw_drilldown' }).Count
$reviewedAnchorQueueCount = @($anchorQueueItems | Where-Object { $_.lane -eq 'reviewed_support' }).Count
$mainlineAnchorQueueCount = @($anchorQueueItems | Where-Object { $_.lane -eq 'mainline_current' }).Count

if ($Mode -eq 'action') {
  $actionState = 'not_ready'
  $actionReason = 'Builder only prepares an anchor_queue; evidence support check has not run.'
} else {
  $actionState = 'not_ready'
  $actionReason = 'Orientation/workbench pack only; not action-facing support.'
}

$lines = New-Object System.Collections.Generic.List[string]
$lines.Add('---') | Out-Null
$lines.Add('record_kind: context_pack_manifest_candidate') | Out-Null
$lines.Add('status: candidate') | Out-Null
$lines.Add("created_at: $createdAt") | Out-Null
$lines.Add("pack_id: $packId") | Out-Null
$lines.Add("topic_id: $TopicId") | Out-Null
$lines.Add("mode: $Mode") | Out-Null
$lines.Add("route_map_ref: $routeMapRef") | Out-Null
if ($intentRouterRef) {
  $lines.Add("query_intent_router_ref: $intentRouterRef") | Out-Null
  $lines.Add("query_intent_selected_mode: $Mode") | Out-Null
}
$lines.Add(('action_facing: ' + ($(if ($Mode -eq 'action') { 'true' } else { 'false' })))) | Out-Null
$lines.Add('truth_boundary: activation_pack_not_truth') | Out-Null
$lines.Add('allowed_use:') | Out-Null
$lines.Add('  - orientation') | Out-Null
$lines.Add('  - navigation') | Out-Null
$lines.Add('  - context_activation') | Out-Null
$lines.Add('  - drilldown_queue') | Out-Null
$lines.Add('forbidden_use:') | Out-Null
$lines.Add('  - truth') | Out-Null
$lines.Add('  - reviewed_relation') | Out-Null
$lines.Add('  - action_basis') | Out-Null
$lines.Add('---') | Out-Null
$lines.Add('') | Out-Null
$lines.Add("# Context Pack Candidate: $TopicId") | Out-Null
$lines.Add('') | Out-Null
$lines.Add('## Query') | Out-Null
$lines.Add('') | Out-Null
$lines.Add('```yaml') | Out-Null
$lines.Add("user_query: `"$($Query -replace '"', "'")`"") | Out-Null
$lines.Add("pattern: `"$Pattern`"") | Out-Null
$lines.Add("original_pattern: `"$originalPattern`"") | Out-Null
$lines.Add("root: `"$resolvedRoot`"") | Out-Null
$lines.Add("mode: $Mode") | Out-Null
$lines.Add("original_mode: $originalMode") | Out-Null
$lines.Add("limit: $Limit") | Out-Null
$lines.Add("route_map_ref: `"$routeMapRef`"") | Out-Null
$lines.Add("query_intent_router_ref: `"$intentRouterRef`"") | Out-Null
$lines.Add('```') | Out-Null
$lines.Add('') | Out-Null
if ($intentRouter) {
  $lines.Add('## Intent Router') | Out-Null
  $lines.Add('') | Out-Null
  $lines.Add('```yaml') | Out-Null
  $lines.Add("selected_mode: $($intentRouter.selected_mode)") | Out-Null
  $lines.Add("confidence: $($intentRouter.confidence)") | Out-Null
  $lines.Add(('fallback_used: ' + ($(if ($intentRouter.fallback_used) { 'true' } else { 'false' })))) | Out-Null
  $lines.Add("matched_terms: $(Format-WarningList -Warnings $intentRouter.matched_terms)") | Out-Null
  $lines.Add("route_bias: $(Format-WarningList -Warnings $intentRouter.route_bias)") | Out-Null
  $lines.Add("warnings: $(Format-WarningList -Warnings $intentRouter.warnings)") | Out-Null
  $lines.Add('truth_boundary: navigation_only_not_truth') | Out-Null
  $lines.Add('action_basis_allowed: false') | Out-Null
  $lines.Add('```') | Out-Null
  $lines.Add('') | Out-Null
}
if ($routeMap) {
  Add-RefList -Lines $lines -Header 'Start Here' -Refs $routeMap.start_here_refs

  $lines.Add('## Source Route Front Door') | Out-Null
  $lines.Add('') | Out-Null
  $lines.Add('| route | matched | include lanes | borrowed from | guard |') | Out-Null
  $lines.Add('|---|---:|---|---|---|') | Out-Null
  foreach ($route in @($routeMap.route_cards)) {
    $matched = if (Test-RouteMatch -Route $route -Text $Pattern) { 'yes' } else { 'no' }
    $lines.Add(
      '| `' + $route.route_id + '` | ' + $matched +
      ' | ' + (Join-List -Values $route.include_lanes) +
      ' | ' + (Join-List -Values $route.borrowed_from) +
      ' | ' + $route.risk_guard + ' |'
    ) | Out-Null
  }
  $lines.Add('') | Out-Null

  Add-RefList -Lines $lines -Header 'External Scout References' -Refs $routeMap.external_scout_refs
}
$lines.Add('## Pack Summary') | Out-Null
$lines.Add('') | Out-Null
$lines.Add('| lane | total_hits | included_by_mode | selected_for_pack |') | Out-Null
$lines.Add('|---|---:|---:|---:|') | Out-Null
foreach ($row in $summaryRows) {
  $selectedCount = @($selectedByLane | Where-Object { $_.lane -eq $row.lane } | Select-Object -ExpandProperty count)
  if ($selectedCount.Count -eq 0) { $selectedCount = 0 }
  $lines.Add('| `' + $row.lane + '` | ' + $row.count + ' | ' + $row.included_by_default + ' | ' + $selectedCount + ' |') | Out-Null
}
$lines.Add('') | Out-Null
$lines.Add('## Pack Items') | Out-Null
$lines.Add('') | Out-Null
$lines.Add('```yaml') | Out-Null
$lines.Add('items:') | Out-Null
foreach ($item in $packItems) {
  $lines.Add("  - item_id: $($item.item_id)") | Out-Null
  $lines.Add("    display_label: `"$($item.display_label)`"") | Out-Null
  $lines.Add("    lane: $($item.lane)") | Out-Null
  $lines.Add("    path_role: $($item.path_role)") | Out-Null
  $lines.Add("    source_ref: `"$($item.source_ref)`"") | Out-Null
  $lines.Add("    selector_or_offset: `"$($item.selector_or_offset)`"") | Out-Null
  $lines.Add("    snippet: `"$($item.snippet)`"") | Out-Null
  $lines.Add("    snippet_status: $($item.snippet_status)") | Out-Null
  $lines.Add("    selection_priority: $($item.selection_priority)") | Out-Null
  $lines.Add("    selection_reason: `"$($item.selection_reason)`"") | Out-Null
  $lines.Add("    citable_status: $($item.citable_status)") | Out-Null
  $lines.Add("    action_basis_allowed: false") | Out-Null
  $lines.Add(('    action_anchor_candidate: ' + ($(if ($item.action_anchor_candidate) { 'true' } else { 'false' })))) | Out-Null
  $lines.Add("    action_role: $($item.action_role)") | Out-Null
  $lines.Add("    matched_channels: [path_or_text_match]") | Out-Null
  $lines.Add("    why_included: `"$($item.why_included)`"") | Out-Null
  $lines.Add("    warnings: $(Format-WarningList -Warnings $item.warnings)") | Out-Null
}
$lines.Add('```') | Out-Null
$lines.Add('') | Out-Null
$lines.Add('## Excluded Or Not Default') | Out-Null
$lines.Add('') | Out-Null
$lines.Add('These hits matched the query but are not selected for this mode/default pack.') | Out-Null
$lines.Add('') | Out-Null
$lines.Add('| file | lane | path_role | caution |') | Out-Null
$lines.Add('|---|---|---|---|') | Out-Null
foreach ($item in $excluded) {
  $warnings = Format-WarningList -Warnings (@($item.warnings) + @(Get-LaneWarning -Lane $item.lane))
  $lines.Add('| `' + $item.file + '` | `' + $item.lane + '` | `' + $item.path_role + '` | `' + $warnings + '` |') | Out-Null
}
$lines.Add('') | Out-Null
$lines.Add('## Coverage Overview') | Out-Null
$lines.Add('') | Out-Null
$lines.Add('```yaml') | Out-Null
$lines.Add('coverage_overview:') | Out-Null
$lines.Add('  supported: 0') | Out-Null
$lines.Add('  weakly_supported: 0') | Out-Null
$lines.Add('  challenged: 0') | Out-Null
$lines.Add('  missing_evidence:') | Out-Null
$lines.Add('    - evidence_support_check_not_run') | Out-Null
$lines.Add('  out_of_scope: 0') | Out-Null
$lines.Add('  risk_flags:') | Out-Null
$lines.Add('    - pack_is_activation_not_truth') | Out-Null
$lines.Add('final_support:') | Out-Null
$lines.Add('  state: none') | Out-Null
$lines.Add('  reason: evidence_support_check_not_run') | Out-Null
$lines.Add('anchor_queue:') | Out-Null
$lines.Add("  total: $($anchorQueueItems.Count)") | Out-Null
$lines.Add("  mainline_current: $mainlineAnchorQueueCount") | Out-Null
$lines.Add("  reviewed_support: $reviewedAnchorQueueCount") | Out-Null
$lines.Add("  raw_drilldown: $rawAnchorQueueCount") | Out-Null
$lines.Add('  note: navigation_queue_only_not_support') | Out-Null
$lines.Add('action_readiness:') | Out-Null
$lines.Add("  state: $actionState") | Out-Null
$lines.Add("  reason: `"$actionReason`"") | Out-Null
$lines.Add('evidence_sufficiency:') | Out-Null
$lines.Add('  state: insufficient') | Out-Null
$lines.Add('  checked_for: context_pack_builder_v0_smoke') | Out-Null
$lines.Add('  required_next_step: open raw/reviewed anchors and run evidence support check before action-facing use') | Out-Null
$lines.Add('context_pack_trace:') | Out-Null
$lines.Add('  retrieval_script: tools/vaks-retrieval-mvp.ps1') | Out-Null
$lines.Add("  route_map_ref: `"$routeMapRef`"") | Out-Null
$lines.Add('  fusion_method: lane_grouping_only_no_cross_lane_rrf') | Out-Null
$lines.Add('  content_trace_policy: refs_only') | Out-Null
$lines.Add('```') | Out-Null

$markdown = $lines -join "`n"

if ($OutFile) {
  $outDir = Split-Path -Parent $OutFile
  if ($outDir -and -not (Test-Path -LiteralPath $outDir)) {
    New-Item -ItemType Directory -Path $outDir | Out-Null
  }
  Set-Content -LiteralPath $OutFile -Value $markdown -Encoding UTF8
}

if ($Json) {
  $jsonResult = New-Object psobject
  $jsonResult | Add-Member -NotePropertyName pack_id -NotePropertyValue $packId
  $jsonResult | Add-Member -NotePropertyName created_at -NotePropertyValue $createdAt
  $jsonResult | Add-Member -NotePropertyName root -NotePropertyValue $resolvedRoot
  $jsonResult | Add-Member -NotePropertyName query -NotePropertyValue $Query
  $jsonResult | Add-Member -NotePropertyName pattern -NotePropertyValue $Pattern
  $jsonResult | Add-Member -NotePropertyName original_pattern -NotePropertyValue $originalPattern
  $jsonResult | Add-Member -NotePropertyName mode -NotePropertyValue $Mode
  $jsonResult | Add-Member -NotePropertyName original_mode -NotePropertyValue $originalMode
  $jsonResult | Add-Member -NotePropertyName intent_router -NotePropertyValue $intentRouter
  $jsonResult | Add-Member -NotePropertyName selected_count -NotePropertyValue $packItems.Count
  $jsonResult | Add-Member -NotePropertyName excluded_count -NotePropertyValue $excluded.Count
  $jsonResult | Add-Member -NotePropertyName summary -NotePropertyValue ([object[]]@($summaryRows))
  $jsonResult | Add-Member -NotePropertyName selected_by_lane -NotePropertyValue ([object[]]@($selectedByLane))
  $jsonResult | Add-Member -NotePropertyName anchor_queue -NotePropertyValue ([pscustomobject]@{
    total = $anchorQueueItems.Count
    mainline_current = $mainlineAnchorQueueCount
    reviewed_support = $reviewedAnchorQueueCount
    raw_drilldown = $rawAnchorQueueCount
  })
  $firstPackItem = if ($packItems.Count -gt 0) { $packItems[0] } else { $null }
  $firstPackItemSummary = if ($firstPackItem) {
    [pscustomobject]@{
      item_id = $firstPackItem.item_id
      lane = $firstPackItem.lane
      source_ref = $firstPackItem.source_ref
      selector_or_offset = $firstPackItem.selector_or_offset
      selection_priority = $firstPackItem.selection_priority
      action_role = $firstPackItem.action_role
    }
  } else {
    $null
  }
  $jsonResult | Add-Member -NotePropertyName first_pack_item -NotePropertyValue $firstPackItemSummary
  $jsonResult | Add-Member -NotePropertyName route_map_ref -NotePropertyValue $routeMapRef
  $jsonResult | Add-Member -NotePropertyName query_intent_router_ref -NotePropertyValue $intentRouterRef
  $jsonResult | Add-Member -NotePropertyName route_cards -NotePropertyValue ([object[]]$(if ($routeMap) { @($routeMap.route_cards) } else { @() }))
  $jsonResult | Add-Member -NotePropertyName out_file -NotePropertyValue $OutFile
  $jsonResult | ConvertTo-Json -Depth 6
} elseif ($OutFile) {
  [pscustomobject]@{
    out_file = $OutFile
    mode = $Mode
    selected_count = $packItems.Count
    excluded_count = $excluded.Count
    anchor_queue_total = $anchorQueueItems.Count
    query_intent_router_ref = $intentRouterRef
  } | Format-List
} else {
  $markdown
}
