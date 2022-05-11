import os
import pandas as pd

from datetime import datetime
from dune.constants import DUNE_DATA
import logging

logging.basicConfig(level=logging.INFO)


class DuneDataManager:
    def __init__(self):
        self.logger = logging.getLogger("DuneDataManager")

    def load_financial_dataset(self, token: str) -> pd.DataFrame:

        try:

            df = pd.read_csv(os.path.join(DUNE_DATA, f"{token}_financials.csv"))
        except:
            self.logger.info(f"Financials not found for {token}")
            exit(1)

        if token == "CRV":
            df["date"] = pd.to_datetime(df.day).dt.date
            df = df.groupby("date").sum().reset_index()

        if token == "UNI":
            df["date"] = pd.to_datetime(df.Time).dt.date
            df["revenue"] = df["V2 Supply-Side Revenue"] + df["V3 Supply-Side Revenue"]

        if token == "MKR":
            df["revenue"] = df["net_income"]
            df = df[~df.revenue.isna()]
            df["date"] = df.period.apply(lambda x: datetime.strptime(x, "%Y-%m"))

        df = df[["date", "revenue"]]
        df = df.sort_values("date")
        return df


if __name__ == "__main__":

    dune = DuneDataManager()
    dune.load_financial_dataset("MKR")
