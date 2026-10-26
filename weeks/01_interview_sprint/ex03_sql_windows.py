"""Exercise 3: SQL window functions. Each function returns a SQL string.

The tests register a temp view named `sales` with columns (store_id, sale_date, amount) and run
your query with spark.sql. Run:  pytest tests/test_w01_sql_windows.py
"""


def running_total_sql() -> str:
    """Columns: store_id, sale_date, amount, running_total.
    running_total = cumulative sum of amount per store, ordered by sale_date."""
    # TODO: SUM(...) OVER (PARTITION BY ... ORDER BY ...)
    raise NotImplementedError


def best_day_per_store_sql() -> str:
    """Columns: store_id, sale_date, amount. Exactly one row per store: its highest-amount day.
    (Hint: ROW_NUMBER in a subquery or CTE, then filter on it.)"""
    # TODO
    raise NotImplementedError


def day_over_day_sql() -> str:
    """Columns: store_id, sale_date, amount, prev_amount.
    prev_amount = the same store's amount on the previous sale_date (NULL for the first day)."""
    # TODO: LAG(...) OVER (...)
    raise NotImplementedError
