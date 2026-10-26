# Week 7: Capstone build (outline, not a guided lesson)

> Honest note: this week is a skeleton. By now the exercises are yours to design, so there are no TODO files or pre-written tests. Ask me for a test skeleton once you pick your table designs.

## Goal
Build raw files -> bronze -> silver -> gold in `src/retail_pipeline/`, ending with a daily sales + weather feature table (one row per store per day) suitable for demand forecasting.

## Concepts
- Reuse everything: explicit schemas, dedupe, quarantine of bad rows, MERGE for late files, quality checks, the Week 6 runner

## Steps
1. `ingest.py`: read each raw file with an explicit schema into bronze Delta tables, adding `_source_file` and `_ingested_at`.
2. `transform.py`: silver. Dedupe transactions, parse timestamps, quarantine bad rows, handle the new column from the later file.
3. `quality.py`: run your null-rate, duplicate and orphan checks on silver.
4. `aggregate.py`: gold `daily_store_features` (sales, gallons, items, loyalty share, temperature, precipitation).
5. Wire the four steps with `run_workflow` from Week 6.

## How to check your work
Write at least one pytest per layer in `tests/` using small hand-made DataFrames. Then `make test`.

## Self-test questions
1. Why is the gold table grain one row per store per day?
2. How does your pipeline behave if the late-arriving file is run twice?
3. Which check would catch a store missing from `stores`?
