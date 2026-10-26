"""Local SparkSession with Delta Lake configured. Nothing here talks to a cloud."""

import glob
import os
import sys

from delta import configure_spark_with_delta_pip
from pyspark.sql import SparkSession


def _use_java_17_if_present() -> None:
    """Spark 3.5 supports Java 8/11/17. Prefer a Java 17 install over a newer default."""
    for pattern in (r"C:\Program Files\Microsoft\jdk-17*", r"C:\Program Files\Java\jdk-17*"):
        found = sorted(glob.glob(pattern))
        if found:
            os.environ["JAVA_HOME"] = found[-1]
            return


def get_spark(app_name: str = "retail-pipeline", shuffle_partitions: int = 8) -> SparkSession:
    """Return a local SparkSession with Delta enabled.

    The first call downloads the Delta jars once (cached afterwards).
    """
    _use_java_17_if_present()
    os.environ.setdefault("PYSPARK_PYTHON", sys.executable)
    os.environ.setdefault("PYSPARK_DRIVER_PYTHON", sys.executable)

    builder = (
        SparkSession.builder.master("local[*]")
        .appName(app_name)
        .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
        .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")
        .config("spark.sql.shuffle.partitions", str(shuffle_partitions))
        .config("spark.ui.showConsoleProgress", "false")
    )
    return configure_spark_with_delta_pip(builder).getOrCreate()
