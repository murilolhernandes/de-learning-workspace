# Week 8: Capstone finish (outline, not a guided lesson)

> Honest note: skeleton only. This is the first week to cut if you fall behind.

## Goal
Make the capstone defensible: tests pass, CI is green, one simple chart exists, and the README explains your design choices and tradeoffs.

## Concepts
- Tradeoffs worth naming: Delta vs plain Parquet, partitioning choice, full vs incremental load, quarantine vs drop

## Steps
1. Run `ruff check .` and `pytest`; fix everything.
2. Push and confirm the GitHub Actions run is green.
3. One chart from the gold table (daily sales vs temperature, for example) saved as an image.
4. Add a "Design choices and tradeoffs" section to the top-level README: 5 bullets, each with the alternative you rejected.

## How to check your work
`ruff check .` and `pytest` both exit 0, and the CI badge/run is green.

## Self-test questions
1. What is the weakest part of your pipeline, and how would you fix it with more time?
2. Why did you choose your partition column?
3. How would this run daily on Databricks?
