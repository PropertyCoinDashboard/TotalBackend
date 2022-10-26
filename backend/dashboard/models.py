from django.db import models
from django.utils.translation import gettext_lazy as _


# 공통 
class SCCommonField(models.Model):
    name = models.CharField(max_length=50, blank=False, null=False)
    price = models.BigIntegerField(verbose_name=_("가격"), null=False, blank=False)
    start_price = models.BigIntegerField(verbose_name=_("시작가"), null=False, blank=False)
    end_price = models.BigIntegerField(verbose_name=_("종가"), null=False, blank=False)
    
    class Meta:
        abstract: bool = True


# 타임 스탬프
class CommonField(models.Model):
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        abstract: bool = True        


# each other
class StockInformationally(CommonField, SCCommonField):
    class Meta:
        db_table: str = "stock"
        # app_label = "default"
        


class CoinInforamtionally(CommonField, SCCommonField):
    class Meta:
        db_table: str = "coin"
        # app_label = "default"
        


class RealstateInformationlly(CommonField):
    name = models.CharField(max_length=50, blank=False, null=False)
    location = models.CharField(verbose_name=_("지역"), max_length=50, blank=False, null=False)
    price = models.BigIntegerField(verbose_name=_("가격"), null=False, blank=False)
    
    class Meta:
        db_table: str = "real"
        # app_label = "default"
        


class DataInjection(CommonField):
    class Meta:
        pass
        # app_label = "default"
        
