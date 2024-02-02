from collections.abc import Iterable
from django.db import models
from django.core.validators import MaxLengthValidator
from django.utils.translation import gettext_lazy as _


# 공통
class Timestamp(models.Model):
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract: bool = True


# 공통
class CoinTradingData(Timestamp):
    timestamp = models.DateField()
    trade_price = models.FloatField()

    class Meta:
        abstract: bool = True
        app_label: str = "coin"
        indexes = [models.Index(fields=["timestamp"], name="coin_endprice_time")]

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
    coinone_existence = models.BooleanField()

    class Meta:
        db_table: str = "coin_symbol"
        db_table_comment: str = "코인 심볼 테이블"
        app_label: str = "coin"
        indexes = [models.Index(fields=["coin_symbol"], name="symbol_index")]


class BitcoinEndPriceData(CoinTradingData):
    class Meta:
        db_table: str = "BTC_coin_end_price_and_upbithumb"
        db_table_comment: str = "비트코인 마지막 거래가"


class EthereumEndPriceData(CoinTradingData):
    class Meta:
        db_table: str = "ETH_coin_end_price_and_upbithumb"
        db_table_comment: str = "이더리움 마지막 거래가"   


class RippleEndPriceData(CoinTradingData):
    class Meta:
        db_table: str = "XRP_coin_end_price_and_upbithumb"
        db_table_comment: str = "리플 마지막 거래가"   



class AverageCoinPresentPrice(Timestamp):
    name = models.CharField(_("코인_이름"), max_length=10, null=False, blank=False)
    timestamp = models.FloatField(_("현재_시각"))
    opening_price = models.FloatField(_("시작가"))
    max_price = models.FloatField(_("최고가"))
    min_price = models.FloatField(_("최저가"))
    prev_closing_price = models.FloatField(_("전일_종가"))
    acc_trade_volume_24h = models.FloatField(_("24시간_볼륨"))
    
    class Meta:
        db_table: str = "Coin_average_price"
        db_table_comment: str = "코인 현재 평균 거래가"
        app_label: str = "coin"
        indexes = [models.Index(fields=["name"], name="name_index")]