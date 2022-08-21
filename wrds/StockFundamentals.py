import pandas as pd
from dataclasses import dataclass

from token_terminal.TokenTerminal import SECOND_QUARTER_2022, LAST_QUARTER_2020


@dataclass
class StockFundamentals:
    """ "
    We download stock fundamentals from the famous
    WRDS database.

    In particular, we focus on the COMPUSTAT & CRSP merged dataset.

    Variables description can be found in:
    https://wrds-www.wharton.upenn.edu/search/?queryTerms=cdvcy&activeTab=navVariablesSearchTab

    Here we have a brief description of them:

    Fundamentals:

        revtq, quarter'ss totalrevenue (in millions)
        atq, quarter's total asset (in millions),
        dlcq, quarter's total liabilities (in millions)

    Market Data:
        prccq, price at close
        mkvaltq, market cap
    """

    def __init__(self):

        self.df = pd.read_csv("data/wrds/stocks_fundamentals.csv")
        self.df["date"] = pd.to_datetime(self.df.datadate).dt.date
        self.df = self.df[
            (self.df.date >= LAST_QUARTER_2020) & (self.df.date <= SECOND_QUARTER_2022)
        ]

        self.df = self.df.rename(
            columns={
                "prccq": "price",
                "mkvaltq": "market_cap",
                "revtq": "revenue",
                "tic": "underlying",
            }
        )
        self.asset_managers = [
            "BRK.B",
            "BLK",
            "MS",
        ]  # "Berkshire Hathaway, BlackRock, Morgan Stanley"

        self.df["net_asset"] = self.df["atq"] - self.df["dlcq"]
        self.df["mkt_cap_revenue_ratio"] = self.df.market_cap / self.df.revenue
        self.df["mkt_cap_assets_ratio"] = self.df.market_cap / self.df.net_asset

        self.exchanges = ["NDAQ", "ICE", "CBOE"]
        self.df = self.df[
            [
                "date",
                "underlying",
                "price",
                "market_cap",
                "revenue",
                "net_asset",
                "mkt_cap_revenue_ratio",
                "mkt_cap_assets_ratio",
                "piq",
                "atq",
                "dlcq",
            ]
        ]
        self.banks = [
            "BAC",
            "WFC",
            "C",
        ]  # Bank of America, "Well Fargo & Co.". "Citigroup"
        self.all_assets = self.banks + self.exchanges + self.asset_managers


if __name__ == "__main__":

    stocks = StockFundamentals()
    breakpoint()
