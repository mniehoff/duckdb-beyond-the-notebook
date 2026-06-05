"""Serverless function simulation: DuckDB behind a REST API."""

from pathlib import Path

import duckdb
from fastapi import FastAPI, Query
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

DATA_FILE = Path(__file__).parent / "nyc_taxi_sample.parquet"


@app.get("/query")
def query_taxi(passengers: int = Query(0), min_fare: int = Query(10)):
    where = f"WHERE fare_amount >= {min_fare}"
    if passengers > 0:
        where += f" AND passenger_count = {passengers}"

    sql = f"""
        SELECT
            PULocationID AS pickup_location,
            COUNT(*) AS trips,
            ROUND(AVG(trip_distance), 2) AS avg_distance_mi,
            ROUND(AVG(fare_amount), 2) AS avg_fare_usd
        FROM '{DATA_FILE}'
        {where}
        GROUP BY PULocationID
        ORDER BY trips DESC
        LIMIT 20
    """
    result = duckdb.sql(sql)
    cols = [desc[0] for desc in result.description]
    rows = [dict(zip(cols, row)) for row in result.fetchall()]
    return {"sql": sql.strip(), "cols": cols, "rows": rows}


@app.get("/")
def index():
    return FileResponse(Path(__file__).parent / "index.html")
