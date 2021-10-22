import logging

from web3 import Web3
from web3.contract import Contract as W3Contract

from models.contract import Contract


class LoadedContract:

    def __init__(self, contract: W3Contract, decimals: int = 18):
        self.contract = contract
        self.decimals = decimals

    @classmethod
    def load_contract(cls, web3: Web3, contract: Contract):
        """
        Creates a Web3 Contract from a Contract
        :param web3: Web3 provider
        :param contract: Contract to load data from
        :return: LoadedContract, containing usable contract and decimals
        """

        # noinspection PyTypeChecker
        c = web3.eth.contract(
            address=contract.address,
            abi=contract.abi
        )

        try:
            decimals = c.functions.decimals().call()
        except Exception as e:
            logging.error(f"Error getting decimals from contract, falling back to 18. Error caught was: {e}")
            decimals = 18

        return cls(
            contract=c,
            decimals=decimals
        )
