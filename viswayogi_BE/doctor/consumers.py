import json
from channels.generic.websocket import AsyncWebsocketConsumer

class QueueConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add("queue_updates", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("queue_updates", self.channel_name)

    async def send_queue_update(self, event):
        queue_data = event["queue_data"]
        await self.send(text_data=json.dumps({"queue_data": queue_data}))
