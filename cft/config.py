# -*- coding: utf-8 -*-

from configirl import ConfigClass, Constant, Derivable


class Config(ConfigClass):
    PROJECT_NAME = Constant()
    STAGE = Constant()

    PROJECT_NAME_SLUG = Derivable()

    @PROJECT_NAME_SLUG.getter
    def get_PROJECT_NAME_SLUG(self):
        return self.PROJECT_NAME.get_value().replace("_", "-")

    ENVIRONMENT_NAME = Derivable()

    @ENVIRONMENT_NAME.getter
    def get_ENVIRONMENT_NAME(self):
        return f"{self.PROJECT_NAME_SLUG.get_value()}-{self.STAGE.get_value()}"

    STACK_NAME = Derivable()

    @STACK_NAME.getter
    def get_STACK_NAME(self):
        return f"{self.ENVIRONMENT_NAME.get_value()}-stack"

    AWS_PROFILE = Constant()
    AWS_ACCOUNT_ID = Constant()
    AWS_REGION = Constant()

    S3_BUCKET_FOR_DEPLOY = Constant()

    GITHUB_URL = Constant()

    # --- Code Build

    CODE_BUILD_PROJECT_NAME = Derivable()

    @CODE_BUILD_PROJECT_NAME.getter
    def get_CODE_BUILD_PROJECT_NAME(self):
        return self.ENVIRONMENT_NAME.get_value()
