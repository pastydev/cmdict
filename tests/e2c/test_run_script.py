"""Test functions for seaching in command line."""
from click.testing import CliRunner

from e2c.run_script import cli, colors, extract, search


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


def test_colors():
    """If `colors` can detect all highlight colors of a PDF file.

    The underline annotation should not be treated as highlight.
    """
    res = CliRunner().invoke(colors, "./tests/sample-1.pdf")
    assert (
        "[0.9803919792175293, 0.8039219975471497, 0.35294100642204285]"
        in res.output
    )
    assert not (
        "[0.9254900217056274, 0.1568630039691925, 0.0784313976764679]"
        in res.output
    )


def test_extract():
    """If extract can detect line-split hyphens.

    `grid struc- ture` is extracted initially, and it should be
    recovered by removing the line-split hyphens.
    """
    res = CliRunner().invoke(
        extract,
        [
            "./tests/sample-1.pdf",
            "[0.9843140244483948, 0.36078399419784546, 0.5372549891471863]",
        ],
    )
    assert res.exit_code == 0
    assert "grid structure" in res.output


def test_extract_range():
    """If `extract` only select words with the right range.

    Note that the range of the highlight in `sample-2.pdf` is very thick
    vertically.
    """
    res = CliRunner().invoke(
        extract,
        [
            "./tests/sample-2.pdf",
            "[0.9843140244483948, 0.36078399419784546, 0.5372549891471863]",
        ],
    )
    assert res.exit_code == 0
    correct_output = (
        "{0: 'optimal operation of combined heat and power plants'}\n"
    )
    assert correct_output == res.output
