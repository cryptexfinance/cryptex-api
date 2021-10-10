from flask import Flask
import os

_INFURA_KEY = "INFURA_KEY"


def create_app():
    app = Flask(__name__, instance_relative_config=True)

    from api.controllers.web3_controller import Web3Controller
    from api.controllers.web3_controller import Contract

    @app.route("/total-supply-tcap", methods=["GET"])
    def total_supply_tcap():
        controller = Web3Controller.infura(
            project_id=os.environ.get(_INFURA_KEY),
            contract=Contract.tcap()
        )
        return controller.get_total_supply()

    @app.route("/total-supply-ctx", methods=["GET"])
    def total_supply_ctx():
        controller = Web3Controller.infura(
            project_id=os.environ.get(_INFURA_KEY),
            contract=Contract.ctx()
        )

        return controller.get_total_supply()

    return app


new_app = create_app()

# if __name__ == "__main__":
#     create_app().run(host="0.0.0.0")
