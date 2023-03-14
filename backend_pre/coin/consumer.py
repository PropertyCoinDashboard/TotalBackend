from channels.generic.websocket import AsyncWebsocketConsumer
import json

class BitcoinConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add("stream_group", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("stream_group", self.channel_name)

    async def stream_data(self, event):
        data = event["data"]
        print(data)
        await self.send(text_data=json.dumps(data))
