# Prerequisites
Log into AWS account using `aws login`

Make sure docker/rancher is running

# Setup stack

run in /cdk/

```
npx cdk bootstrap
npx cdk deploy
```

# Actual Demo
`demo.sh` looks up bucket and function names from the stack, so it survives stack recreation. Run from `lambda/`.

0. Remove old output bucket contents: `./demo.sh clean`
1. Logs (separate terminal): `./demo.sh logs`
2. Upload CSV: `./demo.sh upload`
3. Lambda fires, writes transformed Parquet to the output bucket
4. Query result: `./demo.sh query` (exports AWS credentials for the duckdb CLI itself)

# Cleanup

`npx cdk destroy`


