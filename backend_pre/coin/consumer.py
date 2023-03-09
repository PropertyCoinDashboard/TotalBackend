from channels.generic.websocket import AsyncJsonWebsocketConsumer


class StreamConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        await self.accept()
        await self.channel_layer.group_add("stream_group", self.channel_name)

    async def disconnect(self, code):
        await self.channel_layer.group_discard("stream_group", self.channel_name, self.channel_layer)

    async def receive(self, text_data=None, bytes_data=None, **kwargs):
        await self.send(text_data=text_data)