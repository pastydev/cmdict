"""Test functions for seaching in command line."""
from click.testing import CliRunner

from e2c.run_script import cli, search


def test_cli():
    """Test cli not crash."""
    res = CliRunner().invoke(cli)
    assert not res.exception


def test_cli_search():
    """Test search function in command line."""
    res = CliRunner().invoke(search, "play")
    assert not res.exception
