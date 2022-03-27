"""Main orchestrator."""
import requests

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
        self._fetch_package_data()
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

    def _fetch_package_data(self):
        """Fetch paackage data on each package."""
        for package in self._packages:
            url: str = f"https://pypi.org/pypi/{package.package_name}/json"
            response = requests.get(url)
            if response.status_code != 200:
                continue
            response_json = response.json()
            package.project_urls = response_json.get("info", {}).get("project_urls", {})
            urls = response_json.get("urls", [])
            download_urls = {
                url_details["packagetype"]: url_details["url"] for url_details in urls
            }

            package.download_urls = download_urls
            package.version = response_json.get("info", {}).get("version", "0")

    def _save_packages(self):
        """Save package data into the database."""
        for package in self._packages:
            self._database.add_package(package)
        self._database.close()
