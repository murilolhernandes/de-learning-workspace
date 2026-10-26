"""Solution for Week 3, exercise 3."""

from pyspark.sql import DataFrame


def assert_frames_equal(actual: DataFrame, expected: DataFrame, order_by: list[str]) -> None:
    assert actual.columns == expected.columns, f"columns differ: {actual.columns} vs {expected.columns}"
    got = [tuple(r) for r in actual.orderBy(*order_by).collect()]
    want = [tuple(r) for r in expected.orderBy(*order_by).collect()]
    assert got == want, f"rows differ:\n{got}\n{want}"
