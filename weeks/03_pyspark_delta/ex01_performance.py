"""Exercise 1: shuffles, partitions, caching, broadcast. Run:  pytest tests/test_w03_performance.py"""

from pyspark.sql import DataFrame

# Label each operation "narrow" (no data movement between partitions) or "wide" (shuffle).
WIDE_VS_NARROW = {
    "filter": None,
    "withColumn": None,
    "groupBy.agg": None,
    "join_two_large_tables": None,
    "select": None,
    "orderBy": None,
}


def repartition_by_store(df: DataFrame, n: int) -> DataFrame:
    """Return df split into exactly n partitions, rows with the same store_id together."""
    # TODO: hint: repartition accepts a number and a column
    raise NotImplementedError


def reduce_partitions(df: DataFrame, n: int) -> DataFrame:
    """Return df with n partitions WITHOUT a full shuffle (use for shrinking only)."""
    # TODO: hint: coalesce vs repartition
    raise NotImplementedError


def cache_and_count(df: DataFrame) -> int:
    """Mark df as cached, materialize it with an action, and return its row count."""
    # TODO: hint: cache() is lazy, an action fills it
    raise NotImplementedError


def join_with_broadcast(big: DataFrame, small: DataFrame, key: str) -> DataFrame:
    """Inner join big to small on key, hinting Spark to broadcast the small side."""
    # TODO: hint: pyspark.sql.functions.broadcast (add the import)
    raise NotImplementedError
