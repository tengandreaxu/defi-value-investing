from builtins import breakpoint
from lib2to3.pgen2 import token
import os
import pandas as pd
from datetime import datetime
from dataclasses import dataclass
from typing import Optional

# First Quarter 2022
LAST_QUARTER_2020 = datetime.fromisoformat("2020-09-30").date()
SECOND_QUARTER_2022 = datetime.fromisoformat("2022-06-30").date()

QUARTERS = [
    "2020-09-30",
    "2020-12-31",
    "2021-03-31",
    "2021-06-30",
    "2021-09-30",
    "2021-12-31",
    "2022-03-31",
    "2022-06-30",
]

QUARTERS = [datetime.fromisoformat(x).date() for x in QUARTERS]


@dataclass
class TokenTerminal:
    def __init__(self):

        self.yield_tokens = ["idle-finance", "yearn-finance"]
        self.plf_tokens = ["aave", "compound"]
        self.dex_tokens = ["balancer", "uniswap"]
        self.all_tokens = self.yield_tokens + self.plf_tokens + self.dex_tokens
        self.tokens_2_symbol = {
            "idle-finance": "IDLE",
            "yearn-finance": "YFI",
            "balancer": "BAL",
            "uniswap": "UNI",
            "aave": "AAVE",
            "compound": "COMP",
        }

        self.datasets = os.path.join("data", "token_terminal")

    def compute_quaterly_revenue(self, df: pd.DataFrame) -> pd.DataFrame:
        """computes quaterly revenue"""

        quarters = []
        for i in range(len(QUARTERS) - 1):
            quarter = df[(df.date > QUARTERS[i]) & (df.date <= QUARTERS[i + 1])].copy()
            quarter["revenue"] = quarter.revenue_total.cumsum()
            quarter = quarter[quarter.date == QUARTERS[i + 1]]
            quarters.append(quarter)
        quarters = pd.concat(quarters)
        return quarters

    def get_sorted_df(self, token_name: str) -> pd.DataFrame:
        df = pd.read_csv(os.path.join(self.datasets, f"{token_name}.csv"))
        df["date"] = pd.to_datetime(df.timestamp).dt.date
        df.pop("timestamp")
        df = df.sort_values("date")
        return df

    def load_csv(self, token_name: str) -> pd.DataFrame:
        df = self.get_sorted_df(token_name)
        # Change in millions
        df = df[df.date >= LAST_QUARTER_2020]

        df.treasury = df.treasury / (10**6)
        df.revenue_total = df.revenue_total / (10**6)
        df.market_cap_circulating = df.market_cap_circulating / (10**6)
        df.tvl = df.tvl / (10**6)
        df["mkt_cap_tvl_ratio"] = df.market_cap_circulating / df.tvl
        df = df[~df.treasury.isna()]
        return df

    def get_quaterly_fundamentals(self, token_name: str) -> pd.DataFrame:
        df = self.get_sorted_df(token_name)
        df = df[~df.revenue_total.isna()]
        df = df[(df.date >= LAST_QUARTER_2020) & (df.date <= SECOND_QUARTER_2022)]

        if LAST_QUARTER_2020 not in df.date.unique():
            for quarter in QUARTERS:
                if quarter in df.date.unique():
                    df = df[df.date > quarter]
                    break
        # Change in millions
        df.treasury = df.treasury / (10**6)
        df.revenue_total = df.revenue_total / (10**6)
        df.market_cap_circulating = df.market_cap_circulating / (10**6)

        df = self.compute_quaterly_revenue(df)
        df = df[~df.treasury.isna()]
        df["mkt_cap_revenue_ratio"] = df.market_cap_circulating / df.revenue
        df["mkt_cap_assets_ratio"] = df.market_cap_circulating / df.treasury
        return df

    def get_realized_historical_volatility(
        self, token_name: str, window: Optional[int] = 90
    ) -> pd.DataFrame:
        df = self.get_sorted_df(token_name)
        df["realized_volatility"] = df.price.rolling(window).std()
        df = df[~df.realized_volatility.isna()]
        return df


if __name__ == "__main__":
    token_terminal = TokenTerminal()
    token_terminal.get_realized_historical_volatility("aave")
