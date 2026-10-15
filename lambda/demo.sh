#!/usr/bin/env bash
# Demo helper for DuckdbLambdaStack. Usage: ./demo.sh {clean|logs|upload|query}
set -euo pipefail

STACK=DuckdbLambdaStack
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

output() {
  aws cloudformation describe-stacks --stack-name "$STACK" \
    --query "Stacks[0].Outputs[?OutputKey=='$1'].OutputValue" --output text
}

case "${1:-}" in
  clean)
    aws s3 rm "s3://$(output OutputBucketName)/warehouse/transformed/" --recursive
    ;;
  logs)
    function_name=$(aws cloudformation describe-stack-resources --stack-name "$STACK" \
      --query "StackResources[?ResourceType=='AWS::Lambda::Function' && starts_with(LogicalResourceId,'DuckdbFunction')].PhysicalResourceId | [0]" \
      --output text)
    aws logs tail "/aws/lambda/$function_name" --follow
    ;;
  upload)
    aws s3 cp "$DIR/sample_data.csv" "s3://$(output CsvBucketName)/test.csv"
    ;;
  query)
    unset AWS_ACCESS_KEY_ID AWS_SECRET_ACCESS_KEY AWS_SESSION_TOKEN
    eval "$(aws configure export-credentials --format env)"
    export AWS_REGION="${AWS_REGION:-${AWS_DEFAULT_REGION:-$(aws configure get region)}}"
    duckdb -c "SELECT * FROM read_parquet('s3://$(output OutputBucketName)/warehouse/transformed/*.parquet')"
    ;;
  *)
    echo "Usage: $0 {clean|logs|upload|query}" >&2
    exit 1
    ;;
esac
