import requests
import os
import numpy as np
import pandas as pd
import multiprocessing as mp
from typing import Optional, Generator
from attributedict.collections import AttributeDict
from web3 import Web3
from web3.contract import Contract
from concurrent.futures import ThreadPoolExecutor
from retry import retry

import logging

logging.basicConfig(level=logging.INFO)

DEFAULT_BLOCK_INTERVAL = 1_000


class ArchiveNodeClient:
    """
    This class connects to the ethereum archive node via IPC
    The class and the node must be in the same server
    """

    def __init__(self, http_address: Optional[str] = "http://127.0.0.1:8545"):
        # **************
        # Connects to the node
        # **************
        self.address = http_address  # ""  #
        self.provider = Web3.HTTPProvider(self.address)
        self.w3 = Web3(self.provider)
        self.logger = logging.getLogger("ArchiveNodeClient")
        self.abi_base_url = "http://api.etherscan.io/api?module=contract&action=getabi&address={address}&format=raw"
        self.contract = None

        self.data_folder = "data"
        self.start_message()

    def start_message(self):
        self.logger.info(f"*" * 47)
        self.logger.info(f"Web3 Connected: \t {self.w3.isConnected()}")
        self.logger.info(f"Provider Address: \t {self.address}")
        self.logger.info(f"*" * 47)

    def get_contract(self, contract_address: str, abi_address: str) -> Contract:
        abi = self.fetch_abi(abi_address)
        return self.w3.eth.contract(abi=abi, address=contract_address)

    def get_all_events(self, contract_address: str, abi_address: str):
        self.contract = self.get_contract(contract_address, abi_address)
        breakpoint()

    def get_onchain_data(
        self,
        abi_address: str,
        contract_address: str,
        start_no: int,
        end_no: int,
        function_name: str,
        block_interval: int,
        contract_args: Optional[list] = None,
    ) -> Generator:
        """
        Description:
            retrieves on chain data,
            the code is taken from https://github.com/danhper/ethereum-tools

        Args:
            abi_address (str): [description]
            contract_address (str): [description]
            start_no (int): [description]
            end_no (int): [description]
            file_name (str): [description]
            function_name (str): [description]
            block_interval (int): fetch data every :block_interval
        """
        self.logger.info(f"Pulling {function_name} state: (block, value)")
        # ***************
        # we need the abi before pulling data
        # ***************
        self.contract = self.get_contract(contract_address, abi_address)
        results = self.collect_results(
            function_name,
            start_block=start_no,
            end_block=end_no,
            block_interval=block_interval,
            contract_args=contract_args,
        )

        return results

    def get_block_timestamp(
        self,
        start_block_number: int,
        end_block_number: int,
        processes: Optional[int] = 1,
        file_name: Optional[str] = "block_number_2_timestamp.csv",
    ) -> None:
        """
        retrieves the block data from the chain
        """
        items = []

        if processes < 2:
            while start_block_number <= end_block_number:
                item = self.pull_block_data(start_block_number)
                items.append(item)
                start_block_number += 1
        else:
            block_numbers = np.arange(start_block_number, end_block_number + 1, step=1)
            pool = mp.Pool(processes)
            items += pool.map(
                self.pull_block_data, [block_number for block_number in block_numbers]
            )

        df = pd.DataFrame(items)
        df.to_csv(os.path.join(self.data_folder, file_name), index=False)
        self.logger.info(f"File {file_name} correctly saved.")

    def pull_block_data(self, block_number: int) -> AttributeDict:
        self.logger.info(f"Retrieving Info for block_number: {block_number}")
        result = self.w3.eth.get_block(block_number)
        return self.create_block_item(result)

    def create_block_item(self, raw_block: AttributeDict) -> dict:
        return {
            "difficulty": raw_block.difficulty,
            "gasLimit": raw_block.gasLimit,
            "gasUsed": raw_block.gasUsed,
            "miner": raw_block.miner,
            "number": raw_block.number,
            "size": raw_block.size,
            "timestamp": raw_block.timestamp,
            "totalDifficulty": raw_block.totalDifficulty,
        }

    def fetch_abi(self, address: str, etherscan_api_key: Optional[str] = None) -> dict:
        """Retrieves the abi from etherscan,
        code is taken from https://github.com/danhper/ethereum-tools

        Args:
            address (str): [description]
            etherscan_api_key (Optional[str], optional): [description]. Defaults to None.

        Returns:
            dict: [description]
        """
        url = self.abi_base_url.format(address=address)
        if etherscan_api_key:
            url += f"&apikey={etherscan_api_key}"
        return requests.get(url).json()

    def collect_results(
        self,
        func_name,
        start_block,
        end_block=None,
        block_interval=DEFAULT_BLOCK_INTERVAL,
        contract_args=None,
    ):
        """collects the result from the archive node,
        code taken from https://github.com/danhper/ethereum-tools

        Args:
            func_name ([type]): [description]
            start_block ([type]): [description]
            end_block ([type], optional): [description]. Defaults to None.
            block_interval ([type], optional): [description]. Defaults to DEFAULT_BLOCK_INTERVAL.
            contract_args ([type], optional): [description]. Defaults to None.

        Returns:
            [type]: [description]

        Yields:
            [type]: [description]
        """
        max_workers = 10
        if end_block is None:
            end_block = self.contract.web3.eth.blockNumber
        if start_block is None:
            start_block = end_block
        if contract_args is None:
            contract_args = []

        def run_task(block):
            try:
                return self.call_func(func_name, block, contract_args)
            except Exception as ex:  # pylint: disable=broad-except
                self.logger.error("failed to fetch block %s: %s", block, ex)

        # **************************
        # Thread Pool Executor will just create a set of async workers
        # **************************
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            blocks = range(start_block, end_block + 1, block_interval)
            total_count = len(blocks)
            results = executor.map(run_task, blocks)
            for i, (block, result) in enumerate(zip(blocks, results)):
                if i % 10 == 0 and total_count > 10:
                    self.logger.info(
                        "progress: %s/%s (%.2f%%)",
                        i,
                        total_count,
                        i / total_count * 100,
                    )
                if result is not None:
                    yield (block, result)

    @retry(delay=1, backoff=2, tries=3)
    def call_func(self, func_name, block, contract_args):
        func = getattr(self.contract.functions, func_name)
        return func(*contract_args).call(block_identifier=block)


if __name__ == "__main__":

    archive = ArchiveNodeClient()

    archive.get_all_events("0x7Fc66500c84A76Ad7e9c93437bFc5Ac33E2DDaE9", "0xc13eac3b4f9eed480045113b7af00f7b5655ece8")