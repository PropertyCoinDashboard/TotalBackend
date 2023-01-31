from rest_framework import serializers

from accounts.models import DataInjection
from dashboard.models import (
    CoinSymbolCoinList, SearchBurketCoinIndexing,
)


class CoinSynchronizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataInjection
        fields = ["sync"]
        
        
class CoinBurketSerializer(serializers.ModelSerializer):    
    class Meta:
        model = SearchBurketCoinIndexing
        fields = ["coin_symbol"]
        

class CoinViewExistSerializer(serializers.ModelSerializer):            
    class Meta:
        model = CoinSymbolCoinList
        fields = ["upbit_existence", "bithum_existence", "korbit_existence"]       
       
 
class CoinViewListSerializer(serializers.ModelSerializer):            
    class Meta:
        model = CoinSymbolCoinList
        fields = ["coin_symbol", "korea_name"]

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['market_depend'] = CoinViewExistSerializer(instance).data
        return response    
    

