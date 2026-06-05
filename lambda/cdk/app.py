#!/usr/bin/env python3
"""CDK app entry point."""

import aws_cdk as cdk
from stack import DuckdbLambdaStack

app = cdk.App()
DuckdbLambdaStack(app, "DuckdbLambdaStack")
app.synth()
