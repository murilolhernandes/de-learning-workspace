# SQL interview questions

Practice these in Spark SQL on the `sales` view from Week 1 (`store_id, sale_date, amount`).

1. **Running total per store.**
   Cue: `SUM(amount) OVER (PARTITION BY store_id ORDER BY sale_date)`.

2. **Best day per store.**
   Cue: `ROW_NUMBER() OVER (PARTITION BY store_id ORDER BY amount DESC)` in a subquery, keep `rn = 1`.

3. **Day-over-day change.**
   Cue: `LAG(amount) OVER (PARTITION BY ... ORDER BY ...)`, then subtract. First row has NULL.

4. **`WHERE` vs `HAVING`?**
   Cue: `WHERE` filters rows before grouping; `HAVING` filters groups after aggregation.

5. **INNER vs LEFT vs ANTI join?**
   Cue: inner = matches only; left = all left rows, NULLs when no match; anti = left rows with no match (`LEFT JOIN ... WHERE right.key IS NULL` or `NOT EXISTS`).

6. **Find duplicate transactions.**
   Cue: `GROUP BY transaction_id HAVING COUNT(*) > 1`.

7. **Top 3 stores by revenue per state.**
   Cue: `DENSE_RANK()` partitioned by state, filter `<= 3`. Say why you chose dense_rank vs row_number.

8. **How does `NULL` behave in comparisons and aggregates?**
   Cue: `NULL = NULL` is not true; use `IS NULL`. `COUNT(col)` skips NULLs, `COUNT(*)` does not. `AVG` ignores NULLs.

9. **CTE vs subquery?**
   Cue: mostly readability; CTEs can be referenced more than once. The optimizer usually treats them the same.

10. **What is a star schema?**
    Cue: a central fact table (transactions) with foreign keys to dimensions (store, date, loyalty member). Optimized for analytics and simple joins.

11. **Fact vs dimension table?**
    Cue: facts are events/measures at a grain (one row per transaction item). Dimensions are descriptive context (store attributes).

12. **What is the grain of a table and why state it first?**
    Cue: what one row represents. Wrong grain means double counting after joins.

## Tip

When you write a window query, say the three parts aloud: partition (the group), order (the sequence), function (what you compute).
