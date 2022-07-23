import pandas as pd
from wrds.StockFundamentals import StockFundamentals
from dcf.estimation import terminal_value
from typing import Tuple
from datetime import datetime
from tabulate import tabulate

# From 10-K filings
# Item 8 Financial Statements and Supplementary Data
# Debt -> Senior Structured Notes Debt
COST_OF_DEBT = {
    "BAC": 0.0285,  # https://www.sec.gov/ix?doc=/Archives/edgar/data/70858/000007085822000062/bac-20211231.htm#i06069ff5e5094832bb6e77973dc078a0_208
    "BLK": 0.021,  # https://www.sec.gov/ix?doc=/Archives/edgar/data/1364742/000156459022007117/blk-10k_20211231.htm#ITEM_15_EXHIBITS_FINANCIAL_STATEMENT, pag F-27
    "BRK.B": 0.033,  # https://www.sec.gov/ix?doc=/Archives/edgar/data/1067983/000156459022007322/brka-10k_20211231.htm#ITEM_8_FINANCIAL_STATEMENTS_SUPPLEMENTAR, pag K-99
    "C": 0.0288,  # https://www.sec.gov/ix?doc=/Archives/edgar/data/831001/000083100122000036/c-20211231.htm#if5eae24ef5514bfc97c61b352d017aca_265, pag 226
    "CBOE": 0.0263,  # https://www.sec.gov/ix?doc=/Archives/edgar/data/1374310/000155837022001386/cboe-20211231x10k.htm#Item8FinancialStatementsandSupplementary, pag 115
    "ICE": 0.03,  # https://www.sec.gov/ix?doc=/Archives/edgar/data/1571949/000157194922000006/ice-20211231.htm#ic6ff9fd786c64411b3dd06b169bdbc7d_121, pag 116
    "MS": 0.029,  #  https://www.sec.gov/ix?doc=/Archives/edgar/data/895421/000089542122000400/ms-20211231.htm#i2f6975a563604b0cb1bffa00a50db3ed_100, pag 113
    "NDAQ": 0.0375,  # https://www.sec.gov/ix?doc=/Archives/edgar/data/1120193/000112019322000007/ndaq-20211231.htm#i9ecf2d8b4a9144cbba8a3298cdb989e8_241, pag F-28
    "WFC": 0.0237,  # https://www.sec.gov/ix?doc=/Archives/edgar/data/0000072971/000007297121000267/wfc-20210630.htm, pag 7
}

MARKET_RETURN = 0.1
# https://pages.stern.nyu.edu/~adamodar/New_Home_Page/datafile/Betas.html
BETA_BANKS = 1.12
BETA_INVESTMENTS = 1.05

COST_OF_CAPITAL_BANKS = MARKET_RETURN * BETA_BANKS
COST_OF_CAPITAL_FINANCIAL_SERVICES = MARKET_RETURN * BETA_INVESTMENTS
COST_OF_CAPITAL = {
    "BAC": COST_OF_CAPITAL_BANKS,
    "BLK": COST_OF_CAPITAL_FINANCIAL_SERVICES,
    "BRK.B": COST_OF_CAPITAL_FINANCIAL_SERVICES,
    "C": COST_OF_CAPITAL_BANKS,
    "CBOE": COST_OF_CAPITAL_FINANCIAL_SERVICES,
    "ICE": COST_OF_CAPITAL_FINANCIAL_SERVICES,
    "MS": COST_OF_CAPITAL_FINANCIAL_SERVICES,
    "NDAQ": COST_OF_CAPITAL_FINANCIAL_SERVICES,
    "WFC": COST_OF_CAPITAL_BANKS,
}
# https://pages.stern.nyu.edu/~adamodar/New_Home_Page/datafile/taxrate.html
TAX_RATE_BANKS = 0.1469
TAX_RATE_INVESTMENTS = 0.1337
TAX_RATES = {
    "BAC": TAX_RATE_BANKS,
    "BLK": TAX_RATE_INVESTMENTS,
    "BRK.B": TAX_RATE_INVESTMENTS,
    "C": TAX_RATE_BANKS,
    "CBOE": TAX_RATE_INVESTMENTS,
    "ICE": TAX_RATE_INVESTMENTS,
    "MS": TAX_RATE_INVESTMENTS,
    "NDAQ": TAX_RATE_INVESTMENTS,
    "WFC": TAX_RATE_BANKS,
}


def get_2021_equity_debt_ratio(df: pd.DataFrame) -> Tuple[float, float]:
    """returns the E/(E+D) and D(E+D) from 2021"""
    first_quarter = datetime.fromisoformat("2021-03-31").date()
    last_quarter = datetime.fromisoformat("2021-12-31").date()
    total_equity = df[(df.date >= first_quarter) & (df.date <= last_quarter)].atq.sum()
    total_debt = df[(df.date >= first_quarter) & (df.date <= last_quarter)].dlcq.sum()

    return total_equity / (total_equity + total_debt), total_debt / (
        total_equity + total_debt
    )


def get_wacc(df: pd.DataFrame, ticker: str) -> float:
    equity_ratio, debt_ratio = get_2021_equity_debt_ratio(df)
    cost_of_capital = COST_OF_CAPITAL[ticker]
    cost_of_debt = COST_OF_DEBT[ticker]
    tax_rate = TAX_RATES[ticker]
    return (equity_ratio * cost_of_capital) + (
        debt_ratio * cost_of_debt * (1 - tax_rate)
    )


if __name__ == "__main__":
    """Here we run the canonical DCF model to evaluate ticker projects"""
    # risk free rate
    r = 0.0298
    # growth rate
    gdp = 0.0239

    wrds = StockFundamentals()
    workforce_expense = 0.3
    for ticker in wrds.all_assets:
        df = wrds.df[wrds.df.underlying == ticker].copy()
        df["shares"] = (df.market_cap * (10**6)) / df.price
        last_year_revenue = df[-2:].piq.sum() * 2
        dcf = []
        wacc = get_wacc(df, ticker)

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
                    "discount_factor": 1 / (1 + wacc) ** period,
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
                "fcf": terminal_value(wacc, gdp, current_revenue),
                "workforce_expense": 0,
                "net_income": terminal_value(wacc, gdp, current_revenue),
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
        file_name = f"tables/digital_assets/dcf/{ticker}.tsv"
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
