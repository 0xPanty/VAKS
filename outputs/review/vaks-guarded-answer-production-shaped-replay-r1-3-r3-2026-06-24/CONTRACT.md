# R1.3 Production-Shaped Replay Simulation

This sandbox replays a production-shaped guarded-answer chain:

request -> trusted route metadata -> frozen context pack -> AnswerDraft ->
ClaimSupportMap -> R1.1 brake -> VAKS Guard -> committed final.

It uses query-aligned frozen replay tuples and runtime fault injection through
the same `process_request` orchestrator. It does not call a live LLM, live
retrieval, a database, a service, or a network API.

R1.3 r3 adds a cross-object alignment contract. Query, ContextPack,
AnswerDraft, and ClaimSupportMap must carry the same frozen alignment id before
the answer can be released. Deliberate cross-case mismatches are included as
negative controls.

## Passing meaning

Passing means the replay chain met the configured hard gates in this bounded
sandbox and is eligible to proceed to live-shadow wiring development behind a
feature flag.

It does not mean production runtime is enabled or validated.
