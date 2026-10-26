import pytest

from conftest import load_exercise

ex = load_exercise("01_interview_sprint", "ex03_sql_windows")


@pytest.fixture(autouse=True)
def sales_view(spark):
    spark.createDataFrame(
        [
            ("A", "2025-01-01", 10), ("A", "2025-01-02", 20), ("A", "2025-01-03", 5),
            ("B", "2025-01-01", 7), ("B", "2025-01-02", 3),
        ],
        ["store_id", "sale_date", "amount"],
    ).createOrReplaceTempView("sales")


def test_running_total(spark):
    rows = spark.sql(ex.running_total_sql()).collect()
    got = {(r.store_id, r.sale_date): r.running_total for r in rows}
    assert got == {
        ("A", "2025-01-01"): 10, ("A", "2025-01-02"): 30, ("A", "2025-01-03"): 35,
        ("B", "2025-01-01"): 7, ("B", "2025-01-02"): 10,
    }


def test_best_day_per_store(spark):
    rows = spark.sql(ex.best_day_per_store_sql()).collect()
    assert {(r.store_id, r.sale_date, r.amount) for r in rows} == {
        ("A", "2025-01-02", 20), ("B", "2025-01-01", 7),
    }
    assert len(rows) == 2


def test_day_over_day(spark):
    rows = spark.sql(ex.day_over_day_sql()).collect()
    got = {(r.store_id, r.sale_date): r.prev_amount for r in rows}
    assert got == {
        ("A", "2025-01-01"): None, ("A", "2025-01-02"): 10, ("A", "2025-01-03"): 20,
        ("B", "2025-01-01"): None, ("B", "2025-01-02"): 7,
    }
