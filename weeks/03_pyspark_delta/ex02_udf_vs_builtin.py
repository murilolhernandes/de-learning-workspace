"""Exercise 2: replace a Python UDF with built-in functions. Run:  pytest tests/test_w03_udf.py"""

from pyspark.sql import DataFrame
from pyspark.sql import functions as F
from pyspark.sql.types import StringType


def _basket_label(item_count):
    if item_count is None:
        return "unknown"
    if item_count <= 2:
        return "small"
    if item_count <= 6:
        return "medium"
    return "large"


# Reference implementation: a Python UDF. Works, but slow (rows leave the JVM).
basket_label_udf = F.udf(_basket_label, StringType())


def with_label_udf(df: DataFrame) -> DataFrame:
    return df.withColumn("basket", basket_label_udf("item_count"))


def with_label_builtin(df: DataFrame) -> DataFrame:
    """Same result as with_label_udf, using only built-in column functions."""
    # TODO: hint: F.when(...).when(...).otherwise(...), and handle null first
    raise NotImplementedError


# Replace None with True or False.
UDF_FACTS = {
    "python_udfs_are_opaque_to_the_catalyst_optimizer": None,
    "python_udfs_move_rows_between_the_jvm_and_python": None,
    "built_in_functions_can_be_optimized_by_spark": None,
    "a_udf_is_the_best_first_choice_for_simple_conditions": None,
}
