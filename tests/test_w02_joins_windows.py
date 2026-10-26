from datetime import datetime

from conftest import load_exercise

ex = load_exercise("02_pyspark_delta", "ex01_joins_windows")


def _txns(spark):
    return spark.createDataFrame(
        [
            ("t1", "S1", datetime(2025, 1, 1, 8, 0), 10.0),
            ("t2", "S1", datetime(2025, 1, 1, 8, 30), 20.0),
            ("t3", "S1", datetime(2025, 1, 1, 9, 30), 5.0),
            ("t4", "S2", datetime(2025, 1, 1, 8, 15), 7.0),
            ("t5", "S9", datetime(2025, 1, 1, 8, 20), 3.0),
        ],
        "transaction_id string, store_id string, txn_ts timestamp, total_amount double",
    )


def _stores(spark):
    return spark.createDataFrame(
        [("S1", "TX", "Murphy USA", "Store 1"), ("S2", "AR", "Murphy Express", "Store 2")],
        "store_id string, state string, brand string, store_name string",
    )


def test_broadcast_join_stores(spark):
    out = ex.broadcast_join_stores(_txns(spark), _stores(spark))
    assert set(out.columns) == {
        "transaction_id", "store_id", "txn_ts", "total_amount", "state", "brand",
    }
    assert out.count() == 5  # left join keeps unmatched rows
    rows = {r.transaction_id: r.state for r in out.collect()}
    assert rows["t1"] == "TX"
    assert rows["t5"] is None


def test_unmatched_transactions(spark):
    out = ex.unmatched_transactions(_txns(spark), _stores(spark))
    assert [r.transaction_id for r in out.collect()] == ["t5"]
    assert set(out.columns) == {"transaction_id", "store_id", "txn_ts", "total_amount"}


def test_running_sales(spark):
    out = ex.running_sales(_txns(spark))
    got = {r.transaction_id: r.running_total for r in out.collect()}
    assert got["t1"] == 10.0
    assert got["t2"] == 30.0
    assert got["t3"] == 35.0
    assert got["t4"] == 7.0  # S2 starts its own total


def test_add_prev_gap_minutes(spark):
    out = ex.add_prev_gap_minutes(_txns(spark))
    got = {r.transaction_id: r.prev_gap_min for r in out.collect()}
    assert got["t1"] is None
    assert got["t2"] == 30.0
    assert got["t3"] == 60.0
    assert got["t4"] is None


def test_latest_per_key(spark):
    df = spark.createDataFrame(
        [("a", 1, "old"), ("a", 2, "new"), ("b", 5, "only")],
        "id string, version int, note string",
    )
    out = ex.latest_per_key(df, "id", "version")
    assert out.columns == ["id", "version", "note"]
    assert sorted((r.id, r.note) for r in out.collect()) == [("a", "new"), ("b", "only")]
