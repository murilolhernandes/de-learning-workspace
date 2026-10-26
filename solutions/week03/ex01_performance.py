"""Solution for Week 3, exercise 1."""

from pyspark.sql import DataFrame
from pyspark.sql import functions as F

WIDE_VS_NARROW = {
    "filter": "narrow",
    "withColumn": "narrow",
    "groupBy.agg": "wide",
    "join_two_large_tables": "wide",
    "select": "narrow",
    "orderBy": "wide",
}


def repartition_by_store(df: DataFrame, n: int) -> DataFrame:
    return df.repartition(n, "store_id")


def reduce_partitions(df: DataFrame, n: int) -> DataFrame:
    return df.coalesce(n)


def cache_and_count(df: DataFrame) -> int:
    df.cache()
    return df.count()


def join_with_broadcast(big: DataFrame, small: DataFrame, key: str) -> DataFrame:
    return big.join(F.broadcast(small), key, "inner")
