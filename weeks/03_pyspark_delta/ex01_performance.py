"""Exercise 1: shuffles, partitions, caching, broadcast. Run:  pytest tests/test_w03_performance.py"""

from pyspark.sql import DataFrame, functions as F

# Label each operation "narrow" (no data movement between partitions) or "wide" (shuffle).
WIDE_VS_NARROW = {
    "filter": "narrow",
    "withColumn": "narrow",
    "groupBy.agg": "wide",
    "join_two_large_tables": "wide",
    "select": "narrow",
    "orderBy": "wide",
}


def repartition_by_store(df: DataFrame, n: int) -> DataFrame:
    """Return df split into exactly n partitions, rows with the same store_id together."""
    return df.repartition(n, "store_id")


def reduce_partitions(df: DataFrame, n: int) -> DataFrame:
    """Return df with n partitions WITHOUT a full shuffle (use for shrinking only)."""
    return df.coalesce(n)


def cache_and_count(df: DataFrame) -> int:
    """Mark df as cached, materialize it with an action, and return its row count."""
    return df.cache().count()


def join_with_broadcast(big: DataFrame, small: DataFrame, key: str) -> DataFrame:
    """Inner join big to small on key, hinting Spark to broadcast the small side."""
    return big.join(F.broadcast(small), on=key)