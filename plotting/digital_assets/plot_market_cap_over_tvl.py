import os
import pandas as pd
from plotting.Plotter import Plotter
from token_terminal.TokenTerminal import TokenTerminal

if __name__ == "__main__":
    plotter = Plotter()

    token_terminal = TokenTerminal()

    dfs = []
    labels = []
    # Yield Aggregators
    for yield_ in token_terminal.yield_tokens:
        dfs.append(token_terminal.load_csv(yield_))
        labels.append(token_terminal.tokens_2_symbol[yield_])

    y_column = "mkt_cap_tvl_ratio"
    ylabel = "Market Cap / TVL ratio"
    plotter.plot_line_from_dfs(
        dfs=dfs,
        xs=["date", "date"],
        ys=[y_column, y_column],
        xlabel="Date",
        ylabel=ylabel,
        labels=labels,
        file_name=os.path.join("digital-assets-book", "mkt_cap_tvl_yield_agg.pdf"),
        linestyles=["solid", "dotted"],
        xticks_rotation=90,
        grid=True,
        set_billions=False,
    )

    dfs = []
    labels = []
    # PLFs
    for plf in token_terminal.plf_tokens:
        dfs.append(token_terminal.load_csv(plf))
        labels.append(token_terminal.tokens_2_symbol[plf])

    plotter.plot_line_from_dfs(
        dfs=dfs,
        xs=["date", "date"],
        ys=[y_column, y_column],
        xlabel="Date",
        ylabel=ylabel,
        labels=labels,
        file_name=os.path.join("digital-assets-book", "mkt_cap_tvl_plf.pdf"),
        linestyles=["solid", "dotted"],
        grid=True,
        xticks_rotation=90,
        set_billions=False,
    )
    dfs = []
    labels = []
    # DEXs
    for dex in token_terminal.dex_tokens:
        dfs.append(token_terminal.load_csv(dex))
        labels.append(token_terminal.tokens_2_symbol[dex])
    plotter.plot_line_from_dfs(
        dfs=dfs,
        xs=["date", "date"],
        ys=[y_column, y_column],
        xlabel="Date",
        ylabel=ylabel,
        labels=labels,
        xticks_rotation=90,
        linestyles=["solid", "dotted"],
        grid=True,
        set_billions=False,
        file_name=os.path.join("digital-assets-book", "mkt_cap_tvl_dexs.pdf"),
    )
