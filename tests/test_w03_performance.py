from conftest import load_exercise

ex = load_exercise("03_pyspark_delta", "ex01_performance")


def _txns(spark):
    return spark.createDataFrame(
        [("S1", 10.0), ("S1", 5.0), ("S2", 7.5), ("S3", 1.0)], "store_id string, total double"
    )


def test_wide_vs_narrow():
    assert ex.WIDE_VS_NARROW == {
        "filter": "narrow",
        "withColumn": "narrow",
        "groupBy.agg": "wide",
        "join_two_large_tables": "wide",
        "select": "narrow",
        "orderBy": "wide",
    }


def test_repartition_by_store(spark):
    out = ex.repartition_by_store(_txns(spark), 3)
    assert out.rdd.getNumPartitions() == 3
    assert out.count() == 4


def test_reduce_partitions(spark):
    df = _txns(spark).repartition(4)
    out = ex.reduce_partitions(df, 2)
    assert out.rdd.getNumPartitions() == 2
    assert out.count() == 4


def test_cache_and_count(spark):
    df = _txns(spark).filter("total > 0")
    assert ex.cache_and_count(df) == 4
    assert df.is_cached
    df.unpersist()


def test_join_with_broadcast(spark):
    small = spark.createDataFrame([("S1", "TX"), ("S2", "AR")], "store_id string, state string")
    out = ex.join_with_broadcast(_txns(spark), small, "store_id")
    assert out.count() == 3
    assert "broadcast" in out._jdf.queryExecution().analyzed().toString().lower()
