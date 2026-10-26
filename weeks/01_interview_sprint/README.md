# Week 1: Interview Sprint (5-7 days)

## Goal
Leave this week able to talk honestly and confidently as a beginner who is already building things:
PySpark basics, Delta Lake basics, SQL window functions, and the bronze/silver/gold idea.

## Concepts
- SparkSession, explicit schemas vs `inferSchema`
- select / filter / withColumn / groupBy / agg
- Transformations (lazy) vs actions (trigger work)
- Joins and window functions (`dense_rank`, `SUM OVER`, `LAG`)
- Delta Lake: write, append, history, time travel
- Medallion pattern: bronze (raw, as-is), silver (cleaned, deduplicated), gold (business-ready)

## Steps
1. `ex01_pyspark_core.py` - fill in each TODO (days 1-3).
2. `ex02_delta_basics.py` - Delta write/append/read/time travel (day 4).
3. `ex03_sql_windows.py` - three window-function queries (day 5).
4. Read `interview/pyspark_questions.md` and `interview/sql_questions.md`.
5. Fill in the "how I would explain my learning plan" page in `interview/behavioral_notes.md`.
6. Do a 20-minute mock interview: pick questions at random from `interview/`, answer out loud.

## How to check your work
Run from the workspace root (see the top-level README for the Docker command):

```
pytest tests/test_w01_pyspark_core.py
pytest tests/test_w01_delta_basics.py
pytest tests/test_w01_sql_windows.py
```

Tick the box in `PROGRESS.md` only when the tests pass. The first run downloads the Delta jars once.

## Self-test questions
1. Why is an explicit schema better than `inferSchema` for production reads?
2. What is the difference between a transformation and an action, and why does Spark wait?
3. In one sentence each, what belongs in bronze, silver and gold?
