from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path


SLICE_ID = "2026-06-19-p2-91-old-file-status-normalization-executor-apply-sandbox"
THIS_FILE = Path(__file__).resolve()
SLICE_ROOT = THIS_FILE.parents[1]
REPO_ROOT = THIS_FILE.parents[5]
REPORT = SLICE_ROOT / "artifact" / "old_file_status_normalization_executor_apply.json"
P2_87 = REPO_ROOT / "outputs/review/vaks-implementation-sandbox/2026-06-19-p2-87-old-file-status-normalization-diff-preview-sandbox/artifact/old_file_status_normalization_diff_preview.json"


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def split_newline(line: str) -> tuple[str, str]:
    if line.endswith("\r\n"):
        return line[:-2], "\r\n"
    if line.endswith("\n"):
        return line[:-1], "\n"
    return line, ""


def parse_frontmatter(text: str) -> dict:
    lines = text.splitlines(keepends=True)
    if not lines or lines[0].strip() != "---":
        raise ValueError("missing opening frontmatter fence")
    end_index = None
    for idx in range(1, len(lines)):
        if lines[idx].strip() == "---":
            end_index = idx
            break
    if end_index is None:
        raise ValueError("missing closing frontmatter fence")
    status_index = None
    status_value = None
    for idx in range(1, end_index):
        content, _newline = split_newline(lines[idx])
        if content.startswith("status:"):
            status_index = idx
            status_value = content.split(":", 1)[1].strip()
            break
    if status_index is None:
        raise ValueError("missing status line")
    return {
        "status_value": status_value,
        "body_text": "".join(lines[end_index + 1 :]),
        "non_status_frontmatter_text": "".join(
            line for idx, line in enumerate(lines[1:end_index], start=1) if idx != status_index
        ),
    }


def main() -> None:
    report = json.loads(REPORT.read_text(encoding="utf-8"))
    p87 = json.loads(P2_87.read_text(encoding="utf-8"))
    expected_by_index = {item["operation_index"]: item for item in p87["preview_operations"]}
    repaired_count = 0
    blocked = []

    for op in report["execution_operations"]:
        target = REPO_ROOT / op["target_path"]
        raw_current = target.read_bytes()
        expected = expected_by_index[op["operation_index"]]["proposed_sha256"]
        if sha256_bytes(raw_current) == expected:
            repaired_raw = raw_current
        else:
            candidate = raw_current.replace(b"\r\n", b"\n")
            if sha256_bytes(candidate) != expected:
                blocked.append(
                    {
                        "operation_index": op["operation_index"],
                        "target_path": op["target_path"],
                        "current_sha256": sha256_bytes(raw_current),
                        "expected_proposed_sha256": expected,
                    }
                )
                continue
            target.write_bytes(candidate)
            repaired_raw = candidate
            repaired_count += 1

        parsed = parse_frontmatter(repaired_raw.decode("utf-8"))
        op["post_apply_sha256_actual"] = sha256_bytes(repaired_raw)
        op["post_apply_status_actual"] = parsed["status_value"]
        op["post_apply_status_match"] = parsed["status_value"] == op["proposed_status"]
        op["body_sha256_after_actual"] = sha256_bytes(parsed["body_text"].encode("utf-8"))
        op["non_status_frontmatter_sha256_after_actual"] = sha256_bytes(
            parsed["non_status_frontmatter_text"].encode("utf-8")
        )
        op["body_unchanged_actual"] = op["body_sha256_after_actual"] == op["body_sha256_before"]
        op["non_status_frontmatter_unchanged_actual"] = (
            op["non_status_frontmatter_sha256_after_actual"] == op["non_status_frontmatter_sha256_before"]
        )

    if blocked:
        report["line_ending_repair"] = {
            "status": "blocked",
            "blocked": blocked,
            "attempted_at": datetime.now(timezone.utc).isoformat(),
        }
        REPORT.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        raise SystemExit(f"repair blocked: {blocked[:3]}")

    ops = report["execution_operations"]
    report["summary"]["post_apply_status_match_count"] = sum(1 for item in ops if item["post_apply_status_match"])
    report["summary"]["body_unchanged_count"] = sum(1 for item in ops if item["body_unchanged_actual"])
    report["summary"]["non_status_frontmatter_unchanged_count"] = sum(
        1 for item in ops if item["non_status_frontmatter_unchanged_actual"]
    )
    report["summary"]["protected_path_writes"] = 0
    report["line_ending_repair"] = {
        "status": "repaired",
        "reason": "Initial executor used text-mode write on Windows; repair restored exact p2-87 proposed bytes.",
        "repaired_count": repaired_count,
        "expected_proposed_hash_match_count": sum(
            1
            for item in ops
            if item["post_apply_sha256_actual"] == expected_by_index[item["operation_index"]]["proposed_sha256"]
        ),
        "repaired_at": datetime.now(timezone.utc).isoformat(),
    }
    REPORT.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    fixtures_dir = SLICE_ROOT / "fixtures"
    (fixtures_dir / "body-content-unchanged-after-apply.json").write_text(
        json.dumps(
            {
                "case_id": "body-content-unchanged-after-apply",
                "body_unchanged_count": report["summary"]["body_unchanged_count"],
            },
            indent=2,
            ensure_ascii=False,
        )
        + "\n",
        encoding="utf-8",
    )
    (fixtures_dir / "non-status-frontmatter-unchanged-after-apply.json").write_text(
        json.dumps(
            {
                "case_id": "non-status-frontmatter-unchanged-after-apply",
                "non_status_frontmatter_unchanged_count": report["summary"][
                    "non_status_frontmatter_unchanged_count"
                ],
            },
            indent=2,
            ensure_ascii=False,
        )
        + "\n",
        encoding="utf-8",
    )
    print(json.dumps(report["line_ending_repair"], indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
