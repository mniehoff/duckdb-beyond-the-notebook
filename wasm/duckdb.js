import * as duckdb from 'https://cdn.jsdelivr.net/npm/@duckdb/duckdb-wasm@1.29.0/+esm';

let db = null;

export async function initDuckDB() {
  const BUNDLES = duckdb.getJsDelivrBundles();
  const bundle = await duckdb.selectBundle(BUNDLES);
  const worker_url = URL.createObjectURL(
    new Blob([`importScripts("${bundle.mainWorker}");`], { type: 'text/javascript' })
  );
  const worker = new Worker(worker_url);
  const logger = new duckdb.ConsoleLogger();
  db = new duckdb.AsyncDuckDB(logger, worker);
  await db.instantiate(bundle.mainModule, bundle.pthreadWorker);
  return db;
}

// Alternative: skip registration and reference the file directly in SQL via full URL,
// e.g. SELECT * FROM 'http://localhost:8080/nyc_taxi_sample.parquet'
export async function registerParquet(filename) {
  const url = new URL(filename, window.location.href).href;
  await db.registerFileURL(filename, url, duckdb.DuckDBDataProtocol.HTTP, false);
}

export async function runQuery(sql) {
  const conn = await db.connect();
  try {
    const result = await conn.query(sql);
    const rows = result.toArray().map(r => Object.fromEntries(Object.entries(r.toJSON())));
    const cols = result.schema.fields.map(f => f.name);
    return { rows, cols };
  } finally {
    await conn.close();
  }
}
