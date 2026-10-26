"""Exercise 3: Delta MERGE, schema rules, partitioning. Run:  pytest tests/test_w02_delta_merge.py"""

from pyspark.sql import DataFrame, SparkSession


def upsert_stores(spark: SparkSession, path: str, updates: DataFrame) -> None:
    """MERGE `updates` into the Delta table at path, matching on store_id.

    Matched rows are updated, new rows are inserted. Nothing is deleted.
    """
    # TODO: DeltaTable.forPath(spark, path).alias("t").merge(updates.alias("s"), "...")
    raise NotImplementedError


def append_strict(df: DataFrame, path: str) -> None:
    """Plain append to the Delta table at path. If df has columns the table does not,
    Delta must refuse (schema enforcement); do NOT work around it here."""
    # TODO: one line. The point of the test is to see Delta say no.
    raise NotImplementedError


def append_evolving(df: DataFrame, path: str) -> None:
    """Append df to the Delta table, letting new columns be added to the table (schema evolution)."""
    # TODO: .option("mergeSchema", "true")
    raise NotImplementedError


def write_partitioned(df: DataFrame, path: str, column: str) -> None:
    """Write df as a Delta table (overwrite) partitioned by `column`."""
    # TODO: .partitionBy(column)
    raise NotImplementedError


# Partitioning rules of thumb. Replace each None with True or False.
PARTITIONING_RULES = {
    "partition_by_high_cardinality_id_like_transaction_id_is_good": None,
    "partition_by_a_date_column_often_makes_sense_for_large_tables": None,
    "many_tiny_files_slow_down_reads": None,
    "small_tables_under_a_few_GB_usually_need_partitioning": None,
}
