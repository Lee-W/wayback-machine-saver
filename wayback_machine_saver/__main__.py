import csv
from typing import List

import click
import httpx

from wayback_machine_saver import get_latest_archive, save_url


@click.group()
def main() -> None:
    pass


@main.command()
@click.argument("filename", type=click.Path(exists=True))
@click.option("--deliminator", type=str, default="\n")
def save_urls(filename: str, deliminator: str) -> None:
    with open(filename, "r") as input_file:
        urls = input_file.read().split(deliminator)

    failed_urls: List[str] = []
    with click.progressbar(urls) as urls_bar:
        for url in urls_bar:
            try:
                req = save_url(url)
            except (httpx.ConnectError, httpx.ConnectTimeout):
                click.echo(f"\nFailed on saving {url}", err=True)
                failed_urls.append(url)
            else:
                if req.status_code == 200:
                    click.echo(f"\nSucceeded on Saving {url}")
                else:
                    click.echo(
                        f"\nFailed on Saving {url}\nStatus code:{req.status_code}",
                        err=True,
                    )
                    failed_urls.append(url)

    if failed_urls:
        failed_urls_str = "\n".join(failed_urls)
        click.echo(
            f"\nFailed on the following urls: \n{failed_urls_str}",
            err=True,
        )


@main.command()
@click.argument("filename", type=click.Path(exists=True))
@click.option("--deliminator", type=str, default="\n")
@click.option(
    "--output-filename", type=str, default="retrieved_urls.csv", show_default=True
)
def get_latest_archive_url(
    filename: str, deliminator: str, output_filename: str
) -> None:
    with open(filename, "r") as input_file:
        urls = input_file.read().strip().split(deliminator)

    with click.progressbar(urls) as urls_bar:
        retrieved_urls: List[str] = []
        failed_urls: List[str] = []
        for url in urls_bar:
            click.echo(f"\nProcessing {url}")
            try:
                req = get_latest_archive(url)
                closest_archive_url: str = str(req.url)
            except httpx.ReadTimeout:
                click.echo(f"Failed on retrieving {url}", err=True)
                retrieved_urls.append("Not yet saved")
                failed_urls.append(url)
            except httpx.ConnectTimeout:
                click.echo(f"Failed on retrieving {url}", err=True)
                retrieved_urls.append("Connect time out")
                failed_urls.append(url)
            else:
                click.echo(f"Result URL: {closest_archive_url}")
                retrieved_urls.append(closest_archive_url)

    if failed_urls:
        failed_urls_str = "\n".join(failed_urls)
        click.echo(
            f"\nFailed on the following URLs: \n{failed_urls_str}",
            err=True,
        )

    if retrieved_urls:
        with open(output_filename, "w") as output_file:
            writer = csv.writer(output_file)

            writer.writerow(["Original URL", "Archived URL"])
            for url, retrieved_url in zip(urls, retrieved_urls):
                writer.writerow([url, retrieved_url])


if __name__ == "__main__":
    main()
