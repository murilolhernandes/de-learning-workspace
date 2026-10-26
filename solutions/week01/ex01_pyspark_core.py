"""Reference solution for ex01. Do not open until you have tried (and asked for hints)."""

from pyspark.sql import DataFrame, SparkSession, Window
from pyspark.sql import functions as F
from pyspark.sql.types import (
    DoubleType,
    IntegerType,
    StringType,
    StructField,
    StructType,
)


def transactions_schema() -> StructType:
    return StructType([
        StructField("transaction_id", StringType(), True),
        StructField("store_id", StringType(), True),
        StructField("txn_ts", StringType(), True),
        StructField("loyalty_id", StringType(), True),
        StructField("fuel_gallons", DoubleType(), True),
        StructField("item_count", IntegerType(), True),
        StructField("total_amount", DoubleType(), True),
    ])


def read_transactions(spark: SparkSession, path: str) -> DataFrame:
    return spark.read.csv(path, header=True, schema=transactions_schema())


def large_baskets(df: DataFrame, min_total: float) -> DataFrame:
    return df.filter(F.col("total_amount") >= min_total)


def add_basket_size(df: DataFrame) -> DataFrame:
    return df.withColumn(
        "basket_size", F.when(F.col("total_amount") >= 50, "large").otherwise("small")
    )


def sales_by_store(df: DataFrame) -> DataFrame:
    return df.groupBy("store_id").agg(
        F.count("*").alias("txn_count"), F.sum("total_amount").alias("revenue")
    )


def join_store_state(sales: DataFrame, stores: DataFrame) -> DataFrame:
    return sales.join(stores.select("store_id", "state"), on="store_id", how="inner")


def rank_within_state(df: DataFrame) -> DataFrame:
    w = Window.partitionBy("state").orderBy(F.col("revenue").desc())
    return df.withColumn("state_rank", F.dense_rank().over(w))


TRANSFORMATIONS_VS_ACTIONS = {
    "filter": "transformation",
    "count": "action",
    "groupBy": "transformation",
    "show": "action",
    "withColumn": "transformation",
    "collect": "action",
    "join": "transformation",
}
