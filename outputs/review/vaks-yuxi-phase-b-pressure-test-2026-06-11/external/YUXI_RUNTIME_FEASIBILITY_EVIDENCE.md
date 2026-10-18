---
record_kind: external_runtime_feasibility_evidence
status: current_snapshot
project_id: VAKS
created_at: 2026-06-11
truth_boundary: source_evidence_not_mainline_decision
action_basis_allowed: false
source_repo: https://github.com/xerrors/Yuxi
source_head: a8536a2e8520d1992a31bb6c22f219e60deca131
---

# Yuxi Runtime Feasibility Evidence

## Local Environment

```text
docker --version: command not found
docker compose version: command not found
python --version: Python 3.10.6
uv --version: uv 0.11.18
uv installed Python: cpython-3.12.13 available under uv
node --version: v24.11.0
pnpm --version: 10.29.1
```

## Current Yuxi Snapshot

```text
source repo: https://github.com/xerrors/Yuxi
HEAD: a8536a2e8520d1992a31bb6c22f219e60deca131
```

## Docker Requirement

Yuxi README says:

```text
prerequisite: Docker and Docker Compose
startup: docker compose up --build
lite mode: make up-lite
```

Yuxi `AGENTS.md` says the project is managed entirely through Docker Compose
and development/debugging should happen in the running container environment.

Yuxi `Makefile` confirms:

```text
up: docker compose up -d
up-lite: LITE_MODE=true ... docker compose up -d postgres redis minio api web
seed: docker compose exec api ...
```

Yuxi testing guidelines confirm:

```text
unit tests: docker compose exec api uv run --group test pytest test/unit -m "not slow"
integration tests: docker compose exec api uv run --group test pytest test/integration
e2e tests: docker compose exec api uv run --group test pytest test/e2e -m e2e
```

## Runtime Services

Yuxi `docker-compose.yml` wires runtime services through container hostnames:

```text
RUNNING_IN_DOCKER=true
POSTGRES_URL=...@postgres:5432/...
REDIS_URL=redis://redis:6379/0
MINIO_URI=http://minio:9000
NEO4J_URI=bolt://graph:7687
MILVUS_URI=http://milvus:19530
```

Lite mode skips heavier knowledge / graph services but still starts:

```text
postgres
redis
minio
api
web
```

through Docker Compose.

## Host-Only Smoke Judgment

Host-only smoke is not a valid replacement for original Yuxi full-stack in the
current environment:

```text
default Python is 3.10, while Yuxi backend requires >=3.12,<3.14
uv has Python 3.12, but runtime services are still Docker/Compose based
Lite mode still requires Docker Compose
official tests are documented as docker compose exec api ...
```

Therefore, running a partial host-only import/build would not prove Yuxi
runtime retrieval behavior, Milvus/Neo4j behavior, click-through UX, permissions,
or sandbox behavior.
