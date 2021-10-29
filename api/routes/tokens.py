import os
from typing import Union

from flask import Blueprint
from flask import Response
from flask import abort
from flask import jsonify
from flask import request

from controllers.metrics_controller import MetricsController
from models.token_contract import TokenContract
from routes import INFURA_KEY
from static.contracts import CONTRACTS

tokens_api = Blueprint("tokens_api", __name__, url_prefix="/tokens")

BASE_ROUTE = "/<token>"


class MetricsKeys:
    TOTAL_SUPPLY = "total_supply"
    APY_PERCENTAGE = "apy_percentage"


@tokens_api.route(BASE_ROUTE, methods=["GET"])
def get_all_metrics(token: str) -> Response:
    """
    :param token: Token to get metrics for, either CTX or TCAP
    :return: JSON response containing all metrics for a given token
    """
    controller = MetricsController.infura(
        project_id=os.environ.get(INFURA_KEY),
    )

    try:
        contract: TokenContract = CONTRACTS[token]()
    except KeyError:
        abort(404)
        raise Exception(f"Unable to get metrics for token '{token}'.")

    metrics = {}

    if contract.can_stake:
        metrics[MetricsKeys.APY_PERCENTAGE] = controller.get_apy(contract=contract)

    metrics[MetricsKeys.TOTAL_SUPPLY] = controller.get_total_supply(contract=contract)
    return jsonify(
        metrics
    )


@tokens_api.route(f"{BASE_ROUTE}/apy", methods=["GET"])
def get_apy(token: str) -> Response:
    """
    :param token: Token to get staking APY for. Only CTX is supported
    :return: JSON response containing the raw APY percentage
    """
    controller = MetricsController.infura(
        project_id=os.environ.get(INFURA_KEY),
    )

    try:
        contract = CONTRACTS[token]()
    except KeyError:
        abort(404)
        raise Exception(f"Unable to get staking APY for token '{token}'.")

    apy = controller.get_apy(contract=contract)
    return jsonify({MetricsKeys.APY_PERCENTAGE: apy})


@tokens_api.route(f"{BASE_ROUTE}/total-supply", methods=["GET"])
def get_total_supply(token: str) -> Union[str, Response]:
    """
    :param token: Token to get total supply for, either CTX or TCAP
    :return: JSON response containing the raw APY percentage
    """
    controller = MetricsController.infura(
        project_id=os.environ.get(INFURA_KEY),
    )

    is_cmc_request: str = request.args.get("cmc", "false")
    try:
        contract = CONTRACTS[token]()
    except KeyError:
        abort(404)
        raise Exception(f"Unable to get total supply for token '{token}'.")

    total_supply = controller.get_total_supply(contract=contract)

    if is_cmc_request.lower() == "true":
        return str(total_supply)
    return jsonify({MetricsKeys.TOTAL_SUPPLY: total_supply})
