import logging

from web3 import Web3
from web3.contract import Contract as W3Contract
from web3.exceptions import ABIFunctionNotFound

from models.token_contract import TokenContract
from models.staking_contract import StakingContract


class PreparedContract:

    def __init__(self, contract: W3Contract, decimals: int = 18):
        self.contract = contract
        self.decimals = decimals

    @classmethod
    def load_contract(cls, web3: Web3, contract: TokenContract):
        """
        Creates a Web3 Contract from a Contract
        :param web3: Web3 provider
        :param contract: Contract to load data from
        :return: PreparedContract, containing usable contract and decimals
        """

        # noinspection PyTypeChecker
        c = web3.eth.contract(
            address=contract.address,
            abi=contract.abi
        )

        decimals = 18
        if not isinstance(contract, StakingContract):
            try:
                decimals = c.functions.decimals().call()
            except ABIFunctionNotFound:
                logging.warning(f"The contract '{contract.address}' does not support the decimals function. "
                                f"Falling back to {decimals} decimals.")
            except Exception as e:
                logging.error(f"An unhandled error was caught. Falling back to {decimals} decimals. Error is: {e}")

        return cls(
            contract=c,
            decimals=decimals
        )
