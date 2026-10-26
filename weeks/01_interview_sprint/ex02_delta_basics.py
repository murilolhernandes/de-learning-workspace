"""Exercise 2: Delta Lake basics. Run:  pytest tests/test_w01_delta_basics.py"""

from pyspark.sql import DataFrame, SparkSession


def write_delta(df: DataFrame, path: str) -> None:
    """Write df to path as a Delta table, replacing anything already there."""
    # TODO: df.write.format("delta") ...
    raise NotImplementedError


def append_delta(df: DataFrame, path: str) -> None:
    """Append df to the existing Delta table at path."""
    # TODO
    raise NotImplementedError


def read_delta(spark: SparkSession, path: str) -> DataFrame:
    """Read the Delta table at path."""
    # TODO
    raise NotImplementedError


def version_count(spark: SparkSession, path: str) -> int:
    """How many versions does the table's history show? (Hint: DeltaTable.forPath(...).history())"""
    # TODO
    raise NotImplementedError


def read_version(spark: SparkSession, path: str, version: int) -> DataFrame:
    """Time travel: read the table as it was at the given version number."""
    # TODO: option("versionAsOf", ...)
    raise NotImplementedError
