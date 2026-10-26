# Week 3: Performance, UDFs and testing

## Goal
Explain why Spark jobs are slow or fast, avoid the common traps, and test your own transformations with pytest.

## Concepts
- Narrow vs wide transformations; a wide one causes a shuffle (data moves across the network)
- `repartition` (full shuffle, can raise or lower count) vs `coalesce` (no shuffle, only lowers)
- `cache()` is lazy; use it only for a DataFrame reused several times
- Broadcast hint for small lookup tables
- Python UDFs hide logic from the optimizer and move rows between the JVM and Python; prefer built-ins
- Unit tests for DataFrame functions: small inline data, compare collected rows

## Steps
1. `ex01_performance.py`: classify operations, repartition, coalesce, cache, broadcast.
2. `ex02_udf_vs_builtin.py`: rewrite a UDF with `when/otherwise` so results match.
3. `ex03_testing_dataframes.py`: write `assert_frames_equal`, then write your own first pytest test in `tests/test_my_first.py` for any Week 2 function you finished.

Replace each `TODO` and `raise NotImplementedError`. The docstring is the spec.

## How to check your work
```
make test
docker run --rm --memory=4g --cpus=4 -v "$PWD":/workspace -v de-ivy-cache:/root/.ivy2 de-workspace pytest tests/test_w03_performance.py
```
Tick `PROGRESS.md` only when the test file passes.

## Self-test questions
1. What makes a transformation "wide", and why does that matter for performance?
2. When would you choose `coalesce` over `repartition`, and when would `coalesce` be wrong?
3. Why is a Python UDF usually slower than the equivalent built-in expression?
