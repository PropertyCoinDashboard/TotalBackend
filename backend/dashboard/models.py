from django.db import models
from django.utils.translation import gettext_lazy as _


class NameSchema(models.Model):
    k_name = models.CharField(max_length=50, default="")
    e_name = models.CharField(max_length=50)
    
    class Meta:
        abstract: bool = True


# 공통 
class Timestamp(models.Model):
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)
        
    class Meta:
        abstract: bool = True


class CoinSymbolCoinList(Timestamp):
    coin_symbol = models.CharField(max_length=50)
    
    class Meta:
        db_table: str = "coin_symbol"


class UpbitCoinList(Timestamp, NameSchema):
    market = models.CharField(max_length=15)
    market_warning = models.CharField(max_length=15)
    
    class Meta:
        db_table: str = "upbit_coin_list"
        
        
class BitThumCoinList(Timestamp):
    coin_symbol = models.CharField(max_length=50)
    
    class Meta:
        db_table: str = "bitthum_coin_list"


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
        


        
