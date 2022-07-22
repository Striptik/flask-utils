import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


def custom_request(url, method, headers=None, json=None, timeout=(5, 20), connect_retry=3):
    session = requests.Session()
    retry = Retry(connect=connect_retry, backoff_factor=0.5)
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("https://", adapter)
    session.mount("http://", adapter)
    return session.request(
        headers=headers,
        method=method,
        timeout=timeout,
        url=url,
        json=json,
    )
