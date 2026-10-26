"""Reference solution for ex03. Do not open until you have tried (and asked for hints)."""


def running_total_sql() -> str:
    return """
        SELECT store_id, sale_date, amount,
               SUM(amount) OVER (PARTITION BY store_id ORDER BY sale_date) AS running_total
        FROM sales
    """


def best_day_per_store_sql() -> str:
    return """
        SELECT store_id, sale_date, amount FROM (
            SELECT *, ROW_NUMBER() OVER (PARTITION BY store_id ORDER BY amount DESC) AS rn
            FROM sales
        ) WHERE rn = 1
    """


def day_over_day_sql() -> str:
    return """
        SELECT store_id, sale_date, amount,
               LAG(amount) OVER (PARTITION BY store_id ORDER BY sale_date) AS prev_amount
        FROM sales
    """
