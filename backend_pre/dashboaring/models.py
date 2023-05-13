from django.db import models
from django.urls import reverse
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
        max_length=16, unique=True, primary_key=True)
    korea_name = models.CharField(
        max_length=15, unique=True, blank=False, null=False)
    bithum_existence = models.BooleanField()
    upbit_existence = models.BooleanField()
    korbit_existence = models.BooleanField()

    class Meta:
        db_table: str = "coin_symbol"


"""
## ---------------------------------------------------- ##
"""

# class StockInformationally(Timestamp):
#     k_name = models.CharField(max_length=50, default="")

#     class Meta:
#         db_table: str = "stock"


# class RealstateInformationlly(Timestamp):
#     name = models.CharField(max_length=50, blank=False, null=False)
#     location = models.CharField(verbose_name=_("지역"), max_length=50, blank=False, null=False)
#     price = models.BigIntegerField(verbose_name=_("가격"), null=False, blank=False)

#     class Meta:
#         db_table: str = "real"
