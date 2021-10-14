from flask import Flask
from flask import abort
import os

_INFURA_KEY = "INFURA_KEY"


def create_app():
    app = Flask(__name__, instance_relative_config=True)

    from api.controllers.web3_controller import Web3Controller
    from api.controllers.web3_controller import Contract

    CONTRACTS = {
        "tcap": Contract.tcap,
        "ctx": Contract.ctx,
    }

    @app.route("/cmc/tokens/<token>/total-supply", methods=["GET"])
    def cmc_total_supply(token: str) -> str:
        """
        Returns total supply of a token for CoinMarketCap
        :param token: Token to get total supply for, either CTX or TCAP
        :return: Total supply
        """
        try:
            controller = Web3Controller.infura(
                project_id=os.environ.get(_INFURA_KEY),
                contract=CONTRACTS[token]()
            )
        except KeyError:
            abort(404)
            raise Exception(f"Unable to get total supply for token '{token}'.")

        return controller.get_total_supply()

    return app


new_app = create_app()
