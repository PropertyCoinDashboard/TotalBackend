from rest_framework import serializers
from ...dashboaring.models import CoinSymbolCoinList


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
        response["market_depend"] = CoinViewExistSerializer(instance).data
        return response
