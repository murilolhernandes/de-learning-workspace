"""Exercise 3: a reusable DataFrame assertion. Run:  pytest tests/test_w03_testing.py"""

from pyspark.sql import DataFrame


def assert_frames_equal(actual: DataFrame, expected: DataFrame, order_by: list[str]) -> None:
    """Raise AssertionError unless both frames have the same columns and the same rows.

    Rows are compared after sorting by order_by, so row order does not matter.
    """
    # TODO: hint: compare .columns first, then sorted collect() results
    raise NotImplementedError
