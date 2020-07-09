"""Functions for seaching in command line."""
import click
from colorama import Fore, Style
from colorama import init as _init_colorama

from e2c.db_connector import DBConnector


_init_colorama(autoreset=True)

_divider = Fore.WHITE + "-" * 4


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
@click.argument("word")
def search(word):
    """Type in one English word and echo its Chinese translation.

    Args:
        word (str): one English word to be searched. For example,
            "a lot" or "mirror".
    """
    res = DBConnector().query(word)
    _tab_echo(_divider)
    if res:
        _tab_echo(Fore.CYAN + Style.BRIGHT + word + "\n")
        for k in res:
            if k in ("definition", "trans"):
                items = res[k].split("\n")
                _tab_echo(str(k) + ": ")
                for item in items:
                    _tab_echo("- " + item, tabs=8)
            elif k in ("phonetic", "collins", "oxford", "bnc", "frq"):
                _tab_echo(str(k) + ": " + str(res[k]))
    else:
        _tab_echo(
            Fore.RED
            + Style.BRIGHT
            + word
            + Style.RESET_ALL
            + " can not be found in the database!"
        )
    _tab_echo(_divider)


cli.add_command(search)
