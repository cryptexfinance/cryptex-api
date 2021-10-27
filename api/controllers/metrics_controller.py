import logging

from controllers.common.common import Common
from controllers.base_controller import BaseController
from models.token_contract import TokenContract
from models.staking_contract import StakingContract
from models.prepared_contract import PreparedContract


class MetricsController(BaseController):
    STAKING_CONTRACTS = {
        "ctx": StakingContract.ctx
    }

    def get_apy(self, contract: TokenContract) -> int:
        """
        Gets the current APY for a token based on its corresponding liquidity pool contract, eg. ctx/weth LP
        :param contract: Token contract to get current staking APY for
        :return: APY percentage as an int, eg. 28 for 28%
        """

        try:
            staking_contract = self.STAKING_CONTRACTS[contract.name]()
            loaded_staking_contract = PreparedContract.load_contract(
                web3=self._web3,
                contract=staking_contract
            )
        except KeyError as e:  # TODO: Raise Exception
            logging.error(f"Token '{contract.name}' does not support staking!")
            raise e

        staking_contract_total_supply = Common.get_total_supply(
            loaded_contract=loaded_staking_contract,
            should_convert_wei=False
        )
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
