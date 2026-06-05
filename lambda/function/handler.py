"""
Lambda handler: triggered by S3 CSV upload.
Reads CSV with DuckDB, transforms, writes Parquet to S3.
"""

import os
from datetime import datetime

import duckdb


OUTPUT_BUCKET = os.environ["OUTPUT_BUCKET"]
OUTPUT_PREFIX = os.environ.get("OUTPUT_PREFIX", "warehouse/transformed")


def handler(event, context):
    """Lambda entry point — triggered by S3 PutObject."""
    records = event.get("Records", [])
    if not records:
        return {"statusCode": 200, "body": "No records"}

    con = duckdb.connect()
    con.execute("SET home_directory='/tmp'")
    con.execute("INSTALL httpfs; LOAD httpfs;")

    processed = 0
    for record in records:
        bucket = record["s3"]["bucket"]["name"]
        key = record["s3"]["object"]["key"]

        if not key.endswith(".csv"):
            continue

        s3_input = f"s3://{bucket}/{key}"
        filename = os.path.splitext(os.path.basename(key))[0]
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        s3_output = f"s3://{OUTPUT_BUCKET}/{OUTPUT_PREFIX}/{filename}_{timestamp}.parquet"

        print(f"Processing {s3_input} -> {s3_output}")

        con.execute(f"""
            COPY (
                SELECT
                    row_number() OVER () AS id,
                    LOWER(TRIM(name)) AS name,
                    CAST(value AS DOUBLE) AS value,
                    LOWER(TRIM(category)) AS category,
                    now() AS ingested_at,
                    '{key}' AS source_file
                FROM read_csv_auto('{s3_input}', header=true)
            ) TO '{s3_output}' (FORMAT PARQUET);
        """)

        count = con.execute(f"SELECT count(*) FROM read_parquet('{s3_output}')").fetchone()[0]
        processed += count
        print(f"Wrote {count} rows to {s3_output}")

    con.close()
    return {
        "statusCode": 200,
        "body": f"Processed {processed} rows from {len(records)} file(s)",
    }
