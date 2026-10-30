"""Exercise 3: SQL window functions. Each function returns a SQL string.

The tests register a temp view named `sales` with columns (store_id, sale_date, amount) and run
your query with spark.sql. Run:  pytest tests/test_w01_sql_windows.py
"""


def running_total_sql() -> str:
    """Columns: store_id, sale_date, amount, running_total.
    running_total = cumulative sum of amount per store, ordered by sale_date."""
    return "SELECT store_id, sale_date, amount, SUM(amount) OVER (PARTITION BY store_id ORDER BY sale_date) AS running_total FROM sales;" 


def best_day_per_store_sql() -> str:
    """Columns: store_id, sale_date, amount. Exactly one row per store: its highest-amount day.
    (Hint: ROW_NUMBER in a subquery or CTE, then filter on it.)"""
    return "WITH HighestAmount AS (SELECT store_id, sale_date, amount, ROW_NUMBER() OVER (PARTITION BY store_id ORDER BY amount DESC) AS rn FROM sales) SELECT store_id, sale_date, amount FROM HighestAmount WHERE rn = 1;"


def day_over_day_sql() -> str:
    """Columns: store_id, sale_date, amount, prev_amount.
    prev_amount = the same store's amount on the previous sale_date (NULL for the first day)."""
    return "SELECT store_id, sale_date, amount, LAG(amount) OVER (PARTITION BY store_id ORDER BY sale_date) AS prev_amount FROM sales;"
