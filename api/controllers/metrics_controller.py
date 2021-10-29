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

        staking_contract = self._get_staking_contract(contract=contract)

        staking_contract_total_supply = Common.get_total_supply(
            loaded_contract=staking_contract,
            should_convert_wei=False
        )
        apy = self._calculate_apy(total_supply=staking_contract_total_supply)

        return apy

    def get_total_supply(self, contract: TokenContract) -> int:
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

        return total_supply_raw

    # TODO: This is likely not returning the proper value
    def get_reward_rate_for_duration(self, contract: TokenContract) -> int:
        """
        Queries the contract for the total supply
        :return: Total supply of the specified token
        """

        staking_contract = self._get_staking_contract(contract=contract)

        reward_rate_for_duration = Common.get_reward_for_duration(
            loaded_contract=staking_contract
        )

        return reward_rate_for_duration

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

    def _get_staking_contract(self, contract: TokenContract) -> PreparedContract:
        """
        Gets a staking contract for a given token contract
        :param contract: Contract to get the staking contract for
        :return: PreparedContract for the staking contract
        """
        try:
            staking_contract = self.STAKING_CONTRACTS[contract.name]()
            return PreparedContract.load_contract(
                web3=self._web3,
                contract=staking_contract
            )
        except KeyError as e:  # TODO: Raise Exception
            logging.error(f"Token '{contract.name}' does not support staking!")
            raise e
