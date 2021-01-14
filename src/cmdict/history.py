"""Functions for recording and reading user history."""
import os
import pathlib

from loguru import logger
import yaml

_path = os.path.join(
    str(pathlib.Path(__file__).parent), "data", ".history.yaml"
)


def record(word, path=_path):
    """Append queried word in a yaml file in lowercase format.

    If the path is directed to yaml file, there will be three
    situations. When there is no such file, we create a new one
    according to the specified file name and write the word. When the
    file does exist, we read its content first.

    Args:
        word (str): to be appended at the end of the yaml file.
        path (str): to the yaml file.

    Raises:
        ValueError: when the path is not to a yaml file.
    """
    if not path.endswith(".yaml"):
        raise ValueError(f"{path} is not a path to yaml file.")

    if not pathlib.Path(path).is_file():
        with open(path, "w") as f:
            yaml.safe_dump([word], f)
    else:
        with open(path, "r") as f:
            try:
                hist = yaml.safe_load(f)
            except yaml.YAMLError as exc:
                logger.exception(exc)

        if hist is None:
            with open(path, "w") as f:
                yaml.safe_dump([word], f)
        elif word not in hist:
            with open(path, "a") as f:
                yaml.safe_dump([word], f)
