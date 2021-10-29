import logging
import os
from typing import Union

from flask import Blueprint
from flask import abort
from flask import jsonify
from flask import Response
from flask import request

from controllers.metrics_controller import MetricsController
from routes import INFURA_KEY
from static.contracts import CONTRACTS
from models.token_contract import TokenContract

tokens_api = Blueprint("tokens_api", __name__, url_prefix="/tokens")


class MetricsKeys:
    TOTAL_SUPPLY = "total_supply"
    APY_PERCENTAGE = "apy_percentage"
    STAKING_TOKEN = "staking_token"
    REWARDS_TOKEN = "rewards_token"
    WAIT_TIME = "wait_time"
    PERIOD_FINISH = "period_finish"
    REWARD_RATE = "reward_rate"
    REWARDS_DURATION = "rewards_duration"
    LAST_UPDATE_TIME = "last_update_time"
    REWARD_PER_TOKEN_STORED = "reward_per_token_stored"


@tokens_api.route("/<token>", methods=["GET"])
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
        metrics[MetricsKeys.REWARD_RATE] = controller.get_reward_rate_for_duration(contract=contract)

    metrics[MetricsKeys.TOTAL_SUPPLY] = controller.get_total_supply(contract=contract)
    return jsonify(
        metrics
    )


@tokens_api.route("/<token>/apy", methods=["GET"])
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


@tokens_api.route("/<token>/total-supply", methods=["GET"])
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
