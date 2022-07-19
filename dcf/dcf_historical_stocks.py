from wrds.StockFundamentals import StockFundamentals

if __name__ == "__main__":
    """create the historical revenue table"""
    stocks = StockFundamentals()

    for ticker in stocks.all_assets:
        df = stocks.df[stocks.df.underlying == ticker].copy()
        df["cqgr"] = (df.iloc[-1].piq / df.iloc[0].piq) ** (1 / (df.shape[0] - 1)) - 1
        df = df[
            [
                "date",
                "piq",
                "cqgr",
            ]
        ]
        df["growth"] = df.piq / df.piq.shift(1) - 1
        df.to_csv(f"tables/digital_assets/{ticker}.tsv", sep="\t")
