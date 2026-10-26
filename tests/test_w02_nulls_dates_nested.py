from datetime import date, datetime

from conftest import load_exercise

ex = load_exercise("02_pyspark_delta", "ex02_nulls_dates_nested")


def test_fill_loyalty(spark):
    df = spark.createDataFrame([("t1", "L1"), ("t2", None)], "transaction_id string, loyalty_id string")
    got = {r.transaction_id: (r.loyalty_id, r.is_member) for r in ex.fill_loyalty(df).collect()}
    assert got == {"t1": ("L1", True), "t2": ("GUEST", False)}


def test_parse_timestamps(spark):
    df = spark.createDataFrame(
        [("t1", "2025-01-02 03:04:05"), ("t2", "not a date")], "transaction_id string, txn_ts string"
    )
    got = {r.transaction_id: r.txn_ts for r in ex.parse_timestamps(df).collect()}
    assert got["t1"] == datetime(2025, 1, 2, 3, 4, 5)
    assert got["t2"] is None
    assert dict(ex.parse_timestamps(df).dtypes)["txn_ts"] == "timestamp"


def test_add_date_parts(spark):
    # 2025-01-05 is a Sunday
    df = spark.createDataFrame([(datetime(2025, 1, 5, 14, 30),)], "txn_ts timestamp")
    row = ex.add_date_parts(df).collect()[0]
    assert row.txn_date == date(2025, 1, 5)
    assert row.txn_hour == 14
    assert row.day_of_week == 1


def test_add_store_age_years(spark):
    df = spark.createDataFrame(
        [("S1", date(2015, 6, 15)), ("S2", date(2024, 12, 31))], "store_id string, opened_date date"
    )
    got = {r.store_id: r.age_years for r in ex.add_store_age_years(df, "2025-06-14").collect()}
    assert got == {"S1": 9, "S2": 0}


def test_skus_per_txn(spark):
    df = spark.createDataFrame(
        [("t1", "A"), ("t1", "B"), ("t2", "C")], "transaction_id string, sku string"
    )
    got = {r.transaction_id: (sorted(r.skus), r.sku_count) for r in ex.skus_per_txn(df).collect()}
    assert got == {"t1": (["A", "B"], 2), "t2": (["C"], 1)}


def test_explode_skus(spark):
    df = spark.createDataFrame(
        [("t1", ["A", "B"]), ("t2", []), ("t3", None)], "transaction_id string, skus array<string>"
    )
    out = ex.explode_skus(df)
    assert "skus" not in out.columns
    assert sorted((r.transaction_id, r.sku) for r in out.collect()) == [("t1", "A"), ("t1", "B")]


def test_pack_amounts(spark):
    df = spark.createDataFrame([("t1", 3.5, 20.0)], "transaction_id string, fuel_gallons double, total_amount double")
    out = ex.pack_amounts(df)
    assert {"fuel_gallons", "total_amount", "amounts"} <= set(out.columns)
    row = out.select("amounts.fuel_gallons", "amounts.total_amount").collect()[0]
    assert (row[0], row[1]) == (3.5, 20.0)
