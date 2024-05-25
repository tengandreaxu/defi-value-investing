from tabulate import tabulate
from wrds.StockFundamentals import StockFundamentals

if __name__ == "__main__":
    """create the historical piq table"""
    stocks = StockFundamentals()
    pattern = [" && ", " & ", " & ", " & ", " && ", " & ", " && "]
    for ticker in stocks.all_assets:

        df = stocks.df[stocks.df.underlying == ticker].copy()
        initial_value = df.iloc[1].piq if df.shape[0] == 8 else df.iloc[0].piq
        df["cqgr"] = (
            (df.iloc[-1].piq / df.iloc[0].piq) ** (1 / (df.shape[0] - 1)) - 1
        ) * 100
        df = df[
            [
                "date",
                "piq",
                "cqgr",
            ]
        ]
        df["growth"] = (df.piq / df.piq.shift(1) - 1) * 100
        file_name = f"tables/digital_assets/{ticker}.tsv"
        # df.at[df[df.growth.isna()].index[0], "growth"] = "$NA$"
        df = df.round(2)
        df.growth = df.growth.astype(str)
        df = df.reset_index()
        df.pop("index")
        if df.shape[0] == 8:
            df = df.drop(0)
        with open(file_name, "w") as f:
            f.write(tabulate(df, headers="keys", tablefmt="psql"))
            f.write("\n")
        df.loc[df.growth == "nan", "growth"] = "$NA$"

        for column in ["piq", "growth"]:

            items = df[column].tolist()
            string_ = ""
            for index, item in enumerate(items, 0):
                if column == "piq":
                    try:
                        string_ += f"{item}" + f"{pattern[index]}"
                    except:
                        breakpoint()
                else:
                    percentage_or_not = "\%" if item != "$NA$" else ""
                    item_string = r"\textit{" + f"{item}" + f"{percentage_or_not}" + "}"
                    string_ += f"{item_string}" + f"{pattern[index]}"

            if column == "piq":
                string_ += r"\textit{" + f"{df.iloc[-1].cqgr}" + "\%}"

            with open(file_name, "a") as f:
                f.write(f"{column}:\t{string_}")
                f.write(f"\n")
