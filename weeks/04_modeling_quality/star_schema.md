# Star schema for the retail data

```
dim_store ──┐
dim_date ───┤
dim_product ┼── fact_transaction_item (grain: one SKU line on one transaction)
dim_loyalty ┘
```

| Table | Kind | Key | Notes |
|---|---|---|---|
| `fact_transaction_item` | fact | `transaction_id` + `line_no` | quantity, price, line_total |
| `dim_store` | dimension | `store_id` | state, brand, opened date |
| `dim_loyalty` | dimension | `loyalty_id` | join date, segment; unknown member row for null ids |
| `dim_product` | dimension | `sku` | category |
| `dim_date` | dimension | `date` | day of week, month, holiday flag |
| `fact_weather_daily` | fact | `region` + `date` | temperature, precipitation |

Design choices to be ready to explain:
- Null loyalty ids map to an "unknown" member row, so inner joins do not silently drop sales.
- Fuel gallons live at transaction grain, not item grain. Either a separate `fact_fuel_sale` or a documented nullable measure.
- Weather joins to sales through store region and date, never directly to a transaction.
