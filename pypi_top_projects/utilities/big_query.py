"""Class to interact with Google's Big Query."""
from typing import Optional

from google.cloud import bigquery
from google.oauth2 import service_account

from pypi_top_projects.utilities.configuration import Configuration

TOP_PACKAGES_SQL = """
    SELECT COUNT(file.project) AS download_count, file.project AS project
    FROM `bigquery-public-data.pypi.file_downloads`
    WHERE DATE(timestamp)
        BETWEEN DATE_SUB(CURRENT_DATE(), INTERVAL 30 DAY)
        AND CURRENT_DATE()
    group by file.project
    ORDER BY download_count DESC
    LIMIT 10000
"""


class BigQuery:
    """Class to interact with Google's Big Query."""

    __slots__ = ["_configuration"]

    def __init__(self, configuration: Optional[Configuration] = None):
        """
        Initialize BigQuery.

        Args:
            configuration: Instance of Configuration, if None a new copy is instantiated
        """
        if not configuration:
            configuration = Configuration()
        self._configuration = configuration

    def fetch_data(self, sql: Optional[str] = None):
        """
        Fetch data from Google's Big Query.

        Args:
            sql: SQL to be processed, if None then default SQL used

        Returns:
            List of rows
        """
        if not sql:
            sql = TOP_PACKAGES_SQL

        key_path = self._configuration.json_key_path

        credentials = service_account.Credentials.from_service_account_file(
            key_path,
            scopes=["https://www.googleapis.com/auth/cloud-platform"],
        )

        client = bigquery.Client(
            credentials=credentials,
            project=credentials.project_id,
        )

        return client.query(sql)
