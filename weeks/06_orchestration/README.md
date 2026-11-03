# Week 6: Orchestration

## Goal
Explain jobs, tasks, dependencies, retries and scheduling, and build a tiny local runner that executes ingest -> transform -> quality -> aggregate in order.

## Concepts
- API ingestion: pagination, retries with backoff (429/5xx yes, other 4xx no), rate limits (`Retry-After`)
- Incremental loads: a watermark ("only records newer than X") saved after a successful write
- Bronze keeps the raw payload untouched plus `ingested_at`; parsing happens in silver
- Job = a named workflow; task = one step; dependency = "B runs only after A succeeds"
- The task graph is a DAG (no cycles). A valid run order is a topological order
- Retries handle transient failures; a task that keeps failing marks downstream tasks as skipped
- Scheduling: cron-style triggers (daily 02:00) vs event triggers (file arrives)
- Idempotency: re-running a task must not duplicate data

## Steps
1. Open `ex01_workflow.py` and complete the three TODO functions.
2. Open `ex02_api_ingest.py` and complete its TODO functions, top to bottom. Read the docstring of `tests/mock_weather_api.py` first (it is the fake API; you can also run it by hand and `curl` it).
3. Read the `PIPELINE` dict at the bottom: it is the real task graph for this repo.
4. Optional: write two sentences on how Databricks Jobs expresses the same graph.

## How to check your work
```
docker run --rm --memory=4g --cpus=4 -v "$PWD":/workspace -v de-ivy-cache:/root/.ivy2 de-workspace pytest tests/test_w06_orchestration.py tests/test_w06_api_ingest.py
```
Or: `make test-one T="tests/test_w06_api_ingest.py"`

## Self-test questions
1. Why must a workflow graph have no cycles?
2. When is a retry the wrong answer to a failed task?
3. What does it mean for a task to be idempotent, and why does a scheduler need it?
4. Why save the watermark after writing to bronze, not before?
5. Why store the API response as a raw string in bronze instead of parsing it into columns?
