# Week 6: Orchestration

## Goal
Explain jobs, tasks, dependencies, retries and scheduling, and build a tiny local runner that executes ingest -> transform -> quality -> aggregate in order.

## Concepts
- Job = a named workflow; task = one step; dependency = "B runs only after A succeeds"
- The task graph is a DAG (no cycles). A valid run order is a topological order
- Retries handle transient failures; a task that keeps failing marks downstream tasks as skipped
- Scheduling: cron-style triggers (daily 02:00) vs event triggers (file arrives)
- Idempotency: re-running a task must not duplicate data

## Steps
1. Open `ex01_workflow.py` and complete the three TODO functions.
2. Read the `PIPELINE` dict at the bottom: it is the real task graph for this repo.
3. Optional: write two sentences on how Databricks Jobs expresses the same graph.

## How to check your work
```
docker run --rm --memory=4g --cpus=4 -v "$PWD":/workspace -v de-ivy-cache:/root/.ivy2 de-workspace pytest tests/test_w06_orchestration.py
```

## Self-test questions
1. Why must a workflow graph have no cycles?
2. When is a retry the wrong answer to a failed task?
3. What does it mean for a task to be idempotent, and why does a scheduler need it?
