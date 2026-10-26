TABLE_KIND = {
    "transaction_items": "fact",
    "stores": "dimension",
    "loyalty_members": "dimension",
    "weather_daily": "fact",
}

COLUMN_ROLE = {
    "quantity": "measure",
    "price": "measure",
    "state": "attribute",
    "segment": "attribute",
    "category": "attribute",
}

GRAIN = "One row of fact_transaction_item is one SKU line on one transaction."
