from django.db import models
from django.core.validators import MaxLengthValidator
from django.utils.translation import gettext_lazy as _


# 공통
class Timestamp(models.Model):
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract: bool = True


"""
## ---------------- Symbol 쓰는 class ------------------ ##
"""


class CoinSymbolCoinList(Timestamp):
    coin_symbol = models.CharField(
        max_length=16,
        unique=True,
        primary_key=True,
        validators=[MaxLengthValidator(limit_value=6)],
    )
    bithum_existence = models.BooleanField()
    upbit_existence = models.BooleanField()
    korbit_existence = models.BooleanField()

    class Meta:
        db_table: str = "coin_symbol"
        db_table_comment: str = "코인 심볼 테이블"
        indexes = [models.Index(fields=["coin_symbol"], name="symbol_index")]


class CoinUpbithumTradingData(Timestamp):
    timestamp = models.DateField()
    trade_price = models.FloatField()

    class Meta:
        abstract: bool = True
        indexes = [
            models.Index(fields=["timestamp"], name="coin_endprice_time"),
        ]


class BitcoinEndPriceData(CoinUpbithumTradingData):
    class Meta:
        db_table: str = "BTC_coin_end_price_and_upbithumb"
        db_table_comment: str = "비트코인 마지막 거래가"


class EthereumEndPriceData(CoinUpbithumTradingData):
    class Meta:
        db_table: str = "ETH_coin_end_price_and_upbithumb"
        db_table_comment: str = "이더리움 마지막 거래가"   

"""
## ---------------------------------------------------- ##
"""
