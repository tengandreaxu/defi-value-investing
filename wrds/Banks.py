import pandas as pd
from dataclasses import dataclass
from wrds.StockFundamentals import StockFundamentals
from token_terminal.TokenTerminal import SECOND_QUARTER_2022, LAST_QUARTER_2020


@dataclass
class Banks:
    """
    We download bank's fundamentals from the famous WRDA database.

    Variables of interest:

    atq, quarter's total asset (in millions),
    dlcq, quarter's total liabilities (in millions)
    tcorq,  quarter's total current operating revenue (in millions)
    """

    def __init__(self):
        stocks = StockFundamentals()
        market_cap = stocks.df[["date", "underlying", "market_cap"]]
        self.df = pd.read_csv("data/wrds/banks.csv")
        self.df["date"] = pd.to_datetime(self.df.datadate).dt.date
        self.df = self.df[
            (self.df.date >= LAST_QUARTER_2020) & (self.df.date <= SECOND_QUARTER_2022)
        ]
        self.df = self.df.rename(columns={"tic": "underlying", "tcorq": "revenue"})
        self.df["net_asset"] = self.df["atq"] - self.df["dlcq"]
        self.df = pd.merge(self.df, market_cap)

        self.df["mkt_cap_revenue_ratio"] = self.df.market_cap / self.df.revenue
        self.df["mkt_cap_assets_ratio"] = self.df.market_cap / self.df.net_asset
        self.df = self.df[
            [
                "date",
                "underlying",
                "net_asset",
                "revenue",
                "mkt_cap_revenue_ratio",
                "mkt_cap_assets_ratio",
            ]
        ]
        self.banks = [
            "BAC",
            "WFC",
            "JPM",
        ]  # Bank of America, "Well Fargo & Co.". "Citigroup"


if __name__ == "__main__":
    banks = Banks()
    breakpoint()
