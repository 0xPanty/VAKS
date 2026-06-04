import json
import re
import subprocess
import tempfile
import time
from pathlib import Path

from materialize_clickback_snapshots_live_retry import (
    ROOT,
    SNAP,
    MANIFEST,
    clean_html,
    is_boilerplate_quote,
    landing_class,
    pick_quote,
    semantic_selector_success,
    sha,
    write_json,
)


def read_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def fetch_with_powershell(url):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".html") as tmp:
        tmp_path = Path(tmp.name)
    try:
        command = [
            "powershell",
            "-NoProfile",
            "-Command",
            "& { param([string]$u,[string]$o) $ProgressPreference='SilentlyContinue'; Invoke-WebRequest -Uri $u -UseBasicParsing -TimeoutSec 45 -OutFile $o }",
            url,
            str(tmp_path),
        ]
        result = subprocess.run(command, cwd=ROOT, capture_output=True, text=True, timeout=60)
        if result.returncode != 0:
            return "", {"ok": False, "url": url, "error": (result.stderr or result.stdout).strip()[:500]}
        raw = tmp_path.read_text(encoding="utf-8", errors="replace")
        cleaned = clean_html(raw)
        return cleaned, {"ok": True, "status": 200, "url": url, "bytes": len(raw)}
    finally:
        try:
            tmp_path.unlink()
        except OSError:
            pass


def main():
    SNAP.mkdir(exist_ok=True)
    manifest = read_json(MANIFEST)
    cases = read_json(ROOT / "candidate_cases.json")
    case_by_id = {case["id"]: case for case in cases}
    logs = []
    retried = 0

    for old_log in manifest.get("logs", []):
        if not old_log.get("fallback_used"):
            logs.append(old_log)
            continue

        case_id = old_log["case_id"]
        url = old_log["url"]
        case = case_by_id[case_id]
        snapshot_text, meta = fetch_with_powershell(url)
        live_ok = bool(meta.get("ok")) and len(snapshot_text) >= 500 and "SNAPSHOT_FETCH_FALLBACK" not in snapshot_text
        if not live_ok:
            logs.append({**old_log, **meta, "fallback_used": True, "snapshot_kind": "fallback_wrapper"})
            continue

        snapshot_text = re.sub(r"\s+", " ", snapshot_text).strip()
        quote, start, end, quote_strategy = pick_quote(snapshot_text, case)
        semantic_ok = semantic_selector_success(quote_strategy, quote)
        boilerplate_quote = is_boilerplate_quote(quote)
        landing = landing_class(quote_strategy)
        marker = f"{case_id}_REAL_SNAPSHOT"
        snapshot_text = f"{snapshot_text}\nmarker: {marker}\n"
        snapshot_path = SNAP / f"{case_id}.txt"
        snapshot_path.write_text(snapshot_text, encoding="utf-8")

        case["real_snapshot_url"] = url
        case["full_anchor_kind"] = "real_web_snapshot"
        case["clickback_snapshot_kind"] = "live_powershell_retry"
        case["source_anchor"] = {
            "status": "valid",
            "path": str(snapshot_path.relative_to(ROOT)).replace("\\", "/"),
            "document_hash": sha(snapshot_text),
            "version_id": "real-web-snapshot-v3",
            "selector_type": "text_quote+char_offset",
            "marker": marker,
            "text_quote": quote,
            "start": start,
            "end": end,
            "quote_strategy": quote_strategy,
            "landing_class": landing,
            "semantic_selector_success": semantic_ok,
            "boilerplate_quote": boilerplate_quote,
        }
        (ROOT / case["record_path"]).write_text(json.dumps(case, ensure_ascii=False, indent=2), encoding="utf-8")
        evidence_text = (
            f"# Evidence {case_id}\n"
            f"marker: EVIDENCE_{marker}\n"
            f"quote: {quote}\n"
            f"url: {url}\n"
            f"snapshot_kind: {case['clickback_snapshot_kind']}\n"
            f"quote_strategy: {quote_strategy}\n"
            f"landing_class: {landing}\n"
            f"semantic_selector_success: {str(semantic_ok).lower()}\n"
            f"boilerplate_quote: {str(boilerplate_quote).lower()}\n"
        )
        (ROOT / case["evidence_path"]).write_text(evidence_text, encoding="utf-8")

        meta.update(
            {
                "case_id": case_id,
                "snapshot_path": case["source_anchor"]["path"],
                "quote_start": start,
                "quote_end": end,
                "quote_strategy": quote_strategy,
                "landing_class": landing,
                "semantic_selector_success": semantic_ok,
                "boilerplate_quote": boilerplate_quote,
                "snapshot_kind": case["clickback_snapshot_kind"],
                "fallback_used": False,
            }
        )
        logs.append(meta)
        retried += 1
        time.sleep(0.2)

    write_json(ROOT / "candidate_cases.json", cases)
    updated = {
        "target": len(logs),
        "updated_cases": manifest.get("updated_cases", len(logs)),
        "real_fetch_success": sum(1 for row in logs if row.get("ok") and not row.get("fallback_used")),
        "fallback_used": sum(1 for row in logs if row.get("fallback_used")),
        "retry_method": "urllib_request_then_powershell_fallback",
        "powershell_retried_success": retried,
        "semantic_selector_success": sum(1 for row in logs if row.get("semantic_selector_success")),
        "body_window_used": sum(1 for row in logs if row.get("quote_strategy") == "body_window"),
        "boilerplate_quote": sum(1 for row in logs if row.get("boilerplate_quote")),
        "landing_class_counts": {
            "evidence_landing": sum(1 for row in logs if row.get("landing_class") == "evidence_landing"),
            "claim_landing": sum(1 for row in logs if row.get("landing_class") == "claim_landing"),
            "claim_relevant_context_landing": sum(1 for row in logs if row.get("landing_class") == "claim_relevant_context_landing"),
            "selector_failure": sum(1 for row in logs if row.get("landing_class") == "selector_failure"),
        },
        "logs": logs,
        "note": "real_fetch_success is transport success only. semantic_selector_success is a proxy, split by landing_class; claim_relevant_context_landing is weaker than evidence_landing and needs operator adjudication.",
    }
    write_json(MANIFEST, updated)
    print(json.dumps({k: updated[k] for k in ["target", "real_fetch_success", "fallback_used", "powershell_retried_success"]}, indent=2))


if __name__ == "__main__":
    main()
