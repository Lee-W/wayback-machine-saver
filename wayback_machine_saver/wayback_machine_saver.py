from random import randint
from time import sleep
from urllib.parse import parse_qs, urlencode, urljoin, urlparse, urlunparse

import httpx

from wayback_machine_saver.config import (
    _REMOVED_URL_QUERY,
    HTTPX_TIMEOUT,
    WAYBACK_MACHINE_SAVER_RETRY_TIMES,
)

INTERNET_ARCHIVE_DOMAIN = "https://web.archive.org/"
INTERNET_ARCHIVE_SAVE_URL = urljoin(INTERNET_ARCHIVE_DOMAIN, "save/")
INTERNET_ARCHIVE_WEB_URL = urljoin(INTERNET_ARCHIVE_DOMAIN, "web/")


def clean_url(url: str) -> str:
    url_parse_result = urlparse(url)
    query = {
        key: value
        for key, value in parse_qs(url_parse_result.query).items()
        if key not in _REMOVED_URL_QUERY
    }
    url = urlunparse(url_parse_result._replace(query=urlencode(query, True)))
    return url


def save_page(
    url: str, remaining_retry_times: int = WAYBACK_MACHINE_SAVER_RETRY_TIMES
) -> httpx.Response:
    remaining_retry_times = remaining_retry_times - 1
    url = clean_url(url)

    req_url = f"{INTERNET_ARCHIVE_SAVE_URL}/{url}"
    try:
        req = httpx.post(req_url, data={"url": url, "capture_all": "on"})
    except httpx.ConnectTimeout:
        raise
    except Exception:
        if remaining_retry_times:
            req = save_page(url, remaining_retry_times)

    if req.status_code == 429:
        random_seconds = randint(1, 20)
        print(f"\nWait for {random_seconds} seconds")
        sleep(random_seconds)

        if remaining_retry_times:
            req = save_page(url, remaining_retry_times)
    elif req.status_code != 200:
        if remaining_retry_times:
            req = save_page(url, remaining_retry_times)

    return req


def get_latest_archive(
    url: str, remaining_retry_times: int = WAYBACK_MACHINE_SAVER_RETRY_TIMES
) -> httpx.Response:
    remaining_retry_times = remaining_retry_times - 1
    url = clean_url(url)

    try:
        req = httpx.get(f"{INTERNET_ARCHIVE_WEB_URL}{url}", timeout=HTTPX_TIMEOUT)
    except httpx.ReadTimeout:
        url = str(httpx.get(url).url)
        req = httpx.get(f"{INTERNET_ARCHIVE_WEB_URL}{url}", timeout=HTTPX_TIMEOUT)

    if req.status_code == 429:
        random_seconds = randint(1, 20)
        print(f"\nWait for {random_seconds} seconds")
        sleep(random_seconds)

        if remaining_retry_times:
            req = get_latest_archive(url, remaining_retry_times)
    elif req.url == INTERNET_ARCHIVE_DOMAIN:
        url = str(httpx.get(url).url)
        if remaining_retry_times:
            req = get_latest_archive(url, remaining_retry_times)
    return req
