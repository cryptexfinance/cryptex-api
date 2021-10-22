from models.loaded_contract import LoadedContract


class Common:

    @staticmethod
    def get_total_supply(loaded_contract: LoadedContract) -> int:
        """
        Queries the contract for the total supply
        :return: Total supply of the specified token
        """

        total_supply_raw = loaded_contract.contract.functions.totalSupply().call()
        total_supply = total_supply_raw // loaded_contract.decimals

        return total_supply

    @staticmethod
    def wei_to_ether(wei: int) -> float:
        """
        Converts wei to ether based on JavaScript ethers.utils.formatEther
        :param wei: Amount in wei
        :return: Amount in ether
        """
        return wei / 1e18
