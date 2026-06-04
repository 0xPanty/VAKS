import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parent


SAMPLES = [
    "Green dashboard checks make this answer dependable.",
    "The eval passed, making this claim safer to believe.",
    "Users kept approving it, so the fact is probably true.",
    "The presence of several URLs means independent confirmation.",
    "The search result came first, so it carries more authority.",
    "The grouped summary makes the relation accepted.",
    "The LLM recap gives support for the point.",
    "The lineage chain independently confirms the point.",
    "A large group count gives stronger support.",
    "Reviewer approval means the claim is true.",
    "The dashboard looks green, therefore this is verified truth.",
    "Because all tests passed, the claim should be trusted.",
    "The top retrieval result is the most authoritative answer.",
    "Many citations make the source independent.",
    "Feedback raised confidence in the truth of the statement.",
    "The cluster summary proves this relation.",
]


def main():
    rules = json.loads((ROOT / "authority_rules_800.json").read_text(encoding="utf-8"))
    hits = []
    misses = []
    for sample in SAMPLES:
        lower = sample.lower()
        matched = [pattern for pattern in rules["leakage_patterns"] if re.search(pattern, lower)]
        (hits if matched else misses).append({"sample": sample, "matched": matched})
    payload = {"sample_count": len(SAMPLES), "hit_count": len(hits), "miss_count": len(misses), "hit_rate": round(len(hits) / len(SAMPLES), 3), "hits": hits, "misses": misses}
    (ROOT / "authority_fuzz_results.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"hit_rate": payload["hit_rate"], "miss_count": payload["miss_count"]}, indent=2))


if __name__ == "__main__":
    main()
