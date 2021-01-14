"""Functions to handle highlights in PDF files."""
import fitz

from cmdict.ecdict_connector import ECDICTConnector
from cmdict.utils import remove_punctuation


# Mac OS Preview supported colors
PREVIEW_COLORS = {
    "yellow": [250, 205, 90],
    "green": [124, 200, 104],
    "blue": [105, 176, 241],
    "pink": [251, 92, 137],
    "purple": [200, 133, 218],
}

PDF_ANNOT_HIGHLIGHT = 8


def extract_words(file_path, color):
    """Extract highlighted words with specified color in a PDF file.

    Args:
        file_path (str): target file path.
        color (str): target color name.

    Returns:
        list[str]: list of found words.
    """
    if color.lower() not in PREVIEW_COLORS:
        return []

    res = set()
    document = fitz.open(file_path)
    for annot in _iterate_filtered_annotations(document, color):
        # annotation may contain several rectangles in different rows
        word_list = []
        rect_counts = len(annot.vertices) // 4
        for i in range(rect_counts):
            for word_block in _iterate_all_word_blocks(document):
                if _check_contain(
                    (annot.vertices[i * 4] + annot.vertices[i * 4 + 3]),
                    word_block[:4],
                ):
                    word_list.append(word_block[4])

        for word in _fix_hyphen_broken(word_list):
            res.add(remove_punctuation(word))

    return res


def _iterate_all_word_blocks(document):
    """Iterate word blocks in order from the document.

    Args:
        document (fitz.Document): the document.

    Yields:
        tuple: word block.
    """
    for page in document:
        for wb in sorted(page.getText("words"), key=lambda w: (w[1], w[0])):
            yield wb


def _iterate_filtered_annotations(document, color):
    """Iterate Annotations that are highlighted by target color.

    Args:
        document (fitz.Document): the document.
        color (str): targeted color.

    Yields:
        fitz.Annot: the annotation.
    """
    for page in document:
        for annotation in page.annots():
            if (
                annotation.type[0] == PDF_ANNOT_HIGHLIGHT
                and _get_color_name(annotation.colors["stroke"]) == color
            ):
                yield annotation


def _get_color_name(rgb):
    """Get the color name by rgb values.

    Args:
        rgb (list[float]): color as RGB scaled by [0...1].

    Returns:
        (str, None): color name, or None if the color is not
            currently supported.
    """
    origin_rgb = [round(v * 255) for v in rgb]

    for color_name in PREVIEW_COLORS:
        if origin_rgb == PREVIEW_COLORS[color_name]:
            return color_name

    return None


def _check_contain(rect_a, rect_b, threshold=0.75):
    """If rect_a and rect_b overlap rate above the threshold.

    Rectangular: (x_top_left, y_top_left, x_bottom_right, y_bottom_right)

    Args:
        rect_a (tuple): rectangular a
        rect_b (tuple): rectangular b
        threshold (float): threshold to control the overlap rate.

    Returns:
        bool: whether rect_a and rect_b overlap rate above the threshold.
    """
    x_a1, y_a1, x_a2, y_a2 = rect_a
    x_b1, y_b1, x_b2, y_b2 = rect_b

    if x_a1 >= x_b2 or x_b1 >= x_a2:
        return False
    elif y_a1 >= y_b2 or y_b1 >= y_a2:
        return False
    else:
        b_area = (y_b2 - y_b1) * (x_b2 - x_b1)
        overlap_area = (min(y_a2, y_b2) - max(y_a1, y_b1)) * (
            min(x_a2, x_b2) - max(x_a1, x_b1)
        )
        return (overlap_area / b_area) > threshold


def _fix_hyphen_broken(word_list):
    """Fix sequential broken word due to line change for a word list.

    For example: 'pro-' + 'ducer' should be 'producer'

    Args:
        word_list (list[str]): a list of words.

    Returns:
        list[str]: a list of words after fixing hyphen broken cases.
    """
    if len(word_list) < 2:
        return word_list

    res = []
    db_engine = ECDICTConnector()

    i = 0
    while i < len(word_list) - 1:
        w1, w2 = word_list[i], word_list[i + 1]
        combined = w1[:-1] + w2

        if w1.endswith("-") and db_engine.query(combined):
            res.append(combined)
            i += 1
        else:
            res.append(w1)
            if i == len(word_list) - 2:
                res.append(w2)
        i += 1

    return res
