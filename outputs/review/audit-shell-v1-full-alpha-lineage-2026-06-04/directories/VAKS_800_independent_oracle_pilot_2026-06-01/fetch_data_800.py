import json
import time
from pathlib import Path

import requests
import urllib3


ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
PREV = Path(r"C:\Users\Administrator\Documents\VAKS_480_realdata_paired_pilot_2026-06-01\data\fetched_rows.json")
SERVER = "https://datasets-server.huggingface.co"


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def read_json(path, default):
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return default


def write_json(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding="utf-8")


def get_json(url, params=None, attempts=5):
    last = None
    for attempt in range(1, attempts + 1):
        try:
            response = requests.get(url, params=params, timeout=45, verify=False)
            if response.ok:
                return response.json(), {"ok": True, "status": response.status_code, "attempt": attempt}
            last = f"{response.status_code}: {response.text[:240]}"
            if response.status_code == 429:
                time.sleep(8 * attempt)
        except Exception as exc:
            last = f"{type(exc).__name__}: {exc}"
        time.sleep(1.2 * attempt)
    return None, {"ok": False, "error": last}


def get_text(url, attempts=5):
    last = None
    for attempt in range(1, attempts + 1):
        try:
            response = requests.get(url, timeout=45, verify=False)
            if response.ok:
                return response.text, {"ok": True, "status": response.status_code, "attempt": attempt}
            last = f"{response.status_code}: {response.text[:240]}"
            if response.status_code == 429:
                time.sleep(8 * attempt)
        except Exception as exc:
            last = f"{type(exc).__name__}: {exc}"
        time.sleep(1.2 * attempt)
    return "", {"ok": False, "error": last}


def fetch_rows(dataset, config, split, target, chunk=100):
    rows = []
    logs = []
    offset = 0
    total = None
    while len(rows) < target:
        length = min(chunk, target - len(rows))
        payload, meta = get_json(
            f"{SERVER}/rows",
            {"dataset": dataset, "config": config, "split": split, "offset": offset, "length": length},
        )
        meta.update({"dataset": dataset, "config": config, "split": split, "offset": offset, "length": length})
        logs.append(meta)
        if not payload or not meta["ok"]:
            break
        total = payload.get("num_rows_total", total)
        page = [item["row"] for item in payload.get("rows", [])]
        rows.extend(page)
        if len(page) < length:
            break
        offset += length
        if total is not None and offset >= total:
            break
    return rows, logs


def normalize_averitec(row):
    answers = []
    for question in row.get("questions") or []:
        for answer in question.get("answers") or []:
            value = answer.get("answer") or answer.get("boolean_explanation") or ""
            if value:
                answers.append(value)
    return {
        "claim": row.get("claim", ""),
        "evidence": " ".join(answers[:3]) or row.get("justification", ""),
        "label": row.get("label", ""),
        "source_url": row.get("fact_checking_article") or row.get("original_claim_url") or "",
        "speaker": row.get("speaker", ""),
    }


def normalize_ambifc(row):
    return {
        "claim": row.get("claim", ""),
        "evidence": row.get("passage", ""),
        "label": row.get("label", ""),
        "category": row.get("category", ""),
    }


def normalize_fever(row):
    chunks = []
    for group in row.get("evidence") or []:
        for item in group:
            chunks.append(str(item))
    return {
        "claim": row.get("claim", ""),
        "evidence": " | ".join(chunks),
        "label": row.get("label", ""),
        "verifiable": row.get("verifiable", ""),
        "original_id": row.get("original_id", ""),
    }


def fetch_simple_family(name, dataset, config, split, normalizer, target=220):
    rows, logs = fetch_rows(dataset, config, split, target)
    return {
        "rows": [normalizer(row) for row in rows],
        "source_status": "real_dataset_server" if len(rows) >= 160 else "partial_real_dataset_server",
        "logs": logs,
    }


def fetch_scifact(target=220):
    queries, qlog = fetch_rows("BeIR/scifact", "queries", "queries", 1200)
    corpus, clog = fetch_rows("BeIR/scifact", "corpus", "corpus", 8000)
    qrels, rlog = get_text("https://huggingface.co/datasets/BeIR/scifact-qrels/resolve/main/test.tsv")
    query_by_id = {str(row.get("_id")): row for row in queries}
    corpus_by_id = {str(row.get("_id")): row for row in corpus}
    pairs = []
    for line in qrels.splitlines()[1:]:
        parts = line.strip().split()
        if len(parts) < 3:
            continue
        qid, cid, score = parts[:3]
        query = query_by_id.get(qid)
        evidence = corpus_by_id.get(cid)
        if not query or not evidence:
            continue
        pairs.append(
            {
                "claim": query.get("text", ""),
                "evidence": evidence.get("text", ""),
                "label": f"qrel:{score}",
                "query_id": qid,
                "corpus_id": cid,
                "evidence_title": evidence.get("title", ""),
            }
        )
        if len(pairs) >= target:
            break
    return {
        "rows": pairs,
        "source_status": "real_with_qrels" if len(pairs) >= 160 else "partial_real_with_qrels",
        "logs": qlog + clog + [{"source": "BeIR/scifact-qrels/test.tsv", **rlog}],
    }


def merge_cache(fetched):
    previous = read_json(PREV, {})
    for key, payload in previous.items():
        current = fetched.get(key, {})
        if len(current.get("rows", [])) >= 160:
            continue
        if len(payload.get("rows", [])) > len(current.get("rows", [])):
            fetched[key] = {**payload, "source_status": payload.get("source_status", "previous_cache")}
    return fetched


def main():
    DATA.mkdir(exist_ok=True)
    cache = read_json(DATA / "fetched_rows.json", {})
    fetched = dict(cache)
    fetchers = {
        "averitec": lambda: fetch_simple_family("averitec", "pminervini/averitec", "default", "train", normalize_averitec),
        "ambifc": lambda: fetch_simple_family("ambifc", "just1nseo/ambifc", "default", "train", normalize_ambifc),
        "fever": lambda: fetch_simple_family("fever", "copenlu/fever_gold_evidence", "default", "train", normalize_fever),
        "scifact": fetch_scifact,
    }
    for key, fetcher in fetchers.items():
        if len(fetched.get(key, {}).get("rows", [])) >= 160 and "partial" not in fetched[key].get("source_status", ""):
            continue
        fetched[key] = fetcher()
        write_json(DATA / "fetched_rows.json", merge_cache(fetched))
        fetched = read_json(DATA / "fetched_rows.json", fetched)

    fetched = merge_cache(fetched)
    write_json(DATA / "fetched_rows.json", fetched)
    log = {
        key: {
            "rows": len(value.get("rows", [])),
            "source_status": value.get("source_status", "unknown"),
            "logs": value.get("logs", []),
        }
        for key, value in fetched.items()
    }
    write_json(DATA / "dataset_fetch_log.json", log)
    print(json.dumps({key: {"rows": row["rows"], "status": row["source_status"]} for key, row in log.items()}, indent=2))


if __name__ == "__main__":
    main()
