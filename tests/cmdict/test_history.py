"""Test functions and classes in ``history.py``.

Temporary paths to yaml files will be initiated first. The performance
of ``record`` function will be tested in different situations, namely,
when the file doesn't exist, when the file is empty, and when the file
has some content.
"""
import pathlib

import pytest
import yaml

from cmdict.history import record


@pytest.fixture(scope="module")
def path2yaml(tmp_path_factory):
    """Initiate a path to a yaml file.

    Args:
        tmp_path_factory (TempPathFactory): pytest tool to initiate
            temporary a path.

    Returns:
        str: initated path.
    """
    return str(tmp_path_factory.mktemp("tmp", numbered=False) / "history.yaml")


@pytest.fixture(scope="module")
def path2yaml_touched(path2yaml):
    """Touch the ymal according to the given path.

    Args:
        path2yaml (str): path to a yaml file storing searching history. The
            file doesn't exist.

    Returns:
        str: same path. The file has been touched.
    """
    pathlib.Path(path2yaml).touch()
    assert pathlib.Path(
        path2yaml
    ).is_file(), "An empty yaml file should have been touched."
    return path2yaml


@pytest.fixture(scope="module")
def path2yaml_written(tmp_path_factory):
    """Initiate another path to a yaml file, touch and write it.

    Args:
        tmp_path_factory (TempPathFactory): pytest tool to initiate
            temporary a path.

    Returns:
        str: initated path. The yaml has been touched and written.
    """
    p = str(tmp_path_factory.mktemp("tmp2", numbered=False) / "history.yaml")
    pathlib.Path(p).touch()
    record("banana", p)

    assert pathlib.Path(p).is_file() and _read_yaml(p) == [
        "banana"
    ], "A yaml file should have been touched and written."

    return p


def test_record_no_file(path2yaml):
    """If to touch and write the specified yaml file.

    Args:
        path2yaml (str): path to a yaml file storing searching history. The
            file doesn't exist.
    """
    p = path2yaml
    assert not pathlib.Path(p).is_file(), "The yaml file is not touched."

    record("apple", p)
    assert pathlib.Path(p).is_file() and _read_yaml(p) == [
        "apple"
    ], "A yaml file should have been touched and written."


def test_record_written(path2yaml_written):
    """If to append the specified yaml file when there is content.

    Args:
        path2yaml_written (str): initated path, and the file has been
            touched and written.
    """
    p = path2yaml_written
    record("apple", p)
    words = _read_yaml(p)
    assert "apple" in words and "banana" in words


def test_record_no_content(path2yaml_touched):
    """If to append the specified yaml file when there is no content.

    Args:
        path2yaml_touched (str): initated path, and the file has been
            touched.
    """
    p = path2yaml_touched
    record("apple", p)
    assert _read_yaml(p) == ["apple"]


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
