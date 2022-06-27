import os
import pandas as pd
from dataclasses import dataclass


@dataclass
class TokenTerminal:
    def __init__(self):

        self.yield_tokens = ["rari-capital", "yearn-finance"]
        self.plf_tokens = ["aave", "compound"]
        self.dex_tokens = ["balancer", "uniswap"]

        self.tokens_2_symbol = {
            "rari-capital": "RNG",
            "yearn-finance": "YFI",
            "balancer": "BAL",
            "uniswap": "UNI",
            "aave": "AAVE",
            "compound": "COMP",
        }

        self.datasets = os.path.join("data", "token_terminal")

    def load_csv(self, token_name: str) -> pd.DataFrame:
        df = pd.read_csv(os.path.join(self.datasets, f"{token_name}.csv"))
        df["date"] = pd.to_datetime(df.timestamp).dt.date
        df.pop("timestamp")
        df = df[~df.treasury.isna()]
        return df
