"""Class to handle configuration."""
from os import getenv
from typing import Optional

from dotenv import load_dotenv


class Configuration:
    """Configuration class to be used as a singleton."""

    _instance = None
    __slots__ = [
        "_database_host",
        "_database_name",
        "_database_password",
        "_database_port",
        "_database_username",
        "_json_key_path",
    ]

    def __init__(self):
        """Initialize Configuration."""
        self._json_key_path: Optional[str] = None
        self._database_host: Optional[str] = None
        self._database_name: Optional[str] = None
        self._database_password: Optional[str] = None
        self._database_port: Optional[int] = None
        self._database_username: Optional[str] = None

        load_dotenv()

    @property
    def json_key_path(self) -> str:
        """
        Getter for the location on disk for the JSON key.

        Returns:
            JSON Key path
        """
        if not self._json_key_path:
            self._json_key_path = getenv("JSON_KEY_PATH", "")
        return self._json_key_path or ""

    @property
    def database_host(self) -> str:
        """
        Property for the database host.

        Returns:
            Database host
        """
        if not self._database_host:
            self._database_host = getenv("DATABASE_HOST", "")
        return self._database_host or ""

    @property
    def database_name(self) -> str:
        """
        Property for the database name.

        Returns:
            Database name
        """
        if not self._database_name:
            self._database_name = getenv("DATABASE_NAME", "")
        return self._database_name or ""

    @property
    def database_password(self) -> str:
        """
        Property for the database password.

        Returns:
            Database password
        """
        if not self._database_password:
            self._database_password = getenv("DATABASE_PASSWORD", "")
        return self._database_password or ""

    @property
    def database_port(self) -> int:
        """
        Property for the database port.

        Returns:
            Database port defaulting to 3306
        """
        if not self._database_port:
            self._database_port = int(getenv("DATABASE_PORT", 3306))
        return self._database_port

    @property
    def database_username(self) -> str:
        """
        Property for the database username.

        Returns:
            Database username
        """
        if not self._database_username:
            self._database_username = getenv("DATABASE_USERNAME", "")
        return self._database_username or ""

    @classmethod
    def instance(cls):
        """
        Provide an existing instance of configuration, if none exists a new one is created.

        Returns:
            Instance of Configuration
        """
        if not cls._instance:
            cls._instance = Configuration()
        return cls._instance
