# Week 4: Modeling and data quality

## Goal
Design a star schema for the retail data, state clear bronze/silver/gold rules, and write the data quality checks every pipeline needs.

## Concepts
- Fact tables (events, numbers you sum) vs dimension tables (descriptions you filter and group by)
- Grain: one row of the fact table means exactly what? Decide this first
- Surrogate vs natural keys
- Medallion rules: bronze keeps raw data as-is, silver cleans and conforms, gold serves a business question
- Data quality: null rate, duplicates, referential integrity (orphans)
- Lineage: where each gold column comes from

## Steps
1. Read `star_schema.md` and `medallion_rules.md` in this folder.
2. `ex01_star_schema.py`: classify the columns and state the grain.
3. `ex02_medallion_rules.py`: assign each rule to a layer.
4. Implement the three checks in `src/retail_pipeline/quality.py` (`null_rate`, `duplicate_count`, `orphan_count`).
5. Fill in your own `lineage_notes.md` for `daily_store_sales` (template inside).

## How to check your work
```
docker run --rm --memory=4g --cpus=4 -v "$PWD":/workspace -v de-ivy-cache:/root/.ivy2 de-workspace pytest tests/test_w04_modeling.py tests/test_w04_quality.py
```
Tick `PROGRESS.md` only when both files pass.

## Self-test questions
1. What is the grain of `fact_transaction_item`, and what breaks if you mix grains in one fact table?
2. Why keep a bronze layer at all if silver is cleaner?
3. A check finds 3% null loyalty ids. Is that a failure? What decides it?
