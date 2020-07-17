"""Functions to handle highlights in PDF files.

`e2c colors` should be used first to find all colors of highlights in
the given PDF file. Then `e2c extract` can select all words of those
highlights with the specified color.
"""
import pathlib
import re
import string

import fitz
import numpy as np
from textblob import Word

_threshold_color = 0.000001  # if two colors are different.
_threshold_spell = 0.99  # if the word is spelled correctly.
_threshold_intersection = 0.9  # if the intersection is large enough.
_specials = "“" + "”"  # Some special punctuations to be removed.


def _remove_punctuation(s):
    """Remove all kinds of punctuations in the string.

    Args:
        s (str): to be removed from punctuations.

    Returns:
        str: with all kinds of punctuation removed.
    """
    table = str.maketrans({a: None for a in string.punctuation + _specials})
    return s.translate(table)


def _check_contain(rect_word, points):
    """If `rect_word` is contained in the rectangular area.

    The area of the intersection should be large enough compared to the
    area of the given word.

    Args:
        rect_word (fitz.Rect): rectangular area of a single word.
        points (list): list of points in the rectangular area of the
            given part of a highlight.

    Returns:
        bool: whether `rect_word` is contained in the rectangular area.
    """
    # `r` is mutable, so everytime a new `r` should be initiated.
    r = fitz.Quad(points).rect
    r.intersect(rect_word)

    if r.getArea() >= rect_word.getArea() * _threshold_intersection:
        contain = True
    else:
        contain = False
    return contain


def _extract_annot(annot, words_on_page):
    """Extract words in a given highlight.

    Args:
        annot (fitz.Annot): [description]
        words_on_page (list): [description]

    Returns:
        str: words in the entire highlight.
    """
    quad_points = annot.vertices
    quad_count = int(len(quad_points) / 4)
    sentences = ["" for i in range(quad_count)]
    for i in range(quad_count):
        points = quad_points[i * 4 : i * 4 + 4]  # noqa: E203
        words = [
            w
            for w in words_on_page
            if _check_contain(fitz.Rect(w[:4]), points)
        ]
        sentences[i] = " ".join(w[4] for w in words)
    sentence = " ".join(sentences)

    sentence = _recover_broken(sentence)
    sentence = _remove_punctuation(sentence)
    return sentence


def _recover_broken(s):
    """Recover broken words resulted from line wrapping.

    Note that word with necessary hyphens will be detected to be
    broken as well. So all recovered words will be checked for being
    meaningful English words.

    Args:
        s (str): whole long string to be recovered.

    Returns:
        str: long string with broken words recovered.
    """
    brokens = re.findall(r"\w+- \w+", s)
    recovered = s
    for m in brokens:
        new = m.replace("- ", "")
        w = Word(new)
        if w.spellcheck()[0][1] >= _threshold_spell:
            recovered = recovered.replace(m, new)
    return recovered


def _open_file(path):
    """Try to open the PDF file.

    Args:
        path (str): to the PDF file.

    Returns:
        fitz.Document: the target PDF file.

    Raises:
        ValueError: when the path is not directed to a PDF file.
    """
    if pathlib.Path(path).is_file() and path.endswith(".pdf"):
        doc = fitz.open(path)
        return doc
    else:
        raise ValueError("No such PDF file.")


def _compare_color(c1, c2):
    """Check if two colors are the same.

    Args:
        c1 (List[float]): three float value betweening 0 and 1 of the
            first color.
        c2 (List[float]): three float value betweening 0 and 1 of the
            second color.

    Returns:
        bool: true if two colors are the same.
    """
    diff = sum([np.abs(c1[i] - c2[i]) for i in range(3)])
    return diff <= _threshold_color


def _check_new_color(new, colors):
    """Check if the color is not within the list of colors.

    Args:
        new (List[float]): three float value betweening 0 and 1.
        colors (List[List[float]]): list of recorded colors.

    Returns:
        List[List[float]]: new list of recorded colors.
    """
    _found = False
    for c in list(colors.values()):
        if _compare_color(new, c):
            _found = True
    if not _found:
        colors[len(colors) + 1] = new
    return colors
