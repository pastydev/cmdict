"""Database Connector."""
import os
import pathlib
import sqlite3

import click
from loguru import logger

_path = os.path.join(os.getcwd(), "db", "stardict.db")


class DBConnector:
    """Database Connector."""

    def __init__(self, path: str = _path):
        """Initialize database Connector.

        Args:
            path (str, optional): Path to the database file. Defaults to _path.
        """
        if pathlib.Path(path).is_file() and path.endswith(".db"):
            self._conn = DBConnector._init_conn(path)
        else:
            raise ValueError("Database file is missing or invalid.")

    @staticmethod
    def _init_conn(path: str) -> sqlite3.Connection:
        """Initialize database connection."""
        try:
            return sqlite3.connect(path)
        except sqlite3.Error:
            logger.exception("SQLite DB connection failed.")

    def search(self, word: str = "wrong") -> dict:
        """Search word from the database."""
        try:
            query = "select * from stardict where word = ?"
            cursor = self._conn.cursor()
            cursor.execute(query, (word,))
            res = cursor.fetchone()
            res_dict = {
                "id": res[0],
                "word": res[1],
                "sw": res[2],
                "phonetic": res[3],
                "definition": res[4],
                "trans": res[5],
                "pos": res[6],
                "collins": res[7],
                "oxford": res[8],
                "tag": res[9],
                "bnc": res[10],
                "frq": res[11],
                "exchange": res[12],
            }
            return res_dict
        except sqlite3.Error:
            logger.exception("SQLite DB search failed.")


@click.command()
@click.argument("word")
def search(word):
    """Type in English words and return Chinese translations."""
    res = DBConnector().search(word)
    click.echo("\n" + res["definition"] + "\n\n" + res["trans"])


if __name__ == "__main__":
    search()
