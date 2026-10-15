# Tasks

- Run `uv run nyc_taxi_analysis.py` and note the timings.
- Comment out the two sqlframe lines (`from sqlframe import activate` / `activate(engine="duckdb")`) and run again.
- Compare the output Parquet files, using DuckDB to diff the results.
- Add one aggregation to the script, for example the 95th percentile of `fare_amount` per zone, or tips by `pickup_hour`. Check that it works on both engines.
- Stretch: rewrite the pipeline as one DuckDB SQL statement (`COPY (SELECT ...) TO ...`) and compare the line count and runtime.