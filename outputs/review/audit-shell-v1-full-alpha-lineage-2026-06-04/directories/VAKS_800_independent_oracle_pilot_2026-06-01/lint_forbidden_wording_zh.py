import argparse
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parent


def read_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def lint_text(text, rules, file_label):
    findings = []
    for phrase in rules["exact_banned_phrases"]:
        if phrase in text:
            findings.append(
                {
                    "severity": "fail",
                    "type": "forbidden_phrase",
                    "file": file_label,
                    "phrase": phrase,
                }
            )

    for rule in rules.get("regex_banned_patterns", []):
        for match in re.finditer(rule["pattern"], text, flags=re.IGNORECASE):
            findings.append(
                {
                    "severity": "fail",
                    "type": "forbidden_pattern",
                    "file": file_label,
                    "id": rule["id"],
                    "pattern": rule["pattern"],
                    "match": match.group(0),
                }
            )
    return findings


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--rules", default="forbidden_wording_zh.json")
    parser.add_argument("--out", default="forbidden_wording_lint_zh.json")
    parser.add_argument("files", nargs="+")
    args = parser.parse_args()

    rules = read_json(ROOT / args.rules)
    all_findings = []
    checked = []

    for item in args.files:
        path = ROOT / item
        text = path.read_text(encoding="utf-8", errors="ignore")
        checked.append(item)
        all_findings.extend(lint_text(text, rules, item))

    payload = {
        "status": "pass" if not all_findings else "fail",
        "rules": args.rules,
        "checked_files": checked,
        "findings": all_findings,
        "safe_replacements": rules.get("safe_replacements", []),
        "note": "Chinese forbidden-wording lint for normal operator-facing renderer text. Adversarial trap packets should be checked separately as intentional traps.",
    }
    (ROOT / args.out).write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"out": args.out, "status": payload["status"], "findings": len(all_findings)}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
