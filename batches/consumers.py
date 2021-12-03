import json
from channels.consumer import AsyncConsumer
from channels.db import database_sync_to_async


class BatchConsumer(AsyncConsumer):

    async def websocket_connect(self, event):
        print("CONNECTED TO WEBSOCKET ", event)

    async def websocket_receive(self, event):
        print("RECEIVED FROM WEBSOCKET ", event)

    async def websocket_disconnect(self, event):
        print("DIS-CONNECTED TO WEBSOCKET ", event)
