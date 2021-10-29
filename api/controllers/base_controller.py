from web3 import Web3


class BaseController:

    def __init__(self, provider: Web3.HTTPProvider):
        self._web3 = Web3(provider)

    @classmethod
    def infura(cls, project_id: str):
        """
        Creates a new Web3Controller with Infura as the Ethereum provider
        :param project_id: Infura project ID
        :return: Web3Controller
        """
        provider = Web3.HTTPProvider(f"https://mainnet.infura.io/v3/{project_id}")

        return cls(
            provider=provider
        )
