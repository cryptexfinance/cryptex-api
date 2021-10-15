from flask import Blueprint
from flask import abort
import os

from controllers.web3_controller import Web3Controller
from static.contracts import CONTRACTS

INFURA_KEY = "INFURA_KEY"

# Separate the /cmc route as CoinMarketCap requires _only_ totalSupply in raw/non-JSON format
cmc_api = Blueprint("api", __name__, url_prefix="/cmc")


@cmc_api.route("/tokens/<token>", methods=["GET"])
def cmc_total_supply(token: str) -> str:
    """
    Returns total supply of a token for CoinMarketCap
    :param token: Token to get total supply for, either CTX or TCAP
    :return: Total supply
    """
    try:
        controller = Web3Controller.infura(
            project_id=os.environ.get(INFURA_KEY),
            contract=CONTRACTS[token]()
        )
    except KeyError:
        abort(404)
        raise Exception(f"Unable to get total supply for token '{token}'.")

    return controller.get_total_supply()
