from conftest import load_exercise

ex = load_exercise("03_pyspark_delta", "ex02_udf_vs_builtin")


def test_builtin_matches_udf(spark):
    df = spark.createDataFrame(
        [(1, 0), (2, 2), (3, 3), (4, 6), (5, 7), (6, None)],
        "id int, item_count int",
    )
    expected = {r.id: r.basket for r in ex.with_label_udf(df).collect()}
    got = {r.id: r.basket for r in ex.with_label_builtin(df).collect()}
    assert got == expected
    assert got[6] == "unknown"
    assert got[3] == "medium"


def test_builtin_has_no_python_udf(spark):
    df = spark.createDataFrame([(1, 1)], "id int, item_count int")
    plan = ex.with_label_builtin(df)._jdf.queryExecution().analyzed().toString()
    assert "pythonudf" not in plan.lower()


def test_udf_facts():
    assert ex.UDF_FACTS == {
        "python_udfs_are_opaque_to_the_catalyst_optimizer": True,
        "python_udfs_move_rows_between_the_jvm_and_python": True,
        "built_in_functions_can_be_optimized_by_spark": True,
        "a_udf_is_the_best_first_choice_for_simple_conditions": False,
    }
