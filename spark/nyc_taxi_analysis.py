import time
from datetime import datetime
from pathlib import Path

from sqlframe import activate
activate(engine="duckdb")

from pyspark.sql import SparkSession
from pyspark.sql import functions as F

SCRIPT_DIR = Path(__file__).parent.resolve()
SOURCE = str(SCRIPT_DIR / "nyc_taxi_large.parquet")
OUTPUT_BASE = SCRIPT_DIR / "output"


def main() -> None:
    start = time.perf_counter()
    run_ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    output = str(OUTPUT_BASE / f"{run_ts}.parquet")

    spark = (
        SparkSession.builder.appName("NYC Taxi Analysis")
        .master("local[*]")
        .config("spark.sql.shuffle.partitions", "4")
        .getOrCreate()
    )
    after_session = time.perf_counter()

    # ── Load ──────────────────────────────────────────────────────────────────
    df = spark.read.parquet(SOURCE)
    print(f"Loaded {df.count():,} rows from {SOURCE}")

    # ── Transform ─────────────────────────────────────────────────────────────
    df = df.filter(
        (F.col("passenger_count") > 0)
        & (F.col("trip_distance") > 0)
        & (F.col("fare_amount") > 0)
    )

    df = df.withColumn(
        "fare_per_mile", F.round(F.col("fare_amount") / F.col("trip_distance"), 4)
    ).withColumn(
        "pickup_hour", F.hour(F.col("tpep_pickup_datetime"))
    )

    # ── Aggregate ─────────────────────────────────────────────────────────────
    result = (
        df.groupBy("PULocationID")
        .agg(
            F.count("*").alias("trip_count"),
            F.round(F.avg("passenger_count"), 2).alias("avg_passengers"),
            F.round(F.avg("trip_distance"), 4).alias("avg_trip_distance_miles"),
            F.round(F.avg("fare_amount"), 4).alias("avg_fare_amount"),
            F.round(F.avg("tip_amount"), 4).alias("avg_tip_amount"),
            F.round(F.avg("total_amount"), 4).alias("avg_total_amount"),
            F.round(F.avg("fare_per_mile"), 4).alias("avg_fare_per_mile"),
            F.mode("pickup_hour").alias("peak_pickup_hour"),
        )
        .orderBy(F.col("trip_count").desc())
    ).cache()

    # ── Write ─────────────────────────────────────────────────────────────────
    result.write.mode("overwrite").parquet(output)
    print(f"Written {result.count():,} zones to {output}")

    spark.stop()

    end = time.perf_counter()
    print(f"Query + write time:   {end - after_session:.2f}s")
    print(f"Total execution time: {end - start:.2f}s")


if __name__ == "__main__":
    main()
