=====================================
Python Pypi Fetch Top Projects
=====================================

This project fetches data about the top pypi.org packages from Google's BigQuery
service.

*************************************
Configuration
*************************************

This application can be configured in eiter 2 ways:

.env File
=====================================

The following is an example .env file. All entries are required apart
from port which defaults to 3306. The file must reside in the working
directory for the application.

.. code-block:: shell

   JSON_KEY_PATH=path/to/file.json
   DATABASE_USERNAME=username
   DATABASE_PASSWORD=password
   DATABASE_HOST=host
   DATABASE_NAME=name
   DATABASE_PORT=3306

Environment Variables
=====================================

The configuration items that can be configued in the .env file can
also be set as environment variables.

JSON Key
=====================================

To be able to communicate with the Google Big Query API you are
required to have a JSON Key file. This provides the configuration
required to login to the Google API.

*************************************
Development
*************************************

Git Pre Commit
=====================================

Git pre commit runs tests prior to a commit occurring, this helps
reduce CICD failures. To set this up the following commands can be
carried out:

.. code-block:: shell

   pip install pre-commit
   pre-commit install