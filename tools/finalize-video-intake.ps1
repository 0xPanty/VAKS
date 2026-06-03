<#
.SYNOPSIS
Finalizes a VAKS video source card by linting retained artifacts and syncing them to the formal Obsidian vault.

.DESCRIPTION
This is a project-local connector for the VAKS project.
It does not transcribe media, summarize content, review claims, or promote knowledge.

It checks that a medium/heavy video source card points to project-visible
transcript, timestamp segments, ASR metadata, and ledger files, then copies the
card and artifact folder to the formal Obsidian vault and verifies hashes.

.EXAMPLE
powershell -ExecutionPolicy Bypass -File .\tools\finalize-video-intake.ps1 `
  -CardPath .\raw\videos\2026-06-04-bilibili-obsidian-8-plugins-source.md `
  -ScratchPath C:\Users\Administrator\.codex\video-research\BV1Gjd5BPEhh\asr-vaks `
  -DeleteScratchMedia
#>

[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [string]$CardPath,

    [string]$ProjectRoot = (Get-Location).Path,

    [string]$ObsidianRoot = ('H:\Obsidian\' + [char]0x8D44 + [char]0x6599 + [char]0x5E93),

    [string]$ScratchPath,

    [switch]$DeleteScratchMedia,

    [switch]$SkipObsidianSync,

    [switch]$Json
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

function Get-FullPath {
    param([Parameter(Mandatory = $true)][string]$Path)
    return [System.IO.Path]::GetFullPath($Path)
}

function Assert-UnderRoot {
    param(
        [Parameter(Mandatory = $true)][string]$Path,
        [Parameter(Mandatory = $true)][string]$Root,
        [Parameter(Mandatory = $true)][string]$Name
    )

    $rootFull = Get-FullPath $Root
    $pathFull = if ([System.IO.Path]::IsPathRooted($Path)) {
        Get-FullPath $Path
    } else {
        Get-FullPath (Join-Path $rootFull $Path)
    }

    $rootWithSep = $rootFull.TrimEnd('\', '/') + [System.IO.Path]::DirectorySeparatorChar
    if (($pathFull -ne $rootFull) -and (-not $pathFull.StartsWith($rootWithSep, [System.StringComparison]::OrdinalIgnoreCase))) {
        throw "$Name escapes project root: $Path"
    }

    return $pathFull
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
    return [System.Uri]::UnescapeDataString($baseUri.MakeRelativeUri($targetUri).ToString()).Replace('/', [System.IO.Path]::DirectorySeparatorChar)
}

function Read-FrontMatterFields {
    param([Parameter(Mandatory = $true)][string]$Text)

    $lines = $Text -split "`r?`n"
    if (($lines.Count -eq 0) -or ($lines[0].Trim() -ne '---')) {
        throw 'Source card must start with YAML frontmatter.'
    }

    $fields = @{}
    for ($i = 1; $i -lt $lines.Count; $i++) {
        $line = $lines[$i]
        if ($line.Trim() -eq '---') {
            break
        }

        if ($line -match '^\s*([A-Za-z0-9_-]+):\s*(.*?)\s*$') {
            $key = $matches[1]
            $value = $matches[2].Trim()
            $value = $value.Trim('"')
            $fields[$key] = $value
        }
    }

    return $fields
}

function Add-UniqueFile {
    param(
        [Parameter(Mandatory = $true)]$Map,
        [Parameter(Mandatory = $true)][string]$Path
    )

    $full = Get-FullPath $Path
    if (-not $Map.Contains($full)) {
        $Map[$full] = $true
    }
}

function Test-IsScratchMediaFile {
    param([Parameter(Mandatory = $true)][System.IO.FileInfo]$File)

    $mediaExtensions = @('.m4s', '.m4a', '.mp4', '.webm', '.wav', '.mp3', '.aac', '.flac', '.mkv', '.mov', '.avi', '.ts', '.m3u8', '.part')
    return (($mediaExtensions -contains $File.Extension.ToLowerInvariant()) -or ($File.Name -match 'playurl'))
}

$projectRootFull = Get-FullPath (Resolve-Path -LiteralPath $ProjectRoot).Path
$cardFull = Assert-UnderRoot -Path $CardPath -Root $projectRootFull -Name 'CardPath'

if (-not (Test-Path -LiteralPath $cardFull -PathType Leaf)) {
    throw "Source card not found: $cardFull"
}

$cardText = Get-Content -LiteralPath $cardFull -Raw
$fields = Read-FrontMatterFields -Text $cardText

$requiredArtifactFields = @(
    @{ Name = 'transcript_location'; Aliases = @() },
    @{ Name = 'segments_location'; Aliases = @() },
    @{ Name = 'transcript_metadata_location'; Aliases = @('asr_metadata_location') },
    @{ Name = 'ledger_location'; Aliases = @() }
)

$warnings = New-Object System.Collections.Generic.List[string]
$artifactChecks = New-Object System.Collections.Generic.List[object]

foreach ($fieldSpec in $requiredArtifactFields) {
    $fieldName = $fieldSpec.Name
    $actualFieldName = $null
    $fieldValue = $null

    if ($fields.ContainsKey($fieldName)) {
        $actualFieldName = $fieldName
        $fieldValue = $fields[$fieldName]
    } else {
        foreach ($alias in $fieldSpec.Aliases) {
            if ($fields.ContainsKey($alias)) {
                $actualFieldName = $alias
                $fieldValue = $fields[$alias]
                $warnings.Add("$alias is deprecated; use $fieldName for subtitle/ASR metadata.") | Out-Null
                break
            }
        }
    }

    if ([string]::IsNullOrWhiteSpace($actualFieldName)) {
        throw "Missing required field: $fieldName"
    }

    if ([string]::IsNullOrWhiteSpace($fieldValue)) {
        throw "Empty required field: $actualFieldName"
    }

    if ($fieldValue -match '^\s*inline\s*$') {
        throw "$actualFieldName must point to a project-visible file, not inline."
    }

    if ($fieldValue -match '(^|[\\/])\.codex([\\/]|$)') {
        throw "$actualFieldName must not point to .codex scratch: $fieldValue"
    }

    $artifactFull = Assert-UnderRoot -Path $fieldValue -Root $projectRootFull -Name $actualFieldName
    if (-not (Test-Path -LiteralPath $artifactFull -PathType Leaf)) {
        throw "$actualFieldName target does not exist: $fieldValue"
    }

    $artifactChecks.Add([PSCustomObject]@{
        Field = $fieldName
        SourceField = $actualFieldName
        Path = (Get-RelativePathCompat -BasePath $projectRootFull -TargetPath $artifactFull)
        Exists = $true
        Bytes = (Get-Item -LiteralPath $artifactFull).Length
    }) | Out-Null
}

if ($fields.ContainsKey('formalization_status') -and $fields['formalization_status'] -notmatch 'raw-only|candidate') {
    $warnings.Add("formalization_status is not raw-only/candidate-like: $($fields['formalization_status'])") | Out-Null
}

if ($fields.ContainsKey('verification_status') -and $fields['verification_status'] -notmatch 'unverified|candidate|unknown') {
    $warnings.Add("verification_status may overclaim for a source card: $($fields['verification_status'])") | Out-Null
}

if ($fields.ContainsKey('media_retention') -and $fields.ContainsKey('transcript_method')) {
    $usedLocalMedia = $fields['transcript_method'] -match 'asr|audio|download'
    $mediaWasRetained = $fields['media_retention'] -notmatch 'deleted|not_downloaded|none'
    if ($usedLocalMedia -and $mediaWasRetained) {
        $warnings.Add("media_retention may retain local media after ASR: $($fields['media_retention'])") | Out-Null
    }
}

$syncMap = [ordered]@{}
Add-UniqueFile -Map $syncMap -Path $cardFull

$cardDirectory = Split-Path -Parent $cardFull
$artifactDirectory = Join-Path $cardDirectory ([System.IO.Path]::GetFileNameWithoutExtension($cardFull))
if (Test-Path -LiteralPath $artifactDirectory -PathType Container) {
    Get-ChildItem -LiteralPath $artifactDirectory -File | Sort-Object Name | ForEach-Object {
        if (Test-IsScratchMediaFile -File $_) {
            throw "Project artifact directory contains media/playurl scratch file; remove it or keep it outside the default video intake archive: $($_.FullName)"
        }

        Add-UniqueFile -Map $syncMap -Path $_.FullName
    }
} else {
    $warnings.Add("Sibling artifact directory does not exist: $artifactDirectory") | Out-Null
}

foreach ($check in $artifactChecks) {
    Add-UniqueFile -Map $syncMap -Path (Assert-UnderRoot -Path $check.Path -Root $projectRootFull -Name $check.Field)
}

$syncResults = New-Object System.Collections.Generic.List[object]

if (-not $SkipObsidianSync) {
    $obsidianRootFull = Get-FullPath $ObsidianRoot
    New-Item -ItemType Directory -Path $obsidianRootFull -Force | Out-Null

    foreach ($sourcePath in $syncMap.Keys) {
        $relativePath = Get-RelativePathCompat -BasePath $projectRootFull -TargetPath $sourcePath
        $destinationPath = Join-Path $obsidianRootFull $relativePath
        $destinationDirectory = Split-Path -Parent $destinationPath

        New-Item -ItemType Directory -Path $destinationDirectory -Force | Out-Null
        Copy-Item -LiteralPath $sourcePath -Destination $destinationPath -Force

        $sourceHash = (Get-FileHash -LiteralPath $sourcePath -Algorithm SHA256).Hash
        $destinationHash = (Get-FileHash -LiteralPath $destinationPath -Algorithm SHA256).Hash

        if ($sourceHash -ne $destinationHash) {
            throw "Hash mismatch after sync: $relativePath"
        }

        $syncResults.Add([PSCustomObject]@{
            File = $relativePath
            Hash = $sourceHash
            Match = $true
        }) | Out-Null
    }
}

$deletedScratch = New-Object System.Collections.Generic.List[object]

if ($DeleteScratchMedia) {
    if ([string]::IsNullOrWhiteSpace($ScratchPath)) {
        throw '-DeleteScratchMedia requires -ScratchPath.'
    }

    if (-not (Test-Path -LiteralPath $ScratchPath -PathType Container)) {
        $warnings.Add("ScratchPath does not exist, no media deleted: $ScratchPath") | Out-Null
    } else {
        $scratchFull = Get-FullPath (Resolve-Path -LiteralPath $ScratchPath).Path
        if ($scratchFull -notmatch '\\\.codex\\video-research(\\|$)') {
            throw 'DeleteScratchMedia is only allowed under .codex\video-research by default.'
        }

        $scratchWithSep = $scratchFull.TrimEnd('\', '/') + [System.IO.Path]::DirectorySeparatorChar

        Get-ChildItem -LiteralPath $scratchFull -Recurse -File | Where-Object {
            Test-IsScratchMediaFile -File $_
        } | ForEach-Object {
            $candidate = Get-FullPath $_.FullName
            if (($candidate -ne $scratchFull) -and $candidate.StartsWith($scratchWithSep, [System.StringComparison]::OrdinalIgnoreCase)) {
                $bytes = $_.Length
                Remove-Item -LiteralPath $candidate -Force
                $deletedScratch.Add([PSCustomObject]@{
                    File = $candidate
                    Bytes = $bytes
                }) | Out-Null
            }
        }
    }
}

$result = [PSCustomObject]@{
    Status = 'ok'
    Card = (Get-RelativePathCompat -BasePath $projectRootFull -TargetPath $cardFull)
    ProjectRoot = $projectRootFull
    ObsidianRoot = if ($SkipObsidianSync) { $null } else { Get-FullPath $ObsidianRoot }
    RequiredArtifacts = $artifactChecks
    SyncedFiles = $syncResults
    DeletedScratchMedia = $deletedScratch
    Warnings = $warnings
}

if ($Json) {
    $result | ConvertTo-Json -Depth 6
} else {
    Write-Host "VAKS video intake finalize: ok"
    Write-Host ""
    Write-Host "Card:"
    Write-Host "  $($result.Card)"
    Write-Host ""
    Write-Host "Required artifacts:"
    $artifactChecks | Format-Table Field, Path, Exists, Bytes -AutoSize

    if (-not $SkipObsidianSync) {
        Write-Host ""
        Write-Host "Synced to Obsidian with matching SHA256:"
        $syncResults | Select-Object File, Match, @{Name='HashPrefix'; Expression={$_.Hash.Substring(0, 16)}} | Format-Table -AutoSize
    }

    if ($deletedScratch.Count -gt 0) {
        Write-Host ""
        Write-Host "Deleted scratch media:"
        $deletedScratch | Format-Table File, Bytes -AutoSize
    }

    if ($warnings.Count -gt 0) {
        Write-Host ""
        Write-Host "Warnings:"
        $warnings | ForEach-Object { Write-Host "  - $_" }
    }
}
