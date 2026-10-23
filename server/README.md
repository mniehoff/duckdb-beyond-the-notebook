# duckdb as server with ducklake storage

Server
- runs Ducklake with local duckdb file as catalog
- executes the query & returns result to client.

## Run the data infra
### On the server 

open duckdb cli, run the commands below:

```sql
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

with duckdb 2.0 `duckdb -serve` can be used so that `quack_serve` can be skipped.

on old versions this might be needed before as quack was not part of the core release.

```sql
FORCE INSTALL quack FROM core_nightly;
```

### On the client (another terminal window)

```sql
CREATE SECRET ( TYPE quack, TOKEN 'super_secret');
ATTACH 'quack:localhost' AS remote;
FROM remote.query('SELECT * from analytics_data.taxi_trips'); 
FROM remote.query('FROM whoami()');
FROM whoami();
```

or with 2.0 as client

```sql
ATTACH 'quack:localhost' AS qk (TOKEN 'super_secret');
CONNECT qk;
SELECT * FROM analytics_data.taxi_trips;
FROM whoami();
DISCONNECT;
FROM whoami();
```

or start the cli with `duckdb -connect` so that ATTACH & CONNECT is done (only when server started with `duckdb -serve`)

Use the WASM Shell as a client (not yet working with wasm client 2.0.0; https://github.com/duckdb/duckdb-quack/issues/328):

https://shell.duckdb.org/#queries=v0,CREATE-SECRET-(-TYPE-quack%2C-TOKEN-'super_secret')~,FROM-quack_query('quack%3Alocalhost'%2C-'SELECT-*-from-analytics_data.taxi_trips')~


## Run the app 

Runs as a client

```
uv run fastapi dev main.py
```


## Alternative: Connect directly to catalog database

Server:
- only serves as the ducklake catalog

Difference to the one above: the client executes the query. So the client also needs access to the data.

### Server

**start with `duckdb 'lake_catalog.db'`**
```sql
CALL quack_serve(
    'quack:localhost',
    token => 'super_secret'
);
```

### Client

```sql
CREATE SECRET (
    TYPE quack, TOKEN 'super_secret'
);
ATTACH 'ducklake:quack:localhost'
    AS lake (DATA_PATH 'data');
USE lake;

CREATE TABLE taxi_trips AS FROM "seed_data/nyc_taxi_sample.csv";
SELECT * FROM taxi_trips;
```