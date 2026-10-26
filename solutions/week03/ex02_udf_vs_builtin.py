"""Solution for Week 3, exercise 2."""

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


basket_label_udf = F.udf(_basket_label, StringType())


def with_label_udf(df: DataFrame) -> DataFrame:
    return df.withColumn("basket", basket_label_udf("item_count"))


def with_label_builtin(df: DataFrame) -> DataFrame:
    c = F.col("item_count")
    return df.withColumn(
        "basket",
        F.when(c.isNull(), "unknown")
        .when(c <= 2, "small")
        .when(c <= 6, "medium")
        .otherwise("large"),
    )


UDF_FACTS = {
    "python_udfs_are_opaque_to_the_catalyst_optimizer": True,
    "python_udfs_move_rows_between_the_jvm_and_python": True,
    "built_in_functions_can_be_optimized_by_spark": True,
    "a_udf_is_the_best_first_choice_for_simple_conditions": False,
}
