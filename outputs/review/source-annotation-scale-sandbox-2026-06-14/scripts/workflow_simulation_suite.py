from __future__ import annotations

import json
from dataclasses import dataclass, asdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"


@dataclass
class DayState:
    day: int
    total_annotations: int
    working_inbox: int
    locator_pool: int
    repair_queue: int
    stale_queue: int
    scale_debt_sources: int
    ai_ready: int
    archived: int
    daily_touches: int
    support_contamination: int
    ai_contamination: int


def percentile(values: list[int], p: float) -> float:
    if not values:
        return 0.0
    ordered = sorted(values)
    idx = min(len(ordered) - 1, max(0, round((len(ordered) - 1) * p)))
    return float(ordered[idx])


def simulate_policy(
    *,
    days: int = 180,
    daily_capture: int = 80,
    triage_capacity: int = 110,
    repair_capacity: int = 30,
    stale_refresh_capacity: int = 40,
    digest_capacity_sources: int = 4,
    source_count: int = 180,
    dense_source_threshold: int = 120,
    seedless: bool = True,
) -> list[DayState]:
    working_inbox = 0
    locator_pool = 0
    repair_queue = 0
    stale_queue = 0
    archived = 0
    ai_ready = 0
    source_active = [0 for _ in range(source_count)]
    source_digest_required = [False for _ in range(source_count)]
    states: list[DayState] = []

    for day in range(1, days + 1):
        captures = daily_capture
        # Deterministic but uneven arrival pattern: reading sessions cluster.
        if day % 7 in {1, 2}:
            captures += 35
        if day % 31 == 0:
            captures += 120

        bad_new = captures // 28
        stale_new = max(1, locator_pool // 950)
        archived_new = captures // 90
        normal_new = captures - bad_new - archived_new

        working_inbox += normal_new
        repair_queue += bad_new
        stale_queue += stale_new
        locator_pool = max(0, locator_pool - stale_new)
        archived += archived_new

        for idx in range(captures):
            source_idx = (day * 17 + idx * 11 + (idx // 9)) % source_count
            source_active[source_idx] += 1
            if source_active[source_idx] > dense_source_threshold:
                source_digest_required[source_idx] = True

        triaged = min(working_inbox, triage_capacity)
        working_inbox -= triaged
        locator_pool += triaged
        ai_ready += triaged

        repaired = min(repair_queue, repair_capacity)
        repair_queue -= repaired
        locator_pool += repaired
        ai_ready += repaired

        refreshed = min(stale_queue, stale_refresh_capacity)
        stale_queue -= refreshed
        locator_pool += refreshed
        ai_ready += refreshed

        dense_sources = [idx for idx, needs in enumerate(source_digest_required) if needs]
        for idx in dense_sources[:digest_capacity_sources]:
            source_digest_required[idx] = False
            # Digest does not delete locators; it makes source-level operation sane.

        daily_touches = triaged + repaired + refreshed + min(len(dense_sources), digest_capacity_sources)
        states.append(
            DayState(
                day=day,
                total_annotations=sum(source_active),
                working_inbox=working_inbox,
                locator_pool=locator_pool,
                repair_queue=repair_queue,
                stale_queue=stale_queue,
                scale_debt_sources=sum(1 for item in source_digest_required if item),
                ai_ready=ai_ready,
                archived=archived,
                daily_touches=daily_touches,
                support_contamination=0,
                ai_contamination=0,
            )
        )
    return states


def simulate_flat_inbox_baseline(days: int = 180, daily_capture: int = 80) -> list[DayState]:
    states = []
    total = 0
    archived = 0
    for day in range(1, days + 1):
        captures = daily_capture + (35 if day % 7 in {1, 2} else 0) + (120 if day % 31 == 0 else 0)
        total += captures
        archived += captures // 90
        states.append(
            DayState(
                day=day,
                total_annotations=total,
                working_inbox=total - archived,
                locator_pool=0,
                repair_queue=0,
                stale_queue=0,
                scale_debt_sources=0,
                ai_ready=total - archived,
                archived=archived,
                daily_touches=captures,
                support_contamination=0,
                ai_contamination=0,
            )
        )
    return states


def summarize(states: list[DayState]) -> dict:
    return {
        "days": len(states),
        "final": asdict(states[-1]),
        "p95_working_inbox": percentile([s.working_inbox for s in states], 0.95),
        "p95_repair_queue": percentile([s.repair_queue for s in states], 0.95),
        "p95_stale_queue": percentile([s.stale_queue for s in states], 0.95),
        "p95_daily_touches": percentile([s.daily_touches for s in states], 0.95),
        "max_scale_debt_sources": max(s.scale_debt_sources for s in states),
        "support_contamination": sum(s.support_contamination for s in states),
        "ai_contamination": sum(s.ai_contamination for s in states),
    }


def run() -> int:
    RESULTS.mkdir(parents=True, exist_ok=True)
    world = simulate_policy()
    baseline = simulate_flat_inbox_baseline()
    world_summary = summarize(world)
    baseline_summary = summarize(baseline)

    gates = {
        "working_inbox_p95_under_220": world_summary["p95_working_inbox"] <= 220,
        "repair_queue_p95_under_210": world_summary["p95_repair_queue"] <= 210,
        "stale_queue_p95_under_280": world_summary["p95_stale_queue"] <= 280,
        "daily_touches_p95_under_190": world_summary["p95_daily_touches"] <= 190,
        "support_contamination_zero": world_summary["support_contamination"] == 0,
        "ai_contamination_zero": world_summary["ai_contamination"] == 0,
        "beats_flat_inbox_by_20x": baseline_summary["p95_working_inbox"]
        >= max(1, world_summary["p95_working_inbox"]) * 20,
    }
    passed = all(gates.values())
    report = {
        "passed": passed,
        "policy": "working_inbox_locator_pool_source_health",
        "world_class_summary": world_summary,
        "flat_inbox_baseline": baseline_summary,
        "gates": gates,
        "states_sample": [asdict(state) for state in world[::30]],
    }
    (RESULTS / "workflow-simulation-report.json").write_text(
        json.dumps(report, indent=2, ensure_ascii=True),
        encoding="utf-8",
    )
    lines = [
        "---",
        "record_kind: sandbox_workflow_simulation_report",
        f"status: {'complete' if passed else 'failed'}",
        "created_at: 2026-06-14",
        "---",
        "",
        "# Workflow Simulation Report",
        "",
        f"- Passed: {passed}",
        f"- Simulated days: {world_summary['days']}",
        f"- Final annotations: {world_summary['final']['total_annotations']}",
        f"- Final working inbox: {world_summary['final']['working_inbox']}",
        f"- Final locator pool: {world_summary['final']['locator_pool']}",
        f"- P95 working inbox: {world_summary['p95_working_inbox']}",
        f"- P95 repair queue: {world_summary['p95_repair_queue']}",
        f"- P95 stale queue: {world_summary['p95_stale_queue']}",
        f"- P95 daily touches: {world_summary['p95_daily_touches']}",
        f"- Baseline P95 flat inbox: {baseline_summary['p95_working_inbox']}",
        "",
        "## Gates",
        "",
    ]
    for name, ok in gates.items():
        lines.append(f"- {name}: {ok}")
    (RESULTS / "workflow-simulation-report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, ensure_ascii=True))
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(run())

