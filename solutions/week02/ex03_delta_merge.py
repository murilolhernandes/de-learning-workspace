"""Solution for Week 2, exercise 3."""

from delta.tables import DeltaTable
from pyspark.sql import DataFrame, SparkSession


def upsert_stores(spark: SparkSession, path: str, updates: DataFrame) -> None:
    (
        DeltaTable.forPath(spark, path)
        .alias("t")
        .merge(updates.alias("s"), "t.store_id = s.store_id")
        .whenMatchedUpdateAll()
        .whenNotMatchedInsertAll()
        .execute()
    )


def append_strict(df: DataFrame, path: str) -> None:
    df.write.format("delta").mode("append").save(path)


def append_evolving(df: DataFrame, path: str) -> None:
    df.write.format("delta").mode("append").option("mergeSchema", "true").save(path)


def write_partitioned(df: DataFrame, path: str, column: str) -> None:
    df.write.format("delta").mode("overwrite").partitionBy(column).save(path)


PARTITIONING_RULES = {
    "partition_by_high_cardinality_id_like_transaction_id_is_good": False,
    "partition_by_a_date_column_often_makes_sense_for_large_tables": True,
    "many_tiny_files_slow_down_reads": True,
    "small_tables_under_a_few_GB_usually_need_partitioning": False,
}
