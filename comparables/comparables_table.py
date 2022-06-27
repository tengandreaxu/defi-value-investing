from concurrent.futures.thread import BrokenThreadPool
import pandas as pd
from datetime import datetime
from fetching.fetch_market_caps import COINGECKO_TOKENS, COINGECKO_TOKENS_2_SYMBOLS
from fetching.fetch_tvls import DEFILLAMA_TOKENS, DEFILLAMA_TOKENS_2_SYMBOL
from token_terminal.TokenTerminal import TokenTerminal
from wrds.StockFundamentals import StockFundamentals

# First Quarter 2022
DATE = datetime.fromisoformat("2022-03-31").date()
if __name__ == "__main__":

    wrds = StockFundamentals()
    token_terminal = TokenTerminal()

    for tokens, stocks, category in zip(
        [
            token_terminal.dex_tokens,
            token_terminal.yield_tokens,
            token_terminal.plf_tokens,
        ],
        [wrds.exchanges, wrds.asset_managers, wrds.banks],
        ["Exchanges", "Asset Managers", "Banks"],
    ):

        # Create a dataframe with |token| x |features|
        # features = {price, market_cap} +
        # + {revenue_total, eps, }

        for token in tokens:
            df = token_terminal.load_csv(token)
            # eps = renenue_total / #tokens
            # tokens = market_cap_circulating / price
            breakpoint()
        for stock in stocks:
            df = stocks.df[stocks.df.tic == stock].copy()
