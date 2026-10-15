"""Serverless function simulation: DuckDB behind a REST API."""

from pathlib import Path

import duckdb
from fastapi import FastAPI, Query
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

DATA_FILE = Path(__file__).parent / "nyc_taxi_sample.parquet"

# Stretch task: one shared connection; every request works on its own cursor.
# duckdb.sql() uses a hidden global default connection, which is shared state
# that cannot be configured or closed explicitly. A cursor() is a lightweight
# child connection to the same database: it is safe to use from FastAPI's
# worker threads, gets its own transaction/prepared-statement state, and the
# parquet metadata and buffer cache stay warm in the single parent connection.
con = duckdb.connect()


def build_where(passengers: int, min_fare: float, max_distance: float | None):
    """Return a WHERE clause with `?` placeholders and the matching parameters."""
    clauses = ["fare_amount >= ?"]
    params: list = [min_fare]
    if passengers > 0:
        clauses.append("passenger_count = ?")
        params.append(passengers)
    if max_distance is not None:
        clauses.append("trip_distance <= ?")
        params.append(max_distance)
    return "WHERE " + " AND ".join(clauses), params


def run(sql: str, params: list):
    cur = con.cursor()
    try:
        cur.execute(sql, params)
        cols = [desc[0] for desc in cur.description]
        rows = [dict(zip(cols, row)) for row in cur.fetchall()]
    finally:
        cur.close()
    return {"sql": sql.strip(), "params": params, "cols": cols, "rows": rows}


@app.get("/query")
def query_taxi(
    passengers: int = Query(0),
    min_fare: float = Query(10),
    max_distance: float | None = Query(None, ge=0),
):
    where, params = build_where(passengers, min_fare, max_distance)
    sql = f"""
        SELECT
            PULocationID AS pickup_location,
            COUNT(*) AS trips,
            ROUND(AVG(trip_distance), 2) AS avg_distance_mi,
            ROUND(AVG(fare_amount), 2) AS avg_fare_usd
        FROM read_parquet(?)
        {where}
        GROUP BY PULocationID
        ORDER BY trips DESC
        LIMIT 20
    """
    return run(sql, [str(DATA_FILE), *params])


@app.get("/hourly")
def hourly(
    passengers: int = Query(0),
    min_fare: float = Query(0),
    max_distance: float | None = Query(None, ge=0),
):
    where, params = build_where(passengers, min_fare, max_distance)
    sql = f"""
        SELECT
            hour(tpep_pickup_datetime) AS pickup_hour,
            COUNT(*) AS trips,
            ROUND(AVG(fare_amount), 2) AS avg_fare_usd
        FROM read_parquet(?)
        {where}
        GROUP BY pickup_hour
        ORDER BY pickup_hour
    """
    return run(sql, [str(DATA_FILE), *params])


@app.get("/")
def index():
    return FileResponse(Path(__file__).parent / "index.html")
