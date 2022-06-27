import pandas as pd
from datetime import datetime
from fetching.SimpleHttpClient import Endpoints, SimpleHttpClient

COINGECKO_TOKENS = [
    "idle",
    "compound-governance-token",
    "uniswap",
    "balancer",
    "aave",
    "yearn-finance",
]
COINGECKO_TOKENS_2_SYMBOLS = {
    "idle": "IDLE",
    "compound-governance-token": "COMP",
    "uniswap": "UNI",
    "balancer": "BAL",
    "aave": "AAVE",
    "yearn-finance": "YFI",
}

if __name__ == "__main__":

    client = SimpleHttpClient()
    for token in COINGECKO_TOKENS:

        params = {"vs_currency": "usd", "days": "1000"}
        endpoint = Endpoints.COINGECKO_MARKET_CHART.format(token)

        response = client.get(endpoint, "", params=params)
        df = pd.DataFrame(response)
        df["date"] = df.prices.apply(lambda x: datetime.fromtimestamp(x[0] / 1000))
        df["prices"] = df.prices.apply(lambda x: x[1])
        df["market_caps"] = df.market_caps.apply(lambda x: x[1])
        df["total_volumes"] = df.total_volumes.apply(lambda x: x[1])
        df.to_csv(f"data/market_caps/{token}.csv", index=False)
        print(f"Got {token}")
