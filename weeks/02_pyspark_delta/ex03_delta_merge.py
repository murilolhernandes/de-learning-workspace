"""Exercise 3: Delta MERGE, schema rules, partitioning. Run:  pytest tests/test_w02_delta_merge.py"""

from pyspark.sql import DataFrame, SparkSession
from delta import DeltaTable


def upsert_stores(spark: SparkSession, path: str, updates: DataFrame) -> None:
    """MERGE `updates` into the Delta table at path, matching on store_id.

    Matched rows are updated, new rows are inserted. Nothing is deleted.
    """
    DeltaTable.forPath(spark, path).alias("t").merge(updates.alias("s"), "t.store_id = s.store_id").whenMatchedUpdateAll().whenNotMatchedInsertAll().execute()


def append_strict(df: DataFrame, path: str) -> None:
    """Plain append to the Delta table at path. If df has columns the table does not,
    Delta must refuse (schema enforcement); do NOT work around it here."""
    df.write.format("delta").mode("append").save(path)


def append_evolving(df: DataFrame, path: str) -> None:
    """Append df to the Delta table, letting new columns be added to the table (schema evolution)."""
    df.write.format("delta").mode("append").option("mergeSchema", "true").save(path)


def write_partitioned(df: DataFrame, path: str, column: str) -> None:
    """Write df as a Delta table (overwrite) partitioned by `column`."""
    df.write.format("delta").mode("overwrite").partitionBy(column).save(path)


# Partitioning rules of thumb. Replace each None with True or False.
PARTITIONING_RULES = {
    "partition_by_high_cardinality_id_like_transaction_id_is_good": False,
    "partition_by_a_date_column_often_makes_sense_for_large_tables": True,
    "many_tiny_files_slow_down_reads": True,
    "small_tables_under_a_few_GB_usually_need_partitioning": False,
}
