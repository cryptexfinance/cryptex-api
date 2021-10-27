from controllers.common.common import Common
from controllers.base_controller import BaseController
from models.token_contract import TokenContract
from models.prepared_contract import PreparedContract


class CMCController(BaseController):
    """
    Controller class for providing CoinMarketCap data
    """

    def get_total_supply(self, contract: TokenContract) -> str:
        """
        Queries the contract for the total supply
        :return: Total supply of the specified token
        """

        loaded_contract = PreparedContract.load_contract(
            web3=self._web3,
            contract=contract
        )
        total_supply_raw = Common.get_total_supply(
            loaded_contract=loaded_contract,
            should_convert_wei=True
        )

        return str(total_supply_raw)
