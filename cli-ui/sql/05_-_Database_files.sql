ATTACH 'persisent.db';

DROP TABLE IF EXISTS raw_data

CREATE TABLE raw_data AS SELECT * FROM read_json('data/simple/employees.json')

-- attach to a remote duckdb database file
ATTACH 's3://us-prd-motherduck-open-datasets/content/duckdb-as-catalog/ducky_catalog.ddb';

-- use a duckdb database as a technical catalog for different databases
-- the file itself is just roughly 268KB
SELECT sql FROM duckdb_views() where temporary=false;

SELECT * FROM ducky_catalog.air_quality

ATTACH 'md:'

CREATE DATABASE cloud_ducky_catalog from ducky_catalog;
CREATE SHARE share_ducky_catalog from cloud_ducky_catalog (ACCESS UNRESTRICTED, VISIBILITY HIDDEN, UPDATE AUTOMATIC);
