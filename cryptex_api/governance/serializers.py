from rest_framework import serializers
from .models import CryptKeeper


class KeeperSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CryptKeeper
        fields = ['id', 'address', 'name', 'eth_name', 'expertise', 'why', 'image', 'discord', 'twitter']