"""Data quality checks (Week 4)."""


def null_rate(df, column):
    # TODO: fraction of rows where column is null.
    raise NotImplementedError


def duplicate_count(df, key_columns):
    # TODO: number of rows that share a key with another row.
    raise NotImplementedError


def orphan_count(child_df, parent_df, key):
    # TODO: child rows whose key has no match in parent (referential integrity).
    raise NotImplementedError
