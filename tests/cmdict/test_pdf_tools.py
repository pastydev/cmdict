"""Test functions for extracting highlights in PDF files."""
from cmdict.pdf_tools import _check_contain
from cmdict.pdf_tools import _fix_hyphen_broken
from cmdict.pdf_tools import _get_color_name
from cmdict.pdf_tools import extract_words


def test_get_color_name_func():
    """Test function _get_color_name."""
    yellow_rgb = [0.9803919792175293, 0.8039219975471497, 0.35294100642204285]
    pink_rgb = [0.9843140244483948, 0.36078399419784546, 0.5372549891471863]
    some_rgb = [0.5, 0.5, 0.5]
    assert _get_color_name(yellow_rgb) == "yellow"
    assert _get_color_name(pink_rgb) == "pink"
    assert _get_color_name(some_rgb) is None


def test_extract_words_func():
    """Test function _extract_words."""
    sample2_pdf = "./tests/sample-2.pdf"
    res = extract_words(sample2_pdf, "yellow")
    expected = ["hierarchical", "injections", "generation", "scheduling"]
    assert all(word in res for word in expected)


def test_extract_words_func_with_multiple_rows_annot():
    """Test function _extract_words with the multiple rows annotation case."""
    sample2_pdf = "./tests/sample-2.pdf"
    res = extract_words(sample2_pdf, "purple")
    expected = ["level", "important", "efforts"]
    assert all(word in res for word in expected)


def test_check_contain_func():
    """Test function _check_contain."""
    # (x1, y1) is top-left, (x2, y2) is bottom right
    rect1 = (0, 0, 1, 1)
    rect2 = (3, 3, 4, 4)
    assert not _check_contain(rect1, rect2)

    rect3 = (0, 0, 5, 5)
    assert _check_contain(rect2, rect3, threshold=0.03)

    rect4 = (1, 1, 6, 7)
    assert _check_contain(rect3, rect4, threshold=0.5)


def test_fix_hyphen_broken_func():
    """Test function _fix_hyphen_broken."""
    res = _fix_hyphen_broken(
        [
            "grid",
            "feasi-",
            "bility",
            "tree-",
            "and",
            "cycle-",
            "based",
            "networks",
        ]
    )
    assert res == [
        "grid",
        "feasibility",
        "tree-",
        "and",
        "cycle-",
        "based",
        "networks",
    ]
