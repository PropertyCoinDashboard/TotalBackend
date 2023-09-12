from django.urls import path
from . import apis


urlpatterns = [
    path("api-v1/coin/total-list", apis.MarketListView.as_view()),
    path("api-v1/coinsync", apis.MarketCoinListCreateInitialization.as_view()),
]
