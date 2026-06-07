<#
.SYNOPSIS
Captures public Bilibili video metadata, public subtitles, or optional local ASR artifacts.

.DESCRIPTION
This project-local helper automates the public Bilibili acquisition ladder for
VAKS video intake. It uses public APIs with browser-like headers, avoids
cookies, avoids cloud APIs, and deletes downloaded media after ASR unless
-KeepMedia is explicitly set.

It creates retained text artifacts only. It does not create a source card,
sync to Obsidian, summarize content, review claims, or promote knowledge.

.EXAMPLE
powershell -ExecutionPolicy Bypass -File .\tools\bilibili-public-video-helper.ps1 `
  -Url https://www.bilibili.com/video/BV1xxxx/ `
  -OutputDir C:\Users\Administrator\.codex\video-research\BV1xxxx\asr-vaks `
  -RunAsr
#>

[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [string]$Url,

    [string]$OutputDir,

    [switch]$RunAsr,

    [ValidateSet('tiny', 'base', 'small', 'medium', 'large-v3')]
    [string]$WhisperModel = 'small',

    [ValidateSet('auto', 'cuda', 'cpu')]
    [string]$Device = 'auto',

    [switch]$KeepMedia,

    [string]$PythonCommand = 'python',

    [switch]$Json
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

function Get-BvidFromUrl {
    param([Parameter(Mandatory = $true)][string]$InputUrl)

    if ($InputUrl -match '(BV[0-9A-Za-z]+)') {
        return $matches[1]
    }

    throw "Cannot find Bilibili BV id in URL: $InputUrl"
}

$bvid = Get-BvidFromUrl -InputUrl $Url

if ([string]::IsNullOrWhiteSpace($OutputDir)) {
    $safeStamp = (Get-Date).ToString('yyyyMMdd-HHmmss')
    $OutputDir = Join-Path $env:USERPROFILE ".codex\video-research\$safeStamp-$bvid\asr-vaks"
}

$env:BILI_HELPER_URL = $Url
$env:BILI_HELPER_OUTPUT_DIR = [System.IO.Path]::GetFullPath($OutputDir)
$env:BILI_HELPER_RUN_ASR = if ($RunAsr) { '1' } else { '0' }
$env:BILI_HELPER_KEEP_MEDIA = if ($KeepMedia) { '1' } else { '0' }
$env:BILI_HELPER_MODEL = $WhisperModel
$env:BILI_HELPER_DEVICE = $Device
$env:BILI_HELPER_JSON = if ($Json) { '1' } else { '0' }
$env:PYTHONIOENCODING = 'utf-8'

$python = @'
import hashlib
import json
import os
import re
import sys
import time
from datetime import datetime, timezone, timedelta
from pathlib import Path
from urllib.parse import urlparse

import requests


URL = os.environ["BILI_HELPER_URL"]
OUTPUT_DIR = Path(os.environ["BILI_HELPER_OUTPUT_DIR"])
RUN_ASR = os.environ.get("BILI_HELPER_RUN_ASR") == "1"
KEEP_MEDIA = os.environ.get("BILI_HELPER_KEEP_MEDIA") == "1"
MODEL_NAME = os.environ.get("BILI_HELPER_MODEL") or "small"
DEVICE_SETTING = os.environ.get("BILI_HELPER_DEVICE") or "auto"
JSON_ONLY = os.environ.get("BILI_HELPER_JSON") == "1"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/125.0.0.0 Safari/537.36",
    "Referer": URL if "bilibili.com" in URL else "https://www.bilibili.com/",
    "Origin": "https://www.bilibili.com",
}

ledger = []


def utc_now():
    return datetime.now(timezone.utc).isoformat()


def log(method, status, **kwargs):
    row = {
        "time": utc_now(),
        "method": method,
        "status": status,
        "cookies_used": False,
        "cloud_api_used": False,
    }
    row.update(kwargs)
    ledger.append(row)
    if not JSON_ONLY:
        print(json.dumps(row, ensure_ascii=False), flush=True)


def write_json(name, data):
    path = OUTPUT_DIR / name
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    return str(path)


def write_text(name, text):
    path = OUTPUT_DIR / name
    path.write_text(text, encoding="utf-8")
    return str(path)


def bvid_from_url(url):
    match = re.search(r"(BV[0-9A-Za-z]+)", url)
    if not match:
        raise RuntimeError(f"Cannot find Bilibili BV id in URL: {url}")
    return match.group(1)


def local_time_from_ts(ts):
    if not ts:
        return ""
    return datetime.fromtimestamp(int(ts), timezone.utc).astimezone(
        timezone(timedelta(hours=8))
    ).strftime("%Y-%m-%d %H:%M:%S %z")


def request_json(api_url, method):
    started = time.time()
    try:
        response = requests.get(api_url, headers=headers, timeout=30)
        response.raise_for_status()
        data = response.json()
        log(method, "ok", code=data.get("code"), elapsed_seconds=round(time.time() - started, 2))
        return data
    except Exception as exc:
        log(method, "failed", error=str(exc), elapsed_seconds=round(time.time() - started, 2))
        raise


def extract_subtitle_items(view_data, player_data):
    items = []

    view_subtitle = (((view_data.get("data") or {}).get("subtitle") or {}).get("list") or [])
    for item in view_subtitle:
        items.append(item)

    player_subtitle = (((player_data.get("data") or {}).get("subtitle") or {}).get("subtitles") or [])
    for item in player_subtitle:
        items.append(item)

    deduped = []
    seen = set()
    for item in items:
        url = item.get("subtitle_url") or item.get("url") or item.get("ai_subtitle_url") or ""
        lan = item.get("lan") or item.get("lang") or ""
        key = (lan, url)
        if url and key not in seen:
            seen.add(key)
            deduped.append(item)
    return deduped


def subtitle_url_of(item):
    url = item.get("subtitle_url") or item.get("url") or item.get("ai_subtitle_url") or ""
    if url.startswith("//"):
        url = "https:" + url
    return url


def save_subtitle(item):
    subtitle_url = subtitle_url_of(item)
    started = time.time()
    response = requests.get(subtitle_url, headers=headers, timeout=30)
    response.raise_for_status()
    data = response.json()
    log(
        "download_public_subtitle",
        "ok",
        language=item.get("lan") or item.get("lang") or "",
        elapsed_seconds=round(time.time() - started, 2),
    )

    body = data.get("body") or []
    segments = []
    text_parts = []
    for row in body:
        start = float(row.get("from", 0))
        end = float(row.get("to", start))
        text = str(row.get("content", "")).strip()
        if not text:
            continue
        segments.append({"start": round(start, 2), "end": round(end, 2), "text": text})
        text_parts.append(text)

    transcript = "".join(text_parts)
    write_text("transcript.txt", transcript)
    write_json("segments.json", segments)
    write_text("segments.md", "\n".join(
        f"[{row['start']:07.2f}-{row['end']:07.2f}] {row['text']}" for row in segments
    ))
    write_json("transcript-meta.json", {
        "source_url": URL,
        "bvid": BVID,
        "transcript_method": "public_subtitle",
        "subtitle_language": item.get("lan") or item.get("lang") or "",
        "subtitle_id": item.get("id") or item.get("subtitle_id") or "",
        "segment_count": len(segments),
        "text_chars": len(transcript),
        "captured_at": utc_now(),
        "quality_notes": "public Bilibili subtitle; raw source text, not reviewed knowledge",
    })
    return {
        "transcript_method": "public_subtitle",
        "segment_count": len(segments),
        "text_chars": len(transcript),
    }


def audio_candidates(play_data):
    audio = ((((play_data.get("data") or {}).get("dash") or {}).get("audio")) or [])
    candidates = []
    for item in audio:
        urls = []
        for key in ("baseUrl", "base_url"):
            if item.get(key):
                urls.append(item[key])
        for key in ("backupUrl", "backup_url"):
            if item.get(key):
                urls.extend(item[key])
        host = ""
        if urls:
            host = urlparse(urls[0]).netloc
        candidates.append({
            "id": item.get("id"),
            "bandwidth": item.get("bandwidth"),
            "mime_type": item.get("mimeType") or item.get("mime_type"),
            "codecs": item.get("codecs"),
            "host": host,
            "_urls": urls,
        })
    return sorted(candidates, key=lambda row: row.get("bandwidth") or 0, reverse=True)


def safe_audio_summary(candidates):
    return [
        {
            "id": row.get("id"),
            "bandwidth": row.get("bandwidth"),
            "mime_type": row.get("mime_type"),
            "codecs": row.get("codecs"),
            "host": row.get("host"),
        }
        for row in candidates
    ]


def download_audio(candidate):
    urls = candidate.get("_urls") or []
    if not urls:
        raise RuntimeError("Selected audio has no public URL")

    errors = []
    for idx, audio_url in enumerate(urls):
        media_path = OUTPUT_DIR / f"audio-{candidate.get('id') or 'unknown'}-{idx}.m4s"
        started = time.time()
        try:
            with requests.get(audio_url, headers=headers, stream=True, timeout=30) as response:
                response.raise_for_status()
                digest = hashlib.sha256()
                total = 0
                with media_path.open("wb") as handle:
                    for chunk in response.iter_content(chunk_size=1024 * 1024):
                        if not chunk:
                            continue
                        handle.write(chunk)
                        digest.update(chunk)
                        total += len(chunk)
            log(
                "download_public_audio",
                "ok",
                audio_id=candidate.get("id"),
                mirror_index=idx,
                bytes=total,
                sha256=digest.hexdigest(),
                elapsed_seconds=round(time.time() - started, 2),
                media_path=str(media_path),
            )
            return media_path
        except Exception as exc:
            errors.append(str(exc))
            log(
                "download_public_audio",
                "failed",
                audio_id=candidate.get("id"),
                mirror_index=idx,
                error=str(exc),
                elapsed_seconds=round(time.time() - started, 2),
            )
            if media_path.exists():
                try:
                    media_path.unlink()
                except OSError:
                    pass

    raise RuntimeError("All public audio mirrors failed: " + " | ".join(errors))


def choose_device():
    if DEVICE_SETTING != "auto":
        return DEVICE_SETTING
    try:
        import torch
        return "cuda" if torch.cuda.is_available() else "cpu"
    except Exception:
        return "cpu"


def transcribe(media_path):
    try:
        from faster_whisper import WhisperModel
    except Exception as exc:
        raise RuntimeError("faster-whisper is required for -RunAsr") from exc

    device = choose_device()
    compute_type = "float16" if device == "cuda" else "int8"
    started = time.time()
    model = WhisperModel(MODEL_NAME, device=device, compute_type=compute_type)
    segments_iter, info = model.transcribe(
        str(media_path),
        language="zh",
        vad_filter=True,
        beam_size=5,
    )

    segments = []
    text_parts = []
    for segment in segments_iter:
        text = segment.text.strip()
        if not text:
            continue
        row = {
            "start": round(float(segment.start), 2),
            "end": round(float(segment.end), 2),
            "text": text,
        }
        segments.append(row)
        text_parts.append(text)

    transcript = "".join(text_parts)
    write_text("transcript.txt", transcript)
    write_json("segments.json", segments)
    write_text("segments.md", "\n".join(
        f"[{row['start']:07.2f}-{row['end']:07.2f}] {row['text']}" for row in segments
    ))

    meta = {
        "source_url": URL,
        "bvid": BVID,
        "aid": AID,
        "cid": CID,
        "transcript_method": "local_asr",
        "asr_engine": "faster-whisper",
        "model": MODEL_NAME,
        "device": device,
        "compute_type": compute_type,
        "language": getattr(info, "language", None),
        "language_probability": getattr(info, "language_probability", None),
        "duration": getattr(info, "duration", None),
        "segment_count": len(segments),
        "text_chars": len(transcript),
        "elapsed_seconds": round(time.time() - started, 2),
        "captured_at": utc_now(),
        "quality_notes": "local ASR from public Bilibili audio; raw source text, not reviewed knowledge; proper nouns need confidence checks",
    }
    write_json("transcript-meta.json", meta)
    log("local_gpu_asr" if device == "cuda" else "local_cpu_asr", "ok", **meta)
    return meta


BVID = bvid_from_url(URL)
VIEW_URL = f"https://api.bilibili.com/x/web-interface/view?bvid={BVID}"
view = request_json(VIEW_URL, "public_view_api")
if view.get("code") != 0:
    raise RuntimeError(f"Bilibili view API failed: code={view.get('code')} message={view.get('message')}")

data = view.get("data") or {}
AID = data.get("aid")
CID = data.get("cid")
if not AID or not CID:
    pages = data.get("pages") or []
    if pages and pages[0].get("cid"):
        CID = pages[0]["cid"]
if not AID or not CID:
    raise RuntimeError("Bilibili metadata missing aid/cid")

source_metadata = {
    "platform": "bilibili",
    "platform_id": BVID,
    "source_uri": f"bilibili:{BVID}",
    "url": f"https://www.bilibili.com/video/{BVID}/",
    "input_url": URL,
    "title": data.get("title") or "",
    "author": ((data.get("owner") or {}).get("name") or ""),
    "uploader_id": ((data.get("owner") or {}).get("mid") or ""),
    "published_at": local_time_from_ts(data.get("pubdate")),
    "duration_seconds": data.get("duration"),
    "aid": AID,
    "cid": CID,
    "thumbnail": data.get("pic") or "",
    "description": data.get("desc") or "",
    "stats": data.get("stat") or {},
    "captured_at": utc_now(),
    "fetch_method": "bilibili_public_view_api",
    "access_boundary": "public_no_cookies",
}
write_json("source-metadata.json", source_metadata)

player_urls = [
    f"https://api.bilibili.com/x/player/v2?bvid={BVID}&cid={CID}",
    f"https://api.bilibili.com/x/player/wbi/v2?bvid={BVID}&cid={CID}",
]

player_results = []
subtitle_items = extract_subtitle_items(view, {"data": {"subtitle": {"subtitles": []}}})
for idx, player_url in enumerate(player_urls):
    try:
        player = request_json(player_url, f"public_subtitle_api_{idx + 1}")
        player_results.append(player)
        subtitle_items.extend(extract_subtitle_items(view, player))
    except Exception:
        pass

deduped_subtitles = []
seen_subtitles = set()
for item in subtitle_items:
    url = subtitle_url_of(item)
    key = (item.get("lan") or item.get("lang") or "", url)
    if url and key not in seen_subtitles:
        seen_subtitles.add(key)
        deduped_subtitles.append(item)

result = {
    "status": "metadata_only",
    "output_dir": str(OUTPUT_DIR),
    "source_metadata": source_metadata,
    "subtitles_found": len(deduped_subtitles),
    "transcript_method": "none",
    "media_deleted": None,
}

if deduped_subtitles:
    result.update(save_subtitle(deduped_subtitles[0]))
    result["status"] = "subtitle_saved"
else:
    log("public_subtitle_check", "empty", subtitle_api_count=len(player_results))
    play_url = f"https://api.bilibili.com/x/player/playurl?avid={AID}&cid={CID}&qn=0&fnval=16&fourk=1"
    play = request_json(play_url, "public_playurl_api")
    candidates = audio_candidates(play)
    write_json("audio-candidates.json", {
        "source_url": URL,
        "bvid": BVID,
        "aid": AID,
        "cid": CID,
        "audio_candidates": safe_audio_summary(candidates),
        "captured_at": utc_now(),
        "note": "CDN playurl values are intentionally not retained as stable source identity.",
    })
    result["public_audio_available"] = bool(candidates)
    result["audio_candidates"] = safe_audio_summary(candidates)

    if RUN_ASR:
        if not candidates:
            raise RuntimeError("No public audio candidate available for ASR")
        media_path = download_audio(candidates[0])
        try:
            result.update(transcribe(media_path))
            result["status"] = "asr_saved"
            result["transcript_method"] = "local_asr"
        finally:
            if KEEP_MEDIA:
                log("delete_scratch_media", "skipped_keep_media", media_path=str(media_path))
                result["media_deleted"] = False
            elif media_path.exists():
                media_path.unlink()
                log("delete_scratch_media", "ok", media_path=str(media_path))
                result["media_deleted"] = True
            else:
                log("delete_scratch_media", "already_absent", media_path=str(media_path))
                result["media_deleted"] = True

write_json("acquisition-ledger.json", ledger)

result["files"] = sorted(path.name for path in OUTPUT_DIR.iterdir() if path.is_file())
result["media_files"] = sorted(
    path.name for path in OUTPUT_DIR.iterdir()
    if path.is_file() and path.suffix.lower() in {".m4s", ".m4a", ".mp4", ".webm", ".wav", ".mp3", ".aac", ".flac", ".mkv", ".mov", ".avi", ".ts", ".part"}
)

print(json.dumps(result, ensure_ascii=False, indent=None if JSON_ONLY else 2), flush=True)
'@

$tempScript = Join-Path ([System.IO.Path]::GetTempPath()) ("bilibili-public-video-helper-" + [System.Guid]::NewGuid().ToString('N') + ".py")
try {
    Set-Content -LiteralPath $tempScript -Value $python -Encoding UTF8
    & $PythonCommand $tempScript
    if ($LASTEXITCODE -ne 0) {
        throw "bilibili public helper failed with exit code $LASTEXITCODE"
    }
} finally {
    if (Test-Path -LiteralPath $tempScript -PathType Leaf) {
        Remove-Item -LiteralPath $tempScript -Force
    }
}
