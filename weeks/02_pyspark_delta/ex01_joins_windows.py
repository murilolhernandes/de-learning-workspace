"""Exercise 1: joins and window functions. Run:  pytest tests/test_w02_joins_windows.py"""

from pyspark.sql import DataFrame


def broadcast_join_stores(txns: DataFrame, stores: DataFrame) -> DataFrame:
    """Left join txns to stores on store_id, broadcasting the small stores table.

    Keep every txn column and add only `state` and `brand` from stores.
    """
    # TODO: F.broadcast(stores.select(...))
    raise NotImplementedError


def unmatched_transactions(txns: DataFrame, stores: DataFrame) -> DataFrame:
    """Return the txns whose store_id does not exist in stores (an anti join).

    Output has only the txn columns.
    """
    # TODO: how="left_anti"
    raise NotImplementedError


def running_sales(txns: DataFrame) -> DataFrame:
    """Add `running_total`: cumulative total_amount per store_id, ordered by txn_ts."""
    # TODO: Window.partitionBy(...).orderBy(...).rowsBetween(Window.unboundedPreceding, Window.currentRow)
    raise NotImplementedError


def add_prev_gap_minutes(txns: DataFrame) -> DataFrame:
    """Add `prev_gap_min`: minutes since the previous txn at the same store (null for the first).

    txn_ts is a timestamp column.
    """
    # TODO: F.lag over a window, then (unix_timestamp(a) - unix_timestamp(b)) / 60
    raise NotImplementedError


def latest_per_key(df: DataFrame, key: str, order_col: str) -> DataFrame:
    """Keep only the row with the largest order_col for each key. Same columns as df.

    This is the classic "deduplicate, keep the newest" pattern used in silver layers.
    """
    # TODO: row_number() over a window ordered by order_col descending, keep rn == 1, drop rn
    raise NotImplementedError
