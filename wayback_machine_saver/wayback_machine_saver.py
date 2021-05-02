from random import randint
from time import sleep
from urllib.parse import urlencode, urljoin, urlparse, urlunparse

import httpx

INTERNET_ARCHIVE_DOMAIN = "https://web.archive.org/"
INTERNET_ARCHIVE_SAVE_URL = urljoin(INTERNET_ARCHIVE_DOMAIN, "save/")
INTERNET_ARCHIVE_WEB_URL = urljoin(INTERNET_ARCHIVE_DOMAIN, "web/")


def save_page(url: str) -> httpx.Response:
    req_url = f"{INTERNET_ARCHIVE_SAVE_URL}/{url}"
    req = httpx.post(req_url, data={"url": url, "capture_all": "on"})
    if req.status_code == 429:
        random_seconds = randint(1, 20)
        print(f"\nWait for {random_seconds} seconds")
        sleep(random_seconds)

        req = save_page(url)
    return req


def get_latest_archive(url: str) -> httpx.Response:
    # Clean up query
    url = urlunparse(urlparse(url)._replace(query=urlencode({}, True)))
    try:
        req = httpx.get(f"{INTERNET_ARCHIVE_WEB_URL}{url}")
    except httpx.ReadTimeout:
        url = str(httpx.get(url).url)
        req = httpx.get(f"{INTERNET_ARCHIVE_WEB_URL}{url}")

    if req.status_code == 429:
        random_seconds = randint(1, 20)
        print(f"\nWait for {random_seconds} seconds")
        sleep(random_seconds)

        req = get_latest_archive(url)
    return req
