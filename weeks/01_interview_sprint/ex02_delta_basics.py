"""Exercise 2: Delta Lake basics. Run:  pytest tests/test_w01_delta_basics.py"""

from pyspark.sql import DataFrame, SparkSession
from delta.tables import DeltaTable


def write_delta(df: DataFrame, path: str) -> None:
    """Write df to path as a Delta table, replacing anything already there."""
    df.write.format("delta").mode("overwrite").save(path)


def append_delta(df: DataFrame, path: str) -> None:
    """Append df to the existing Delta table at path."""
    df.write.format("delta").mode("append").save(path)


def read_delta(spark: SparkSession, path: str) -> DataFrame:
    """Read the Delta table at path."""
    return spark.read.format("delta").load(path)


def version_count(spark: SparkSession, path: str) -> int:
    """How many versions does the table's history show? (Hint: DeltaTable.forPath(...).history())"""
    return DeltaTable.forPath(spark, path).history().count()


def read_version(spark: SparkSession, path: str, version: int) -> DataFrame:
    """Time travel: read the table as it was at the given version number."""
    return spark.read.format("delta").option("versionAsOf", version).load(path)
