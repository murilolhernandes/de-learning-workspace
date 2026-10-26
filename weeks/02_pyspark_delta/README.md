# Week 2: PySpark and Delta depth

## Goal
Join, window and clean data the way a silver layer needs, then use Delta features (MERGE, schema rules, partitions) you will be asked about in interviews.

## Concepts
- Broadcast join (small table copied to every worker) vs shuffle join; anti join finds "missing" rows
- Window functions: running totals, `lag`, `row_number` for "keep the newest"
- Nulls (`coalesce`), bad dates becoming null, date parts, arrays (`collect_list`, `explode`) and structs
- Delta MERGE (upsert), schema enforcement (refuses extra columns) vs evolution (`mergeSchema`)
- Partitioning: low-cardinality columns only, avoid many tiny files

## Steps
1. `ex01_joins_windows.py`: five functions on joins and windows.
2. `ex02_nulls_dates_nested.py`: seven functions on nulls, dates, arrays, structs.
3. `ex03_delta_merge.py`: MERGE, strict vs evolving append, partitioned write, and the true/false rules.

Replace each `TODO` and `raise NotImplementedError`. Read the docstring: it is the spec.

## How to check your work
```
make test        # all tests, in Docker
docker run --rm --memory=4g --cpus=4 -v "$PWD":/workspace -v de-ivy-cache:/root/.ivy2 de-workspace pytest tests/test_w02_joins_windows.py
```
Tick the boxes in `PROGRESS.md` only when the matching test file passes.

## Self-test questions
1. When is a broadcast join a good idea, and what goes wrong if the "small" table is not small?
2. Why does `row_number() ... filter(rn = 1)` beat `dropDuplicates` when you want the newest row?
3. What is the difference between Delta rejecting a new column and `mergeSchema`, and when would you want each?
