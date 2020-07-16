"""Test functions for extracting highlights in PDF files."""
from e2c.pdf_tools import _recover_broken


def test_recover_broken():
    """Test if recover line-split words only.

    Also, the function should not recover words with necessary hyphens.
    """
    res = _recover_broken("grid struc- ture, tree- and cycle- based networks")
    assert res == "grid structure, tree- and cycle- based networks"
