"""Exercise 1: joins and window functions. Run:  pytest tests/test_w02_joins_windows.py"""

from pyspark.sql import DataFrame, Window, functions as F


def broadcast_join_stores(txns: DataFrame, stores: DataFrame) -> DataFrame:
    """Left join txns to stores on store_id, broadcasting the small stores table.

    Keep every txn column and add only `state` and `brand` from stores.
    """
    return txns.join(F.broadcast(stores.select("store_id", "state", "brand")), on="store_id", how="left")


def unmatched_transactions(txns: DataFrame, stores: DataFrame) -> DataFrame:
    """Return the txns whose store_id does not exist in stores (an anti join).

    Output has only the txn columns.
    """
    return txns.join(F.broadcast(stores), on="store_id", how="left_anti")


def running_sales(txns: DataFrame) -> DataFrame:
    """Add `running_total`: cumulative total_amount per store_id, ordered by txn_ts."""
    window = F.sum("total_amount").over(Window.partitionBy(txns.store_id).orderBy(txns.txn_ts).rowsBetween(Window.unboundedPreceding, Window.currentRow))
    return txns.withColumn("running_total", window)


def add_prev_gap_minutes(txns: DataFrame) -> DataFrame:
    """Add `prev_gap_min`: minutes since the previous txn at the same store (null for the first).

    txn_ts is a timestamp column.
    """
    prev_ts = F.lag("txn_ts", 1).over(Window.partitionBy("store_id").orderBy("txn_ts"))
    return txns.withColumn("prev_gap_min", ((F.unix_timestamp("txn_ts") - F.unix_timestamp(prev_ts)) / 60))


def latest_per_key(df: DataFrame, key: str, order_col: str) -> DataFrame:
    """Keep only the row with the largest order_col for each key. Same columns as df.

    This is the classic "deduplicate, keep the newest" pattern used in silver layers.
    """
    window = F.row_number().over(Window.partitionBy(key).orderBy(F.col(order_col).desc()))
    return df.withColumn("rn", window).filter(F.col("rn") == 1).drop("rn")
