from concurrent.futures.thread import BrokenThreadPool
import pandas as pd
from datetime import datetime
from fetching.fetch_market_caps import COINGECKO_TOKENS, COINGECKO_TOKENS_2_SYMBOLS
from fetching.fetch_tvls import DEFILLAMA_TOKENS, DEFILLAMA_TOKENS_2_SYMBOL
from token_terminal.TokenTerminal import TokenTerminal
from wrds.StockFundamentals import StockFundamentals

# First Quarter 2022
DATE = datetime.fromisoformat("2022-03-31").date()
BEGIN_YEAR = datetime.fromisoformat("2022-01-01").date()
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
        final_df = []
        # Create a dataframe with |token| x |features|
        # features = {price, market_cap} +
        # + {treasury/assets, revenue_total/revenue} + {market_cap/treasury, market_cap/revenue}

        for token in tokens:
            df = token_terminal.load_csv(token)
            df = df[(df.date >= BEGIN_YEAR) & (df.date <= DATE)]

            df.treasury = df.treasury / (10**6)
            df.revenue_total = df.revenue_total / (10**6)
            df.market_cap_circulating = df.market_cap_circulating / (10**6)
            df["revenueq"] = df.revenue_total.cumsum()

            # eps = renenue_total / #tokens
            # tokens = market_cap_circulating / price
            df = df[["price", "market_cap_circulating", "treasury", "revenueq", "date"]]
            # convert in millions

            df["Mkt Cap/Assets"] = df.market_cap_circulating / df.treasury
            df["Mkt Cap/Revenue"] = df.market_cap_circulating / df.revenueq

            df = df.rename(
                columns={
                    "price": "Price",
                    "market_cap_circulating": "Market Cap",
                    "treasury": "Net Assets",
                    "revenueq": "Revenue",
                }
            )

            df = df[df.date == DATE]

            df.pop("date")
            record = df.to_dict(orient="records")[0]

            record["Underlying"] = token_terminal.tokens_2_symbol[token]
            final_df.append(record)
        for stock in stocks:
            df = wrds.df[wrds.df.tic == stock].copy()
            breakpoint()
            df = df.rename(
                columns={
                    "prccq": "Price",
                    "mkvaltq": "Market Cap",
                    "atq": "Net Assets",
                    "revtq": "Revenue",
                }
            )

            df = df[["Price", "Market Cap", "Net Assets", "Revenue", "date"]]
            df["Mkt Cap/Assets"] = df["Market Cap"] / df["Assets"]
            df["Mkt Cap/Revenue"] = df["Market Cap"] / df["Revenue"]
            df = df[df.date == DATE]
            df.pop("date")

            record = df.to_dict(orient="records")[0]

            record["Underlying"] = stock
            final_df.append(record)
        final_df = pd.DataFrame(final_df)
        final_df = final_df.round(
            {
                "Price": 2,
                "Market Cap": 2,
                "Assets": 2,
                "Revenue": 2,
                "Mkt Cap/Assets": 2,
                "Mkt Cap/Revenue": 2,
            }
        )
        final_df.index = final_df.Underlying
        final_df.pop("Underlying")
        final_df.to_latex(f"tables/{category}.tex")
