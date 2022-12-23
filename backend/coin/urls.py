from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import apis

            
urlpatterns = [
    path('api-v1/coinsync', apis.MarketListTotal.as_view()),
    path('api-v1/coinsync/symbol', apis.MarketListView.as_view()),

    path('api-v1/coinsync/upbit', apis.UpbitListInitialization.as_view()),
    path('api-v1/coinsync/bitthum', apis.BithumListInitialization.as_view()),
]
