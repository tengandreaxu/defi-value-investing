import pandas as pd
from plotting.Plotter import Plotter

if __name__ == "__main__":

    df = pd.read_csv("data/token_terminal/balancer.csv")
    df = df[~df.treasury.isna()]
    df["date"] = pd.to_datetime(df.timestamp).dt.date
    plotter = Plotter()
    breakpoint()
    plotter.plot_line_from_columns(
        df,
        "date",
        ys=[
            "tvl",
            "market_cap_circulating",
            "treasury",
            "revenue_total",
        ],
        linestyles=["solid", "dotted", "dashed", "dashdot"],
        xlabel="Date",
        ylabel="Metrics",
        labels=["TVL", "Mkt Cap", "Treasury", "Total Revenue"],
        file_name="digital-assets-book/token_terminal_metrics.png",
    )
