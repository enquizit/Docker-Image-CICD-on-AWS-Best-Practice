.. image:: https://codebuild.us-east-1.amazonaws.com/badges?uuid=eyJlbmNyeXB0ZWREYXRhIjoiU1F0blFHLzBqaDhUd0c0SjhTcmJib0w4VUFiVXo2eW9WNmRzYUxjV1crTW9ZcmlJNDN2bEFSdjRmb2M3dGpQMEQ5MFZmenk5RFpKYkhhaDRKc3kzLzQ0PSIsIml2UGFyYW1ldGVyU3BlYyI6IlpzcjRYQUx4MG93UzJGUmIiLCJtYXRlcmlhbFNldFNlcmlhbCI6MX0%3D&branch=master
    :alt: AWS CodeBuild Status
    :target: https://console.aws.amazon.com/codesuite/codebuild/projects/sanhe-docker-cicd-dev/history?region=us-east-1


Docker Image CICD on AWS Best Practice
==============================================================================


What Problem does this Solution solved
------------------------------------------------------------------------------

Move your infrastructure to Cloud and use dockerized application becomes more and more popular in 2020. Lots of federal organizations are moving to the Cloud. But they don't trust DockerHub and CircleCI. A lots of company want to have 100% control IT system.

Personally I love CircleCI + DockerHub for open source. But for enterprise, people may have concerns.

In this repo, a private CI/CD docker image build, test, publish solution is provided. In this solution nothing go beyond enterprise owned AWS Account. And it scales to any number of docker images and tags. And it comes with a CloudFormation template allows you to just enter few information like your AWS Account ID, AWS Region and AWS Profile you want to use, and the CICD pipeline is ready to use.


How to Deploy this Solution to AWS
------------------------------------------------------------------------------


Pre-requisite
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. install python Make sure your laptop installed ``Python3.6+``, and run ``pip install -r requirements.txt``. Make sure your ``pip`` command refers to the correct Python version.

2. prepare your AWS Account and AWS IAM User. create an AWS Account, and create an IAM User with proper privilege (be able to run cloudformation and create related resources). Then make your aws cli works and aws credential configured on your laptop.


Edit Config
------------------------------------------------------------------------------

1. open ``./cft/01-config-shared.json``, fill in related information. Make sure you have the s3 bucket readfy for cloudformation template uploads.

2. choose the environment you want to use. In this example, I use ``./cft/switch-env dev``. Of course you can use test or prod.


Deploy this Solution
------------------------------------------------------------------------------

First, let's deploy via cloudformation.

.. code-block:: bash

    # VERY IMPORTANT!
    cd ./cft

    # run deploy script
    python deploy.py

Then, go to your CodeBuild project control. Add your github OAUTH token and choose your git repo. And then check the box that triggers a build every time you push to Git.

IMPORTANT:

    **Configure git credential and link GitHub repo can not done via CloudFormation, and it is sensitive, you have to manually do it. And, everytime you have update the CloudFormation template, you have to re-configure it again. However, it doesn't take much time.**


Pull image from ECR
------------------------------------------------------------------------------

.. code-block:: bash

    # get temp ecr login
    aws ecr get-login --region us-east-1 --no-include-email --profile eq_sanhe

    # login docker client
    docker login -u AWS

    # pull image
    docker pull 110330507156.dkr.ecr.us-east-1.amazonaws.com/sanhe-docker-cicd-dev-web-app:hello-world-flask-app

    # remove image
    docker image rm 110330507156.dkr.ecr.us-east-1.amazonaws.com/sanhe-docker-cicd-dev-web-app:hello-world-flask-app
