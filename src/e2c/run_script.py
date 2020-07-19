"""Functions for seaching in command line."""
import click
from colorama import Fore, Style
from colorama import init as _init_colorama

from e2c.db_connector import DBConnector
from e2c.pdf_tools import extract_words


_init_colorama(autoreset=True)

_divider = Fore.WHITE + "-" * 8
_engine = DBConnector()


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


@cli.command()
@click.argument("words", nargs=-1)
def search(words):
    """Type in one English word and echo its Chinese translation.

    Args:
        words (str): one English word to be searched. For example,
            "a lot" or "mirror".
    """
    for i, word in enumerate(words):
        _echo_item(word)


@cli.command()
@click.argument("pdf_path", type=click.Path(exists=True))
@click.option("--color", default="yellow", show_default=True)
def extract(pdf_path, color):
    """Extract highlighted words with specified color in a PDF file.

    Args:
        pdf_path (str): path to the PDF file.
        color (str): three numbers ranging between 0 and 1.
    """
    words = extract_words(pdf_path, color)
    for i, word in enumerate(words):
        _echo_item(word)


def _echo_item(word):
    """Echo word search result to cli.

    Args:
        word (str): The word.
    """
    res = _engine.query(word)

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
