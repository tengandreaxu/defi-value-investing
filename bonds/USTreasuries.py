import pandas as pd
from dataclasses import dataclass


@dataclass
class USTreasuries:
    def __init__(self):

        self.treasury_10 = pd.read_csv("data/10-year-treasury-bond.csv")
        self.treasury_10 = self.treasury_10.dropna()
        self.treasury_10.date = pd.to_datetime(self.treasury_10.date).dt.date


if __name__ == "__main__":

    treasury = USTreasuries()
    breakpoint()
