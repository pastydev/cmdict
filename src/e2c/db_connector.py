"""Database Connector."""
import os
import sqlite3

from loguru import logger

_path = os.path.join(os.getcwd(), "db", "stardict.db")


class DBConnector:
    """Database Connector."""

    def __init__(self, path=_path):
        self._connection = DBConnector._init_connection(path)

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
