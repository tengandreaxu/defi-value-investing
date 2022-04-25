import os
import pandas as pd

from web3 import Web3
from enum import Enum
from archive_node.ArchiveNodeClient import ArchiveNodeClient
from parameters.constants import END_BLOCK
from parameters.Contracts import AAVE_POOLS
from models.AAVE import AAVE

import logging


logging.basicConfig(level=logging.INFO)


class EgetReserveData(Enum):

    configuration = "configuration"
    liquidityIndex = "liquidityIndex"
    variableBorrowIndex = "variableBorrowIndex"
    currentLiquidityRate = "currentLiquidityRate"
    currentVariableBorrowRate = "currentVariableBorrowRate"
    currentStableBorrowRate = "currentStableBorrowRate"
    lastUpdateTimestamp = "lastUpdateTimestamp"
    aTokenAddress = "aTokenAddress"
    stableDebtTokenAddress = "stableDebtTokenAddress"
    variableDebtTokenAddress = "variableDebtTokenAddress"
    interestRateStrategyAddress = "interestRateStrategyAddress"
    id = "id"


if __name__ == "__main__":
    """
    This script given retrieves the state and configuration
    for a particular reserve.

    The collected data variables:

    1. configuration
    2. liquidityIndex, in ray
    3. variableBorrowIndex, in ray
    4. currentLiquidityRate, in ray
    5. currentVariableBorrowRate, in ray
    6. currentStateBorrowRate, in ray
    7. lastUpdateTimestamp
    8. aTokenAddress
    9. stableDebtTokenAddress
    10. variableDebtTokenAddress
    11. interestRateStrategyAddress
    12. id

    For further details see:
    https://docs.aave.com/developers/v/2.0/the-core-protocol/lendingpool#EEEEgetReserveData
    """

    data_folder = os.path.join("data", "aave_reserves")
    os.makedirs(data_folder, exist_ok=True)

    client = ArchiveNodeClient()  # MORALIS_HTTP)

    aave = AAVE()
    # *****************
    # we don't want to pull data that we have already
    # *****************
    we_have_tokens = os.listdir(data_folder)
    we_have_tokens = [x.replace(".csv", "") for x in we_have_tokens]

    no_lending_pools = open("no_reserve_aave.log")
    no_lending_pools_tokens = no_lending_pools.readlines()
    no_lending_pools_tokens = [x.replace("\n", "") for x in no_lending_pools_tokens]

    for aave_pool in AAVE_POOLS:

        for _, token in aave.tokens.iterrows():

            if (
                token.symbol in we_have_tokens
                or token.symbol in no_lending_pools_tokens
            ):
                continue

            logging.info(f"*" * 47)
            logging.info(
                f"Pulling Lending Pool Reserve Data: {token.symbol} \t {token.id}"
            )
            logging.info(f"*" * 47)
            results = client.get_onchain_data(
                abi_address=aave_pool.abi,
                contract_address=aave_pool.contract_address,
                start_no=aave_pool.start_block,
                end_no=END_BLOCK,
                function_name="getReserveData",
                block_interval=1,
                contract_args=[Web3.toChecksumAddress(token.underlyingAsset.lower())],
            )

            df = []

            for x in results:
                if x[1][4] == 0:
                    with open("no_reserve_aave.log", "a") as f:
                        f.write(f"{token.symbol}")
                        f.write(f"\n")
                    break
                df.append(
                    {
                        "block_number": x[0],
                        EgetReserveData.configuration.value: x[1][0],
                        EgetReserveData.liquidityIndex.value: x[1][1],
                        EgetReserveData.variableBorrowIndex.value: x[1][2],
                        EgetReserveData.currentLiquidityRate.value: x[1][3],
                        EgetReserveData.currentVariableBorrowRate.value: x[1][4],
                        EgetReserveData.currentStableBorrowRate.value: x[1][5],
                        EgetReserveData.lastUpdateTimestamp.value: x[1][6],
                        EgetReserveData.aTokenAddress.value: x[1][7],
                        EgetReserveData.stableDebtTokenAddress.value: x[1][8],
                        EgetReserveData.variableDebtTokenAddress.value: x[1][9],
                        EgetReserveData.interestRateStrategyAddress.value: x[1][10],
                        EgetReserveData.id.value: x[1][11],
                    }
                )
            df = pd.DataFrame(df)
            df.to_csv(os.path.join(data_folder, f"{token.symbol}.csv"), index=False)
