"""Reference solution for ex02. Do not open until you have tried (and asked for hints)."""

from delta.tables import DeltaTable
from pyspark.sql import DataFrame, SparkSession


def write_delta(df: DataFrame, path: str) -> None:
    df.write.format("delta").mode("overwrite").save(path)


def append_delta(df: DataFrame, path: str) -> None:
    df.write.format("delta").mode("append").save(path)


def read_delta(spark: SparkSession, path: str) -> DataFrame:
    return spark.read.format("delta").load(path)


def version_count(spark: SparkSession, path: str) -> int:
    return DeltaTable.forPath(spark, path).history().count()


def read_version(spark: SparkSession, path: str, version: int) -> DataFrame:
    return spark.read.format("delta").option("versionAsOf", version).load(path)
