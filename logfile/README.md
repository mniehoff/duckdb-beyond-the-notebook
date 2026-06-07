# duckdb for log file analysis

As example for various admin tasks, you would usually do with a shell cmd/script

```bash
duckdb -c "SELECT COUNT(*) FROM read_csv('Spark_2k.log', header = False)"
```

```bash
duckdb -c "
SELECT
    regexp_extract(line, '(INFO|WARN|ERROR)', 1) AS level,
    regexp_extract(line, '(?:INFO|WARN|ERROR) ([^:]+):', 1) AS component,
    count(*) AS count
FROM read_csv('Spark_2k.log', columns={'line': 'VARCHAR'}, header=false)
WHERE line != ''
GROUP BY level, component
ORDER BY count DESC
"
```

Same query again, but `duckdb -csv -c "...""`

https://duckdb.org/docs/lts/clients/cli/output_formats

More: https://blobs.duckdb.org/slides/duckdb-ubuntu-summit-2026.pdf