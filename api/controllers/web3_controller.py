from web3 import Web3
import logging

from models.contract import Contract


class Web3Controller:
    """
    Controller class for interacting with the TCAP contract
    """

    def __init__(self, provider: Web3.HTTPProvider, contract: Contract):
        self._web3 = Web3(provider)
        # noinspection PyTypeChecker
        self._contract = self._web3.eth.contract(
            address=contract.address,
            abi=contract.abi
        )

        try:
            self._decimals = self._contract.functions.decimals().call()
        except Exception as e:
            logging.error(f"Error getting decimals from contract, falling back to 18. Error caught was: {e}")
            self._decimals = 18

    @property
    def decimals(self) -> int:
        return 10 ** self._decimals

    @decimals.setter
    def decimals(self, decimals: int):
        self._decimals = decimals

    @classmethod
    def infura(cls, project_id: str, contract: Contract):
        """
        Creates a new Web3Controller with Infura as the Ethereum provider
        :param project_id: Infura project ID
        :param contract: Contract to use
        :return: Web3Controller
        """
        provider = Web3.HTTPProvider(f"https://mainnet.infura.io/v3/{project_id}")

        return cls(
            provider=provider,
            contract=contract
        )

    def get_total_supply(self) -> str:
        """
        Queries the contract for the total supply
        :return: Total supply of TCAP
        """

        total_supply_raw = self._contract.functions.totalSupply().call()
        total_supply = total_supply_raw // self.decimals

        return str(total_supply)

