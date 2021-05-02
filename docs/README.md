[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](http://makeapullrequest.com)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

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
*  --error-log-filename TEXT  [default: error-log.csv]

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
*  --output-filename TEXT     [default: retrieved_urls.csv]
*  --error-log-filename TEXT  [default: error-log.csv]

## Contributing
See [Contributing](contributing.md)

## Authors
Wei Lee <weilee.rx@gmail.com>

Created from [Lee-W/cookiecutter-python-template](https://github.com/Lee-W/cookiecutter-python-template/tree/0.9.0) version 0.9.0
