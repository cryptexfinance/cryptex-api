from web3 import Web3
import logging

from api.models.contract import Contract

# Addresses must be in lower case
_FOUNDERS_ADDRESS = "0x7059928231d115bb47d46fdfd5e574c5e4fe38c0"
_LIQUIDITY_REWARD_ADDRESS = "0xc8bb1cd417d20116387a5e0603e195ca4f3cf59a"
_LIQUIDITY_REWARD2_ADDRESS = "0xdc4cdd5db9ee777efd891690dc283638cb3a5f94"
_MULTISIG_ADDRESS = "0xa70b638b70154edfcbb8dbbbd04900f328f32c35"
_TREASURY_ADDRESS = "0xa54074b2cc0e96a43048d4a68472f7f046ac0da8"

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
    
    def get_total_circulating_supply_ctx(self) -> str:
        """
        Queries the contract for the total supply
        :return: Total circulating supply of CTX
        """

        total_supply_raw = self._contract.functions.totalSupply().call()
        founders_total_raw = self._contract.functions.balanceOf(
            self._web3.toChecksumAddress(_FOUNDERS_ADDRESS)
        ).call()
        initial_incentive_raw = self._contract.functions.balanceOf(
            self._web3.toChecksumAddress(_LIQUIDITY_REWARD_ADDRESS)
        ).call()
        initial_incentive2_raw = self._contract.functions.balanceOf(
            self._web3.toChecksumAddress(_LIQUIDITY_REWARD2_ADDRESS)
        ).call()
        multisig_raw = self._contract.functions.balanceOf(
            self._web3.toChecksumAddress(_MULTISIG_ADDRESS)
        ).call()
        treasury_total_raw = self._contract.functions.balanceOf(
            self._web3.toChecksumAddress(_TREASURY_ADDRESS)
        ).call()

        ciculating_supply_raw = total_supply_raw - founders_total_raw - initial_incentive_raw - initial_incentive2_raw - \
                                multisig_raw - treasury_total_raw

        total_circulating_supply = ciculating_supply_raw // self.decimals

        return str(total_circulating_supply)

