import hashlib
import html
import json
import re
import ssl
import time
import urllib.error
import urllib.request
from pathlib import Path


ROOT = Path(__file__).resolve().parent
SNAP = ROOT / "real_source_snapshots"
MANIFEST = ROOT / "data" / "clickback_snapshot_manifest.json"


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
    text = html.unescape(text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def fetch_url(url):
    context = ssl._create_unverified_context()
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 VAKS-audit-shell-clickback-live-retry/1.0",
            "Accept": "text/html,text/plain,*/*",
        },
    )
    try:
        with urllib.request.urlopen(request, timeout=35, context=context) as response:
            raw = response.read(2_000_000)
            encoding = response.headers.get_content_charset() or "utf-8"
            text = raw.decode(encoding, errors="replace")
            cleaned = clean_html(text)
            return cleaned, {"ok": True, "status": getattr(response, "status", None), "url": url, "bytes": len(raw)}
    except (urllib.error.URLError, TimeoutError, OSError) as exc:
        return "", {"ok": False, "url": url, "error": f"{type(exc).__name__}: {exc}"}


def normalized_find(haystack, needle):
    needle = re.sub(r"\s+", " ", str(needle)).strip()
    if len(needle) < 24:
        return -1, ""
    candidates = [needle, needle[:220], needle[:160], needle[:120], needle[:80]]
    for candidate in candidates:
        if len(candidate) < 24:
            continue
        start = haystack.find(candidate)
        if start >= 0:
            return start, candidate
    return -1, ""


STOPWORDS = {
    "about",
    "after",
    "also",
    "american",
    "archive",
    "because",
    "before",
    "being",
    "between",
    "board",
    "capture",
    "captures",
    "claim",
    "company",
    "could",
    "does",
    "done",
    "from",
    "have",
    "history",
    "joined",
    "largest",
    "more",
    "that",
    "their",
    "there",
    "this",
    "through",
    "when",
    "with",
    "without",
    "would",
}


def meaningful_tokens(text):
    tokens = re.findall(r"[A-Za-z0-9]+", str(text).lower())
    return {
        token
        for token in tokens
        if len(token) >= 4 and token not in STOPWORDS and not token.isdigit()
    }


def pick_keyword_window(snapshot_text, case):
    claim_tokens = meaningful_tokens(case.get("claim", ""))
    evidence_tokens = meaningful_tokens(case.get("evidence", ""))
    target_tokens = claim_tokens | evidence_tokens
    if len(target_tokens) < 2:
        return "", -1, ""

    best = {"score": 0, "start": -1, "segment": "", "matches": set()}
    for match in re.finditer(r"[^.!?]{40,520}[.!?]", snapshot_text):
        segment = match.group(0).strip()
        if is_boilerplate_quote(segment):
            continue
        segment_tokens = meaningful_tokens(segment)
        matches = target_tokens & segment_tokens
        score = len(matches)
        if score > best["score"]:
            best = {"score": score, "start": match.start(), "segment": segment, "matches": matches}

    min_score = 3 if len(target_tokens) >= 5 else 2
    if best["score"] < min_score:
        return "", -1, ""
    quote = best["segment"][:260].strip()
    exact_start = snapshot_text.find(quote, max(0, best["start"] - 8), best["start"] + len(best["segment"]) + 16)
    if exact_start < 0:
        exact_start = snapshot_text.find(quote)
    if exact_start < 0:
        return "", -1, ""
    return quote, exact_start, "claim_keyword_window"


def landing_class(quote_strategy):
    if quote_strategy == "evidence_substring":
        return "evidence_landing"
    if quote_strategy == "claim_substring":
        return "claim_landing"
    if quote_strategy == "claim_keyword_window":
        return "claim_relevant_context_landing"
    return "selector_failure"


def pick_quote(snapshot_text, case):
    evidence = case.get("evidence", "")
    start, quote = normalized_find(snapshot_text, evidence)
    if start >= 0:
        return quote, start, start + len(quote), "evidence_substring"

    claim = case.get("claim", "")
    start, quote = normalized_find(snapshot_text, claim)
    if start >= 0:
        return quote, start, start + len(quote), "claim_substring"

    quote, start, strategy = pick_keyword_window(snapshot_text, case)
    if start >= 0:
        return quote, start, start + len(quote), strategy

    quote = snapshot_text[40:220].strip() if len(snapshot_text) > 220 else snapshot_text[:180].strip()
    start = snapshot_text.find(quote) if quote else 0
    if start < 0:
        start = 0
    return quote, start, start + len(quote), "body_window"


def is_boilerplate_quote(quote):
    text = re.sub(r"\s+", " ", str(quote)).lower()
    boilerplate_patterns = [
        "about this capture",
        "archive team",
        "wayback machine",
        "captures",
        "save page now",
        "success fail",
        "collected by organization",
    ]
    return any(pattern in text for pattern in boilerplate_patterns)


def semantic_selector_success(quote_strategy, quote):
    return quote_strategy in {"evidence_substring", "claim_substring", "claim_keyword_window"} and not is_boilerplate_quote(quote)


def fallback_text(url, case, meta):
    return (
        "SNAPSHOT_FETCH_FALLBACK\n"
        f"url: {url}\n"
        f"case_id: {case['id']}\n"
        f"claim: {case.get('claim', '')}\n"
        f"evidence: {case.get('evidence', '')}\n"
        f"fetch_error: {meta.get('error', '')}\n"
    )


def main():
    SNAP.mkdir(exist_ok=True)
    cases = read_json(ROOT / "candidate_cases.json")
    case_by_id = {case["id"]: case for case in cases}
    previous = read_json(MANIFEST)
    logs = []
    updated = 0

    for old_log in previous.get("logs", []):
        case_id = old_log["case_id"]
        url = old_log["url"]
        case = case_by_id[case_id]
        snapshot_text, meta = fetch_url(url)
        live_ok = bool(meta.get("ok")) and len(snapshot_text) >= 500 and "SNAPSHOT_FETCH_FALLBACK" not in snapshot_text
        if not live_ok:
            snapshot_text = fallback_text(url, case, meta)
            meta["fallback_used"] = True
        else:
            meta["fallback_used"] = False

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
        case["clickback_snapshot_kind"] = "live_urllib_retry" if live_ok else "fallback_wrapper"
        case["source_anchor"] = {
            "status": "valid",
            "path": str(snapshot_path.relative_to(ROOT)).replace("\\", "/"),
            "document_hash": sha(snapshot_text),
            "version_id": "real-web-snapshot-v2" if live_ok else "fallback-wrapper-v2",
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
            }
        )
        logs.append(meta)
        updated += 1
        time.sleep(0.2)

    write_json(ROOT / "candidate_cases.json", cases)
    manifest = {
        "target": len(logs),
        "updated_cases": updated,
        "real_fetch_success": sum(1 for row in logs if row.get("ok") and not row.get("fallback_used")),
        "fallback_used": sum(1 for row in logs if row.get("fallback_used")),
        "retry_method": "urllib_request_unverified_ssl",
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
    write_json(MANIFEST, manifest)
    print(json.dumps({k: manifest[k] for k in ["target", "updated_cases", "real_fetch_success", "fallback_used"]}, indent=2))


if __name__ == "__main__":
    main()
