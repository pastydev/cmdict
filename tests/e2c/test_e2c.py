"""Test e2c."""
from e2c import e2c
from e2c.minimal import cover_it


def test_e2c():
    """Minimal test for e2c."""
    assert e2c() == "Welcome to e2c!"


def test_coverage():
    """Test code coverage."""
    assert cover_it() == "Test code coverage."
