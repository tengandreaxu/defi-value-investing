import os
from plotting.Plotter import Plotter
from dune.pull_data import QUERIES_FINANCIALS
from dune.DuneDataManager import DuneDataManager

if __name__ == "__main__":

    data_manager = DuneDataManager()
    plotter = Plotter()

    for token in QUERIES_FINANCIALS.keys():

        df = data_manager.load_financial_dataset(token)
        df["cumsum"] = df.revenue.cumsum()

        plotter.plot_line(
            df,
            x="date",
            y="cumsum",
            xlabel="Date",
            ylabel="Cumulative Revenue",
            label=token,
            file_name=f"financials_{token}.png",
            set_millions=True,
        )
