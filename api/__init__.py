from flask import Flask
import os

# _INFURA_KEY = "INFURA_KEY"


def create_app():
    app = Flask(__name__, instance_relative_config=True)

    from api.controllers.web3_controller import Web3Controller
    from api.controllers.web3_controller import Contract

    @app.route("/total-supply-tcap", methods=["GET"])
    def total_supply_tcap():
        controller = Web3Controller.infura(
            project_id=os.environ.get("INFURA_KEY"),
            contract=Contract.tcap()
        )
        return controller.get_total_supply()

    @app.route("/total-supply-ctx", methods=["GET"])
    def total_supply_ctx():
        print(" key ")
        print(os.environ.get("INFURA_KEY"))
        controller = Web3Controller.infura(
            project_id=os.environ.get("INFURA_KEY"),
            contract=Contract.ctx()
        )

        return controller.get_total_circulating_supply_ctx()

    @app.route("/total-crypto-market-cap", methods=["GET"])
    def total_market_cap():
        controller = Web3Controller.infura(
            project_id=os.environ.get("INFURA_KEY"),
            contract=Contract.tcap_oracle()
        )

        return controller.get_total_market_cap()

    @app.route("/tcap-oracle-price", methods=["GET"])
    def tcap_price():
        controller = Web3Controller.infura(
            project_id=os.environ.get("INFURA_KEY"),
            contract=Contract.tcap_oracle()
        )

        return controller.get_tcap_price()

    @app.route("/tcap-market-price", methods=["GET"])
    def tcap_market_price():
        controller = Web3Controller.infura(
            project_id=os.environ.get("INFURA_KEY"),
            contract=Contract.tcap_oracle()
        )

        return controller.get_tcap_market_price()    

    return app


new_app = create_app()
