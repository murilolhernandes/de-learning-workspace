from conftest import load_exercise

ex = load_exercise("01_interview_sprint", "ex02_delta_basics")


def test_write_read_roundtrip(spark, tmp_path):
    path = str(tmp_path / "t")
    ex.write_delta(spark.createDataFrame([(1, "a"), (2, "b")], ["id", "v"]), path)
    assert ex.read_delta(spark, path).count() == 2


def test_write_overwrites(spark, tmp_path):
    path = str(tmp_path / "t")
    ex.write_delta(spark.createDataFrame([(1,), (2,)], ["id"]), path)
    ex.write_delta(spark.createDataFrame([(9,)], ["id"]), path)
    assert [r.id for r in ex.read_delta(spark, path).collect()] == [9]


def test_append(spark, tmp_path):
    path = str(tmp_path / "t")
    ex.write_delta(spark.createDataFrame([(1,)], ["id"]), path)
    ex.append_delta(spark.createDataFrame([(2,)], ["id"]), path)
    assert ex.read_delta(spark, path).count() == 2


def test_history_and_time_travel(spark, tmp_path):
    path = str(tmp_path / "t")
    ex.write_delta(spark.createDataFrame([(1,)], ["id"]), path)
    ex.append_delta(spark.createDataFrame([(2,)], ["id"]), path)
    ex.append_delta(spark.createDataFrame([(3,)], ["id"]), path)
    assert ex.version_count(spark, path) == 3
    assert ex.read_version(spark, path, 0).count() == 1
    assert ex.read_version(spark, path, 1).count() == 2
