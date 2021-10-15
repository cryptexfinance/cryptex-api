from flask import Blueprint
from flask import abort

import os

from . import INFURA_KEY

metrics_api = Blueprint("api", __name__, url_prefix="/metrics")


@metrics_api.route("/tokens/<token>/metrics", methods=["GET"])
def get_metrics(token: str) -> dict:
    """
    :param token: Token to get metrics for, either CTX or TCAP
    :return: Metrics for the token as a dict
    """
    pass