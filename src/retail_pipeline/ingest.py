"""Bronze layer: load raw files as-is, add ingestion metadata (Weeks 7-8)."""


def ingest_transactions(spark, raw_dir, bronze_path):
    # TODO: read transactions_*.csv with an explicit schema, add _ingested_at and
    # _source_file columns, append to a Delta table at bronze_path.
    raise NotImplementedError
