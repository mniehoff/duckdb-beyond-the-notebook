Make sure docker/rancher is running

run in /cdk/

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


0. Remove old output bucket contents: `aws s3 rm s3://duckdblambdastack-parquetoutputbucket4dbf9759-y70czgi2wkcs/warehouse/transformed/ --recursive`
1. Logs: `aws logs tail /aws/lambda/DuckdbLambdaStack-DuckdbFunctionFD0177BA-WBlkPO9wG2tO --follow`
2. Upload CSV: `aws s3 cp ../sample_data.csv s3://duckdblambdastack-csvuploadbuckete5303144-bap7exgadcsd/test.csv`
3. Lambda fires, writes transformed Parquet to the output bucket
4.Query result: `duckdb -c "SELECT * FROM read_parquet('s3://duckdblambdastack-parquetoutputbucket4dbf9759-y70czgi2wkcs/warehouse/transformed/*.parquet')"`



