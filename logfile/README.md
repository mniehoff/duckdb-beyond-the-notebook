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


## Question:

Which Spark stages sent the most data back to the driver?

### Hint
- "result sent to driver" in log message
- split_part function: https://duckdb.org/docs/lts/sql/functions/text#split_partstring-separator-index
- `delim='\t', quote=''` as paramaters for read_csv reads the line as one column

### Solution:

```
SELECT
    split_part(line, ' ', 10)::DOUBLE::INT AS stage,
    count(*)                               AS finished_tasks,
    sum(split_part(line, ' ', 13)::INT)    AS bytes_to_driver
FROM read_csv('Spark_2k.log', columns={'line': 'VARCHAR'},
              header=false, delim='\t', quote='')
WHERE contains(line, 'Finished task')
GROUP BY stage
ORDER BY bytes_to_driver DESC
LIMIT 5;
```

https://duckdb.org/docs/lts/clients/cli/output_formats

More: https://blobs.duckdb.org/slides/duckdb-ubuntu-summit-2026.pdf