"""Functions for seaching in command line."""
import click
from colorama import Fore, Style
from colorama import init as _init_colorama

from e2c.db_connector import DBConnector
from e2c.pdf_tools import (
    _check_new_color,
    _compare_color,
    _extract_annot,
    _open_file,
)


_init_colorama(autoreset=True)

_divider = Fore.WHITE + "-" * 8


def _tab_echo(s, tabs=4):
    """Echo via click with tabs at the beginning.

    Args:
        s (str): The string.
        tabs (int, optional): Tabs before the string. Defaults to 4.
    """
    click.echo(tabs * " " + s)


@click.group()
def cli():
    """Command line interface."""


@click.command()
@click.argument("words", nargs=-1)
def search(words):
    """Type in one English word and echo its Chinese translation.

    Args:
        words (str): one English word to be searched. For example,
            "a lot" or "mirror".
    """
    engine = DBConnector()
    for i, word in enumerate(words):
        _echo_item(word, engine.query(word))


def _echo_item(word, res):
    """Echo word search result to cli.

    Args:
        word (str): The word.
        res (dict): The search result.
    """
    click.echo(_divider)
    if res:
        click.echo(Fore.CYAN + Style.BRIGHT + word + "\n")
        for k in res:
            if k in ("definition", "trans"):
                items = res[k].split("\n")
                _tab_echo(str(k) + ": ")
                for item in items:
                    _tab_echo("- " + item, tabs=8)
            elif k in ("phonetic", "collins", "oxford", "bnc", "frq"):
                _tab_echo(str(k) + ": " + str(res[k]))
    else:
        click.echo(
            Fore.RED
            + Style.BRIGHT
            + word
            + Style.RESET_ALL
            + " can not be found in the database!"
        )


@click.command()
@click.argument("pdf_path", type=click.Path(exists=True))
@click.argument("color")
def extract(pdf_path, color):
    """Extract highlights with the specified color in a PDF file.

    You can use ``e2c colors('path/to/PDF/file')`` first to
    obtain list of colors in the PDF file.

    Args:
        pdf_path (str): to the PDF file.
        color (List[float]): three numbers ranging between 0 and 1.

    Raises:
        ValueError: when the input `color` is not a list after
            evaluation.
        ValueError: when there is no highlight found.
    """
    # turn the input string to a Python list.
    color = eval(color)
    if not isinstance(color, list):
        raise ValueError("Incorrect way to specify the highlight color!")

    doc = _open_file(pdf_path)
    sentences = {}
    i = 0
    for page in doc:
        words_on_page = page.getText("words")  # list of words on page
        words_on_page.sort(key=lambda w: (w[3], w[0]))  # ascending y, then x

        annot = page.firstAnnot
        while annot:
            if annot.type[
                0
            ] == 8 and _compare_color(  # The annotation is a highlight.
                annot.colors["stroke"], color
            ):
                sentences[i] = _extract_annot(annot, words_on_page)
            annot = annot.next  # None returned after last annotation.
            i += 1

    # print the result for now.
    if len(sentences) == 0:
        raise ValueError(
            "Possibly wrong way to specify the highlight color! "
            "Because nothing is extracted."
        )
    else:
        click.echo(sentences)


@click.command()
@click.argument("path", type=click.Path(exists=True))
def colors(path):
    """List colors of highlights in the PDF file.

    Args:
        path (str): to the PDF file.
    """
    doc = _open_file(path)
    colors = {0: [0, 0, 0]}
    for page in doc:
        annot = page.firstAnnot
        while annot:
            if annot.type[0] == 8:  # The annotation is a highlight.
                colors = _check_new_color(annot.colors["stroke"], colors)
            annot = annot.next

    del colors[0]
    for color in list(colors.values()):
        click.echo(color)


cli.add_command(search)
cli.add_command(colors)
cli.add_command(extract)
