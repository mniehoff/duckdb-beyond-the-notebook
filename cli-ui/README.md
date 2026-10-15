# CLI/UI Examples

Example queries to run in the UI or CLI

## Start UI

Run the command in the cli-ui directory!

```
duckdb --ui
```

On Windows ARM64 the UI is not supported. Use the cli (just `duckdb`) instead

## Tasks

Read the files in `data/csv`.
- Run `sniff_csv` on `events.csv`
- Load `faulty_folks.csv` with `store_rejects = true`. Find the bad row in `reject_errors`. 
- Read `inventory.csv` (broken quoting, ragged rows) with `strict_mode = false` and `null_padding = true`
- Combine `report_jan.csv` and `report_feb.csv` with `union_by_name`
- **Stretch**: `COPY` the combined result to Parquet and read it back.

Docs for CSVs: https://duckdb.org/docs/current/data/csv/overview
Parquet Export: https://duckdb.org/docs/current/guides/file_formats/parquet_export