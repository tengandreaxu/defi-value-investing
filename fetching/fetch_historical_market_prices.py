"""
author: andrea.xu@epfl.ch

This script pulls Binance candle stick historical data.
The Crypto Tokens are specified in SYMBOLS.

The data is pulled with frequency: 1 minute.

STARTING Date
"""

import sys
import os
import pytz
import time
import pandas as pd
from datetime import datetime
from binance.client import Client

import logging

logging.basicConfig(level=logging.INFO, stream=sys.stderr)
TOKENS = ["BALUSDT", "YFIUSDT", "CVXUSDT", "UNIUSDT", "AAVEUSDT", "COMPUSDT"]

utc = pytz.timezone("UTC")

START_TIME = 1504220400000  # 2017/09/01
LIMIT = 500  # it will retrieve 500 minutes data
CANDLE_DATA_COLUMNS = [
    "timestamp",
    "open",
    "high",
    "low",
    "close",
    "volume",
    "close_time",
    "quote_asset_volume",
    "trades",
    "taker_buy_base_asset_volume",
    "taker_buy_quote_asset_volume",
    "ignore",
]


def generate_timestamps() -> list:
    """
    We need to generate tuples of
    (start_time, end_time)
    From 2017-01-01 until today
    """

    now = datetime.now(utc).timestamp() * 1000
    start_time = START_TIME
    timestamps = []

    # 1 day
    time_frame = 24 * 60 * 60 * 1000  # expressed in milliseconds
    while start_time < now:

        end_time = start_time + (time_frame * LIMIT)
        timestamps.append((start_time, end_time))

        # avoid overlaps
        start_time = end_time + time_frame
    return timestamps


def create_dataframe_from_candle_data(candle_data: list) -> pd.DataFrame:
    """
    Candle data is a list of 1 minute data

    For each element we have the following values:

    1499040000000,      // Open time
    "0.01634790",       // Open
    "0.80000000",       // High
    "0.01575800",       // Low
    "0.01577100",       // Close
    "148976.11427815",  // Volume
    1499644799999,      // Close time
    "2434.19055334",    // Quote asset volume
    308,                // Number of trades
    "1756.87402397",    // Taker buy base asset volume
    "28.46694368",      // Taker buy quote asset volume
    "17928899.62484339" // Ignore.


    Source: https://github.com/binance/binance-spot-api-docs/blob/master/rest-api.md#klinecandlestick-data
    """
    return pd.DataFrame(candle_data, columns=CANDLE_DATA_COLUMNS)


if __name__ == "__main__":
    client = Client()
    symbols = TOKENS

    for symbol in symbols:

        dataframe = pd.DataFrame()
        i = 0
        dfs = []
        timestamps = generate_timestamps()
        for start_time, end_time in timestamps:

            start_date = utc.localize(
                datetime.fromtimestamp(start_time / 1000)
            ).isoformat()
            end_date = utc.localize(datetime.fromtimestamp(end_time / 1000)).isoformat()

            logging.info(
                f"Pulling {symbol}, start_date={start_date}, end_date={end_date}"
            )

            candle_data = client.get_klines(
                symbol=symbol,
                interval=Client.KLINE_INTERVAL_1MINUTE,
                startTime=start_time,
                endTime=end_time,
                limit=1000,
            )
            if len(candle_data) > 0:
                dfs.append(create_dataframe_from_candle_data(candle_data))
                logging.info(f"saved dataframe {i}")

            time.sleep(0.1)

        df = pd.concat(dfs)
        file = symbol.replace("USDT", "")
        df.to_csv(os.path.join("data/daily_mkt_prices", f"{file}.csv"))
