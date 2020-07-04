"""Functions for seaching in command line."""
import click

from e2c.db_connector import DBConnector


@click.command()
@click.argument("word")
def search(word):
    """Type in one English word and echo its Chinese translation.

    Args:
        word (str): one English word to be searched. For example, "a
        lot" or "mirror".
    """
    res = DBConnector().query(word)
    click.echo("\n" + res["definition"] + "\n\n" + res["trans"])


if __name__ == "__main__":
    search()
