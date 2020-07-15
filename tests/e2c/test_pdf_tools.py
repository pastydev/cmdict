"""Test functions for extracting highlights in PDF files."""
from click.testing import CliRunner

from e2c.pdf_tools import _recover_broken, colors, extract


def test_colors():
    """If `colors` can detect all highlight colors of a PDF file."""
    res = CliRunner().invoke(colors, "./tests/sample-1.pdf")
    assert (
        "[0.9803919792175293, 0.8039219975471497, 0.35294100642204285]"
        in res.output
    )


def test_recover_broken():
    """Test if recover line-split words only.

    Also, the function should not recover words with necessary hyphens.
    """
    res = _recover_broken("grid struc- ture, tree- and cycle- based networks")
    assert res == "grid structure, tree- and cycle- based networks"


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
