Make sure docker/rancher is running

```
npx cdk bootstrap
npx cdk deploy
```

Get Outputs (include bucket names)
```
aws cloudformation describe-stacks --stack-name DuckdbLambdaStack --query "Stacks[0].Outputs"
```

Prepare env vars for duckdb cli

```
unset AWS_ACCESS_KEY_ID AWS_SECRET_ACCESS_KEY AWS_SESSION_TOKEN
eval "$(aws configure export-credentials --format env)"
```

1. Upload CSV: aws s3 cp ../sample_data.csv s3://<csv-bucket>/test.csv
2. Lambda fires, writes transformed Parquet to the output bucket
3. Query result: duckdb -c "SELECT * FROM read_parquet('s3://<output-bucket>/warehouse/transformed/*.parquet')"



