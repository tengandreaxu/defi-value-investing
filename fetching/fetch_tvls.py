import pandas as pd
from datetime import datetime
from fetching.SimpleHttpClient import Endpoints
from fetching.SimpleHttpClient import SimpleHttpClient

DEFILLAMA_TOKENS = [
    "yearn-finance",
    "idle-finance",
    "uniswap",
    "balancer",
    "aave",
    "compound",
]

DEFILLAMA_TOKENS_2_SYMBOL = {
    "yearn-finance": "YFI",
    "idle-finance": "IDLE",
    "uniswap": "UNI",
    "balancer": "BAL",
    "aave": "AAVE",
    "compound": "COMP",
}

if __name__ == "__main__":

    client = SimpleHttpClient()

    for token in DEFILLAMA_TOKENS:

        response = client.get(Endpoints.DEFI_LLAMA_PROTOCOL_TVL, token)
        df = pd.DataFrame(response["tvl"])
        df.date = df.date.apply(lambda x: datetime.fromtimestamp(int(x)))
        df.to_csv(f"data/tvls/{token}.csv", index=False)
        print(f"Fetched {token} data")
