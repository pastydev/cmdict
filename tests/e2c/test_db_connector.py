"""Test DBConnector."""
import pytest

from e2c.db_connector import DBConnector


def test_db_connect():
    """Test database connection and single query."""
    res = DBConnector().query("play")
    assert isinstance(res, dict) and len(res) > 0


def test_no_file_connect():
    """Test database connection when .db file doesn't exist."""
    with pytest.raises(ValueError):
        DBConnector("./no_such_file").search("play")
