# Feedback Event Logs

This folder is for append-only feedback event records.

v0.1 storage rule:

```text
Markdown remains the readable knowledge layer.
JSONL records query-run and feedback-event truth.
SQLite, if added later, is only a rebuildable cache.
```

Recommended paths:

```text
outputs/feedback/query-runs/YYYY-MM-DD.jsonl
outputs/feedback/events/YYYY-MM-DD.jsonl
```

Do not store full private conversations when a query summary, turn id, target id, and short reason are enough.
