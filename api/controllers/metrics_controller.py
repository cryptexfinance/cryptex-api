import logging

from controllers.common.common import Common
from controllers.base_controller import BaseController
from models.contract import Contract
from models.liquidity_pool import LiquidityPool
from models.loaded_contract import LoadedContract


class MetricsController(BaseController):
    STAKING_CONTRACTS = {
        "ctx": LiquidityPool.ctx_weth
    }

    def get_apy(self, contract: Contract) -> int:
        """
        Gets the current APY for a token based on its corresponding liquidity pool contract, eg. ctx/weth LP
        :param contract: Token contract to get current staking APY for
        :return: APY percentage as an int, eg. 28 for 28%
        """

        try:
            staking_contract = self.STAKING_CONTRACTS[contract.name]()
            loaded_staking_contract = LoadedContract.load_contract(
                web3=self._web3,
                contract=staking_contract
            )
        except KeyError as e:  # TODO: Raise Exception
            logging.error(f"Unable to load contract: {contract.name}!")
            raise e

        staking_contract_total_supply = Common.get_total_supply(loaded_contract=loaded_staking_contract)
        apy = self._calculate_apy(total_supply=staking_contract_total_supply)

        return apy

    @staticmethod
    def _calculate_apy(total_supply: int):
        """
        Calculate APY based on total supply within SushiSwap LP Contract for CTX/WETH
        :param total_supply: Total supply
        :return: Raw APY, unformatted
        """
        six_month_ctx_reward_amount = 60000
        total_staked = Common.wei_to_ether(wei=total_supply)

        apy = round(((2 * six_month_ctx_reward_amount) / total_staked) * 100)
        return apy
