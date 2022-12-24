from rest_framework import serializers

from accounts.models import DataInjection
from dashboard.models import CoinSymbolCoinList, SearchBurketCoinIndexing


class CoinSynchronizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataInjection
        fields = ["sync"]
        

class CoinViewListSerializer(serializers.ModelSerializer):            
    class Meta:
        model = CoinSymbolCoinList
        fields = ["coin_symbol"]
    

class CoinBurketSerializer(serializers.ModelSerializer):    
    class Meta:
        model = SearchBurketCoinIndexing
        fields = ["coin_symbol"]