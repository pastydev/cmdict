"""Functions for seaching in command line."""
import click

from e2c.db_connector import DBConnector

_divider = "=" * 50


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
    click.echo(_divider)
    if res:
        click.echo(word + "\n" + res["definition"] + "\n\n" + res["trans"])
    else:
        click.echo("'" + word + "' can not be found in the database!")
    click.echo(_divider)


cli.add_command(search)
