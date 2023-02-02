import os
from rest_framework.response import Response
from rest_framework.views import APIView
from oauth2_provider.contrib.rest_framework import IsAuthenticatedOrTokenHasScope, OAuth2Authentication

from web3_app.controllers import Web3Controller
from .models import Contract

class TotalSupplyTCAP(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
        controller = Web3Controller.infura(
            project_id = os.environ.get("INFURA_KEY"),
            contract = Contract.tcap()
        )
        return Response(controller.get_total_supply())

class TotalSupplyCTX(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
        controller = Web3Controller.infura(
            project_id=os.environ.get("INFURA_KEY"),
            contract=Contract.ctx()
        )
        return Response(controller.get_total_circulating_supply_ctx())

class TotalMarketCap(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
        controller = Web3Controller.infura(
            project_id=os.environ.get("INFURA_KEY"),
            contract=Contract.tcap_oracle()
        )

        return Response(controller.get_total_market_cap())

class TcapOraclePrice(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
        controller = Web3Controller.infura(
            project_id=os.environ.get("INFURA_KEY"),
            contract=Contract.tcap_oracle()
        )

        return Response(controller.get_tcap_price())

class TcapMarketPrice(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
        controller = Web3Controller.infura(
            project_id=os.environ.get("INFURA_KEY"),
            contract=Contract.tcap_oracle()
        )

        return Response(controller.get_tcap_market_price())