# -*- coding: utf-8 -*-

"""
Generate the Cloudformation Template to deploy this solution.
"""

import json
from config_init import config
from configirl import strip_comments
from pathlib_mate import PathCls as Path
from troposphere_mate import (
    Template, Parameter,
    iam, ecr, codebuild,
    camelcase,
)
from troposphere_mate.canned.iam import create_assume_role_policy_document, AWSServiceName

template = Template()

param_env_name = Parameter(
    title="EnvironmentName",
    Description="",
    Type="String",
    Default=config.ENVIRONMENT_NAME.get_value(),
)
template.add_parameter(param_env_name)

# --- AWS Resource

# --- IAM Role

code_build_service_role = iam.Role(
    title="CodeBuildServiceRole",
    template=template,
    RoleName=f"{config.ENVIRONMENT_NAME.get_value()}-code-build-service-role",
    AssumeRolePolicyDocument=create_assume_role_policy_document([AWSServiceName.codeBuild]),
    Policies=[
        iam.Policy(
            PolicyName="AllowEcrAction",
            PolicyDocument={
                "Version": "2012-10-17",
                "Statement": [
                    {
                        "Action": [
                            "ecr:BatchCheckLayerAvailability",
                            "ecr:CompleteLayerUpload",
                            "ecr:GetAuthorizationToken",
                            "ecr:InitiateLayerUpload",
                            "ecr:PutImage",
                            "ecr:UploadLayerPart"
                        ],
                        "Resource": "*",
                        "Effect": "Allow"
                    },
                    # only allow all codebuild operation on this code build project
                    {
                        "Action": [
                            "codebuild:*"
                        ],
                        "Resource": f"arn:aws:codebuild:{config.AWS_REGION.get_value()}:{config.AWS_ACCOUNT_ID.get_value()}:project/{config.CODE_BUILD_PROJECT_NAME.get_value()}",
                        "Effect": "Allow"
                    }
                ]
            }
        ),
    ],
)

# --- ECR Repository
cft_dir = Path(__file__).parent
repos_dir = cft_dir.change(new_basename="repos")

DEFAULT_UNTAGGED_IMAGE_EXPIRE_DAYS = 30


repo_names = list()
for subfolder in repos_dir.select_dir(recursive=False):
    repo_config_file = Path(subfolder, "config.json")
    repo_basename = subfolder.basename
    if repo_config_file.exists():
        repo_config_data = json.loads(strip_comments(repo_config_file.read_text("utf-8")))
        try:
            untagged_image_expire_days = repo_config_data["untagged_image_expire_days"]
        except:
            untagged_image_expire_days = DEFAULT_UNTAGGED_IMAGE_EXPIRE_DAYS
    else:
        untagged_image_expire_days = DEFAULT_UNTAGGED_IMAGE_EXPIRE_DAYS

    repo_logic_id = f"EcrRepo{camelcase(repo_basename)}"
    repo_name = f"{config.ENVIRONMENT_NAME.get_value()}-{repo_basename}"
    repo_names.append(repo_name)

    ecr_lifecycle_policy = {
        "rules": [
            {
                "rulePriority": 1,
                "description": f"Remove old images (untagged) when it becomes not active in {untagged_image_expire_days} days",
                "selection": {
                    "tagStatus": "untagged",
                    "countType": "sinceImagePushed",
                    "countNumber": untagged_image_expire_days,
                    "countUnit": "days"
                },
                "action": {"type": "expire"}
            }
        ]
    }

    res_ecr_repo = ecr.Repository(
        title=repo_logic_id,
        template=template,
        RepositoryName=repo_name,
        DeletionPolicy="Retain",
        LifecyclePolicy=ecr.LifecyclePolicy(
            LifecyclePolicyText=json.dumps(ecr_lifecycle_policy),
            RegistryId=config.AWS_ACCOUNT_ID.get_value()
        )
    )

# --- Code Build
EnvironmentVariables = [
    {
        "Name": "ENVIRONMENT_NAME",
        "Value": config.ENVIRONMENT_NAME.get_value(),
        "Type": "PLAINTEXT"
    },
    {
        "Name": "AWS_ACCOUNT_ID",
        "Value": config.AWS_ACCOUNT_ID.get_value(),
        "Type": "PLAINTEXT"
    },
    {
        "Name": "AWS_DEFAULT_REGION",
        "Value": config.AWS_REGION.get_value(),
        "Type": "PLAINTEXT"
    },
]

code_build_project = codebuild.Project(
    title="CodeBuildProject",
    template=template,
    Name=config.CODE_BUILD_PROJECT_NAME.get_value(),
    Description="Docker Image CICD on AWS Best Practice",
    Source=codebuild.Source(
        Type="GITHUB",
        Location=config.GITHUB_URL.get_value(),
        GitCloneDepth=1,
        GitSubmodulesConfig=codebuild.GitSubmodulesConfig(
            FetchSubmodules=False,
        ),
        ReportBuildStatus=False,
    ),
    Artifacts=codebuild.Artifacts(Type="NO_ARTIFACTS"),
    Environment=codebuild.Environment(
        Type="LINUX_CONTAINER",
        Image="aws/codebuild/standard:2.0",
        ComputeType="BUILD_GENERAL1_SMALL",
        EnvironmentVariables=EnvironmentVariables,
        PrivilegedMode=True,
        ImagePullCredentialsType="CODEBUILD",
    ),
    ServiceRole=code_build_service_role.iam_role_arn,
    BadgeEnabled=True,
    # Triggers=codebuild.ProjectTriggers(
    #     Webhook=True,
    #     FilterGroups=[
    #         [
    #             codebuild.WebhookFilter(
    #                 Type="EVENT",
    #                 Pattern="PUSH,PULL_REQUEST_CREATED,PULL_REQUEST_UPDATED",
    #                 ExcludeMatchedPattern=False,
    #             ),
    #         ]
    #     ],
    # ),
)

# --- Tags
common_tags = {
    "Creator": "Sanhe Hu",
    "ProjectName": config.PROJECT_NAME_SLUG.get_value(),
    "Stage": config.STAGE.get_value(),
    "EnvironmentName": config.ENVIRONMENT_NAME.get_value(),
}
template.update_tags(
    tags_dct=common_tags
)
template.create_resource_type_label()
