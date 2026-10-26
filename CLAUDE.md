
## Who I am and the goal

I am a new graduate (BS in Software Development) preparing for a Data Engineer role at Murphy USA, a convenience-store and fuel retailer. They already know I have no data engineering experience; they said they want a software development background and a desire to learn. Their public job posting lists: Databricks, a cloud-based data lake, Python and SQL (Scala optional), PySpark (my hiring manager named it), Terraform, DevOps automation for pipelines, ETL orchestration, data quality, governance and BI. The cloud provider is not confirmed, so keep everything cloud-neutral.

I may get an interview invitation this week, and a start date is likely early next year, so I have about  **10 weeks** . Assume 10-15 hours per week unless I tell you otherwise. Build me a self-contained **simulated workspace** on my own machine where I learn these skills by doing, with the most job-relevant skills first. Nothing may require a paid account, real cloud credentials or network access beyond installing packages.

## Priorities

1. PySpark and Delta Lake on a local Spark, the core of the job. Hands-on first, theory second.
2. Enough SQL, data modeling and the bronze/silver/gold pattern to explain my design choices.
3. Terraform and CI at the "can read it, run it, and explain it" level, not mastery.
4. Skip or keep light: BI tools (one simple chart only), Scala, streaming, and advanced tuning.

## Rules

1. Work only inside this folder. Never create cloud resources, never ask for or write real credentials, and never run `terraform apply`. Terraform is validate/plan-only against local or mock providers.
2. Act as a tutor, not a code generator. Exercise files contain `TODO` markers and failing tests. Put full solutions in `solutions/` and do not open them or show them unless I ask for a hint first, then a bigger hint, then the solution.
3. Check prerequisites before building anything: Python 3.10+, Java 11 or 17 (Spark needs it), `git`. If something is missing, tell me how to install it and stop.
4. Use a virtual environment. Install `pyspark`, `delta-spark`, `pandas`, `pytest`, `ruff`. Pin versions in `requirements.txt` and make sure `pytest` runs.
5. Keep each README short: goal, concepts, steps, how to check my work, and 3 self-test questions.
6. After building, print the folder tree and tell me which exercise to start with. Do not complete exercises for me.

## Folder structure to create

```
de-learning-workspace/
  README.md                  # how to use this workspace, study order
  PROGRESS.md                # checklist per week, ticked only when tests pass
  requirements.txt
  pyproject.toml             # src-layout package: retail_pipeline
  data/
    generate_data.py         # synthetic retail data (see below)
    raw/                     # generated CSV/JSON, git-ignored
  src/retail_pipeline/
    __init__.py
    spark_session.py         # local SparkSession + Delta config
    ingest.py                # bronze layer (TODO)
    transform.py             # silver layer (TODO)
    aggregate.py             # gold layer (TODO)
    quality.py               # data quality checks (TODO)
  weeks/
    01_interview_sprint/     # PySpark core + Delta basics + SQL windows + talking points
    02_pyspark_delta/        # joins, windows, nulls/dates, MERGE, partitioning
    03_pyspark_delta/        # performance, shuffles, caching, UDF vs built-ins, testing
    04_modeling_quality/     # star schema, medallion rules, data quality checks
    05_terraform_ci/         # Terraform (validate only), GitHub Actions, Makefile
    06_orchestration/        # job/task structure, scheduling concepts, one DAG-style workflow
    07_capstone_build/       # end-to-end pipeline: raw -> gold
    08_capstone_finish/      # tests, CI passing, README with tradeoffs, one simple chart
    09_10_polish_cert/       # mock interviews, resume bullets, optional Databricks exam prep
  tests/                     # pytest tests the exercises must pass
  solutions/                 # full solutions, off limits until I ask
  interview/
    pyspark_questions.md     # 12+ questions with short answer cues
    sql_questions.md
    behavioral_notes.md      # my background: client success + construction superintendent
    questions_to_ask.md      # smart questions for Murphy USA (cloud, orchestration, team, data)
  .github/workflows/ci.yml   # lint + tests
```

## Synthetic data to generate

`data/generate_data.py` should create realistic, reproducible (seeded) data for a fuel-and-convenience chain:

* `stores` (about 50 stores, state, brand, opened date)
* `transactions` (a few hundred thousand rows: store, timestamp, loyalty id nullable, fuel gallons, items, totals)
* `transaction_items` (SKU, category, quantity, price)
* `loyalty_members` (join date, segment)
* `weather_daily` (store region, date, temperature, precipitation)
* Deliberately include messy rows: duplicate transactions, null loyalty ids, bad timestamps, a late-arriving file, and one new column in a later file to test schema evolution.

## Weekly plan

* **Week 1, interview sprint (do this first, in 5-7 days):** SparkSession, reading files with explicit schemas, select/filter/withColumn/groupBy/agg, transformations vs actions, one join, one window function, Delta read/write, the bronze/silver/gold idea, and SQL window functions. End the week with a 20-minute mock interview from `interview/` and a one-page "how I would explain my learning plan" in `behavioral_notes.md`. I should leave this week able to talk honestly and confidently as a beginner who is already building things.
* **Weeks 2-3, PySpark and Delta depth (most important):** joins including broadcast, anti joins, window functions, null and date handling, arrays and structs, Delta MERGE upserts, schema enforcement and evolution, partitioning, shuffles, caching, replacing a UDF with built-ins, and unit-testing DataFrame functions with pytest.
* **Week 4, modeling and quality:** star schema for the retail data, written bronze/silver/gold layer rules, data quality checks in `quality.py` (null rate, duplicates, referential integrity), and short lineage notes.
* **Week 5, Terraform and CI:** Terraform files for a generic storage bucket and a Databricks workspace resource, checked with `terraform validate` and `terraform plan` only; explain state, modules and variables. A GitHub Actions workflow that runs lint and tests.
* **Week 6, orchestration:** explain jobs, tasks, dependencies, retries and scheduling; build a small local workflow that runs ingest, transform, quality and aggregate in order.
* **Weeks 7-8, capstone:** pipeline from raw files to gold tables with a daily sales and weather feature table for demand forecasting, tests, CI passing, one simple chart, and a README explaining design choices and tradeoffs.
* **Weeks 9-10, polish:** mock interviews (technical and behavioral), resume bullets using posting keywords, and optional Databricks Data Engineer Associate exam prep if time allows.

## Progress tracking

Use `PROGRESS.md` with a checklist per week. When I tell you I finished an exercise, run its tests, check the result, and tick the box only if the tests pass. At the end of each week, quiz me with the 3 self-test questions before moving on. If I fall behind, cut scope from weeks 6, 8 and 9-10 before touching the PySpark weeks, and tell me what you cut.

Start by checking prerequisites, then build the workspace, with Week 1 fully ready first.
