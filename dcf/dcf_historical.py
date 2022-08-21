import pandas as pd
import numpy as np
from token_terminal.TokenTerminal import TokenTerminal, QUARTERS
from tabulate import tabulate

if __name__ == "__main__":
    """create the historical revenue table"""
    token_terminal = TokenTerminal()
    QUARTERS.pop(0)
    quarters = np.flip(np.array(QUARTERS))
    pattern = [" && ", " & ", " & ", " & ", " && ", " & ", " && "]
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
        df["growth"] = (df.revenue / df.revenue.shift(1) - 1) * 100
        file_name = f"tables/digital_assets/{token}.tsv"

        df = df.round(2)

        for quart in quarters:
            if quart not in df.date.tolist():
                df = pd.concat(
                    [
                        pd.DataFrame(
                            [
                                {
                                    "date": quart,
                                    "revenue": "$NA$",
                                    "cqgr": "",
                                    "growth": "$NA$",
                                }
                            ]
                        ),
                        df,
                    ]
                )

        df.at[df[df.growth.isna()].index[0], "growth"] = "$NA$"

        with open(file_name, "w") as f:
            f.write(tabulate(df, headers="keys", tablefmt="psql"))
            f.write("\n")

        for column in ["revenue", "growth"]:

            items = df[column].tolist()
            string_ = ""
            for index, item in enumerate(items, 0):
                if column == "revenue":
                    string_ += f"{item}" + f"{pattern[index]}"
                else:
                    percentage_or_not = "\%" if item != "$NA$" else ""
                    item_string = r"\textit{" + f"{item}" + f"{percentage_or_not}" + "}"
                    string_ += f"{item_string}" + f"{pattern[index]}"

            if column == "revenue":
                string_ += r"\textit{" + f"{df.iloc[-1].cqgr}" + "\%}"

            with open(file_name, "a") as f:
                f.write(f"{column}:\t{string_}")
                f.write(f"\n")
