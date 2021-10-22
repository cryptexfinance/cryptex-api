from common.common import Common
from controllers.base_controller import BaseController
from models.contract import Contract
from models.loaded_contract import LoadedContract


class CMCController(BaseController):
    """
    Controller class for providing CoinMarketCap data
    """

    def get_total_supply(self, contract: Contract) -> str:
        """
        Queries the contract for the total supply
        :return: Total supply of the specified token
        """

        loaded_contract = LoadedContract.load_contract(
            web3=self._web3,
            contract=contract
        )
        total_supply_raw = Common.get_total_supply(loaded_contract=loaded_contract)

        return str(total_supply_raw)
