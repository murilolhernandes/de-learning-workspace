"""Exercise 1: model the retail data. Run:  pytest tests/test_w04_modeling.py"""

# Replace each None with "fact" or "dimension".
TABLE_KIND = {
    "transaction_items": "fact",
    "stores": "dimension",
    "loyalty_members": "dimension",
    "weather_daily": "fact",
}

# Replace None with "measure" or "attribute" (measures are summed, attributes are grouped by).
COLUMN_ROLE = {
    "quantity": "measure",
    "price": "measure",
    "state": "attribute",
    "segment": "attribute",
    "category": "attribute",
}

# TODO: finish the sentence in one short string: "One row of fact_transaction_item is ..."
GRAIN = "One row of fact_transaction_item is one SKU line on one transaction"
