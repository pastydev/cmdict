"""Test functions for seaching in command line."""
from click.testing import CliRunner

from e2c.search_func import search


def test_search():
    """Test search function in command line."""
    res = CliRunner().invoke(search, "play")
    assert not res.exception
