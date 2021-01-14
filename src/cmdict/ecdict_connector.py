"""Database Connector."""
import os
import pathlib
import sqlite3

from loguru import logger

from cmdict.history import record

_path = os.path.join(str(pathlib.Path(__file__).parent), "data", "stardict.db")
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


class ECDICTConnector:
    """ECDICT database Connector.

    Database from `https://github.com/skywind3000/ECDICT`.

    """

    def __init__(self, path=_path):
        """Initialize database Connector.

        Args:
            path (str, optional): Path to the database file.
                Defaults to ``_path``.

        Raises:
            ValueError: When the database file is missing or invalid.
        """
        if pathlib.Path(path).is_file() and path.endswith(".db"):
            self._conn = ECDICTConnector._init_conn(path)
        else:
            raise ValueError("Database file is missing or invalid.")

    @staticmethod
    def _init_conn(path):
        """Initialize database connection.

        Args:
            path (str): Path to the database file..

        Returns:
            sqlite3.Connection: Connection object to the database.
        """
        try:
            return sqlite3.connect(path)
        except sqlite3.Error:
            logger.exception("SQLite DB connection failed.")

    def query(self, word):
        """Query word from the database.

        Args:
            word (str): the word to be queried.

        Returns:
            dict: Query result with format:
                {
                    id: (int)
                    word: (str)
                    sw: (str)
                    phonetic: (str)
                    definition: (str)
                    trans: (str)
                    "pos": (str)
                    "collins": (int)
                    "oxford": (int)
                    "tag": (str)
                    "bnc": (int)
                    "frq": (int)
                    "exchange": (str)
                }
        """
        try:
            query = "select * from stardict where word = ?"
            cursor = self._conn.cursor()
            cursor.execute(query, (word,))
            record(word)
            res = cursor.fetchone()

            return (
                dict([(x, y) for x, y in zip(_key_names, res)])
                if res
                else None
            )

        except sqlite3.Error:
            logger.exception("SQLite DB search failed.")
