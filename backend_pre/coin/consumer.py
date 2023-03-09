from channels.generic.websocket import AsyncWebsocketConsumer
import json


class BitcoinAverageSocketing(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add(
            'stream_group',
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            'stream_group',
            self.channel_name
        )

    async def receive(self, text_data=None, bytes_data=None):
        # 수신된 데이터 처리
        print(text_data)
        data = json.loads(text_data)
        print('수신된 데이터:', data)

        # 처리된 결과를 클라이언트로 전송
        result = {'result': 'success'}
        await self.send(text_data=json.dumps(result))

    async def send_stream_data(self, event):
        print(event)
        data = event['data']
        print(data)
        await self.send(text_data=json.dumps(data))