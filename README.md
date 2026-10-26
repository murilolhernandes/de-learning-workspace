# Data Engineering Learning Workspace

A self-contained, 10-week practice workspace for a Data Engineer role (PySpark, Delta Lake, SQL, Terraform, CI, orchestration). Everything runs locally on synthetic fuel-and-convenience retail data. No cloud account or credentials are needed.

## How it works

Each week has a folder in `weeks/` with a short README and exercise files containing `TODO` markers. The tests in `tests/` fail until you finish each exercise. `PROGRESS.md` is ticked only when the tests pass.

`solutions/` holds reference answers. Ask for a hint first, then a bigger hint, and only then the solution.

## Study order

| Week | Folder | Focus |
|---|---|---|
| 1 | `01_interview_sprint` | PySpark core, Delta basics, SQL windows, talking points |
| 2-3 | `02_pyspark_delta`, `03_pyspark_delta` | Joins, windows, MERGE, partitioning, performance, testing |
| 4 | `04_modeling_quality` | Star schema, medallion rules, data quality |
| 5 | `05_terraform_ci` | Terraform (validate/plan only), GitHub Actions, Makefile |
| 6 | `06_orchestration` | Jobs, tasks, retries, a local workflow |
| 7-8 | `07_capstone_build`, `08_capstone_finish` | End-to-end pipeline, tests, CI, chart |
| 9-10 | `09_10_polish_cert` | Mock interviews, resume bullets, optional exam prep |

If you fall behind, cut weeks 6, 8 and 9-10 before touching the PySpark weeks.

## Setup

Spark needs Java and (on Windows) `winutils.exe`, so run it in Docker on Linux.

```bash
docker build -t de-workspace .
make test            # runs pytest in the container
make test-solutions  # sanity check: reference solutions should pass
```

`make` uses `--memory=4g` and a named volume so the Delta jars are downloaded only once (the first run needs network access for that).

Without Docker, on a Linux or Mac machine:

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt && pip install -e .
pytest
```

Generate the data (runs anywhere, with no Spark):

```bash
python data/generate_data.py --rows-per-month 50000
```

## Start here

`weeks/01_interview_sprint/README.md`, then `ex01_pyspark_core.py`.

## Safety rules

- Work only inside this folder.
- Never create cloud resources or write real credentials.
- Never run `terraform apply`. Use `validate` and `plan` only.
