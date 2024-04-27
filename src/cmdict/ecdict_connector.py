"""Database Connector."""
from pathlib import Path
from sqlite3 import connect
from sqlite3 import Error
from typing import Optional
from typing import Union

from loguru import logger

from cmdict.history import record

_PATH = Path(__file__).parent / "data" / "stardict.db"
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

    def __init__(self, path: Optional[Union[str, Path]] = _PATH):
        """Initialize database Connector.

        Args:
            path: Path to the database file. Defaults to be ``stardict``.

        Raises:
            ValueError: When the database file is missing or invalid.
        """
        _path = Path(path) if isinstance(path, str) else path

        if _path.is_file() and (_path.suffix == ".db"):
            self._conn = ECDICTConnector._init_conn(path)
        else:
            raise ValueError(
                f'Database file at "{_path}" is missing or invalid.'
            )

    @staticmethod
    def _init_conn(path):
        """Initialize database connection.

        Args:
            path (str): Path to the database file..

        Returns:
            sqlite3.Connection: Connection object to the database.
        """
        try:
            return connect(path)
        except Error:
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

        except Error:
            logger.exception("SQLite DB search failed.")
