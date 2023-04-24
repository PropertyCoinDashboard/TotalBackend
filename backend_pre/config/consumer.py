import json
from channels.generic.websocket import AsyncWebsocketConsumer

class MyConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add(
            'my-group-name',  # group name of the WebSocket consumers
            self.channel_name
        )
        await self.accept()
        print(self.channel_layer.group_add)

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            'my-group-name',  # group name of the WebSocket consumers
            self.channel_name
        )

    async def send_data_to_consumers(self, event):
        data = event['text']
        print(data)
        await self.send(json.dumps(data))
