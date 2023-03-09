from django.urls import path
from coin.consumer import BitcoinAverageSocketing


websocket_urlpatterns = [
    path("ws/bitcoin-streaming/", BitcoinAverageSocketing.as_asgi())
]