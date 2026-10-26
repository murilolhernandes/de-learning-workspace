import os

import pytest
from conftest import load_exercise

ex = load_exercise("02_pyspark_delta", "ex03_delta_merge")

STORE_SCHEMA = "store_id string, state string"


def _write_initial(spark, path):
    spark.createDataFrame([("S1", "TX"), ("S2", "AR")], STORE_SCHEMA).write.format("delta").save(path)


def test_upsert_stores(spark, tmp_path):
    path = str(tmp_path / "stores")
    _write_initial(spark, path)
    updates = spark.createDataFrame([("S2", "MS"), ("S3", "LA")], STORE_SCHEMA)
    ex.upsert_stores(spark, path, updates)
    got = {r.store_id: r.state for r in spark.read.format("delta").load(path).collect()}
    assert got == {"S1": "TX", "S2": "MS", "S3": "LA"}


def test_append_strict_refuses_new_column(spark, tmp_path):
    path = str(tmp_path / "stores")
    _write_initial(spark, path)
    wider = spark.createDataFrame([("S3", "LA", "Murphy USA")], STORE_SCHEMA + ", brand string")
    with pytest.raises(Exception):
        ex.append_strict(wider, path)
    assert spark.read.format("delta").load(path).count() == 2


def test_append_strict_allows_same_schema(spark, tmp_path):
    path = str(tmp_path / "stores")
    _write_initial(spark, path)
    ex.append_strict(spark.createDataFrame([("S3", "LA")], STORE_SCHEMA), path)
    assert spark.read.format("delta").load(path).count() == 3


def test_append_evolving_adds_column(spark, tmp_path):
    path = str(tmp_path / "stores")
    _write_initial(spark, path)
    wider = spark.createDataFrame([("S3", "LA", "Murphy USA")], STORE_SCHEMA + ", brand string")
    ex.append_evolving(wider, path)
    out = spark.read.format("delta").load(path)
    assert "brand" in out.columns
    assert out.count() == 3
    assert out.filter("store_id = 'S1'").collect()[0].brand is None


def test_write_partitioned(spark, tmp_path):
    path = str(tmp_path / "by_state")
    df = spark.createDataFrame([("S1", "TX"), ("S2", "AR"), ("S3", "TX")], STORE_SCHEMA)
    ex.write_partitioned(df, path, "state")
    dirs = {d for d in os.listdir(path) if d.startswith("state=")}
    assert dirs == {"state=TX", "state=AR"}
    assert spark.read.format("delta").load(path).count() == 3


def test_partitioning_rules():
    assert ex.PARTITIONING_RULES == {
        "partition_by_high_cardinality_id_like_transaction_id_is_good": False,
        "partition_by_a_date_column_often_makes_sense_for_large_tables": True,
        "many_tiny_files_slow_down_reads": True,
        "small_tables_under_a_few_GB_usually_need_partitioning": False,
    }
