import time
import requests
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type,
)
from requests.exceptions import RequestException
from config import USER_AGENT, REQUEST_DELAY, MAX_RETRIES, TIMEOUT


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
