"""Solution for Week 2, exercise 2."""

from pyspark.sql import DataFrame
from pyspark.sql import functions as F


def fill_loyalty(df: DataFrame) -> DataFrame:
    return df.withColumn("is_member", F.col("loyalty_id").isNotNull()).withColumn(
        "loyalty_id", F.coalesce("loyalty_id", F.lit("GUEST"))
    )


def parse_timestamps(df: DataFrame) -> DataFrame:
    return df.withColumn("txn_ts", F.expr("try_to_timestamp(txn_ts, 'yyyy-MM-dd HH:mm:ss')"))


def add_date_parts(df: DataFrame) -> DataFrame:
    return (
        df.withColumn("txn_date", F.to_date("txn_ts"))
        .withColumn("txn_hour", F.hour("txn_ts"))
        .withColumn("day_of_week", F.dayofweek("txn_ts"))
    )


def add_store_age_years(stores: DataFrame, as_of: str) -> DataFrame:
    months = F.months_between(F.to_date(F.lit(as_of)), F.col("opened_date"))
    return stores.withColumn("age_years", F.floor(months / 12).cast("int"))


def skus_per_txn(items: DataFrame) -> DataFrame:
    return (
        items.groupBy("transaction_id")
        .agg(F.collect_list("sku").alias("skus"))
        .withColumn("sku_count", F.size("skus"))
    )


def explode_skus(df: DataFrame) -> DataFrame:
    return df.withColumn("sku", F.explode("skus")).drop("skus")


def pack_amounts(df: DataFrame) -> DataFrame:
    return df.withColumn("amounts", F.struct("fuel_gallons", "total_amount"))
