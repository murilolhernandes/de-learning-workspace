# Bronze / silver / gold rules

| Layer | Rule |
|---|---|
| Bronze | Append raw data as it arrived, plus `_ingested_at` and `_source_file`. No fixes, no dedup. Schema evolution allowed. |
| Silver | Typed, deduplicated, validated. Bad rows go to a quarantine table, not the bin. Business keys are unique. |
| Gold | Aggregated or modeled for one consumer (BI, forecasting). Built only from silver. Documented grain. |

Cross-layer rules:
1. Data flows one way: bronze to silver to gold. Never read gold to build silver.
2. Every layer must be rebuildable from the one before it.
3. Quality checks run at the silver boundary and fail the job on breach.
4. Gold tables never contain a column nobody asked for.
