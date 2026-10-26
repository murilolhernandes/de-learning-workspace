import pytest
from conftest import load_exercise

ex = load_exercise("03_pyspark_delta", "ex03_testing_dataframes")

SCHEMA = "k string, v int"


def test_equal_frames_ignore_row_order(spark):
    a = spark.createDataFrame([("a", 1), ("b", 2)], SCHEMA)
    b = spark.createDataFrame([("b", 2), ("a", 1)], SCHEMA)
    ex.assert_frames_equal(a, b, ["k"])


def test_different_values_fail(spark):
    a = spark.createDataFrame([("a", 1), ("b", 2)], SCHEMA)
    b = spark.createDataFrame([("a", 1), ("b", 3)], SCHEMA)
    with pytest.raises(AssertionError):
        ex.assert_frames_equal(a, b, ["k"])


def test_different_row_count_fails(spark):
    a = spark.createDataFrame([("a", 1)], SCHEMA)
    b = spark.createDataFrame([("a", 1), ("b", 2)], SCHEMA)
    with pytest.raises(AssertionError):
        ex.assert_frames_equal(a, b, ["k"])


def test_different_columns_fail(spark):
    a = spark.createDataFrame([("a", 1)], SCHEMA)
    b = spark.createDataFrame([("a", 1)], "k string, w int")
    with pytest.raises(AssertionError):
        ex.assert_frames_equal(a, b, ["k"])
