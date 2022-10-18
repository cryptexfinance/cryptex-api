from flask import Blueprint
import os
web3_blueprint = Blueprint('web3_app', __name__)

_INFURA_KEY = "INFURA_KEY"


from api.web3_app.controllers.web3_controller import Web3Controller
from api.web3_app.controllers.web3_controller import Contract


@web3_blueprint.route("/total-supply-tcap", methods=["GET"])
def total_supply_tcap():
    controller = Web3Controller.infura(
        project_id=os.environ.get(_INFURA_KEY),
        contract=Contract.tcap()
    )
    return controller.get_total_supply()

@web3_blueprint.route("/total-supply-ctx", methods=["GET"])
def total_supply_ctx():
    controller = Web3Controller.infura(
        project_id=os.environ.get(_INFURA_KEY),
        contract=Contract.ctx()
    )

    return controller.get_total_circulating_supply_ctx()

@web3_blueprint.route("/total-market-cap", methods=["GET"])
def total_market_cap():
    controller = Web3Controller.infura(
        project_id=os.environ.get("INFURA_KEY"),
        contract=Contract.tcap_oracle()
    )

    return controller.get_total_market_cap()

@web3_blueprint.route("/tcap-price", methods=["GET"])
def tcap_price():
    controller = Web3Controller.infura(
        project_id=os.environ.get("INFURA_KEY"),
        contract=Contract.tcap_oracle()
    )

    return controller.get_tcap_price()
