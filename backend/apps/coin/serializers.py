from rest_framework import serializers
from collections import OrderedDict
from .models import (
    CoinSymbolCoinList,
    BitcoinEndPriceData,
    EthereumEndPriceData,
    RippleEndPriceData,
)


class CoinViewExistSerializer(serializers.ModelSerializer):
    """
    코인 상장 여부
    """

    class Meta:
        model = CoinSymbolCoinList
        fields = ("upbit_existence", "bithum_existence", "korbit_existence", "coinone_existence")


class CoinViewListSerializer(serializers.ModelSerializer):
    class Meta:
        model = CoinSymbolCoinList
        fields = ("coin_symbol",)

    def to_representation(self, instance) -> OrderedDict:
        response = super().to_representation(instance)
        response["market_depend"] = CoinViewExistSerializer(instance).data
        return response


class CoinEndPriceCollectSerializer(serializers.ModelSerializer):
    timestamp = serializers.DateField(format="%Y-%m-%d")
    trade_price = serializers.FloatField()

    class Meta:
        fields = ("timestamp", "trade_price")


# End Price BTC, ETH
class BtcEndPriceSerializer(CoinEndPriceCollectSerializer):
    class Meta(CoinEndPriceCollectSerializer.Meta):
        model = BitcoinEndPriceData


class EthEndPriceSerializer(CoinEndPriceCollectSerializer):
    class Meta(CoinEndPriceCollectSerializer.Meta):
        model = EthereumEndPriceData


class XrpEndPriceSerializer(CoinEndPriceCollectSerializer):
    class Meta(CoinEndPriceCollectSerializer.Meta):
        model = RippleEndPriceData
