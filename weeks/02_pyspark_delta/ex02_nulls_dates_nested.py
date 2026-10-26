"""Exercise 2: nulls, dates, arrays and structs. Run:  pytest tests/test_w02_nulls_dates_nested.py"""

from pyspark.sql import DataFrame


def fill_loyalty(df: DataFrame) -> DataFrame:
    """Replace a null loyalty_id with 'GUEST' and add boolean `is_member` (True when it was not null)."""
    # TODO: compute is_member BEFORE you overwrite loyalty_id
    raise NotImplementedError


def parse_timestamps(df: DataFrame) -> DataFrame:
    """Convert string column txn_ts (format 'yyyy-MM-dd HH:mm:ss') to a timestamp.

    Values that do not parse must become null (not an error).
    """
    # TODO: F.to_timestamp(col, fmt). Check what happens with spark.sql.ansi.enabled off.
    raise NotImplementedError


def add_date_parts(df: DataFrame) -> DataFrame:
    """Given timestamp column txn_ts, add txn_date (date), txn_hour (int) and day_of_week (int, 1=Sunday)."""
    # TODO: to_date, hour, dayofweek
    raise NotImplementedError


def add_store_age_years(stores: DataFrame, as_of: str) -> DataFrame:
    """Add `age_years`: whole years between opened_date (a date column) and as_of ('yyyy-MM-dd')."""
    # TODO: months_between, then floor(... / 12)
    raise NotImplementedError


def skus_per_txn(items: DataFrame) -> DataFrame:
    """From item rows (transaction_id, sku), return one row per transaction_id with
    `skus` (array of sku) and `sku_count` (size of that array)."""
    # TODO: groupBy + collect_list, then F.size
    raise NotImplementedError


def explode_skus(df: DataFrame) -> DataFrame:
    """Given a column `skus` (array), return one row per sku: all other columns plus `sku`.
    Drop the `skus` column. Rows with an empty or null array are dropped."""
    # TODO: F.explode
    raise NotImplementedError


def pack_amounts(df: DataFrame) -> DataFrame:
    """Add a struct column `amounts` with fields fuel_gallons and total_amount (keep the originals too)."""
    # TODO: F.struct(...).alias? Remember you read struct fields with "amounts.total_amount".
    raise NotImplementedError
