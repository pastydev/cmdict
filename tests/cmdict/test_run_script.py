"""Test functions for seaching in command line."""
from click.testing import CliRunner

from cmdict.run_script import cli, extract, search


def test_cli():
    """Test cli not crash."""
    res = CliRunner().invoke(cli)
    assert res.exit_code == 0


def test_cli_search():
    """Test cli word search."""
    res = CliRunner().invoke(search, "play")
    assert "theatrical performance of a drama" in res.output


def test_cli_non_exist_search():
    """Test cli non-exist word search."""
    res = CliRunner().invoke(search, "notaword")
    assert "can not be found" in res.output


def test_cli_extract_from_pdf():
    """Test cli extract words from pdf.

    `grid struc- ture` is extracted initially, and it should be
    recovered by removing the line-split hyphens.
    """
    sample_pdf = "./tests/sample-1.pdf"

    res = CliRunner().invoke(extract, sample_pdf)
    assert res.exit_code == 0 and "district" in res.output

    res = CliRunner().invoke(extract, [sample_pdf, "--color=pink"])
    expected = ["combined", "optimal", "realistic"]
    assert res.exit_code == 0 and all(word in res.output for word in expected)

    res = CliRunner().invoke(extract, [sample_pdf, "--color=blue"])
    expected = ["solution", "feasibility", "method"]
    assert res.exit_code == 0 and all(word in res.output for word in expected)

    res = CliRunner().invoke(extract, [sample_pdf, "--color=not_support"])
    assert res.exit_code == 0
