import pytest
from conftest import load_src_module

q = load_src_module("quality", "week04")


@pytest.fixture
def df(spark):
    return spark.createDataFrame(
        [(1, "a"), (2, None), (2, "b"), (3, None)], "id int, loyalty string"
    )


def test_null_rate(df):
    assert q.null_rate(df, "loyalty") == pytest.approx(0.5)
    assert q.null_rate(df, "id") == 0.0


def test_null_rate_empty(spark):
    empty = spark.createDataFrame([], "id int")
    assert q.null_rate(empty, "id") == 0.0


def test_duplicate_count(df, spark):
    assert q.duplicate_count(df, ["id"]) == 2  # both rows with id=2
    assert q.duplicate_count(df, ["id", "loyalty"]) == 0


def test_orphan_count(spark):
    child = spark.createDataFrame([(1,), (2,), (9,), (None,)], "store_id int")
    parent = spark.createDataFrame([(1,), (2,), (3,)], "store_id int")
    assert q.orphan_count(child, parent, "store_id") == 1  # 9; null is not an orphan
