from django.urls import path, include
from . import apis

            
urlpatterns = [
    path('api-v1/coin/list/total', apis.MarketListView.as_view()),
    path('api-v1/coin/list/<str:coin_symbol>', apis.MarketRetriveView.as_view()),

    path('api-v1/coin/burket', apis.MarketDataCreateBurketInitialization.as_view()),

    path('api-v1/coinsync', apis.MarketListTotal.as_view()),
    path('api-v1/coinsync/upbit', apis.UpbitListInitialization.as_view()),
    path('api-v1/coinsync/bitthum', apis.BithumListInitialization.as_view()),
]
