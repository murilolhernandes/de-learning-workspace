"""Generate reproducible, deliberately messy retail data for a fuel-and-convenience chain.

Usage:  python data/generate_data.py [--out data/raw] [--rows-per-month 50000] [--seed 42]

Output (all under --out):
  stores.csv, loyalty_members.csv, weather_daily.csv
  transactions_2025_01.csv ... transactions_2025_06.csv
  transactions_2025_03_late.csv     late-arriving file: March sales that showed up in April
  transaction_items_2025_MM.jsonl   one JSON object per line item

Planted problems (find them, then handle them in silver):
  - ~1% duplicate transaction rows
  - ~60% null loyalty_id (customers who did not scan a card)
  - ~0.5% unparseable timestamps
  - a late-arriving file for March
  - the June file has a new column, payment_method (schema evolution)
"""

import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd

MONTHS = [1, 2, 3, 4, 5, 6]
YEAR = 2025
STATES = {
    "AR": "South", "LA": "South", "MS": "South", "AL": "South",
    "TX": "West", "OK": "West", "TN": "East", "KY": "East", "GA": "East", "FL": "East",
}
BRANDS = ["Murphy USA", "Murphy Express"]
CATEGORIES = {
    "beverage": (1.2, 3.5), "snack": (0.9, 4.0), "tobacco": (6.0, 12.0),
    "candy": (0.8, 2.5), "grocery": (2.0, 9.0), "car_care": (4.0, 25.0),
}
SKUS_PER_CATEGORY = 15


def make_stores(rng, n=50):
    states = rng.choice(list(STATES), n)
    opened = pd.to_datetime("1998-01-01") + pd.to_timedelta(rng.integers(0, 9500, n), unit="D")
    return pd.DataFrame({
        "store_id": [f"S{i:03d}" for i in range(1, n + 1)],
        "store_name": [f"Store {i}" for i in range(1, n + 1)],
        "state": states,
        "region": [STATES[s] for s in states],
        "brand": rng.choice(BRANDS, n, p=[0.6, 0.4]),
        "opened_date": opened.strftime("%Y-%m-%d"),
    })


def make_loyalty(rng, n=20000):
    joined = pd.to_datetime("2022-01-01") + pd.to_timedelta(rng.integers(0, 1300, n), unit="D")
    return pd.DataFrame({
        "loyalty_id": [f"L{i:06d}" for i in range(1, n + 1)],
        "join_date": joined.strftime("%Y-%m-%d"),
        "segment": rng.choice(["fuel_only", "in_store", "both", "occasional"], n,
                              p=[0.25, 0.2, 0.35, 0.2]),
    })


def make_weather(rng):
    days = pd.date_range(f"{YEAR}-01-01", f"{YEAR}-06-30")
    rows = []
    for region in sorted(set(STATES.values())):
        base = {"South": 62, "West": 58, "East": 52}[region]
        season = 18 * np.sin((days.dayofyear.values - 80) / 365 * 2 * np.pi)
        temp = base + season + rng.normal(0, 5, len(days))
        precip = np.where(rng.random(len(days)) < 0.28, rng.gamma(1.5, 0.25, len(days)), 0.0)
        rows.append(pd.DataFrame({
            "region": region, "date": days.strftime("%Y-%m-%d"),
            "temp_f": temp.round(1), "precip_in": precip.round(2),
        }))
    return pd.concat(rows, ignore_index=True)


def make_month(rng, month, stores, loyalty, rows, start_id):
    """Return (transactions, items) for one month, without any mess applied yet."""
    start = pd.Timestamp(YEAR, month, 1)
    seconds = int((start + pd.offsets.MonthBegin(1) - start).total_seconds())
    ts = start + pd.to_timedelta(rng.integers(0, seconds, rows), unit="s")
    ids = [f"T{i:08d}" for i in range(start_id, start_id + rows)]
    has_fuel = rng.random(rows) < 0.7
    gallons = np.where(has_fuel, rng.gamma(6.0, 1.9, rows).round(2), 0.0)
    item_count = rng.choice([0, 1, 2, 3, 4, 5], rows, p=[0.2, 0.25, 0.25, 0.15, 0.1, 0.05])
    item_count = np.where((item_count == 0) & ~has_fuel, 1, item_count)

    # Items: one row per line item.
    owner = np.repeat(np.arange(rows), item_count)
    cats = rng.choice(list(CATEGORIES), len(owner))
    prices = np.array([rng.uniform(*CATEGORIES[c]) for c in cats]).round(2)
    skus = [f"{c[:3].upper()}-{rng.integers(1, SKUS_PER_CATEGORY + 1):03d}" for c in cats]
    qty = rng.choice([1, 1, 1, 2, 3], len(owner))
    items = pd.DataFrame({
        "transaction_id": np.array(ids)[owner], "sku": skus, "category": cats,
        "quantity": qty, "price": prices,
    })

    item_total = (items["quantity"] * items["price"]).groupby(owner).sum().reindex(
        range(rows), fill_value=0.0).values
    fuel_price = 3.05 + rng.normal(0, 0.08, rows)
    total = (item_total + gallons * fuel_price).round(2)

    loyalty_ids = np.where(rng.random(rows) < 0.4, rng.choice(loyalty["loyalty_id"], rows), None)
    txns = pd.DataFrame({
        "transaction_id": ids,
        "store_id": rng.choice(stores["store_id"], rows),
        "txn_ts": ts.strftime("%Y-%m-%d %H:%M:%S"),
        "loyalty_id": loyalty_ids,
        "fuel_gallons": gallons,
        "item_count": item_count,
        "total_amount": total,
    })
    return txns, items


def add_mess(rng, txns):
    """Duplicates and unparseable timestamps."""
    txns = txns.copy()
    bad = rng.random(len(txns)) < 0.005
    txns.loc[bad, "txn_ts"] = rng.choice(["not-a-date", "2025-13-45 99:00:00", ""], bad.sum())
    dupes = txns.sample(frac=0.01, random_state=int(rng.integers(0, 10**6)))
    return pd.concat([txns, dupes], ignore_index=True).sample(frac=1, random_state=1)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=str(Path(__file__).parent / "raw"))
    ap.add_argument("--rows-per-month", type=int, default=50000)
    ap.add_argument("--seed", type=int, default=42)
    args = ap.parse_args()

    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    rng = np.random.default_rng(args.seed)

    stores, loyalty = make_stores(rng), make_loyalty(rng)
    stores.to_csv(out / "stores.csv", index=False)
    loyalty.to_csv(out / "loyalty_members.csv", index=False)
    make_weather(rng).to_csv(out / "weather_daily.csv", index=False)

    next_id = 1
    for m in MONTHS:
        txns, items = make_month(rng, m, stores, loyalty, args.rows_per_month, next_id)
        next_id += args.rows_per_month

        if m == 3:  # about 3% of March arrives late, in its own file
            late_mask = rng.random(len(txns)) < 0.03
            add_mess(rng, txns[late_mask]).to_csv(out / "transactions_2025_03_late.csv", index=False)
            txns = txns[~late_mask]

        txns = add_mess(rng, txns)
        if m == 6:  # schema evolution: a new column appears
            txns["payment_method"] = rng.choice(["card", "cash", "mobile"], len(txns),
                                                p=[0.7, 0.2, 0.1])
        txns.to_csv(out / f"transactions_{YEAR}_{m:02d}.csv", index=False)

        with open(out / f"transaction_items_{YEAR}_{m:02d}.jsonl", "w", encoding="utf-8") as f:
            for rec in items.to_dict("records"):
                rec["quantity"], rec["price"] = int(rec["quantity"]), float(rec["price"])
                f.write(json.dumps(rec) + "\n")
        print(f"month {m:02d}: {len(txns):,} transaction rows, {len(items):,} items")

    print(f"Done. Files written to {out}")


if __name__ == "__main__":
    main()
