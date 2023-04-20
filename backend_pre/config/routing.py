from django.urls import path
from . import consumer

websocket_urlpatterns = [
    path("ws/bitcoin-streaming/", consumer.MyConsumer.as_asgi())
]