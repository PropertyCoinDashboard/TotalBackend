from typing import List
from rest_framework import serializers

from accounts.models import DataInjection
from dashboard.models import CoinSymbolCoinList


class CoinSynchronizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataInjection
        fields: List[str] = ["sync"]
        

class CoinViewListSerializer(serializers.ModelSerializer):
    class Meta:
        model = CoinSymbolCoinList
        fields: List[str] = ["coin_symbol"]
        
