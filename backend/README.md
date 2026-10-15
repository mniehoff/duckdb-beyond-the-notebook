## Tasks

- Run `uv run fastapi dev main.py` and use the UI at `localhost:8000`.
- Read `main.py` and find the SQL injection risk in the f-string `WHERE`. Fix it with prepared parameters: `duckdb.execute(sql, [min_fare])`.
- Add a new endpoint `/hourly` that returns trips and average fare per pickup hour.
- Add a `max_distance` filter parameter.
- Stretch: keep one connection with `duckdb.connect()` and a `cursor()` per request, instead of the global `duckdb.sql`. Discuss why.