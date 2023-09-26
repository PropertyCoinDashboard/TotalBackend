from django.urls import path
from . import apis


urlpatterns = [
    path("api-v1/coin/total-list/", apis.CoinMarketListView.as_view()),
    path("api-v1/coinsync/", apis.MarketCoinListCreateInitialization.as_view()),
    path("api-v1/coinsync/present/<str:coin_symbol>/", apis.CoinPriceView.as_view(), name='coin_price'),
    path("api-v1/coinsync/coinprice/btc/", apis.BtcCoinDataListCreateView.as_view()),
    path("api-v1/coinsync/coinprice/eth/", apis.EthCoinDataListCreateView.as_view()),
    path("api-v1/coinsync/coinprice/xrp/", apis.XrpCoinDataListCreateView.as_view())
]
