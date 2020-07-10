"""Test DBConnector."""
import pytest

from e2c.db_connector import DBConnector


def test_no_file_connect():
    """Test database connection when .db file doesn't exist."""
    with pytest.raises(ValueError):
        _ = DBConnector("./no_such_file")


def test_no_file_connect_word_query():
    """Test database connection when .db file doesn't exist."""
    with pytest.raises(ValueError):
        _ = DBConnector("./no_such_file").query("play")


def test_word_query():
    """Test single word query."""
    res = DBConnector().query("play")
    assert (
        isinstance(res, dict) and len(res) == 13 and isinstance(res["id"], int)
    )


def test_non_exist_word_search():
    """Test non-exist word query."""
    res = DBConnector().query("notaword")
    assert res is None
