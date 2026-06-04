import json
import time
from pathlib import Path

import requests
import urllib3


ROOT = Path(__file__).resolve().parent
DATA_DIR = ROOT / "data"
DATASETS_SERVER = "https://datasets-server.huggingface.co"


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def get_json(url, params=None, attempts=4):
    last_error = None
    for attempt in range(1, attempts + 1):
        try:
            response = requests.get(url, params=params, timeout=40, verify=False)
            if response.ok:
                return response.json(), {"ok": True, "status": response.status_code, "attempt": attempt}
            last_error = f"{response.status_code}: {response.text[:400]}"
            if response.status_code == 429:
                time.sleep(10 * attempt)
        except Exception as exc:  # Network turbulence is recorded, not hidden.
            last_error = f"{type(exc).__name__}: {exc}"
        time.sleep(1.5 * attempt)
    return None, {"ok": False, "error": last_error}


def get_text(url, attempts=4):
    last_error = None
    for attempt in range(1, attempts + 1):
        try:
            response = requests.get(url, timeout=40, verify=False)
            if response.ok:
                return response.text, {"ok": True, "status": response.status_code, "attempt": attempt}
            last_error = f"{response.status_code}: {response.text[:400]}"
        except Exception as exc:
            last_error = f"{type(exc).__name__}: {exc}"
        time.sleep(1.5 * attempt)
    return "", {"ok": False, "error": last_error}


def fetch_rows(dataset, config, split, count, offset=0, chunk=100):
    rows = []
    log = []
    current = offset
    while len(rows) < count:
        length = min(chunk, count - len(rows))
        payload, meta = get_json(
            f"{DATASETS_SERVER}/rows",
            {
                "dataset": dataset,
                "config": config,
                "split": split,
                "offset": current,
                "length": length,
            },
        )
        meta.update({"dataset": dataset, "config": config, "split": split, "offset": current, "length": length})
        log.append(meta)
        if not payload or not meta["ok"]:
            break
        page = [item["row"] for item in payload.get("rows", [])]
        rows.extend(page)
        if len(page) < length:
            break
        current += length
    return rows, log


def fetch_scifact():
    queries, query_log = fetch_rows("BeIR/scifact", "queries", "queries", 1200)
    corpus, corpus_log = fetch_rows("BeIR/scifact", "corpus", "corpus", 6000)
    qrels_text, qrels_log = get_text("https://huggingface.co/datasets/BeIR/scifact-qrels/resolve/main/test.tsv")

    query_by_id = {str(row.get("_id")): row for row in queries}
    corpus_by_id = {str(row.get("_id")): row for row in corpus}
    pairs = []
    for line in qrels_text.splitlines()[1:]:
        parts = line.strip().split()
        if len(parts) < 3:
            continue
        qid, cid, score = parts[:3]
        query = query_by_id.get(qid)
        evidence = corpus_by_id.get(cid)
        if query and evidence:
            pairs.append(
                {
                    "query_id": qid,
                    "corpus_id": cid,
                    "score": score,
                    "claim": query.get("text", ""),
                    "evidence_title": evidence.get("title", ""),
                    "evidence": evidence.get("text", ""),
                }
            )
        if len(pairs) >= 160:
            break

    return {
        "rows": pairs,
        "logs": query_log + corpus_log + [{"source": "BeIR/scifact-qrels/test.tsv", **qrels_log}],
        "source_status": "real_with_qrels" if len(pairs) >= 120 else "partial_real_with_qrels",
    }


def fetch_averitec():
    rows, logs = fetch_rows("pminervini/averitec", "default", "train", 140)
    normalized = []
    for row in rows:
        answers = []
        for question in row.get("questions") or []:
            for answer in question.get("answers") or []:
                value = answer.get("answer") or answer.get("boolean_explanation") or ""
                if value:
                    answers.append(value)
        normalized.append(
            {
                "claim": row.get("claim", ""),
                "label": row.get("label", ""),
                "justification": row.get("justification", ""),
                "speaker": row.get("speaker", ""),
                "source_url": row.get("fact_checking_article") or row.get("original_claim_url") or "",
                "evidence": " ".join(answers[:3]) or row.get("justification", ""),
            }
        )
    return {"rows": normalized, "logs": logs, "source_status": "real_dataset_server" if len(normalized) >= 120 else "partial_real_dataset_server"}


def fetch_ambifc():
    rows, logs = fetch_rows("just1nseo/ambifc", "default", "train", 140)
    normalized = []
    for row in rows:
        normalized.append(
            {
                "claim": row.get("claim", ""),
                "label": row.get("label", ""),
                "category": row.get("category", ""),
                "passage": row.get("passage", ""),
                "evidence": row.get("passage", ""),
            }
        )
    return {"rows": normalized, "logs": logs, "source_status": "real_dataset_server" if len(normalized) >= 120 else "partial_real_dataset_server"}


def fetch_fever():
    rows, logs = fetch_rows("copenlu/fever_gold_evidence", "default", "train", 140)
    normalized = []
    for row in rows:
        evidence_chunks = []
        for evidence_group in row.get("evidence") or []:
            for item in evidence_group:
                evidence_chunks.append(str(item))
        normalized.append(
            {
                "claim": row.get("claim", ""),
                "label": row.get("label", ""),
                "verifiable": row.get("verifiable", ""),
                "original_id": row.get("original_id", ""),
                "evidence": " | ".join(evidence_chunks),
            }
        )
    return {"rows": normalized, "logs": logs, "source_status": "real_dataset_server" if len(normalized) >= 120 else "partial_real_dataset_server"}


def main():
    DATA_DIR.mkdir(exist_ok=True)
    cache_path = DATA_DIR / "fetched_rows.json"
    fetched = load_cache(cache_path)
    fetchers = {
        "averitec": fetch_averitec,
        "ambifc": fetch_ambifc,
        "fever": fetch_fever,
        "scifact": fetch_scifact,
    }
    for family, fetcher in fetchers.items():
        current = fetched.get(family, {})
        if len(current.get("rows", [])) >= 120 and "partial" not in current.get("source_status", ""):
            continue
        fetched[family] = fetcher()
        (DATA_DIR / "fetched_rows.json").write_text(json.dumps(fetched, ensure_ascii=False, indent=2), encoding="utf-8")
    (DATA_DIR / "fetched_rows.json").write_text(json.dumps(fetched, ensure_ascii=False, indent=2), encoding="utf-8")

    fetch_log = {}
    for family, payload in fetched.items():
        fetch_log[family] = {
            "row_count": len(payload["rows"]),
            "source_status": payload["source_status"],
            "logs": payload["logs"],
        }
    (DATA_DIR / "dataset_fetch_log.json").write_text(json.dumps(fetch_log, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({key: {"rows": len(value["rows"]), "status": value["source_status"]} for key, value in fetched.items()}, indent=2))


def load_cache(path):
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}


if __name__ == "__main__":
    main()
