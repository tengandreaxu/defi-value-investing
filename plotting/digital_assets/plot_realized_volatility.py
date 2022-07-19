import os
from token_terminal.TokenTerminal import TokenTerminal
from wrds.StockDaily import StockDaily
from wrds.StockFundamentals import StockFundamentals
from plotting.Plotter import Plotter
from wrds.Banks import Banks

if __name__ == "__main__":

    plotter = Plotter()
    token_terminal = TokenTerminal()
    stocks_daily = StockDaily()
    stocks = StockFundamentals()
    banks = Banks()
    dfs = []
    labels = []

    # Yield Aggregators / Asset Managers
    for yield_ in token_terminal.yield_tokens:
        dfs.append(token_terminal.get_realized_historical_volatility(yield_))
        labels.append(token_terminal.tokens_2_symbol[yield_])

    for asset_manager in stocks.asset_managers:
        dfs.append(stocks_daily.get_realized_historical_volatility(asset_manager))
        labels.append(asset_manager)

    ys = ["realized_volatility" for _ in range(5)]
    xs = ["date" for _ in range(5)]
    linestyles = ["dashed", "dashed"]
    linestyles += ["solid" for _ in range(3)]
    markers = []
    ylabel = "Realized Historical Volatility 90d"
    plotter.plot_line_from_dfs(
        dfs=dfs,
        xs=xs,
        ys=ys,
        xlabel="Date",
        ylabel=ylabel,
        labels=labels,
        file_name=os.path.join(
            "digital-assets-book", "realized_std_asset_managers.png"
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
        dfs.append(token_terminal.get_realized_historical_volatility(dex))
        labels.append(token_terminal.tokens_2_symbol[dex])

    for cex in stocks.exchanges:
        dfs.append(stocks_daily.get_realized_historical_volatility(cex))
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
        file_name=os.path.join("digital-assets-book", "realized_std_ex.png"),
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
        dfs.append(stocks_daily.get_realized_historical_volatility(banks))
        labels.append(bank)

    plotter.plot_line_from_dfs(
        dfs=dfs,
        xs=xs,
        ys=ys,
        xlabel="Date",
        ylabel=ylabel,
        labels=labels,
        file_name=os.path.join("digital-assets-book", "realized_std_banks.png"),
        linestyles=linestyles,
        grid=True,
        markers=markers,
        xticks_rotation=90,
    )
