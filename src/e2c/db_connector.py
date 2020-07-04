"""Database Connector."""
import os
import pathlib
import sqlite3

from loguru import logger

_path = os.path.join(os.getcwd(), "db", "stardict.db")
_key_names = (
    "id",
    "word",
    "sw",
    "phonetic",
    "definition",
    "trans",
    "pos",
    "collins",
    "oxford",
    "tag",
    "bnc",
    "frq",
    "exchange",
)


class DBConnector:
    """Database Connector."""

    def __init__(self, path=_path):
        """Initialize database Connector.

        Args:
            path (str, optional): Path to the database file.
                Defaults to ``_path``.
        """
        if pathlib.Path(path).is_file() and path.endswith(".db"):
            self._conn = DBConnector._init_conn(path)
        else:
            raise ValueError("Database file is missing or invalid.")

    @staticmethod
    def _init_conn(path):
        """Initialize database connection."""
        try:
            return sqlite3.connect(path)
        except sqlite3.Error:
            logger.exception("SQLite DB connection failed.")

    def query(self, word):
        """Search word from the database."""
        try:
            query = "select * from stardict where word = ?"
            cursor = self._conn.cursor()
            cursor.execute(query, (word,))
            res = cursor.fetchone()
            return dict([(x, y) for x, y in zip(_key_names, res)])
        except sqlite3.Error:
            logger.exception("SQLite DB search failed.")
