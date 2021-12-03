import json
from channels.consumer import AsyncConsumer
from channels.db import database_sync_to_async
from .utils import get_batch, get_batch_class, get_user_by_token


class BatchConsumer(AsyncConsumer):

    async def websocket_connect(self, event):
        print("CONNECTED TO WEBSOCKET ", event)
        await self.send({
            "type": "websocket.accept"
        })

        query_string = self.scope["query_string"].decode("utf-8")
        dictio = {}
        split1 = query_string.split("&")
        for i in split1:
            split2 = i.split("=")
            dictio[split2[0]] = split2[-1]

        print(dictio)
        
        return 
        token = query_string.get("token")
        if token is None:
            await self.send({
                "type": "websocket.close"
            })
            return False
        
        # batch_id = query_string.get("batch_id")        
        # batch = await get_batch(batch_id)

        user = await get_user_by_token(token)
        if user is None:
            await self.send({
                "type": "websocket.close"
            })
            return False

        self.scope["user"] = user



    async def websocket_receive(self, event):
        print("RECEIVED FROM WEBSOCKET ", event)

    async def websocket_disconnect(self, event):
        print("DIS-CONNECTED TO WEBSOCKET ", event)
