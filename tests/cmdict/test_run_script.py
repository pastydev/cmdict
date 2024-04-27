"""Test functions for seaching in command line."""
import os
import pathlib

import yaml
from click.testing import CliRunner

from cmdict.run_script import cli
from cmdict.run_script import extract
from cmdict.run_script import scan
from cmdict.run_script import search

_path_yaml = os.path.join(
    str(pathlib.Path(__file__).parents[2]), "src/cmdict/data/.extraction.yaml"
)


def test_cli():
    """Test cli not crash."""
    res = CliRunner().invoke(cli)
    assert res.exit_code == 0


def test_cli_search():
    """Test cli word search."""
    res = CliRunner().invoke(search, "play")
    assert "theatrical performance of a drama" in res.output


def test_cli_search_non_exist_word():
    """Test cli non-exist word search."""
    res = CliRunner().invoke(search, "notaword")
    assert "can not be found" in res.output


def test_cli_search_word_with_none_definition_or_trans():
    """Test cli non-exist word search."""
    res = CliRunner().invoke(search, "ducer")
    assert res.exit_code == 0


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


def test_cli_extract_from_pdf_with_save():
    """Test cli extract words from PDF and save it in a yaml file."""

    def _read_yaml(path):
        """Read the yaml file and return content in a list.

        Args:
            path (str): to the yaml file.

        Returns:
            List[str]: all words in the yaml file.
        """
        with open(path, "r") as f:
            try:
                hist = yaml.safe_load(f)
            except yaml.YAMLError as exc:
                print(exc)
        return hist

    sample_pdf = "./tests/sample-1.pdf"
    res = CliRunner().invoke(extract, [sample_pdf, "--color=green", "-s"])
    expected = ["producer", "ensure", "optimal", "production"]
    assert res.exit_code == 0 and all(
        word in _read_yaml(_path_yaml) for word in expected
    )


def test_cli_scan():
    """Test cli scan words from a txt file."""
    sample_txt = "./tests/sample-3.txt"
    expected = ["typically", "predicate", "exclamation"]
    res = CliRunner().invoke(scan, sample_txt)
    assert res.exit_code == 0 and all(word in res.output for word in expected)
