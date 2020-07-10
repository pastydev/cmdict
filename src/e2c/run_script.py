"""Functions for seaching in command line."""
import os
import textwrap

import click
from colorama import Fore, Style
from colorama import init as _init_colorama
from tabulate import tabulate

from e2c.db_connector import DBConnector


_init_colorama(autoreset=True)
_headers = ["collins", "oxford", "bnc", "frq"]


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

    # Avoid the error during tests caused by `os` module.
    try:
        _terminal_size = os.get_terminal_size()[0]
    except Exception:
        _terminal_size = 20

    for i, word in enumerate(words):
        _echo_item(word, engine.query(word), _terminal_size)


def _echo_item(word, res, _terminal_size):
    """Echo word search result to cli.

    Args:
        word (str): The word.
        res (dict): The search result.
        _terminal_size (str): The size of the current terminal.
    """
    _divider = Fore.WHITE + "-" * _terminal_size
    click.echo(_divider)
    if res:
        click.echo(Fore.CYAN + Style.BRIGHT + word + "\n")

        # Print the table for attributes of the word.
        msg = tabulate(
            [[res.get(key) for key in _headers]],
            headers=_headers,
            tablefmt="pretty",
        )
        msg = msg.split("\n")
        msg = [4 * " " + m for m in msg]
        for m in msg:
            click.echo(m)
        click.echo("")

        for k in res:
            if k in ("definition", "trans"):
                items = res[k].split("\n")
                _tab_echo(str(k) + ": ")
                for item in items:
                    item = textwrap.fill(item, _terminal_size - 10)
                    item = item.split("\n")
                    _tab_echo("- " + item[0], tabs=8)
                    if len(item) > 1:
                        for i in item[1 : len(item)]:
                            _tab_echo(i, tabs=10)
            elif k in ("phonetic"):
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
