# PySpark and Delta interview questions

Answer out loud first, then check the cue. Cues are reminders, not scripts.

1. **What is the difference between a transformation and an action?**
   Cue: transformations are lazy and build a plan (`filter`, `select`, `join`); actions trigger execution (`count`, `show`, `collect`, `write`). Laziness lets Spark optimize the whole plan.

2. **Why define an explicit schema instead of `inferSchema`?**
   Cue: inference needs an extra pass over the data, can guess wrong (IDs become ints, dates become strings), and hides bad data. An explicit schema is faster, stable and documents the contract.

3. **What is a shuffle and why is it expensive?**
   Cue: data is redistributed across the network between partitions (joins, `groupBy`, `distinct`, window). Cost: disk and network I/O plus serialization. Reduce it with filters first, broadcast joins and fewer wide operations.

4. **Narrow vs wide transformations?**
   Cue: narrow = each output partition depends on one input partition (`map`, `filter`). Wide = needs data from many partitions (`groupBy`, `join`) and creates a stage boundary.

5. **When would you use a broadcast join?**
   Cue: one side is small (a stores dimension table). Spark ships it to every executor and skips shuffling the big side. Mention the size limit (`autoBroadcastJoinThreshold`) and out-of-memory risk if it is not small.

6. **How do window functions differ from `groupBy`?**
   Cue: `groupBy` collapses rows; windows keep every row and add a computed column over a partition/order (`rank`, `lag`, running sum). Example: rank stores within a state.

7. **`rank` vs `dense_rank` vs `row_number`?**
   Cue: ties. `row_number` is always unique, `rank` leaves gaps after ties, `dense_rank` has no gaps. `row_number` is the usual pick for "latest row per key" dedup.

8. **What does Delta Lake add on top of Parquet?**
   Cue: a transaction log, so you get ACID writes, schema enforcement, time travel, `MERGE`/`UPDATE`/`DELETE`, and consistent reads while writes happen.

9. **How does Delta time travel work, and when is it useful?**
   Cue: every commit is a numbered version in `_delta_log`. Read with `versionAsOf` or `timestampAsOf`. Useful for audits, debugging a bad load and rollback. Old files are removed by `VACUUM`.

10. **Explain bronze, silver and gold.**
    Cue: bronze = raw, append-only, as received. Silver = cleaned, deduplicated, typed, conformed. Gold = business-ready aggregates and features. Each layer can be rebuilt from the one before.

11. **How would you handle duplicate rows in incoming data?**
    Cue: define the business key, then `dropDuplicates` on it, or `row_number` over key ordered by ingestion time and keep 1. In Delta, use `MERGE` so reruns are idempotent.

12. **What is a `MERGE` (upsert) and why use it?**
    Cue: match source to target on a key; update when matched, insert when not. Makes pipelines idempotent and handles late-arriving data without full rewrites.

13. **What is schema enforcement vs schema evolution in Delta?**
    Cue: enforcement rejects writes that do not match the table schema. Evolution (`mergeSchema`) lets you add new columns on purpose. Example: a new `payment_method` column appears in a later file.

14. **Why avoid Python UDFs when possible?**
    Cue: UDFs run row by row in Python, are opaque to the Catalyst optimizer, and cost serialization. Prefer built-in functions; if needed, use pandas UDFs.

15. **How do you decide how many partitions and whether to partition a table by a column?**
    Cue: partition on a low-cardinality column used in filters (e.g. date). Too many small partitions means the small-files problem. Shuffle partitions default is 200, tune to data size.

16. **When should you `cache()` a DataFrame?**
    Cue: when it is reused across multiple actions and is expensive to recompute. Remember it is lazy and takes memory; `unpersist` when done.

17. **How would you test PySpark code?**
    Cue: keep transformations as pure functions `DataFrame -> DataFrame`, build tiny inline DataFrames in pytest with a shared local SparkSession, assert on collected rows.

## Honest-beginner framing

If you do not know something: say what you do know, how you would find out, and a related thing you have built. Example: "I have not tuned a 10 TB job, but I built a local pipeline where I compared a shuffle join with a broadcast join and read the plan with `explain()`."
