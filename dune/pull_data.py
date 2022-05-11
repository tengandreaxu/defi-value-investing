import os
import time
import pandas as pd

from duneanalytics import DuneAnalytics
from dune.DuneCredentials import DuneCredentials
from dune.constants import DUNE_DATA

import logging

logging.basicConfig(level=logging.INFO)

QUERIES_FINANCIALS = {
    "MKR": 17392,  # https://dune.com/SebVentures/maker---accounting_1
    "UNI": 251978,  # https://dune.com/messari/Messari:-Uniswap-Macro-Financial-Statements,
    "CRV": 151024,  # https://dune.com/Marcov/Convex-Finance
}


def pull_data(dune: DuneAnalytics):

    for token in QUERIES_FINANCIALS.keys():
        logging.info(f"Pulling \t {token}")
        result_id = dune.query_result_id(query_id=QUERIES_FINANCIALS[token])
        data = dune.query_result(result_id)

        df_list = data["data"]["get_result_by_result_id"]
        df = [x["data"] for x in df_list]
        df = pd.DataFrame(df)
        df.to_csv(os.path.join(DUNE_DATA, f"{token}_financials.csv"), index=False)
        logging.info(f"Saved {df.shape[0]} rows")
        time.sleep(1)


if __name__ == "__main__":

    dune = DuneAnalytics(DuneCredentials.username, DuneCredentials.password)
    dune.login()

    dune.fetch_auth_token()

    pull_data(dune)
