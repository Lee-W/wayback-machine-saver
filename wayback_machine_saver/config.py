import os

WAYBACK_MACHINE_SAVER_RETRY_TIMES = int(
    os.environ.get("WAYBACK_MACHINE_SAVER_RETRY_TIMES", 3)
)

HTTPX_TIMEOUT = int(os.environ.get("HTTPX_TIMEOUT", 10))
_REMOVED_URL_QUERY = ["fbclid"]
