# -*- coding: utf-8 -*-

import boto3
from master import config, template
from troposphere_mate import upload_template, deploy_stack

session = boto3.session.Session(profile_name=config.AWS_PROFILE.get_value())
s3_client = session.client("s3")
cf_client = session.client("cloudformation")

template.to_file("master.json")
template_url = upload_template(
    s3_client,
    template_content=template.to_json(),
    bucket_name=config.S3_BUCKET_FOR_DEPLOY.get_value()
)

stack_tags = {
    "ENVIRONMENT_NAME": config.ENVIRONMENT_NAME.get_value()
}

response = deploy_stack(
    cf_client,
    stack_name=config.STACK_NAME.get_value(),
    template_url=template_url,
    stack_tags=stack_tags,
    include_iam=True,
)
