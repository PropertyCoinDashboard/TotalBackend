from django.urls import path
from coin import consumer


websocket_urlpatterns = [
    path("ws/bitcoin-streaming/", consumer.BitcoinConsumer.as_asgi())
]