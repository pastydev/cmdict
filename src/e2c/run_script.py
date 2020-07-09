"""Functions for seaching in command line."""
import click
from colorama import Fore, Style
from colorama import init as _init_colorama

from e2c.db_connector import DBConnector


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


cli.add_command(search)
