"""Test functions for txt files."""
from cmdict.txt_tools import scan_words


def test_scan_words():
    """Test if return a list of word with punctuations removed."""
    words = scan_words("tests/sample-3.txt")
    expected = ["typically", "predicate", "exclamation"]
    assert all(word in words for word in expected)
