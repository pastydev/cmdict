"""Test functions for seaching in command line."""
from click.testing import CliRunner

from e2c.run_script import cli, search


def test_cli():
    """Test cli not crash."""
    res = CliRunner().invoke(cli)
    assert res.exit_code == 0


def test_cli_search():
    """Test cli word search."""
    res = CliRunner().invoke(search, "play")
    assert "游戏" in res.output


def test_cli_non_exist_search():
    """Test cli non-exist word search."""
    res = CliRunner().invoke(search, "notaword")
    assert "can not be found" in res.output
