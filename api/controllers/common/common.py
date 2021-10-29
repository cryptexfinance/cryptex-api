from models.prepared_contract import PreparedContract


class Common:

    @staticmethod
    def get_total_supply(loaded_contract: PreparedContract, should_convert_wei: bool) -> int:
        """
        Queries the contract for the total supply
        :param loaded_contract: PreparedContract to get totalSupply for
        :param should_convert_wei: Whether or not the total supply should be converted from wei to ether
        :return: Total supply of the specified token
        """

        total_supply = loaded_contract.contract.functions.totalSupply().call()

        if should_convert_wei:
            total_supply = Common.wei_to_ether(total_supply)

        return int(total_supply)

    @staticmethod
    def get_reward_for_duration(loaded_contract: PreparedContract) -> int:
        """
        Queries the contract for the total supply
        :param loaded_contract: PreparedContract to get totalSupply for
        :param should_convert_wei: Whether or not the total supply should be converted from wei to ether
        :return: Total supply of the specified token
        """

        reward_rate_for_duration = loaded_contract.contract.functions.getRewardForDuration().call()
        reward_rate_for_duration = Common.wei_to_ether(reward_rate_for_duration)

        return int(reward_rate_for_duration)

    @staticmethod
    def wei_to_ether(wei: int) -> float:
        """
        Converts wei to ether based on JavaScript ethers.utils.formatEther
        :param wei: Amount in wei
        :return: Amount in ether
        """
        return wei // 1e18
