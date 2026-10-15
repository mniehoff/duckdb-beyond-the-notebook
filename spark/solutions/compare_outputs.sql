CREATE TABLE spark AS SELECT * FROM read_parquet('output/<spark_run>.parquet/*.parquet');
CREATE TABLE sqlf  AS SELECT * FROM read_parquet('output/<sqlframe_run>.parquet');

-- Row counts
SELECT (SELECT count(*) FROM spark) AS spark_rows, (SELECT count(*) FROM sqlf) AS sqlf_rows;

-- Rows present in one result but not the other
SELECT 'only_spark' AS side, * FROM (FROM spark EXCEPT FROM sqlf)
UNION ALL
SELECT 'only_sqlframe', * FROM (FROM sqlf EXCEPT FROM spark)
ORDER BY PULocationID, side;

-- Which columns differ, joined on the key
SELECT s.PULocationID, s.peak_pickup_hour AS spark_hour, q.peak_pickup_hour AS sqlf_hour
FROM spark s JOIN sqlf q ON s.PULocationID = q.pulocationid
WHERE s.peak_pickup_hour IS DISTINCT FROM q.peak_pickup_hour;