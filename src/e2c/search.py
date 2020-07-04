# coding=utf-8

"""
This is an example script.

It seems that it has to have THIS docstring with a summary line, a blank line
and sume more text like here. Wow.
"""
import click

from e2c.db_connector import DBConnector


@click.command()
@click.argument("word")
def search(word):
    """Type in English words and return Chinese translations."""
    res = DBConnector(".../db/stardict-short.db").search(word)
    print(res)


# if __name__ == "__main__":
#     search()
