import os
import pandas as pd
from tabulate import tabulate
from token_terminal.TokenTerminal import TokenTerminal


def terminal_value(r: float, g: float, fcf_n: float) -> float:
    """compute the terminal value"""

    return (fcf_n * (1 + g)) / (r - g)


if __name__ == "__main__":
    """Here we run the canonical DCF model to evaluate token projects"""
    # risk free rate as risky asset
    r = 0.25
    gdp = 0.0239

    workforce_expense = 0.2
    token_terminal = TokenTerminal()

    for token in token_terminal.all_tokens:

        df = token_terminal.get_quaterly_fundamentals(token)

        # revenues are in millions -
        # I am taking the first two quarters
        # multiply per 2
        last_year_revenue = df[-2:].revenue.sum() * 2
        dcf = []
        for year, growth, period in [
            (2022, 0, 0),
            (2023, 0.05, 1),
            (2024, 0.05, 2),
            (2025, 0.05, 3),
            (2026, 0.05, 4),
            (2027, 0.05, 5),
        ]:

            current_revenue = last_year_revenue + (last_year_revenue * growth)
            last_year_revenue = current_revenue
            workforce_expense_t = workforce_expense * current_revenue
            net_income = current_revenue - workforce_expense_t
            dcf.append(
                {
                    "discount_factor": 1 / (1 + r) ** period,
                    "fcf": current_revenue,
                    "workforce_expense": workforce_expense_t,
                    "net_income": net_income,
                    "year": year,
                    "growth_rate": growth,
                }
            )

        dcf.append(
            {
                "discount_factor": 1 / (1 + r) ** (period + 1),
                "fcf": terminal_value(r, gdp, net_income),
                "workforce_expense": 0,
                "net_income": terminal_value(r, gdp, net_income),
                "year": 0,
                "growth_rate": 0,
            }
        )

        dcf_df = pd.DataFrame(dcf)
        dcf_df["pv_income"] = dcf_df.discount_factor * dcf_df.net_income

        dcf_df["net_present_value"] = dcf_df.pv_income.sum()

        # price per token are not in millions
        dcf_df["price_per_token"] = (dcf_df.net_present_value * (10**6)) / df.iloc[
            -1
        ].shares
        output_dir = f"tables/digital_assets/dcf/"

        os.makedirs(output_dir, exist_ok=True)
        file_name = os.path.join(output_dir, f"{token}.tsv")
        dcf_df = dcf_df.round(3)
        with open(file_name, "w") as f:
            f.write(tabulate(dcf_df, headers="keys", tablefmt="psql"))
            f.write("\n")

        for column in [
            "fcf",
            "workforce_expense",
            "net_income",
            "pv_income",
            "net_present_value",
            "price_per_token",
        ]:
            string_to_print = f"{column}: \t"
            if column in ["net_present_value", "price_per_token"]:
                columns = str(dcf_df.iloc[-1][column])
            else:
                columns = " && ".join(dcf_df[column].round(2).astype(str).tolist())
            string_to_print = string_to_print + columns
            with open(file_name, "a") as f:
                f.write(string_to_print)
                f.write("\n")
