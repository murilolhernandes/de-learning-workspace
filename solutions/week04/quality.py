"""Data quality checks (Week 4) - solution."""

from pyspark.sql import functions as F


def null_rate(df, column):
    total = df.count()
    if total == 0:
        return 0.0
    return df.filter(F.col(column).isNull()).count() / total


def duplicate_count(df, key_columns):
    dupes = df.groupBy(*key_columns).count().filter(F.col("count") > 1)
    return dupes.agg(F.coalesce(F.sum("count"), F.lit(0))).first()[0]


def orphan_count(child_df, parent_df, key):
    child = child_df.filter(F.col(key).isNotNull())
    return child.join(parent_df.select(key).distinct(), on=key, how="left_anti").count()
