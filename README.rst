.. image:: https://codebuild.us-east-1.amazonaws.com/badges?uuid=eyJlbmNyeXB0ZWREYXRhIjoiU1F0blFHLzBqaDhUd0c0SjhTcmJib0w4VUFiVXo2eW9WNmRzYUxjV1crTW9ZcmlJNDN2bEFSdjRmb2M3dGpQMEQ5MFZmenk5RFpKYkhhaDRKc3kzLzQ0PSIsIml2UGFyYW1ldGVyU3BlYyI6IlpzcjRYQUx4MG93UzJGUmIiLCJtYXRlcmlhbFNldFNlcmlhbCI6MX0%3D&branch=master
    :alt: AWS CodeBuild Status
    :target: https://console.aws.amazon.com/codesuite/codebuild/projects/sanhe-docker-cicd-dev/history?region=us-east-1

Just a read me




In this tutorial, it is:

.. code-block:: bash

    # get temp ecr login
    aws ecr get-login --region us-east-1 --no-include-email --profile eq_sanhe

    # login docker client
    docker login -u AWS

    # pull image
    docker pull 110330507156.dkr.ecr.us-east-1.amazonaws.com/sanhe-docker-cicd-dev-web-app:hello-world-flask-app

    # remove image
    docker image rm 110330507156.dkr.ecr.us-east-1.amazonaws.com/sanhe-docker-cicd-dev-web-app:hello-world-flask-app


