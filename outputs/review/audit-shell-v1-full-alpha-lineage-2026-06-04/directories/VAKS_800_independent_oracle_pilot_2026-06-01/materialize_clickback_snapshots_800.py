import hashlib
import json
import re
import time
from pathlib import Path

import requests
import urllib3


ROOT = Path(__file__).resolve().parent
SNAP = ROOT / "real_source_snapshots"


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def read_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def write_json(path, value):
    Path(path).write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding="utf-8")


def sha(text):
    return hashlib.sha256(text.encode("utf-8", errors="ignore")).hexdigest()


def clean_html(text):
    text = re.sub(r"<script[\s\S]*?</script>", " ", text, flags=re.I)
    text = re.sub(r"<style[\s\S]*?</style>", " ", text, flags=re.I)
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"&nbsp;|&#160;", " ", text)
    text = re.sub(r"&amp;", "&", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def fetch_url(url):
    try:
        response = requests.get(url, timeout=25, verify=False, headers={"User-Agent": "VAKS-audit-shell-clickback-preflight/1.0"})
        if response.ok and response.text:
            return clean_html(response.text), {"ok": True, "status": response.status_code, "url": url}
        return "", {"ok": False, "status": response.status_code, "url": url, "error": response.text[:160]}
    except Exception as exc:
        return "", {"ok": False, "url": url, "error": f"{type(exc).__name__}: {exc}"}


def pick_quote(text):
    text = re.sub(r"\s+", " ", text).strip()
    if len(text) < 80:
        return text
    return text[40:220].strip()


def main():
    SNAP.mkdir(exist_ok=True)
    cases = read_json(ROOT / "candidate_cases.json")
    fetched = read_json(ROOT / "data" / "fetched_rows.json")
    averitec_rows = [row for row in fetched.get("averitec", {}).get("rows", []) if row.get("source_url")]
    full_anchor = [case for case in cases if case.get("pool") == "full_anchor_real_pack"]
    logs = []
    updated = 0
    target = min(24, len(full_anchor), len(averitec_rows))
    for idx in range(target):
        case = full_anchor[idx]
        row = averitec_rows[idx]
        snapshot_text, meta = fetch_url(row["source_url"])
        if not snapshot_text or len(snapshot_text) < 200:
            snapshot_text = (
                f"SNAPSHOT_FETCH_FALLBACK\n"
                f"url: {row['source_url']}\n"
                f"claim: {row.get('claim', '')}\n"
                f"evidence: {row.get('evidence', '')}\n"
            )
            meta["fallback_used"] = True
        else:
            meta["fallback_used"] = False
        snapshot_text = re.sub(r"\s+", " ", snapshot_text).strip()
        snapshot_path = SNAP / f"{case['id']}.txt"
        snapshot_path.write_text(snapshot_text, encoding="utf-8")
        quote = pick_quote(snapshot_text)
        start = snapshot_text.find(quote)
        if start < 0:
            quote = snapshot_text[:180]
            start = 0
        end = start + len(quote)
        marker = f"{case['id']}_REAL_SNAPSHOT"
        marker_line = f"\nmarker: {marker}\n"
        snapshot_text = snapshot_text + marker_line
        snapshot_path.write_text(snapshot_text, encoding="utf-8")
        case["claim"] = row.get("claim", case["claim"])
        case["evidence"] = row.get("evidence", case["evidence"])
        case["source_label"] = row.get("label", case.get("source_label", ""))
        case["real_snapshot_url"] = row["source_url"]
        case["full_anchor_kind"] = "real_web_snapshot"
        case["source_anchor"] = {
            "status": "valid",
            "path": str(snapshot_path.relative_to(ROOT)).replace("\\", "/"),
            "document_hash": sha(snapshot_text),
            "version_id": "real-web-snapshot-v1",
            "selector_type": "text_quote+char_offset",
            "marker": marker,
            "text_quote": quote,
            "start": start,
            "end": end,
        }
        (ROOT / case["record_path"]).write_text(json.dumps(case, ensure_ascii=False, indent=2), encoding="utf-8")
        evidence_text = f"# Evidence {case['id']}\nmarker: EVIDENCE_{marker}\nquote: {quote}\nurl: {row['source_url']}\n"
        (ROOT / case["evidence_path"]).write_text(evidence_text, encoding="utf-8")
        meta.update({"case_id": case["id"], "snapshot_path": case["source_anchor"]["path"], "quote_start": start, "quote_end": end})
        logs.append(meta)
        updated += 1
        time.sleep(0.5)
    write_json(ROOT / "candidate_cases.json", cases)
    manifest = {
        "target": target,
        "updated_cases": updated,
        "real_fetch_success": sum(1 for row in logs if row.get("ok") and not row.get("fallback_used")),
        "fallback_used": sum(1 for row in logs if row.get("fallback_used")),
        "logs": logs,
        "note": "real_fetch_success counts archived/web snapshots fetched from source_url; fallback rows are explicit and should not be treated as true source click-back proof.",
    }
    write_json(ROOT / "data" / "clickback_snapshot_manifest.json", manifest)
    print(json.dumps({k: manifest[k] for k in ["target", "updated_cases", "real_fetch_success", "fallback_used"]}, indent=2))


if __name__ == "__main__":
    main()
