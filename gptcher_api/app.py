#!/usr/bin/env python3
import aws_cdk as cdk

from cdk.cdk_stack import CdkStack

app = cdk.App()
CdkStack(
    app,
    "gptcher_api-stack",
    env=cdk.Environment(account="802148339218", region="eu-central-1"),
)

app.synth()
