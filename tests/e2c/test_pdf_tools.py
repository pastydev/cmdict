"""Test functions for extracting highlights in PDF files."""
from e2c.pdf_tools import _check_contain, _get_color_name, _remove_punctuation


def test_get_color_name_func():
    """Test function _get_color_name."""
    yellow_rgb = [0.9803919792175293, 0.8039219975471497, 0.35294100642204285]
    pink_rgb = [0.9843140244483948, 0.36078399419784546, 0.5372549891471863]
    some_rgb = [0.5, 0.5, 0.5]
    assert _get_color_name(yellow_rgb) == "yellow"
    assert _get_color_name(pink_rgb) == "pink"
    assert _get_color_name(some_rgb) is None


def test_check_contain_func():
    """Test function _check_contain."""
    # (x1, y1) is top-left, (x2, y2) is bottom right
    rect1 = (0, 0, 1, 1)
    rect2 = (3, 3, 4, 4)
    assert not _check_contain(rect1, rect2)

    rect3 = (0, 0, 5, 5)
    assert _check_contain(rect2, rect3, threshold=0.1)

    rect4 = (1, 1, 6, 7)
    assert _check_contain(rect3, rect4, threshold=0.5)


def test_remove_punctuation_func():
    """Test function _remove_punctuation."""
    assert _remove_punctuation("other.") == "other"
    assert _remove_punctuation("'quote") == "quote"
