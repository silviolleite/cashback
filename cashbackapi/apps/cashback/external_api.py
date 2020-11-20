import logging
from urllib.parse import urljoin

import requests

logger = logging.getLogger(__name__)


class CashbackAPIClient:

    def __init__(self, base_url, token):
        self.base_url = base_url
        self.token = token
        self.headers = {"token": self.token}

    endpoints = {
        "fetch": "v1/cashback?cpf={}",
    }

    def fetch(self, document):
        logger.info("Fetching external API")
        url = self.get_url("fetch", document)
        return requests.get(url, headers=self.headers)

    def get_url(self, key, *parts):
        logger.info(f"Mounting the external API endpoint, key={key}")
        endpoint = self.endpoints.get(key, "").format(*parts)
        logger.debug(f"Endpoint mounted is {endpoint}")

        if not endpoint:
            msg = f"No endpoint match for key={key}"
            logger.error(msg)
            raise ValueError(msg)

        if not self.base_url.endswith("/"):
            self.base_url = "/"

        url = urljoin(self.base_url, endpoint)

        logger.info("Returning the mounted endpoint")
        logger.debug(f"Mounted URL: {url}")
        return url
