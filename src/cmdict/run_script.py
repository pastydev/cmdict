"""Functions for seaching in command line."""
import os
import pathlib
import zipfile

import click
from colorama import Fore, Style
from colorama import init as _init_colorama
import requests
from tqdm import tqdm
import yaml

from cmdict.ecdict_connector import ECDICTConnector
from cmdict.pdf_tools import extract_words
from cmdict.txt_tools import scan_words

DB_URL = "https://github.com/skywind3000/ECDICT/releases/download/1.0.28/ecdict-sqlite-28.zip"  # noqa: E501
DB_VALID_SIZE = (851288064, 17408)  # (full size, test size)

_init_colorama(autoreset=True)

_db_dir = os.path.join(str(pathlib.Path(__file__).parent), "data")
_db_file = os.path.join(_db_dir, "stardict.db")
_db_path = pathlib.Path(_db_file)


@click.group()
def cli():
    """Command line interface."""


@cli.command()
def download():
    """Download necessary database before using cmdict."""
    # check if data folder needs to be created
    data_dir_path = pathlib.Path(_db_dir)
    if not data_dir_path.exists():
        data_dir_path.mkdir(parents=True)

    db_zip = os.path.join(_db_dir, "stardict.zip")

    _echo_divider()
    if _valid_db_exists():
        _echo_ready()
    else:
        try:
            click.echo("Downloading the dictionary...")
            r = requests.get(DB_URL, stream=True)
            total_size = int(r.headers.get("content-length", 0))
            block_size = 1024

            with tqdm(total=total_size, unit="iB", unit_scale=True) as t, open(
                db_zip, "wb"
            ) as f:
                for data in r.iter_content(block_size):
                    t.update(len(data))
                    f.write(data)

            with zipfile.ZipFile(db_zip, "r") as ref:
                ref.extractall(_db_dir)

            _echo_ready()
        except Exception:
            click.echo(
                "\n"
                + Fore.RED
                + Style.BRIGHT
                + "Something went wrong! Please try again."
            )
        finally:
            zip_path = pathlib.Path(db_zip)
            if zip_path.is_file():
                zip_path.unlink()
            if (
                _db_path.is_file()
                and _db_path.stat().st_size not in DB_VALID_SIZE
            ):
                _db_path.unlink()


@cli.command()
@click.argument("words", nargs=-1)
def search(words):
    """Type in one English word and echo its Chinese translation.

    Args:
        words (str): one English word to be searched. For example,
            "a lot" or "mirror".
    """
    if _valid_db_exists():
        db_engine = ECDICTConnector()
        for i, word in enumerate(words):
            _echo_item(word, db_engine.query(word))
    else:
        _echo_warn_download()


@cli.command()
@click.argument("txt_path", type=click.Path(exists=True))
def scan(txt_path):
    """Scan all words in a txt file and return search results.

    Args:
        txt_path (str): path to the txt file.
    """
    if _valid_db_exists():
        db_engine = ECDICTConnector()
        words = scan_words(txt_path)
        for i, word in enumerate(words):
            _echo_item(word, db_engine.query(word))
    else:
        _echo_warn_download()


@cli.command()
@click.argument("pdf_path", type=click.Path(exists=True))
@click.option(
    "--color",
    default="yellow",
    help="Which color the highlights are in.",
    show_default=True,
)
@click.option(
    "--save", "-s", is_flag=True, help="Whether to save extracted words."
)
def extract(pdf_path, color, save):
    """Extract highlighted words with specified color in a PDF file.

    Args:
        pdf_path (str): path to the PDF file.
        color (str): three numbers ranging between 0 and 1.
        save (bool): if extracted words will be saved in yaml file.
    """
    if _valid_db_exists():
        db_engine = ECDICTConnector()
        words = extract_words(pdf_path, color)

        if save:
            with open(_db_dir + "/.extraction.yaml", "w") as f:
                yaml.safe_dump(list(words), f)

        for i, word in enumerate(words):
            _echo_item(word, db_engine.query(word))
    else:
        _echo_warn_download()


def _tab_echo(s, tabs=4):
    """Echo via click with tabs at the beginning.

    Args:
        s (str): The string.
        tabs (int, optional): Tabs before the string. Defaults to 4.
    """
    click.echo(tabs * " " + s)


def _echo_item(word, res):
    """Echo word search result to cli.

    Args:
        word (str): The word.
        res (dict): The word search result.
    """
    _echo_divider()
    if res:
        click.echo(Fore.CYAN + Style.BRIGHT + word + "\n")
        for k in res:
            if k in ("definition", "trans"):
                if res[k]:
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


def _valid_db_exists():
    """Return if a valid database is found.

    Returns:
        bool: if a valid database is found.
    """
    return _db_path.is_file() and _db_path.stat().st_size in DB_VALID_SIZE


def _echo_divider():
    """Echo cmdict divider."""
    click.echo(Fore.WHITE + "-" * 8)


def _echo_warn_download():
    """Echo cmdict needs download before use."""
    _echo_divider()
    click.echo(
        Fore.RED
        + Style.BRIGHT
        + "Database does not exist! Please download: `cmdict download`."
    )


def _echo_ready():
    """Echo cmdict is ready to use."""
    click.echo("\n" + Fore.GREEN + Style.BRIGHT + "cmdict is ready to use!")
