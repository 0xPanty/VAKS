<#
.SYNOPSIS
Creates a VAKS video source-card skeleton from video metadata and retained transcript artifacts.

.DESCRIPTION
This project-local runner handles the mechanical part of medium/heavy video
intake: source identity, artifact copying, source-card frontmatter, and optional
finalizer invocation. It does not transcribe media, summarize content, review
claims, or promote knowledge.

Use it after subtitles or ASR outputs already exist, then fill the candidate
comprehension and VAKS-fit sections manually or with Codex.

.EXAMPLE
powershell -ExecutionPolicy Bypass -File .\tools\new-video-source-card.ps1 `
  -Url https://www.bilibili.com/video/BV1Gjd5BPEhh/ `
  -ArtifactSourceDir C:\Users\Administrator\.codex\video-research\BV1Gjd5BPEhh\asr-vaks `
  -ProcessingLevel medium `
  -TranscriptMethod local_asr `
  -Finalize `
  -ScratchPath C:\Users\Administrator\.codex\video-research\BV1Gjd5BPEhh\asr-vaks `
  -DeleteScratchMedia
#>

[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [string]$Url,

    [string]$ProjectRoot = (Get-Location).Path,

    [string]$Slug,

    [ValidateSet('light', 'medium', 'heavy')]
    [string]$ProcessingLevel = 'medium',

    [ValidateSet('none', 'public_subtitle', 'local_asr', 'user_supplied')]
    [string]$TranscriptMethod = 'local_asr',

    [string]$Platform,
    [string]$PlatformId,
    [string]$Title,
    [string]$Author,
    [string]$PublishedAt,
    [string]$Duration,
    [string]$SourceFamily,
    [string[]]$Topics = @('video-intake'),

    [string]$MetadataPath,
    [switch]$NoMetadataFetch,

    [string]$ArtifactSourceDir,
    [string]$TranscriptPath,
    [string]$SegmentsPath,
    [string]$SegmentsJsonPath,
    [string]$TranscriptMetadataPath,
    [string]$LedgerPath,
    [string]$SourceMetadataPath,

    [switch]$AllowIncompleteArtifacts,
    [switch]$Finalize,
    [switch]$SkipObsidianSync,
    [string]$ScratchPath,
    [switch]$DeleteScratchMedia,
    [switch]$Force,
    [switch]$Json
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

function Get-FullPath {
    param([Parameter(Mandatory = $true)][string]$Path)
    return [System.IO.Path]::GetFullPath($Path)
}

function Resolve-PathOrNull {
    param([string]$Path)
    if ([string]::IsNullOrWhiteSpace($Path)) {
        return $null
    }

    if (Test-Path -LiteralPath $Path) {
        return (Resolve-Path -LiteralPath $Path).Path
    }

    return $null
}

function Get-RelativePathCompat {
    param(
        [Parameter(Mandatory = $true)][string]$BasePath,
        [Parameter(Mandatory = $true)][string]$TargetPath
    )

    $baseFull = Get-FullPath $BasePath
    if (-not $baseFull.EndsWith([System.IO.Path]::DirectorySeparatorChar)) {
        $baseFull += [System.IO.Path]::DirectorySeparatorChar
    }

    $targetFull = Get-FullPath $TargetPath
    $baseUri = New-Object System.Uri($baseFull)
    $targetUri = New-Object System.Uri($targetFull)
    return [System.Uri]::UnescapeDataString($baseUri.MakeRelativeUri($targetUri).ToString()).Replace('\', '/')
}

function ConvertTo-YamlScalar {
    param([string]$Value)
    if ([string]::IsNullOrWhiteSpace($Value)) {
        return ''
    }

    $clean = ($Value -replace "`r", ' ' -replace "`n", ' ').Trim()
    if ($clean -match '^[A-Za-z0-9_.:/@+-]+$') {
        return $clean
    }

    return "'" + ($clean -replace "'", "''") + "'"
}

function ConvertTo-YamlList {
    param([string[]]$Values)
    $items = @($Values | Where-Object { -not [string]::IsNullOrWhiteSpace($_) } | Select-Object -Unique)
    if ($items.Count -eq 0) {
        return @('  -')
    }

    return @($items | ForEach-Object { '  - ' + (ConvertTo-YamlScalar $_) })
}

function Get-VideoIdentity {
    param([Parameter(Mandatory = $true)][string]$InputUrl)

    if ($InputUrl -match '(BV[0-9A-Za-z]+)') {
        return [PSCustomObject]@{ Platform = 'bilibili'; PlatformId = $matches[1] }
    }

    if ($InputUrl -match 'youtu\.be/([^?&/]+)') {
        return [PSCustomObject]@{ Platform = 'youtube'; PlatformId = $matches[1] }
    }

    if ($InputUrl -match '[?&]v=([^?&/]+)') {
        return [PSCustomObject]@{ Platform = 'youtube'; PlatformId = $matches[1] }
    }

    if ($InputUrl -match 'youtube\.com/(shorts|embed)/([^?&/]+)') {
        return [PSCustomObject]@{ Platform = 'youtube'; PlatformId = $matches[2] }
    }

    return [PSCustomObject]@{ Platform = 'video'; PlatformId = '' }
}

function Get-JsonProperty {
    param(
        [Parameter(Mandatory = $true)]$Object,
        [Parameter(Mandatory = $true)][string[]]$Names
    )

    foreach ($name in $Names) {
        if ($null -ne $Object -and $Object.PSObject.Properties.Name -contains $name) {
            $value = $Object.$name
            if ($null -ne $value -and -not [string]::IsNullOrWhiteSpace([string]$value)) {
                return [string]$value
            }
        }
    }

    return ''
}

function Get-BilibiliMetadata {
    param(
        [Parameter(Mandatory = $true)][string]$Bvid,
        [Parameter(Mandatory = $true)][string]$InputUrl
    )

    $headers = @{
        'User-Agent' = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125 Safari/537.36'
        'Referer' = 'https://www.bilibili.com/'
        'Origin' = 'https://www.bilibili.com'
    }
    $apiUrl = 'https://api.bilibili.com/x/web-interface/view?bvid=' + [uri]::EscapeDataString($Bvid)
    $response = Invoke-RestMethod -Method Get -Uri $apiUrl -Headers $headers
    if ($response.code -ne 0) {
        throw ("Bilibili metadata API failed for " + $Bvid + ": code=" + $response.code)
    }

    $data = $response.data
    $owner = ''
    if ($data.owner -and $data.owner.name) {
        $owner = [string]$data.owner.name
    }

    $pubdate = ''
    if ($data.pubdate) {
        $pubdate = ([DateTimeOffset]::FromUnixTimeSeconds([int64]$data.pubdate).ToOffset([TimeSpan]::FromHours(8))).ToString('yyyy-MM-dd HH:mm:ss zzz')
    }

    return [PSCustomObject]@{
        platform = 'bilibili'
        platform_id = $Bvid
        source_uri = "bilibili:$Bvid"
        url = "https://www.bilibili.com/video/$Bvid/"
        title = [string]$data.title
        author = $owner
        publisher = $owner
        published_at = $pubdate
        duration_seconds = [int]$data.duration
        raw = $response
        captured_at = (Get-Date).ToString('o')
        fetch_method = 'bilibili_public_view_api'
    }
}

function Get-YoutubeMetadata {
    param(
        [Parameter(Mandatory = $true)][string]$VideoId,
        [Parameter(Mandatory = $true)][string]$InputUrl
    )

    $ytDlp = Get-Command yt-dlp -ErrorAction SilentlyContinue
    if ($null -eq $ytDlp) {
        return [PSCustomObject]@{
            platform = 'youtube'
            platform_id = $VideoId
            source_uri = "youtube:$VideoId"
            url = $InputUrl
            title = ''
            author = ''
            publisher = ''
            published_at = ''
            duration_seconds = ''
            raw = $null
            captured_at = (Get-Date).ToString('o')
            fetch_method = 'youtube_identity_only_yt_dlp_missing'
        }
    }

    $rawLines = & $ytDlp.Source --skip-download --dump-single-json --no-warnings --no-playlist $InputUrl 2>$null
    if ($LASTEXITCODE -ne 0) {
        return [PSCustomObject]@{
            platform = 'youtube'
            platform_id = $VideoId
            source_uri = "youtube:$VideoId"
            url = $InputUrl
            title = ''
            author = ''
            publisher = ''
            published_at = ''
            duration_seconds = ''
            raw = $null
            captured_at = (Get-Date).ToString('o')
            fetch_method = 'youtube_identity_only_yt_dlp_failed'
        }
    }

    $meta = ($rawLines -join "`n") | ConvertFrom-Json
    $published = Get-JsonProperty -Object $meta -Names @('timestamp')
    if (-not [string]::IsNullOrWhiteSpace($published)) {
        $published = ([DateTimeOffset]::FromUnixTimeSeconds([int64]$published)).ToString('yyyy-MM-dd HH:mm:ss zzz')
    } else {
        $published = Get-JsonProperty -Object $meta -Names @('upload_date')
    }

    $durationSeconds = Get-JsonProperty -Object $meta -Names @('duration')

    return [PSCustomObject]@{
        platform = 'youtube'
        platform_id = (Get-JsonProperty -Object $meta -Names @('id'))
        source_uri = 'youtube:' + (Get-JsonProperty -Object $meta -Names @('id'))
        url = (Get-JsonProperty -Object $meta -Names @('webpage_url', 'original_url'))
        title = (Get-JsonProperty -Object $meta -Names @('title'))
        author = (Get-JsonProperty -Object $meta -Names @('uploader', 'channel'))
        publisher = (Get-JsonProperty -Object $meta -Names @('channel', 'uploader'))
        published_at = $published
        duration_seconds = $durationSeconds
        raw = $meta
        captured_at = (Get-Date).ToString('o')
        fetch_method = 'yt_dlp_public_metadata'
    }
}

function Normalize-Slug {
    param([Parameter(Mandatory = $true)][string]$Text)
    $slugText = $Text.ToLowerInvariant() -replace '[^a-z0-9]+', '-'
    $slugText = $slugText -replace '-+', '-'
    $slugText = $slugText.Trim('-')
    if ([string]::IsNullOrWhiteSpace($slugText)) {
        return 'video-source'
    }

    return $slugText
}

function Copy-Artifact {
    param(
        [string]$Source,
        [Parameter(Mandatory = $true)][string]$Destination
    )

    if ([string]::IsNullOrWhiteSpace($Source)) {
        return $false
    }

    if (-not (Test-Path -LiteralPath $Source -PathType Leaf)) {
        throw "Artifact not found: $Source"
    }

    Copy-Item -LiteralPath $Source -Destination $Destination -Force
    return $true
}

function Write-JsonArtifact {
    param(
        [Parameter(Mandatory = $true)]$Value,
        [Parameter(Mandatory = $true)][string]$Destination
    )

    ($Value | ConvertTo-Json -Depth 8) | Set-Content -LiteralPath $Destination -Encoding UTF8
}

$projectRootFull = Get-FullPath (Resolve-Path -LiteralPath $ProjectRoot).Path
$rawVideosDir = Join-Path $projectRootFull 'raw\videos'
$templatePath = Join-Path $projectRootFull 'templates\video-source.md'

if (-not (Test-Path -LiteralPath $templatePath -PathType Leaf)) {
    throw "Template not found: $templatePath"
}

New-Item -ItemType Directory -Path $rawVideosDir -Force | Out-Null

$identity = Get-VideoIdentity -InputUrl $Url
$meta = $null

if (-not [string]::IsNullOrWhiteSpace($MetadataPath)) {
    $metadataFull = Get-FullPath (Resolve-Path -LiteralPath $MetadataPath).Path
    $loaded = Get-Content -LiteralPath $metadataFull -Raw | ConvertFrom-Json
    $meta = [PSCustomObject]@{
        platform = Get-JsonProperty -Object $loaded -Names @('platform')
        platform_id = Get-JsonProperty -Object $loaded -Names @('platform_id', 'bvid', 'id')
        source_uri = Get-JsonProperty -Object $loaded -Names @('source_uri')
        url = Get-JsonProperty -Object $loaded -Names @('url', 'source_url', 'webpage_url')
        title = Get-JsonProperty -Object $loaded -Names @('title')
        author = Get-JsonProperty -Object $loaded -Names @('author', 'owner', 'uploader', 'channel')
        publisher = Get-JsonProperty -Object $loaded -Names @('publisher', 'owner', 'uploader', 'channel')
        published_at = Get-JsonProperty -Object $loaded -Names @('published_at', 'pubdate_local', 'upload_date')
        duration_seconds = Get-JsonProperty -Object $loaded -Names @('duration_seconds', 'duration')
        raw = $loaded
        captured_at = Get-JsonProperty -Object $loaded -Names @('captured_at')
        fetch_method = 'metadata_path'
    }
} elseif (-not $NoMetadataFetch) {
    if ($identity.Platform -eq 'bilibili' -and -not [string]::IsNullOrWhiteSpace($identity.PlatformId)) {
        $meta = Get-BilibiliMetadata -Bvid $identity.PlatformId -InputUrl $Url
    } elseif ($identity.Platform -eq 'youtube' -and -not [string]::IsNullOrWhiteSpace($identity.PlatformId)) {
        $meta = Get-YoutubeMetadata -VideoId $identity.PlatformId -InputUrl $Url
    }
}

if ($null -eq $meta) {
    $meta = [PSCustomObject]@{
        platform = $identity.Platform
        platform_id = $identity.PlatformId
        source_uri = if ($identity.PlatformId) { "$($identity.Platform):$($identity.PlatformId)" } else { '' }
        url = $Url
        title = ''
        author = ''
        publisher = ''
        published_at = ''
        duration_seconds = ''
        raw = $null
        captured_at = (Get-Date).ToString('o')
        fetch_method = 'identity_only'
    }
}

$platformValue = if ($Platform) { $Platform } elseif ($meta.platform) { [string]$meta.platform } else { $identity.Platform }
$platformIdValue = if ($PlatformId) { $PlatformId } elseif ($meta.platform_id) { [string]$meta.platform_id } else { $identity.PlatformId }
$sourceUrlValue = if ($meta.url) { [string]$meta.url } else { $Url }
$titleValue = if ($Title) { $Title } elseif ($meta.title) { [string]$meta.title } else { $sourceUrlValue }
$authorValue = if ($Author) { $Author } elseif ($meta.author) { [string]$meta.author } else { '' }
$publisherValue = if ($meta.publisher) { [string]$meta.publisher } else { $authorValue }
$publishedAtValue = if ($PublishedAt) { $PublishedAt } elseif ($meta.published_at) { [string]$meta.published_at } else { '' }
$durationValue = if ($Duration) { $Duration } elseif ($meta.duration_seconds) { ([string]$meta.duration_seconds + 's') } else { '' }
$capturedAtValue = (Get-Date).ToString('yyyy-MM-dd HH:mm:ss zzz')

if ([string]::IsNullOrWhiteSpace($SourceFamily)) {
    $SourceFamily = "$platformValue-video-source"
}

if ([string]::IsNullOrWhiteSpace($Slug)) {
    $datePrefix = (Get-Date).ToString('yyyy-MM-dd')
    $slugSeed = "$datePrefix-$platformValue-$platformIdValue-source"
    $Slug = Normalize-Slug -Text $slugSeed
}

$cardPath = Join-Path $rawVideosDir ($Slug + '.md')
$artifactDir = Join-Path $rawVideosDir $Slug

if ((Test-Path -LiteralPath $cardPath) -and -not $Force) {
    throw "Card already exists: $cardPath. Use -Force to overwrite."
}

if ((Test-Path -LiteralPath $artifactDir) -and -not $Force) {
    throw "Artifact directory already exists: $artifactDir. Use -Force to overwrite."
}

New-Item -ItemType Directory -Path $artifactDir -Force | Out-Null

$artifactSourceFull = Resolve-PathOrNull -Path $ArtifactSourceDir
if ($artifactSourceFull) {
    if (-not $TranscriptPath) { $TranscriptPath = Resolve-PathOrNull -Path (Join-Path $artifactSourceFull 'transcript.txt') }
    if (-not $SegmentsPath) { $SegmentsPath = Resolve-PathOrNull -Path (Join-Path $artifactSourceFull 'segments.md') }
    if (-not $SegmentsJsonPath) { $SegmentsJsonPath = Resolve-PathOrNull -Path (Join-Path $artifactSourceFull 'segments.json') }
    if (-not $TranscriptMetadataPath) {
        $TranscriptMetadataPath = Resolve-PathOrNull -Path (Join-Path $artifactSourceFull 'transcript-meta.json')
        if (-not $TranscriptMetadataPath) {
            $TranscriptMetadataPath = Resolve-PathOrNull -Path (Join-Path $artifactSourceFull 'asr-meta.json')
        }
    }
    if (-not $LedgerPath) { $LedgerPath = Resolve-PathOrNull -Path (Join-Path $artifactSourceFull 'acquisition-ledger.json') }
    if (-not $SourceMetadataPath) { $SourceMetadataPath = Resolve-PathOrNull -Path (Join-Path $artifactSourceFull 'source-metadata.json') }
}

$needsArtifacts = ($ProcessingLevel -eq 'medium' -or $ProcessingLevel -eq 'heavy')

if ($needsArtifacts) {
    if (-not $TranscriptPath) {
        throw 'Medium/heavy video cards require -TranscriptPath or ArtifactSourceDir\transcript.txt.'
    }

    if (-not $SegmentsPath -and -not $AllowIncompleteArtifacts) {
        throw 'Medium/heavy video cards require -SegmentsPath or ArtifactSourceDir\segments.md.'
    }

    if (-not $TranscriptMetadataPath -and -not $AllowIncompleteArtifacts) {
        throw 'Medium/heavy video cards require -TranscriptMetadataPath or ArtifactSourceDir\transcript-meta.json.'
    }
}

$transcriptDest = Join-Path $artifactDir 'transcript.txt'
$segmentsDest = Join-Path $artifactDir 'segments.md'
$segmentsJsonDest = Join-Path $artifactDir 'segments.json'
$transcriptMetaDest = Join-Path $artifactDir 'transcript-meta.json'
$ledgerDest = Join-Path $artifactDir 'acquisition-ledger.json'
$sourceMetaDest = Join-Path $artifactDir 'source-metadata.json'

$artifactWarnings = New-Object System.Collections.Generic.List[string]

if ($TranscriptPath) {
    Copy-Artifact -Source $TranscriptPath -Destination $transcriptDest | Out-Null
}

if ($SegmentsPath) {
    Copy-Artifact -Source $SegmentsPath -Destination $segmentsDest | Out-Null
} elseif ($AllowIncompleteArtifacts -and $needsArtifacts) {
    Set-Content -LiteralPath $segmentsDest -Encoding UTF8 -Value '[00:00] timestamps not supplied; runner placeholder created for review visibility.'
    $artifactWarnings.Add('segments.md was generated as an incomplete placeholder.') | Out-Null
}

if ($SegmentsJsonPath) {
    Copy-Artifact -Source $SegmentsJsonPath -Destination $segmentsJsonDest | Out-Null
}

if ($TranscriptMetadataPath) {
    Copy-Artifact -Source $TranscriptMetadataPath -Destination $transcriptMetaDest | Out-Null
} elseif ($AllowIncompleteArtifacts -and $needsArtifacts) {
    Write-JsonArtifact -Destination $transcriptMetaDest -Value ([PSCustomObject]@{
        status = 'incomplete_placeholder'
        transcript_method = $TranscriptMethod
        note = 'Transcript metadata was not supplied to new-video-source-card.ps1.'
        captured_at = (Get-Date).ToString('o')
    })
    $artifactWarnings.Add('transcript-meta.json was generated as an incomplete placeholder.') | Out-Null
}

if ($LedgerPath) {
    Copy-Artifact -Source $LedgerPath -Destination $ledgerDest | Out-Null
} elseif ($needsArtifacts -or $TranscriptPath) {
    Write-JsonArtifact -Destination $ledgerDest -Value ([PSCustomObject]@{
        url = $sourceUrlValue
        captured_at = (Get-Date).ToString('o')
        access_boundary = 'public'
        steps = @(
            [PSCustomObject]@{
                method = 'new-video-source-card.ps1'
                status = 'generated_card_from_supplied_artifacts'
                result = 'Source-card skeleton and project-visible artifact paths created.'
                cookies_used = $false
                cloud_api_used = $false
            }
        )
        media_retention = if ($TranscriptMethod -eq 'local_asr') { 'delete_or_confirm_via_finalizer' } else { 'not_downloaded' }
        scratch_boundary = 'If .codex was used, it is scratch only and must not be the final archive.'
    })
}

if ($SourceMetadataPath) {
    Copy-Artifact -Source $SourceMetadataPath -Destination $sourceMetaDest | Out-Null
} else {
    Write-JsonArtifact -Destination $sourceMetaDest -Value ([PSCustomObject]@{
        platform = $platformValue
        platform_id = $platformIdValue
        source_uri = if ($platformIdValue) { ($platformValue + ':' + $platformIdValue) } else { '' }
        url = $sourceUrlValue
        title = $titleValue
        author = $authorValue
        publisher = $publisherValue
        published_at = $publishedAtValue
        duration = $durationValue
        captured_at = (Get-Date).ToString('o')
        metadata_fetch_method = $meta.fetch_method
        raw_metadata_available = ($null -ne $meta.raw)
    })
}

$transcriptRel = if (Test-Path -LiteralPath $transcriptDest) { Get-RelativePathCompat -BasePath $projectRootFull -TargetPath $transcriptDest } else { '' }
$segmentsRel = if (Test-Path -LiteralPath $segmentsDest) { Get-RelativePathCompat -BasePath $projectRootFull -TargetPath $segmentsDest } else { '' }
$transcriptMetaRel = if (Test-Path -LiteralPath $transcriptMetaDest) { Get-RelativePathCompat -BasePath $projectRootFull -TargetPath $transcriptMetaDest } else { '' }
$ledgerRel = if (Test-Path -LiteralPath $ledgerDest) { Get-RelativePathCompat -BasePath $projectRootFull -TargetPath $ledgerDest } else { '' }
$rawLocationRel = Get-RelativePathCompat -BasePath $projectRootFull -TargetPath $cardPath

$sourceId = if ($platformIdValue) { "$platformValue-$platformIdValue" } else { "$platformValue-source" }
$sourceUri = if ($platformIdValue) { ($platformValue + ':' + $platformIdValue) } else { '' }
$mediaRetention = if ($TranscriptMethod -eq 'local_asr') { 'deleted' } elseif ($TranscriptMethod -eq 'none') { 'not_downloaded' } else { 'not_downloaded' }
$topicsValue = @($Topics + @($platformValue) | Where-Object { -not [string]::IsNullOrWhiteSpace($_) } | Select-Object -Unique)
$tagsValue = @('raw-video', $platformValue, 'candidate-only') | Where-Object { -not [string]::IsNullOrWhiteSpace($_) }

$frontMatter = New-Object System.Collections.Generic.List[string]
$frontMatter.Add('---') | Out-Null
$frontMatter.Add('type: source') | Out-Null
$frontMatter.Add('status: source-captured') | Out-Null
$frontMatter.Add('title: ' + (ConvertTo-YamlScalar $titleValue)) | Out-Null
$frontMatter.Add('source_id: ' + (ConvertTo-YamlScalar $sourceId)) | Out-Null
$frontMatter.Add('source_uri: ' + (ConvertTo-YamlScalar $sourceUri)) | Out-Null
$frontMatter.Add('source_url: ' + (ConvertTo-YamlScalar $sourceUrlValue)) | Out-Null
$frontMatter.Add('source_type: video') | Out-Null
$frontMatter.Add('platform: ' + (ConvertTo-YamlScalar $platformValue)) | Out-Null
$frontMatter.Add('platform_id: ' + (ConvertTo-YamlScalar $platformIdValue)) | Out-Null
$frontMatter.Add('author: ' + (ConvertTo-YamlScalar $authorValue)) | Out-Null
$frontMatter.Add('publisher: ' + (ConvertTo-YamlScalar $publisherValue)) | Out-Null
$frontMatter.Add('published_at: ' + (ConvertTo-YamlScalar $publishedAtValue)) | Out-Null
$frontMatter.Add('updated_at:') | Out-Null
$frontMatter.Add('duration: ' + (ConvertTo-YamlScalar $durationValue)) | Out-Null
$frontMatter.Add('captured_at: ' + (ConvertTo-YamlScalar $capturedAtValue)) | Out-Null
$frontMatter.Add('captured_by: Codex') | Out-Null
$frontMatter.Add('raw_location: ' + (ConvertTo-YamlScalar $rawLocationRel)) | Out-Null
$frontMatter.Add('processing_mode: runner') | Out-Null
$frontMatter.Add('processing_level: ' + (ConvertTo-YamlScalar $ProcessingLevel)) | Out-Null
$frontMatter.Add('review_priority: normal') | Out-Null
$frontMatter.Add('review_owner: Codex') | Out-Null
$frontMatter.Add('formalization_status: raw-only') | Out-Null
$frontMatter.Add('access_boundary: public') | Out-Null
$frontMatter.Add('transcript_method: ' + (ConvertTo-YamlScalar $TranscriptMethod)) | Out-Null
$frontMatter.Add('transcript_location: ' + (ConvertTo-YamlScalar $transcriptRel)) | Out-Null
$frontMatter.Add('segments_location: ' + (ConvertTo-YamlScalar $segmentsRel)) | Out-Null
$frontMatter.Add('transcript_metadata_location: ' + (ConvertTo-YamlScalar $transcriptMetaRel)) | Out-Null
$frontMatter.Add('ledger_location: ' + (ConvertTo-YamlScalar $ledgerRel)) | Out-Null
$frontMatter.Add('media_retention: ' + (ConvertTo-YamlScalar $mediaRetention)) | Out-Null
$frontMatter.Add('source_status: active') | Out-Null
$frontMatter.Add('topics:') | Out-Null
ConvertTo-YamlList $topicsValue | ForEach-Object { $frontMatter.Add($_) | Out-Null }
$frontMatter.Add('projects:') | Out-Null
$frontMatter.Add('  - verified-action-knowledge-system') | Out-Null
$frontMatter.Add('source_family: ' + (ConvertTo-YamlScalar $SourceFamily)) | Out-Null
$frontMatter.Add('upstream_sources: []') | Out-Null
$frontMatter.Add('verification_status: unverified') | Out-Null
$frontMatter.Add('candidate_relation_suggestions: []') | Out-Null
$frontMatter.Add('tags:') | Out-Null
ConvertTo-YamlList $tagsValue | ForEach-Object { $frontMatter.Add($_) | Out-Null }
$frontMatter.Add('---') | Out-Null

$template = Get-Content -LiteralPath $templatePath -Raw
$body = $template -replace '(?s)^---.*?---\s*', ''
$heading = '# ' + $titleValue
$body = $body -replace '(?m)^#\s+.*$', $heading

$cardText = ($frontMatter -join "`r`n") + "`r`n`r`n" + $body
$cardText | Set-Content -LiteralPath $cardPath -Encoding UTF8

$finalizeResult = $null
if ($Finalize) {
    $finalizer = Join-Path $PSScriptRoot 'finalize-video-intake.ps1'
    if (-not (Test-Path -LiteralPath $finalizer -PathType Leaf)) {
        throw "Finalizer not found: $finalizer"
    }

    $args = @('-ExecutionPolicy', 'Bypass', '-File', $finalizer, '-CardPath', $cardPath, '-ProjectRoot', $projectRootFull)
    if ($SkipObsidianSync) {
        $args += '-SkipObsidianSync'
    }
    if ($ScratchPath) {
        $args += @('-ScratchPath', $ScratchPath)
    }
    if ($DeleteScratchMedia) {
        $args += '-DeleteScratchMedia'
    }

    $finalizeText = & powershell @args
    if ($LASTEXITCODE -ne 0) {
        throw "finalize-video-intake.ps1 failed for $cardPath"
    }
    $finalizeResult = ($finalizeText -join "`n")
}

$result = [PSCustomObject]@{
    Status = 'ok'
    CardPath = Get-RelativePathCompat -BasePath $projectRootFull -TargetPath $cardPath
    ArtifactDirectory = Get-RelativePathCompat -BasePath $projectRootFull -TargetPath $artifactDir
    Platform = $platformValue
    PlatformId = $platformIdValue
    Title = $titleValue
    ProcessingLevel = $ProcessingLevel
    TranscriptMethod = $TranscriptMethod
    Finalized = [bool]$Finalize
    Warnings = $artifactWarnings
}

if ($Json) {
    $result | ConvertTo-Json -Depth 6
} else {
    Write-Host "VAKS video source-card runner: ok"
    Write-Host ""
    Write-Host "Card:"
    Write-Host "  $($result.CardPath)"
    Write-Host "Artifacts:"
    Write-Host "  $($result.ArtifactDirectory)"
    Write-Host "Platform:"
    Write-Host "  $($result.Platform) / $($result.PlatformId)"
    Write-Host "Title:"
    Write-Host "  $($result.Title)"
    if ($artifactWarnings.Count -gt 0) {
        Write-Host ""
        Write-Host "Warnings:"
        $artifactWarnings | ForEach-Object { Write-Host "  - $_" }
    }
    if ($Finalize -and $finalizeResult) {
        Write-Host ""
        Write-Host "Finalizer output:"
        Write-Host $finalizeResult
    }
}
