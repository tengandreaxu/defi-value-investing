from click import style
import requests
import time
import os

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import matplotlib.dates as mdates

from typing import Optional
from datetime import datetime
from dateutil.relativedelta import relativedelta

import logging

logging.basicConfig(level=logging.INFO)

START_DATE = datetime.fromisoformat("2020-05-18").date()


class CryptoFees:
    def __init__(self):
        # *****************
        # CryptoFees requests
        # *****************
        self.today = datetime.today().date()
        self.dates = self.create_date_list_in_chunks()
        self.url = "https://cryptofees.info/api/v1/feesByDay"

        # *******************
        # Paths and files
        # ********************
        self.id_csvs = "data/cryptofees_tokens.csv"
        self.data_folder = os.path.join("data", "crypto_fees")
        self.plots_folder = os.path.join("plots", "crypto_fees")
        os.makedirs(self.data_folder, exist_ok=True)
        os.makedirs(self.plots_folder, exist_ok=True)

        # *******************
        # Logger
        # *******************
        self.logger = logging.getLogger("CryptoFees")

    def create_date_list_in_chunks(self) -> list:
        """
        creates a list of lists of dates to be specified
        in the Cryptofees GET request
        """
        current_date = START_DATE
        output = []
        subset = []
        while current_date < self.today:
            subset.append(current_date)
            current_date = current_date + relativedelta(days=1)

            if len(subset) == 100:
                output.append(subset)
                subset = []
        output.append(subset)
        return output

    def pull_crypto_fees(self, id_: str) -> pd.DataFrame:
        """
        This function retrieves data from Cryptofees
        """
        session = requests.Session()
        output = pd.DataFrame()
        for subset_dates in self.dates:
            self.logger.info(
                f"pulling {id_} from {subset_dates[0]} to {subset_dates[-1]}"
            )
            response = session.get(self.url, params={id_: subset_dates})

            if response.status_code == 200:
                try:
                    df = pd.DataFrame(response.json()["data"][0]["data"])
                    output = pd.concat([output, df])
                except:
                    self.logger.error(f"Error pulling {id_} subset={subset_dates}")
            else:
                self.logger.error(
                    f"Error pulling {id_} status_code = {response.status_code}"
                )
            time.sleep(0.125)
        return output

    def load_data(self, id_: str) -> pd.DataFrame:
        """loads all fees, joins token different versions"""

        # *********************
        # retrieve all token's fees
        # *********************
        files = os.listdir(self.data_folder)
        files = [x for x in files if x.startswith(id_)]

        output = pd.DataFrame()

        for file_ in files:
            df = pd.read_csv(os.path.join(self.data_folder, file_))
            df = df[~df.fee.isna()]
            df.index = df["date"]
            df.pop("date")
            if output.empty:
                output = df

            else:

                output = output.join(
                    df, on=["date"], how="outer", lsuffix="_x", rsuffix="_y"
                )
                output.fee_y = output.fee_y.fillna(0)
                output.fee_x = output.fee_x.fillna(0)
                output["fee"] = output["fee_x"] + output["fee_y"]
                output.pop("fee_x")
                output.pop("fee_y")

        output = output.reset_index()
        output["date"] = output["date"].apply(
            lambda x: datetime.fromisoformat(x).date()
        )
        output = output.sort_values("date")
        return output
