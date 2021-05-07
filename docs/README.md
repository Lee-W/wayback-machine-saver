[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](http://makeapullrequest.com)
[![Conventional Commits](https://img.shields.io/badge/Conventional%20Commits-1.0.0-yellow.svg?style=flat-square)](https://conventionalcommits.org)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Github Actions](https://github.com/Lee-W/wayback-machine-saver/actions/workflows/python-check.yaml/badge.svg)](https://github.com/Lee-W/wayback-machine-saver/wayback-machine-saver/actions/workflows/python-check.yaml)
[![PyPI Package latest release](https://img.shields.io/pypi/v/wayback_machine_saver.svg?style=flat-square)](https://pypi.org/project/wayback_machine_saver/)
[![PyPI Package download count (per month)](https://img.shields.io/pypi/dm/wayback_machine_saver?style=flat-square)](https://pypi.org/project/wayback_machine_saver/)
[![Supported versions](https://img.shields.io/pypi/pyversions/wayback_machine_saver.svg?style=flat-square)](https://pypi.org/project/wayback_machine_saver/)

# Wayback Machine Saver

Python tool for archiving web pages through Internet Archive Wayback Machine

## Getting Started

### Prerequisites
* [Python](https://www.python.org/downloads/)
* [pipx](https://pipxproject.github.io/pipx/installation/)


## Installation

It's recommended to use tools like [pipx](https://pipxproject.github.io/pipx/installation/) to install this command-line tool.


```sh
pipx install wayback-machine-saver
```

## Usage

### Save pages

Save URLs from the input file to [Internet Archive - Wayback Machine](http://web.archive.org/)

```sh
wayback_machine_saver save-pages FILENAME
```

#### Argument
* FILENAME: filename to the file that consists of URLs to save

e.g.,

```txt
https://example.com
https://another-example.com
```

#### options

*  --deliminator TEXT         [default:  "\n"]
*  --error-log-filename TEXT  [default: save-pages-error-log-"timestamp".csv]

## Get latest archive urls
After the URLs have been saved, [Internet Archive - Wayback Machine](http://web.archive.org/) will snap-shot the page to their database and create a timestamp. You can access the latest one through `http://web.archive.org/web/[Your URL]` and it will be redirected to `http://web.archive.org/web/[timestamp]/[Your URL]`. This command is used to get the redirected URLs.

```sh
wayback_machine_saver get-latest-archive-urls FILENAME
```

#### Argument
* FILENAME: filename to the file that consists of URLs to retrieved

e.g.,

```txt
https://example.com
https://another-example.com
```

#### options

*  --deliminator TEXT         [default: "\n"]
*  --output-filename TEXT     [default: retrieved-urls-"timestamp".csv]]
*  --error-log-filename TEXT  [default: get-url-error-log-"timestamp".csv]

## Configuration

Wayback Machine Saves supports configurating through environment variable. You can run `export VARIABLE=VALUE` before running the script to change the behavior.

* WAYBACK_MACHINE_SAVER_RETRY_TIMES
    * times to retry (default: 3)
* HTTPX_TIMEOUT
    * timeout for all GET operations (default: 10)

## Contributing
See [Contributing](contributing.md)

## Authors
Wei Lee <weilee.rx@gmail.com>

Created from [Lee-W/cookiecutter-python-template](https://github.com/Lee-W/cookiecutter-python-template/tree/0.9.0) version 0.9.0
