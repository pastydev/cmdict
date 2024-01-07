# cmdict &middot; [![pypi](https://badge.fury.io/py/cmdict.svg)](https://pypi.org/project/cmdict/) [![GitHub license](https://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/zequnyu/cmdict/blob/master/LICENSE) [![CI](https://github.com/pasty-dev/cmdict/actions/workflows/ci.yml/badge.svg)](https://github.com/pasty-dev/cmdict/actions/workflows/ci.yml) [![codecov](https://codecov.io/gh/zequnyu/cmdict/branch/master/graph/badge.svg)](https://codecov.io/gh/zequnyu/cmdict) [![poetry](https://img.shields.io/badge/PyPM-poetry-5975aa)](https://python-poetry.org) [![black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

`cmdict` not only is an English-to-Chinese dictionary application with a command-line interface, but also provide out-of-box features like extracting highlighted words from a PDF file. It runs on Linux, macOS, and Windows. Additionally, it can be used as a Python package.

## How to install

The easiest way is to use [Homebrew](https://brew.sh/):

```sh
brew install pastydev/cmdict/cmdict
```

To install it from [PyPI](https://pypi.org/project/cmdict/):

```sh
pip install cmdict
```

## How to use

```console
$ cmdict --help
Usage: cmdict [OPTIONS] COMMAND [ARGS]...

  Command line interface.

Options:
  --help  Show this message and exit.

Commands:
  download  Download necessary database before using cmdict.
  extract   Extract highlighted words with specified color in a PDF file.
  scan      Scan all words in a txt file and return search results.
  search    Type in one English word and echo its Chinese translation.
```

To echo Chinese translation for one or multiple English words.

```console
$ cmdict search apple
--------
apple

    phonetic: 'æpl
    definition:
        - n. fruit with red or yellow or green skin and sweet to tart crisp whitish flesh
        - n. native Eurasian tree widely cultivated in many varieties for its firm rounded edible fruits
    trans:
        - n. 苹果, 家伙
        - [医] 苹果
    collins: 3
    oxford: 1
    bnc: 2446
    frq: 2695
```

```console
$ cmdict search apple banana
```

To extract highlighted words in blue of `sample.pdf`:

```console
$ cmdict extract sample.pdf --color blue
--------
apple

    phonetic: 'æpl
    definition:
        - n. fruit with red or yellow or green skin and sweet to tart crisp whitish flesh
        - n. native Eurasian tree widely cultivated in many varieties for its firm rounded edible fruits
    trans:
        - n. 苹果, 家伙
        - [医] 苹果
    collins: 3
    oxford: 1
    bnc: 2446
    frq: 2695
```

## Data support

- [`skywind3000/ECDICT`](https://github.com/skywind3000/ECDICT/releases): a free English to Chinese dictionary database (英中双解词典数据库).

```console
$ cmdict download
--------
Downloading the dictionary...
100%|████████████████████████| 217M/217M [00:29<00:00, 666MiB/s]

cmdict is ready to use!
```

## How to contribute

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://github.com/codespaces/new?hide_repo_select=true&ref=master&repo=266903250&machine=largePremiumLinux&location=WestEurope)
