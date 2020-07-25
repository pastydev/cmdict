"""Functions for reading words in txt files."""
from cmdict.utils import remove_punctuation


def scan_words(txt_path):
    """Scan all words in a txt file.

    Args:
        txt_path (str): to the txt file.

    Returns:
        list: containing all English words without any punctuation.
    """
    with open(txt_path, "r") as f:
        all_text = f.read()
        words = all_text.split()
    words = [remove_punctuation(w) for w in words]
    return words
