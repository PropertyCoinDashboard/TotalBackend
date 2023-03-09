from django.urls import path
from . import apis


urlpatterns = [
    path('api-v1/coin/list/total', apis.MarketListView.as_view()),
    path('api-v1/coin/burket', apis.MarketDataCreateBurketInitialization.as_view()),
    path('api-v1/coinsync', apis.MarketListTotalInitialization.as_view()),
]
