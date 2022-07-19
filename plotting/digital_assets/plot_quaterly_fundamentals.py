import os
import pandas as pd
from plotting.Plotter import Plotter
from token_terminal.TokenTerminal import TokenTerminal
from wrds.Banks import Banks
from wrds.StockFundamentals import StockFundamentals

if __name__ == "__main__":
    plotter = Plotter()

    token_terminal = TokenTerminal()
    banks = Banks()
    stocks = StockFundamentals()
    dfs = []
    labels = []

    # Yield Aggregators / Asset Managers
    for yield_ in token_terminal.yield_tokens:
        dfs.append(token_terminal.get_quaterly_fundamentals(yield_))
        labels.append(token_terminal.tokens_2_symbol[yield_])

    for asset_manager in stocks.asset_managers:
        dfs.append(stocks.df[stocks.df.underlying == asset_manager].copy())
        labels.append(asset_manager)

    ys = ["mkt_cap_revenue_ratio" for _ in range(5)]
    xs = ["date" for _ in range(5)]
    linestyles = ["dashed", "dashed"]
    linestyles += ["solid" for _ in range(3)]
    markers = ["o", "o", "x", "x", "x"]

    ys_asset = ["mkt_cap_assets_ratio" for _ in range(5)]

    ylabel = "Market Cap / Revenue ratio"
    plotter.plot_line_from_dfs(
        dfs=dfs,
        xs=xs,
        ys=ys,
        xlabel="Date",
        ylabel=ylabel,
        labels=labels,
        file_name=os.path.join(
            "digital-assets-book", "fundamentals_asset_managers_mkt_cap_revenue.png"
        ),
        linestyles=linestyles,
        xticks_rotation=90,
        markers=markers,
        grid=True,
    )

    ylabel_asset = "Market Cap / Asset ratio"
    plotter.plot_line_from_dfs(
        dfs=dfs,
        xs=xs,
        ys=ys_asset,
        xlabel="Date",
        ylabel=ylabel_asset,
        labels=labels,
        file_name=os.path.join(
            "digital-assets-book", "fundamentals_asset_managers_mkt_cap_net_asset.png"
        ),
        linestyles=linestyles,
        xticks_rotation=90,
        markers=markers,
        grid=True,
    )

    dfs = []
    labels = []
    # DEXs
    for dex in token_terminal.dex_tokens:
        dfs.append(token_terminal.get_quaterly_fundamentals(dex))
        labels.append(token_terminal.tokens_2_symbol[dex])

    for cex in stocks.exchanges:
        dfs.append(stocks.df[stocks.df.underlying == cex].copy())
        labels.append(cex)

    plotter.plot_line_from_dfs(
        dfs=dfs,
        xs=xs,
        ys=ys,
        xlabel="Date",
        ylabel=ylabel,
        labels=labels,
        xticks_rotation=90,
        linestyles=linestyles,
        grid=True,
        markers=markers,
        file_name=os.path.join(
            "digital-assets-book", "fundamentals_ex_mkt_cap_revenue.png"
        ),
    )
    plotter.plot_line_from_dfs(
        dfs=dfs,
        xs=xs,
        ys=ys_asset,
        xlabel="Date",
        ylabel=ylabel_asset,
        labels=labels,
        file_name=os.path.join(
            "digital-assets-book", "fundamentals_ex_mkt_cap_net_asset.png"
        ),
        markers=markers,
        linestyles=linestyles,
        xticks_rotation=90,
        grid=True,
    )
    # ***************
    # Banks
    # ****************
    dfs = []
    labels = []
    # PLFs
    for plf in token_terminal.plf_tokens:
        dfs.append(token_terminal.get_quaterly_fundamentals(plf))
        labels.append(token_terminal.tokens_2_symbol[plf])

    for bank in banks.banks:
        dfs.append(banks.df[banks.df.underlying == bank].copy())
        labels.append(bank)

    plotter.plot_line_from_dfs(
        dfs=dfs,
        xs=xs,
        ys=ys,
        xlabel="Date",
        ylabel=ylabel,
        labels=labels,
        file_name=os.path.join(
            "digital-assets-book", "fundamentals_banks_mkt_cap_net_revenue.png"
        ),
        linestyles=linestyles,
        grid=True,
        markers=markers,
        xticks_rotation=90,
    )
    plotter.plot_line_from_dfs(
        dfs=dfs,
        xs=xs,
        ys=ys_asset,
        xlabel="Date",
        ylabel=ylabel_asset,
        labels=labels,
        file_name=os.path.join(
            "digital-assets-book", "fundamentals_banks_mkt_cap_net_asset.png"
        ),
        linestyles=linestyles,
        xticks_rotation=90,
        markers=markers,
        grid=True,
    )
