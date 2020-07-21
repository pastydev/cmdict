"""Functions to handle highlights in PDF files."""
import string

import fitz

# Mac OS Preview supported colors
PREVIEW_COLORS = {
    "yellow": [250, 205, 90],
    "green": [124, 200, 104],
    "blue": [105, 176, 241],
    "pink": [251, 92, 137],
    "purple": [200, 133, 281],
}

PDF_ANNOT_HIGHLIGHT = 8
SPECIAL_CHARS = "“”"


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
    for page in fitz.open(file_path):
        for word_tuple in sorted(
            page.getText("words"), key=lambda w: (w[1], w[0])
        ):
            if word_tuple[4] in res:
                continue

            for annotation in page.annots():
                if (
                    annotation.type[0] == PDF_ANNOT_HIGHLIGHT
                    and _get_color_name(annotation.colors["stroke"]) == color
                    and _check_contain(
                        word_tuple[:4],
                        annotation.vertices[0] + annotation.vertices[3],
                    )
                ):
                    print(annotation.colors["stroke"])
                    res.add(_remove_punctuation(word_tuple[4]))
    return res


def _get_color_name(rgb):
    """Get the color name by rgb values.

    Args:
        rgb ([float]): Color as RGB scaled by [0...1].

    Returns:
        (str, None): color name, or None if the color is not
            currently supported.
    """
    origin_rgb = [round(v * 255) for v in rgb]

    for color_name in PREVIEW_COLORS:
        if origin_rgb == PREVIEW_COLORS[color_name]:
            return color_name

    return None


def _check_contain(rect_a, rect_b, threshold=0.9):
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
        b_area = (y_b2 - y_b1) * (y_a2 - y_a1)
        overlap_area = (min(y_a2, y_b2) - max(y_a1, y_b1)) * (
            min(x_a2, x_b2) - max(x_a1, x_b1)
        )
        return (overlap_area / b_area) > threshold


def _remove_punctuation(s):
    """Remove all kinds of punctuations in the string.

    Args:
        s (str): to be removed from punctuations.

    Returns:
        str: with all kinds of punctuation removed.
    """
    table = str.maketrans("", "", string.punctuation + SPECIAL_CHARS)
    return s.translate(table)
