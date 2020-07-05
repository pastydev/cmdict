"""Functions for seaching in command line."""
import click

from e2c.db_connector import DBConnector

_divider = "=" * 50


@click.group()
def cli():
    """Command line interface."""
    pass


@click.command()
@click.argument("word")
def search(word):
    """Type in one English word and echo its Chinese translation.

    Args:
        word (str): one English word to be searched. For example,
            "a lot" or "mirror".
    """
    res = DBConnector().query(word)
    click.echo(_divider + "\n" + word)
    click.echo(res["definition"] + "\n\n" + res["trans"] + "\n" + _divider)


cli.add_command(search)
