"""Exercise 3: a reusable DataFrame assertion. Run:  pytest tests/test_w03_testing.py"""

from pyspark.sql import DataFrame, functions as F


def assert_frames_equal(actual: DataFrame, expected: DataFrame, order_by: list[str]) -> None:
    """Raise AssertionError unless both frames have the same columns and the same rows.

    Rows are compared after sorting by order_by, so row order does not matter.
    """
    # TODO: hint: compare .columns first, then sorted collect() results
    if actual.columns != expected.columns:
        raise AssertionError(f"Columns differ: {actual.columns}, {expected.columns}")

    actual_rows = actual.orderBy(*order_by).collect()
    expected_rows = expected.orderBy(*order_by).collect()

    if actual_rows != expected_rows:
        raise AssertionError(f"Columns differ: {actual_rows}, {expected_rows}")
        