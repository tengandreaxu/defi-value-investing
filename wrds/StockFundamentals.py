import pandas as pd
from dataclasses import dataclass


@dataclass
class StockFundamentals:
    """ "
    We download stock fundamentals from the famous
    WRDS database.

    In particular, we focus on the COMPUSTAT & CRSP merged dataset.

    Variables description can be found in:
    https://wrds-www.wharton.upenn.edu/search/?queryTerms=cdvcy&activeTab=navVariablesSearchTab

    Here we have a brief description of them:

    csh12q, number of common shares outstanding used to compute eps (in millions)
    cshoq, common shares outstanding (in millions)
    cdvcy, cash dividends on common stocks (in millions)
    dvy,cash dividends (in millions)
        This item represents the total amount of cash dividends paid
        for common/ordinary capital, preferred/preference capital and other share capital.
    epspxy, earnings per share excluding extraordinary items (ratio)
    fincfy, This item represents cash paid or received for all transactions classified as
            Financing Activities on a Statement of Cash Flows (Format Code = 7).
            (in millions)
    revty, total revenue (in millions)
            This item represents the gross income received from all divisions of the company.
    sivy, This item represents a source of funds from the sale of investments (in millions)
    cshtrq, common shares traded quarter (in millions)
    dvpspq, This item represents the cash dividends per share for which
            the payable dates occurred during the reporting period. (Dollar and cents)
    dvpsxq, This item represents the unadjusted cash dividends per share
            for which the ex-dividend dates occurred during the reporting period (dollar and cent)
    mkvaltq, market value quarter (in millions)
    prccq, price close quarter

    """

    def __init__(self):

        self.df = pd.read_csv("data/wrds/stock_fundamentals.csv")
        self.df["date"] = pd.to_datetime(self.df.datadate).dt.date
        self.df.pop("datadate")
        self.banks = [
            "BAC",
            "WFC",
            "C",
        ]  # Bank of America, "Well Fargo & Co.". "Citigroup"
        self.asset_managers = [
            "BRK.B",
            "BLK",
            "JPM",
        ]  # "Berkshire Hathaway, BlackRock, JP Morgan"

        self.exchanges = ["NDAQ", "ICE", "CBOE"]


if __name__ == "__main__":

    stocks = StockFundamentals()
    breakpoint()
