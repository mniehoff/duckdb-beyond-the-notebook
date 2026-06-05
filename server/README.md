# duckdb as server with ducklake storage

## Run the data infra
On the server

```sql
FORCE INSTALL quack FROM core_nightly;
INSTALL ducklake;
ATTACH 'ducklake:analytics_data.ducklake' AS analytics_data;
USE analytics_data;
CREATE TABLE taxi_trips AS FROM "seed_data/nyc_taxi_sample.csv";
CALL quack_serve('quack:localhost', token = 'super_secret');
CALL quack_identify(
    name => 'matthias-local-mac',
    provider => 'local-mac',
    region => 'eu-central-1',
    meta => '{"role": "demo"}'
);

```

On the client

```sql
FORCE INSTALL quack FROM core_nightly;
CREATE SECRET ( TYPE quack, TOKEN 'super_secret');
ATTACH 'quack:localhost' AS remote;
FROM remote.query("SELECT * from analytics_data.taxi_trips"); 
```

WASM Shell

https://shell.duckdb.org/#queries=v0,FORCE-INSTALL-quack-FROM-core_nightly~,LOAD-quack~,CREATE-SECRET-(-TYPE-quack%2C-TOKEN-'super_secret')~,FROM-quack_query('quack%3Alocalhost'%2C-'SELECT-*-from-analytics_data.taxi_trips')~


## Run the app

```
uv run fastapi dev main.py
```