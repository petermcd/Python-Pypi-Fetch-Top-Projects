"""Class to handle database interactions."""

import mariadb

from pypi_top_projects.models.package import Package
from pypi_top_projects.utilities.configuration import Configuration

DESCRIBE_TABLE_SQL = """
    DESCRIBE packages;
"""

CREATE_TABLE_SQLS = [
    """
    CREATE TABLE packages (
        id int(11) NOT NULL AUTO_INCREMENT,
        name varchar(256) NOT NULL UNIQUE,
        downloads int(15) UNSIGNED NOT NULL DEFAULT 0,
        version varchar(20) DEFAULT NULL,
        status int(2) UNSIGNED NOT NULL DEFAULT 0,
        PRIMARY KEY (id)
    )
    ENGINE = INNODB;
    """,
    """
    CREATE TABLE package_download_urls (
        id int(11) NOT NULL AUTO_INCREMENT,
        name varchar(256) NOT NULL DEFAULT '',
        url varchar(256) NOT NULL DEFAULT '',
        for_package int(11) NOT NULL,
        PRIMARY KEY (id)
    )
    ENGINE = INNODB;
    """,
    """
    ALTER TABLE package_download_urls
    ADD CONSTRAINT FK_download_urls_for_package FOREIGN KEY (for_package)
    REFERENCES packages (id) ON DELETE CASCADE ON UPDATE CASCADE;
    """,
    """
    CREATE TABLE package_urls (
        id int(11) NOT NULL AUTO_INCREMENT,
        name varchar(256) NOT NULL DEFAULT '',
        url varchar(256) NOT NULL DEFAULT '',
        for_package int(11) NOT NULL,
        PRIMARY KEY (id)
    )
    ENGINE = INNODB;
    """,
    """
    ALTER TABLE package_urls
    ADD CONSTRAINT FK_package_urls_for_package FOREIGN KEY (for_package)
    REFERENCES packages (id) ON DELETE CASCADE ON UPDATE CASCADE;
    """,
]

INSERT_RECORD_SQL = """
    INSERT INTO packages
        (name, downloads, version)
    VALUES
        (?, ?, ?);
"""

INSERT_PACKAGE_DOWNLOAD_URL_SQL = """
    INSERT INTO package_download_urls
        (name, url, for_package)
    VALUES
        (?, ?, ?);
"""

INSERT_PACKAGE_URL_SQL = """
    INSERT INTO package_urls
        (name, url, for_package)
    VALUES
        (?, ?, ?);
"""


class Database:
    """Class to handle database interaction."""

    __slots__ = [
        "_commit_required",
        "_configuration",
        "_connection",
        "_cursor",
    ]

    def __init__(self, configuration: Configuration | None = None):
        """
        Initialize Database.

        Args:
            configuration: Instance of Configuration, if None a new copy is instantiated
        """
        self._commit_required: bool = False
        if not configuration:
            configuration = Configuration()
        self._configuration = configuration
        self._create_connection()
        self._initialize_database()

    def _create_connection(self):
        """Create a database connection."""
        self._connection = mariadb.connect(
            user=self._configuration.database_username,
            password=self._configuration.database_password,
            host=self._configuration.database_host,
            port=self._configuration.database_port,
            database=self._configuration.database_name,
        )
        self._cursor = self._connection.cursor()

    def _initialize_database(self):
        """Create relevant tables in the database if they do not exist."""
        try:
            self._cursor.execute(DESCRIBE_TABLE_SQL)
        except mariadb.ProgrammingError:
            for sql in CREATE_TABLE_SQLS:
                self._cursor.execute(sql)

    def add_package(self, package: Package):
        """
        Add package details to the database.

        Args:
            package: Package object to be added
        """
        self._commit_required = True
        self._cursor.execute(
            INSERT_RECORD_SQL,
            (package.package_name, package.downloads, package.version),
        )
        package.database_id = self._cursor.lastrowid
        self._connection.commit()
        for download_url_name in package.download_urls.keys():
            self._cursor.execute(
                INSERT_PACKAGE_DOWNLOAD_URL_SQL,
                (
                    download_url_name,
                    package.download_urls[download_url_name],
                    package.database_id,
                ),
            )

        for project_url_name in package.project_urls.keys():
            self._cursor.execute(
                INSERT_PACKAGE_URL_SQL,
                (
                    project_url_name,
                    package.project_urls[project_url_name],
                    package.database_id,
                ),
            )

    def close(self):
        """Close the database connection."""
        if self._commit_required:
            self._connection.commit()
        self._connection.close()
