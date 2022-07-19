from token_terminal.TokenTerminal import TokenTerminal

if __name__ == "__main__":
    """create the historical revenue table"""
    token_terminal = TokenTerminal()

    for token in token_terminal.all_tokens:
        df = token_terminal.get_quaterly_fundamentals(token)
        df = df[~df.revenue.isna()]
        df["cqgr"] = (df.iloc[-1].revenue / df.iloc[0].revenue) ** (
            1 / (df.shape[0] - 1)
        ) - 1
        df = df[
            [
                "date",
                "revenue",
                "cqgr",
            ]
        ]
        df["growth"] = df.revenue / df.revenue.shift(1) - 1
        df.to_csv(f"tables/digital_assets/{token}.tsv", sep="\t")
