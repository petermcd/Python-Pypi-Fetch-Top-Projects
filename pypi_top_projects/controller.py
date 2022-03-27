"""Main orchestrator."""
from pypi_top_projects.models.package import Package
from pypi_top_projects.utilities.big_query import BigQuery
from pypi_top_projects.utilities.database import Database


class Controller:
    """Main orchestrator for the system."""

    __slots__ = ["_big_query", "_database", "_packages"]

    def __init__(self):
        """Initialize Controller."""
        self._big_query = BigQuery()
        self._database = Database()
        self._packages = []

    def run(self):
        """Run."""
        self._fetch_download_counts()
        self._save_packages()

    def _fetch_download_counts(self):
        """Fetch details for the most popular packages on pypi.org."""
        for top_package in self._big_query.fetch_data():
            package = Package(
                package_name=top_package["project"],
                downloads=top_package["download_count"],
            )
            self._packages.append(package)
            print(top_package["download_count"])
            print(top_package["project"])

    def _save_packages(self):
        """Save package data into the database."""
        for package in self._packages:
            self._database.add_package(package)
        self._database.close()
