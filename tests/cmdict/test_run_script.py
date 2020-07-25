"""Test functions for seaching in command line."""
from click.testing import CliRunner

from cmdict.run_script import cli, extract, scan, search


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
    """Test cli extract words from pdf."""
    sample_pdf = "./tests/sample-1.pdf"

    res = CliRunner().invoke(extract, sample_pdf)
    assert res.exit_code == 0 and "district" in res.output


def test_cli_extract_from_pdf_with_color_option():
    """Test cli extract words from pdf with color specified."""
    sample_pdf = "./tests/sample-1.pdf"

    res = CliRunner().invoke(extract, [sample_pdf, "--color=pink"])
    expected = ["combined", "optimal", "realistic"]
    assert res.exit_code == 0 and all(word in res.output for word in expected)

    res = CliRunner().invoke(extract, [sample_pdf, "--color=blue"])
    expected = ["solution", "feasibility", "method"]
    assert res.exit_code == 0 and all(word in res.output for word in expected)

    res = CliRunner().invoke(extract, [sample_pdf, "--color=not_support"])
    assert res.exit_code == 0


def test_cli_extract_from_pdf_with_hyphen_broken_fix():
    """Test cli extract words from pdf with hyphen broken case."""
    sample_pdf = "./tests/sample-1.pdf"
    res = CliRunner().invoke(extract, [sample_pdf, "--color=green"])
    expected = ["producer", "ensure", "optimal", "production"]
    assert res.exit_code == 0 and all(word in res.output for word in expected)


def test_cli_scan():
    """Test cli scan words from a txt file."""
    sample_txt = "./tests/sample-3.txt"
    expected = ["typically", "predicate", "exclamation"]
    res = CliRunner().invoke(scan, sample_txt)
    assert res.exit_code == 0 and all(word in res.output for word in expected)
