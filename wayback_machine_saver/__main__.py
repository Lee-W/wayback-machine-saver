import csv
from dataclasses import dataclass
from datetime import datetime
from time import sleep
from typing import List

import click
import httpx

from wayback_machine_saver.wayback_machine_saver import get_latest_archive, save_page


@dataclass
class FailedLog:
    url: str
    message: str


def _export_failed_log(failed_logs: List[FailedLog], error_log_filename: str) -> None:
    with open(error_log_filename, "w") as output_file:
        writer = csv.writer(output_file)

        writer.writerow(["Failed URL", "Log message"])
        for failed_log in failed_logs:
            writer.writerow([failed_log.url, failed_log.message])
    click.echo(f"\nFailed logs has been written into {error_log_filename}")


current_timestamp = datetime.now().strftime("%Y%m%d%H%M%S")


@click.group()
def main() -> None:
    pass


@main.command()
@click.argument("filename", type=click.Path(exists=True))
@click.option("--deliminator", type=str, default="\n", show_default=True)
@click.option(
    "--error-log-filename",
    type=str,
    default=f"save-pages-error-log-{current_timestamp}.csv",
    show_default=True,
)
def save_pages(filename: str, deliminator: str, error_log_filename: str) -> None:
    """Save URLs from input file to Internet Archive"""

    with open(filename, "r") as input_file:
        urls = input_file.read().strip().split(deliminator)

    failed_logs: List[FailedLog] = []
    with click.progressbar(urls) as urls_bar:
        for url in urls_bar:
            click.echo(f"\nProcessing {url}")
            try:
                req = save_page(url)
            except Exception as err:
                click.secho(
                    f"\nFailed on saving {url}\nError message: {err}",
                    err=True,
                    fg="red",
                )
                failed_logs.append(FailedLog(url, str(err)))
            else:
                if req.status_code == 200:
                    click.secho(f"Succeeded on Saving {url}", fg="green")
                else:
                    click.secho(
                        f"\nFailed on Saving {url}\nStatus code: {req.status_code}",
                        err=True,
                        fg="red",
                    )
                    failed_logs.append(
                        FailedLog(url, f"Status Code: {req.status_code}")
                    )

    if failed_logs:
        _export_failed_log(failed_logs, error_log_filename)


@main.command()
@click.argument("filename", type=click.Path(exists=True))
@click.option("--deliminator", type=str, default="\n", show_default=True)
@click.option(
    "--output-filename",
    type=str,
    default=f"retrieved-urls-{current_timestamp}.csv",
    show_default=True,
)
@click.option(
    "--error-log-filename",
    type=str,
    default=f"get-url-error-log-{current_timestamp}.csv",
    show_default=True,
)
def get_latest_archive_urls(
    filename: str, deliminator: str, output_filename: str, error_log_filename: str
) -> None:
    """Get the latest achived URLs from input file"""
    with open(filename, "r") as input_file:
        urls = input_file.read().strip().split(deliminator)

    with click.progressbar(urls) as urls_bar:
        retrieved_urls: List[str] = []
        failed_logs: List[FailedLog] = []
        for url in urls_bar:
            click.echo(f"\nProcessing {url}")
            try:
                req = get_latest_archive(url)
                latests_archive_url: str = str(req.url)
            except httpx.ReadTimeout as err:
                click.secho(f"Failed on retrieving {url}", err=True, fg="red")
                retrieved_urls.append("Possibly not yet saved")
                failed_logs.append(FailedLog(url, str(err)))
            except httpx.ConnectTimeout as err:
                click.secho(f"Failed on retrieving {url}", err=True, fg="red")
                retrieved_urls.append("Connect time out. Possibly a dead page.")
                failed_logs.append(FailedLog(url, str(err)))
            except Exception as err:
                click.secho(f"Failed on retrieving {url}", err=True, fg="red")
                retrieved_urls.append(str(err))
                failed_logs.append(FailedLog(url, str(err)))
            else:
                click.secho(f"Result URL: {latests_archive_url}", fg="green")
                retrieved_urls.append(latests_archive_url)
            sleep(1)

    if failed_logs:
        _export_failed_log(failed_logs, error_log_filename)

    if retrieved_urls:
        with open(output_filename, "w") as output_file:
            writer = csv.writer(output_file)

            writer.writerow(["Original URL", "Archived URL"])
            for url, retrieved_url in zip(urls, retrieved_urls):
                writer.writerow([url, retrieved_url])


if __name__ == "__main__":
    main()
