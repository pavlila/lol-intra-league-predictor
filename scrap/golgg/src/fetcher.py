import time

import requests
from requests.exceptions import RequestException
from tenacity import (
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)

from config import MAX_RETRIES, REQUEST_DELAY, TIMEOUT, USER_AGENT


class Fetcher:
    def __init__(self, delay=REQUEST_DELAY, user_agent=USER_AGENT, timeout=TIMEOUT):
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": user_agent})
        self.delay = delay
        self.timeout = timeout

    @retry(
        stop=stop_after_attempt(MAX_RETRIES),
        wait=wait_exponential(min=1, max=10),
        retry=retry_if_exception_type(RequestException),
    )
    def get(self, url):
        resp = self.session.get(url, timeout=self.timeout)
        if resp.status_code >= 500:
            resp.raise_for_status()
        time.sleep(self.delay)
        return resp
