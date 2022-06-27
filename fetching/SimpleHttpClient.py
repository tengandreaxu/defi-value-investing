import requests
from typing import Optional
from dataclasses import dataclass


class Endpoints:
    DEFI_LLAMA_PROTOCOL_TVL = "https://api.llama.fi/protocol/"
    COINGECKO_MARKET_CHART = "https://api.coingecko.com/api/v3/coins/{}/market_chart"
    TOKEN_TERMINAL_IDS = "https://api.tokenterminal.com/v2/projects"
    TOKEN_TERMINAL_METRICS = "https://api.tokenterminal.com/v2/projects/{}/metrics"


class SimpleHttpClient:
    def __init__(self):
        self.headers = {"Content-Type": "application/json"}
        self.client = requests.Session()

    def get(
        self,
        https: str,
        endpoint: str,
        headers: Optional[dict] = {},
        params: Optional[dict] = {},
    ) -> dict:
        """simple get request wrapper"""
        if len(headers) == 0:
            headers = self.headers

        response = self.client.get(f"{https}{endpoint}", headers=headers, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(response.text)
