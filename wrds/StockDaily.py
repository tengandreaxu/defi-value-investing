import pandas as pd
from typing import Optional
from dataclasses import dataclass


@dataclass
class StockDaily:
    def __init__(self):

        self.df = pd.read_csv("data/wrds/stocks_daily.csv")
        self.df.date = pd.to_datetime(self.df.date).dt.date

    def get_realized_historical_volatility(
        self, ticker: str, window: Optional[int] = 90
    ) -> pd.DataFrame:
        df = self.df[self.df.TICKER == ticker].copy()
        df["realized_volatility"] = df.PRC.rolling(window).std()
        df = df[~df.realized_volatility.isna()]
        return df


if __name__ == "__main__":
    stocks = StockDaily()
    breakpoint()
