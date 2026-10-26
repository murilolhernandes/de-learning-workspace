from conftest import load_exercise

star = load_exercise("04_modeling_quality", "ex01_star_schema")
rules = load_exercise("04_modeling_quality", "ex02_medallion_rules")


def test_table_kind():
    assert star.TABLE_KIND == {
        "transaction_items": "fact",
        "stores": "dimension",
        "loyalty_members": "dimension",
        "weather_daily": "fact",
    }


def test_column_role():
    assert star.COLUMN_ROLE == {
        "quantity": "measure",
        "price": "measure",
        "state": "attribute",
        "segment": "attribute",
        "category": "attribute",
    }


def test_grain_mentions_line_and_transaction():
    grain = (star.GRAIN or "").lower()
    assert "transaction" in grain
    assert "line" in grain or "item" in grain or "sku" in grain


def test_rule_layers():
    assert rules.RULE_LAYER == {
        "keeps rows exactly as received, including duplicates": "bronze",
        "removes duplicate transactions": "silver",
        "casts timestamp strings to timestamp type": "silver",
        "daily sales per store joined to weather": "gold",
        "adds _source_file lineage column": "bronze",
        "quarantines rows with unparseable timestamps": "silver",
    }
