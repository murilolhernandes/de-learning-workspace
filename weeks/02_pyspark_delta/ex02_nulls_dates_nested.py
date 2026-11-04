"""Exercise 2: nulls, dates, arrays and structs. Run:  pytest tests/test_w02_nulls_dates_nested.py"""

from pyspark.sql import DataFrame, functions as F


def fill_loyalty(df: DataFrame) -> DataFrame:
    """Replace a null loyalty_id with 'GUEST' and add boolean `is_member` (True when it was not null)."""
    return df.withColumn("is_member", F.col("loyalty_id").isNotNull()).withColumn("loyalty_id", F.when(F.col("loyalty_id").isNull(), "GUEST").otherwise(F.col("loyalty_id")))


def parse_timestamps(df: DataFrame) -> DataFrame:
    """Convert string column txn_ts (format 'yyyy-MM-dd HH:mm:ss') to a timestamp.

    Values that do not parse must become null (not an error).
    """
    return df.withColumn("txn_ts", F.to_timestamp(F.col("txn_ts"), 'yyyy-MM-dd HH:mm:ss'))


def add_date_parts(df: DataFrame) -> DataFrame:
    """Given timestamp column txn_ts, add txn_date (date), txn_hour (int) and day_of_week (int, 1=Sunday)."""
    return df.withColumn("txn_date", F.to_date(F.col("txn_ts"))).withColumn("txn_hour", F.hour(F.col("txn_ts"))).withColumn("day_of_week", F.dayofweek(F.col("txn_ts")))


def add_store_age_years(stores: DataFrame, as_of: str) -> DataFrame:
    """Add `age_years`: whole years between opened_date (a date column) and as_of ('yyyy-MM-dd')."""
    return stores.withColumn("age_years", F.floor(F.months_between(F.lit(as_of), F.col("opened_date")) / 12))


def skus_per_txn(items: DataFrame) -> DataFrame:
    """From item rows (transaction_id, sku), return one row per transaction_id with
    `skus` (array of sku) and `sku_count` (size of that array)."""
    return items.groupBy("transaction_id").agg(F.collect_list("sku").alias("skus")).withColumn("sku_count", F.size("skus"))


def explode_skus(df: DataFrame) -> DataFrame:
    """Given a column `skus` (array), return one row per sku: all other columns plus `sku`.
    Drop the `skus` column. Rows with an empty or null array are dropped."""
    return df.withColumn("sku", F.explode("skus")).drop("skus")


def pack_amounts(df: DataFrame) -> DataFrame:
    """Add a struct column `amounts` with fields fuel_gallons and total_amount (keep the originals too)."""
    return df.withColumn("amounts", F.struct("fuel_gallons", "total_amount"))
