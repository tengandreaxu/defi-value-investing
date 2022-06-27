from bonds.USTreasuries import USTreasuries
from plotting.Plotter import Plotter

if __name__ == "__main__":
    """
    Reads and Plots the 10 year treasury bond
    """
    plotter = Plotter()
    treasury = USTreasuries()

    plotter.plot_line(
        treasury.treasury_10,
        x="date",
        y="value",
        xlabel="Date",
        ylabel="Interest Rate",
        label="",
        file_name="digital-assets-book/10-year-treasury-bond.png",
        grid=True,
    )
