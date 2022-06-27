from concurrent.futures.thread import BrokenThreadPool
import pandas as pd
from datetime import datetime
from fetching.fetch_market_caps import COINGECKO_TOKENS, COINGECKO_TOKENS_2_SYMBOLS
from fetching.fetch_tvls import DEFILLAMA_TOKENS, DEFILLAMA_TOKENS_2_SYMBOL

DATE = datetime.fromisoformat("2022-01-01").date()
if __name__ == "__main__":

    table = {}

    # Load Market Caps
    for token in COINGECKO_TOKENS:
        df = pd.read_csv(f"data/market_caps/{token}.csv")
        df.date = pd.to_datetime(df.date).dt.date
        dict_ = df[df.date == DATE].to_dict(orient="records")[0]
        dict_["token"] = COINGECKO_TOKENS_2_SYMBOLS[token]
        table[COINGECKO_TOKENS_2_SYMBOLS[token]] = dict_

    # Load TVLs
    for token in DEFILLAMA_TOKENS:
        df = pd.read_csv(f"data/tvls/{token}.csv")
        df.date = pd.to_datetime(df.date).dt.date
        dict_ = df[df.date == DATE].to_dict(orient="records")[0]
        symbol = DEFILLAMA_TOKENS_2_SYMBOL[token]
        prev_dict = table[symbol]
        dict_.pop("date")

        prev_dict.update(dict_)

    # Create table
    df = [table[key] for key in table]
    df = pd.DataFrame(df)
    df.index = df.token
    df["Mkt Cap"] = df.totalLiquidityUSD * 0.2
    df["Protocol Revenue (PR)"] = df.totalLiquidityUSD * 0.1 * 0.2
    df.pop("total_volumes")
    df.pop("date")
    df.pop("token")

    columns = [
        ("Market Data", "Prices"),
        ("Market Data", "Mkt Cap"),
        ("Financial Data", "TVL"),
        ("Estimations", "Mkt Cap"),
        ("Estimations", "Protocol Revenue"),
    ]
    df.columns = pd.MultiIndex.from_tuples(columns)

    mean_mkt_cap = df[("Estimations", "Mkt Cap")].mean()
    median_mkt_cap = df[("Estimations", "Mkt Cap")].median()

    mean_protocol_revenue = df[("Estimations", "Protocol Revenue")].mean()
    median_protocol_revenue = df[("Estimations", "Protocol Revenue")].median()

    df.to_latex("tables/digital_assets/comparables.tex")
