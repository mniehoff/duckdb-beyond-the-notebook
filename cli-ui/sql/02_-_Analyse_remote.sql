-- parquet file
SELECT *
FROM   read_parquet("https://github.com/plotly/datasets/raw/master/oil-and-gas.parquet");

SELECT "reporting year"         AS year,
       sum("gas produced, mcf") AS gas
FROM   read_parquet("https://github.com/plotly/datasets/raw/master/oil-and-gas.parquet" )
GROUP  BY "reporting year";

SET force_download=true;
SELECT unnest(results)
FROM read_json("https://ll.thespacedevs.com/2.3.0/launches/?mode=list&format=json&limit=100")

-- multiple formats can be combined in a single query
--SELECT * FROM read_json(...) JOIN read_parquet(...)
