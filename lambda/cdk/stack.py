"""CDK Stack: S3 bucket → Lambda (DuckDB) → Parquet on S3."""

from aws_cdk import (
    CfnOutput,
    Stack,
    Duration,
    RemovalPolicy,
    aws_s3 as s3,
    aws_s3_notifications as s3n,
    aws_lambda as _lambda,
    aws_ecr_assets as ecr_assets,
)
from constructs import Construct


class DuckdbLambdaStack(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # S3 bucket for CSV uploads
        csv_bucket = s3.Bucket(
            self,
            "CsvUploadBucket",
            removal_policy=RemovalPolicy.DESTROY,
            auto_delete_objects=True,
        )

        # S3 bucket for Parquet output
        output_bucket = s3.Bucket(
            self,
            "ParquetOutputBucket",
            removal_policy=RemovalPolicy.DESTROY,
            auto_delete_objects=True,
        )

        # Lambda function (Docker image)
        function = _lambda.DockerImageFunction(
            self,
            "DuckdbFunction",
            code=_lambda.DockerImageCode.from_image_asset(
                "../function",
                platform=ecr_assets.Platform.LINUX_ARM64,
            ),
            architecture=_lambda.Architecture.ARM_64,
            memory_size=1024,
            timeout=Duration.minutes(5),
            environment={
                "OUTPUT_BUCKET": output_bucket.bucket_name,
            },
        )

        # Grant permissions
        csv_bucket.grant_read(function)
        output_bucket.grant_read_write(function)

        # S3 event trigger: notify Lambda on .csv uploads
        csv_bucket.add_event_notification(
            s3.EventType.OBJECT_CREATED,
            s3n.LambdaDestination(function),
            s3.NotificationKeyFilter(suffix=".csv"),
        )

        # Outputs
        CfnOutput(self, "CsvBucketName", value=csv_bucket.bucket_name)
        CfnOutput(self, "OutputBucketName", value=output_bucket.bucket_name)
