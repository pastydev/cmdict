"""Test DBConnector."""
from e2c.db_connector import DBConnector


def test_db_connect():
    """Test database connection."""
    res = DBConnector().search("play")
    assert isinstance(res, tuple) and len(res) > 0
