import pytest
from pyspark.sql import Row
from pyspark.sql.types import DoubleType, IntegerType, StringType

from conftest import load_exercise

ex = load_exercise("01_interview_sprint", "ex01_pyspark_core")


@pytest.fixture
def txns(spark):
    return spark.createDataFrame(
        [
            Row(transaction_id="T1", store_id="A", total_amount=80.0),
            Row(transaction_id="T2", store_id="A", total_amount=20.0),
            Row(transaction_id="T3", store_id="B", total_amount=50.0),
            Row(transaction_id="T4", store_id="C", total_amount=10.0),
        ]
    )


def test_schema_types_and_nullability():
    fields = {f.name: f for f in ex.transactions_schema().fields}
    assert set(fields) == {
        "transaction_id", "store_id", "txn_ts", "loyalty_id",
        "fuel_gallons", "item_count", "total_amount",
    }
    assert isinstance(fields["txn_ts"].dataType, StringType)
    assert isinstance(fields["fuel_gallons"].dataType, DoubleType)
    assert isinstance(fields["total_amount"].dataType, DoubleType)
    assert isinstance(fields["item_count"].dataType, IntegerType)
    assert all(f.nullable for f in fields.values())


def test_read_transactions(spark, tmp_path):
    p = tmp_path / "t.csv"
    p.write_text(
        "transaction_id,store_id,txn_ts,loyalty_id,fuel_gallons,item_count,total_amount\n"
        "T1,S001,2025-01-01 10:00:00,,5.5,2,30.25\n"
    )
    df = ex.read_transactions(spark, str(p))
    assert df.schema == ex.transactions_schema()
    row = df.collect()[0]
    assert row.loyalty_id is None and row.item_count == 2 and row.total_amount == 30.25


def test_large_baskets(txns):
    ids = {r.transaction_id for r in ex.large_baskets(txns, 50.0).collect()}
    assert ids == {"T1", "T3"}


def test_add_basket_size(txns):
    got = {r.transaction_id: r.basket_size for r in ex.add_basket_size(txns).collect()}
    assert got == {"T1": "large", "T2": "small", "T3": "large", "T4": "small"}


def test_sales_by_store(txns):
    got = {r.store_id: (r.txn_count, r.revenue) for r in ex.sales_by_store(txns).collect()}
    assert got == {"A": (2, 100.0), "B": (1, 50.0), "C": (1, 10.0)}


def test_join_store_state(spark, txns):
    sales = ex.sales_by_store(txns)
    stores = spark.createDataFrame([("A", "TX"), ("B", "AR"), ("Z", "LA")], ["store_id", "state"])
    got = {r.store_id: r.state for r in ex.join_store_state(sales, stores).collect()}
    assert got == {"A": "TX", "B": "AR"}


def test_rank_within_state(spark):
    df = spark.createDataFrame(
        [("A", "TX", 100.0), ("B", "TX", 100.0), ("C", "TX", 50.0), ("D", "AR", 10.0)],
        ["store_id", "state", "revenue"],
    )
    got = {r.store_id: r.state_rank for r in ex.rank_within_state(df).collect()}
    assert got == {"A": 1, "B": 1, "C": 2, "D": 1}


def test_transformations_vs_actions():
    assert ex.TRANSFORMATIONS_VS_ACTIONS == {
        "filter": "transformation",
        "count": "action",
        "groupBy": "transformation",
        "show": "action",
        "withColumn": "transformation",
        "collect": "action",
        "join": "transformation",
    }
