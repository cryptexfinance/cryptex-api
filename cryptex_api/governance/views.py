from rest_framework.response import Response
from rest_framework.views import APIView
from oauth2_provider.contrib.rest_framework import IsAuthenticatedOrTokenHasScope, OAuth2Authentication

from .controllers import CryptKeeperController
from .serializers import KeeperSerializer


class CreateKeeper(APIView):
    authentication_classes = [OAuth2Authentication]
    permission_classes = [IsAuthenticatedOrTokenHasScope]
    required_scopes = ['write']

    def post(self, request, format=None):
        keeper = CryptKeeperController(False)
        reponse = keeper.create(request.POST, request.FILES)
        
        return Response(reponse)

class UpdateKeeper(APIView):  
    authentication_classes = [OAuth2Authentication]
    permission_classes = [IsAuthenticatedOrTokenHasScope]
    required_scopes = ['write']

    def post(self, request, format=None):  
        keeper = CryptKeeperController(True)
        reponse = keeper.update(request.POST, request.FILES)
        return Response(reponse)


class KeepersAll(APIView):
    authentication_classes = []
    permission_classes = []
    serializer_class = KeeperSerializer

    def get(self, request, format=None):
        keeper = CryptKeeperController(False)
        keepers = keeper.all()

        serializer = self.serializer_class(keepers, many=True)

        return Response(serializer.data)

