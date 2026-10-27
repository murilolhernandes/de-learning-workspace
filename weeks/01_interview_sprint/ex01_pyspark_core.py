"""Exercise 1: PySpark core. Replace every TODO, then run:  pytest tests/test_w01_pyspark_core.py

Columns in the transactions CSV (see data/generate_data.py):
  transaction_id, store_id, txn_ts, loyalty_id, fuel_gallons, item_count, total_amount
"""

from pyspark.sql import DataFrame, SparkSession
from pyspark.sql.types import StructType, StructField, StringType, DoubleType, IntegerType


def transactions_schema() -> StructType:
    """Return an explicit schema: ids and txn_ts as strings, fuel_gallons and total_amount as
    doubles, item_count as an integer. Every field nullable."""
    return StructType([StructField("transaction_id", StringType(), True),
                          StructField("store_id", StringType(), True),
                          StructField("txn_ts", StringType(), True),
                          StructField("loyalty_id", StringType(), True),
                          StructField("fuel_gallons", DoubleType(), True),
                          StructField("item_count", IntegerType(), True),
                          StructField("total_amount", DoubleType(), True)])


def read_transactions(spark: SparkSession, path: str) -> DataFrame:
    """Read a transactions CSV that has a header row, using transactions_schema()."""
    # TODO: spark.read ... .csv(path)
    raise NotImplementedError


def large_baskets(df: DataFrame, min_total: float) -> DataFrame:
    """Keep rows whose total_amount is at least min_total."""
    # TODO: filter
    raise NotImplementedError


def add_basket_size(df: DataFrame) -> DataFrame:
    """Add a string column basket_size: 'large' when total_amount >= 50, otherwise 'small'."""
    # TODO: withColumn + when/otherwise
    raise NotImplementedError


def sales_by_store(df: DataFrame) -> DataFrame:
    """One row per store_id with txn_count (number of rows) and revenue (sum of total_amount)."""
    # TODO: groupBy + agg
    raise NotImplementedError


def join_store_state(sales: DataFrame, stores: DataFrame) -> DataFrame:
    """Add the store's `state` to the sales rows. Keep only stores present in both."""
    # TODO: join on store_id (inner)
    raise NotImplementedError


def rank_within_state(df: DataFrame) -> DataFrame:
    """Add state_rank: 1 for the highest revenue in each state, 2 for the next, and so on.
    Ties share a rank and the next rank is NOT skipped."""
    # TODO: Window.partitionBy(...).orderBy(...) + dense_rank
    raise NotImplementedError


# Fill each value with "transformation" or "action". Spark is lazy: which of these actually
# trigger work?
TRANSFORMATIONS_VS_ACTIONS = {
    "filter": None,
    "count": None,
    "groupBy": None,
    "show": None,
    "withColumn": None,
    "collect": None,
    "join": None,
}
