"""Utility functions."""
import string

SPECIAL_CHARS = "“”"


def remove_punctuation(s):
    """Remove all kinds of punctuations in the string.

    Args:
        s (str): to be removed from punctuations.

    Returns:
        str: with all kinds of punctuation removed.
    """
    table = str.maketrans("", "", string.punctuation + SPECIAL_CHARS)
    return s.translate(table)
