import os

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import matplotlib.dates as mdates
import matplotlib.pylab as pylab

from typing import Optional

import logging

logging.basicConfig(level=logging.INFO)

# *******************
# PALETTE and STYLES
# *******************
params = {
    "axes.labelsize": 14,
    "axes.labelweight": "bold",
    "xtick.labelsize": 12,
    "ytick.labelsize": 12,
    "axes.titlesize": 12,
}
pylab.rcParams.update(params)


def millions(x, pos):
    """x value, pos positions"""
    return "$%1.0fM" % (x * 10 ** (-6))


class Plotter:
    def __init__(self):

        # *******************
        # Logger
        # *******************
        self.logger = logging.getLogger("Plotter")

        self.colors = ["black", "brown", "green", "blue", "pink"]

    def format_yticks_in_millions(self, ax):
        """Format the y ticks to show dollar sign and format in millions"""

        tick = mtick.FuncFormatter(millions)
        ax.yaxis.set_major_formatter(tick)

    def format_xticks_using_concise_date_formatter(self, ax):
        """ "Format x ticks to use the concise date formatter
        source: https://matplotlib.org/stable/gallery/text_labels_and_annotations/date.html
        """

        ax.xaxis.set_major_formatter(
            mdates.ConciseDateFormatter(ax.xaxis.get_major_locator())
        )

    def plot_line(
        self,
        df: pd.DataFrame,
        x: str,
        y: str,
        xlabel: str,
        ylabel: str,
        label: str,
        file_name: str,
        title: Optional[str] = "",
        grid: Optional[bool] = False,
        ylim: Optional[list] = [],
        folder: Optional[str] = "",
        set_millions: Optional[bool] = False,
    ):
        plt.plot(df[x], df[y], label=label, color="black")
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.legend()
        plt.grid(grid)
        plt.title(title)
        if len(ylim) > 0:
            ax = plt.gca()
            ax.set_ylim(ylim)

        if set_millions:
            ax = plt.gca()
            self.format_yticks_in_millions(ax)

        plt.tight_layout()

        save_folder = self.get_save_folder(folder)
        plt.savefig(os.path.join(save_folder, file_name))
        plt.close()

    def plot_scatter(
        self,
        df: pd.DataFrame,
        x: str,
        y: str,
        xlabel: str,
        ylabel: str,
        label: str,
        file_name: str,
        title: Optional[str] = "",
        grid: Optional[bool] = False,
        ylim: Optional[list] = [],
        folder: Optional[str] = "",
    ):
        plt.scatter(df[x], df[y], label=label, color="black")
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.legend()
        plt.grid(grid)
        plt.title(title)
        if len(ylim) > 0:
            ax = plt.gca()
            ax.set_ylim(ylim)
        plt.tight_layout()

        save_folder = self.get_save_folder(folder)
        plt.savefig(os.path.join(save_folder, file_name))
        plt.close()

    def plot_line_from_dfs(
        self,
        dfs: list,
        xs: list,
        ys: list,
        xlabel: str,
        ylabel: str,
        labels: list,
        file_name: str,
        title: Optional[str] = "",
        grid: Optional[bool] = False,
        ylim: Optional[list] = [],
        xticks_rotation: Optional[int] = 0,
        folder: Optional[str] = "",
    ):

        for (df, x, y, label, color) in zip(dfs, xs, ys, labels, self.colors):
            plt.plot(df[x], df[y], label=label, color=color)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.legend()
        plt.grid(grid)
        plt.title(title)

        ax = plt.gca()
        if len(ylim) > 0:
            ax.set_ylim(ylim)

        if xticks_rotation > 0:
            for tick in ax.get_xticklabels():
                tick.set_rotation(xticks_rotation)
        save_folder = self.get_save_folder(folder)
        plt.tight_layout()
        plt.savefig(os.path.join(save_folder, file_name))
        plt.close()

    def plot_line_from_columns(
        self,
        df: pd.DataFrame,
        x: str,
        ys: list,
        xlabel: str,
        ylabel: str,
        labels: str,
        file_name: str,
        linestyles: list,
        title: Optional[str] = "",
        grid: Optional[bool] = False,
        ylim: Optional[list] = [],
        xticks_rotation: Optional[int] = 0,
        folder: Optional[str] = "",
    ):

        for (y, label, color, linestyle) in zip(ys, labels, self.colors, linestyles):
            plt.plot(df[x], df[y], label=label, color=color, linestyle=linestyle)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.legend()
        plt.grid(grid)
        plt.title(title)

        ax = plt.gca()
        if len(ylim) > 0:
            ax.set_ylim(ylim)

        if xticks_rotation > 0:
            for tick in ax.get_xticklabels():
                tick.set_rotation(xticks_rotation)

        plt.tight_layout()
        save_folder = self.get_save_folder(folder)
        plt.savefig(os.path.join(save_folder, file_name))
        plt.close()

    def get_save_folder(self, folder: str) -> str:
        save_folder = "plots"
        if len(folder) > 0:
            save_folder = os.path.join("plots", folder)
            os.makedirs(save_folder, exist_ok=True)
        return save_folder
