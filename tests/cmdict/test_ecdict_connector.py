"""Test ECDICTConnector."""
import pytest

from cmdict.ecdict_connector import ECDICTConnector


def test_no_file_connect():
    """Test database connection when .db file doesn't exist."""
    with pytest.raises(ValueError):
        _ = ECDICTConnector("./no_such_file")


def test_word_query():
    """Test single word query."""
    res = ECDICTConnector().query("play")
    assert isinstance(res, dict) and len(res) > 0


def test_non_exist_word_search():
    """Test non-exist word query."""
    res = ECDICTConnector().query("notaword")
    assert res is None
