"""Test utility functions."""
from cmdict.utils import remove_punctuation


def test_remove_punctuation_func():
    """Test function _remove_punctuation."""
    assert remove_punctuation("other.") == "other"
    assert remove_punctuation("'quote") == "quote"
