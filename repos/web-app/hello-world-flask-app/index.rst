Hello World Flask App Image
==============================================================================


Test Locally
------------------------------------------------------------------------------

Build the docker image, give it a name ``my-app:1``

.. code-block:: bash

    docker build -t web-app:hello-world-flask-app .

Run docker as a command:

.. code-block:: bash

    docker run --rm -dt --name web-app -p 80:12345 web-app:hello-world-flask-app
