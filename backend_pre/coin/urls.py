from django.urls import path, include, re_path
from . import apis
from . import consumer


urlpatterns = [
    path('api-v1/coin/list/total', apis.MarketListView.as_view()),
    path('api-v1/coin/ws/stream', consumer.StreamConsumer.as_asgi()),

    path('api-v1/coin/burket', apis.MarketDataCreateBurketInitialization.as_view()),
    path('api-v1/coinsync', apis.MarketListTotalInitialization.as_view()),
]
