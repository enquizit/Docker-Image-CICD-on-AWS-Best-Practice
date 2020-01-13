# -*- coding: utf-8 -*-

from config_init import config
from pathlib_mate import Path
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

# --- Resorce

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
                ]
            }
        ),
    ],
)

code_build_project = codebuild.Project(
    title="CodeBuildProject",
    template=template,
    Name=config.ENVIRONMENT_NAME.get_value(),
    Description="Docker Image CICD on AWS Best Practice",
    Source=codebuild.Source(
        Type="GITHUB",
        Location="https://github.com/enquizit/Docker-Image-CICD-on-awsBest-Practice",
        GitCloneDepth=1,
        ReportBuildStatus=False,
    ),
    Artifacts=codebuild.Artifacts(Type="NO_ARTIFACTS"),
    Environment=codebuild.Environment(
        Type="LINUX_CONTAINER",
        Image="sanhe/cicd:awscli-python3.6.8-packer-slim",
        ComputeType="BUILD_GENERAL1_SMALL",
        EnvironmentVariables=[],
        PrivilegedMode=True,
        ImagePullCredentialsType="SERVICE_ROLE",
    ),
    ServiceRole=code_build_service_role.iam_role_arn,
    BadgeEnabled=True,
)


# --- ECR Repository
cft_dir = Path(__file__).parent
repos_dir = cft_dir.change(new_basename="repos")

for subfolder in repos_dir.select_dir():
    repo_name = subfolder.basename
    repo_logic_id = f"EcrRepo{camelcase(repo_name)}"
    res_ecr_repo = ecr.Repository(
        title=repo_logic_id,
        template=template,
        RepositoryName=f"{config.ENVIRONMENT_NAME.get_value()}-{repo_name}"
    )

# --- Code Build


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
