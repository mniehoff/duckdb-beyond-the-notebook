COPY (
    SELECT
        PULocationID,
        count(*) AS trip_count,
        round(avg(passenger_count), 2) AS avg_passengers,
        round(avg(trip_distance), 4) AS avg_trip_distance_miles,
        round(avg(fare_amount), 4) AS avg_fare_amount,
        round(avg(tip_amount), 4) AS avg_tip_amount,
        round(avg(total_amount), 4) AS avg_total_amount,
        round(avg(round(fare_amount / trip_distance, 4)), 4) AS avg_fare_per_mile,
        mode(hour(tpep_pickup_datetime)) AS peak_pickup_hour,
        round(quantile_cont(fare_amount, 0.95), 4) AS p95_fare_amount
    FROM 'nyc_taxi_large.parquet'
    WHERE passenger_count > 0 AND trip_distance > 0 AND fare_amount > 0
    GROUP BY PULocationID
    ORDER BY trip_count DESC
) TO 'output/duckdb_p95.parquet' (FORMAT parquet);
