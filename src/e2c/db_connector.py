"""Database Connector."""
import os
import pathlib
import sqlite3

from loguru import logger

_path = os.path.join(os.getcwd(), "db", "stardict.db")


class DBConnector:
    """Database Connector."""

    def __init__(self, path=_path):
        """Initialize database Connector.

        Args:
            path (str, optional): Path to the database file. Defaults to _path.
        """
        if pathlib.Path(path).is_file() and path.endswith(".db"):
            self._connection = DBConnector._init_connection(path)
        else:
            raise ValueError("Database file is missing or invalid.")

    @staticmethod
    def _init_connection(path):
        """Initialize database connection."""
        try:
            return sqlite3.connect(path)
        except sqlite3.Error:
            logger.exception("SQLite DB connection failed.")

    def search(self, word):
        """Search word from the database."""
        try:
            query = "select * from stardict where word = ?"
            cursor = self._connection.cursor()
            cursor.execute(query, (word,))
            return cursor.fetchone()
        except sqlite3.Error:
            logger.exception("SQLite DB search failed.")
