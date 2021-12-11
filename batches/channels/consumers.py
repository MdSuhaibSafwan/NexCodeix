import json
from channels.consumer import AsyncConsumer
from channels.db import database_sync_to_async
from .utils import get_batch, get_batch_class, get_user_by_token, get_user_by_id, get_class_joined_user_obj


class ClassConsumer(AsyncConsumer):

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

        token = dictio.get("token")
        user = await get_user_by_token(token)
        if user is None:
            await self.send({
                "type": "websocket.close"
            })
            return False

        class_id = dictio.get("class_id")
        class_obj = await get_batch_class(class_id)
        if class_obj is None:
            await self.send({
                "type": "websocket.close"
            })
            return False
        
        self.scope["user"] = user

        room = "class_room_" + str(class_obj.id)
        print(room)
        self.chat_room = room
        await self.channel_layer.group_add(
            self.chat_room,
            self.channel_name,
        )

    async def websocket_receive(self, event):
        print("RECEIVED FROM WEBSOCKET ", event)
        """
        TYPES,
            1. UJS --> User Joined Successfully
        """

        data = json.loads(event.get("text"))
        if not data:
            await self.send({
                "type": "websocket.close"
            })
            return None

        if data["msg_type"] == "UJS":
            obj_id = data['class_joined_user_id']
            cj_user_id = await get_class_joined_user_obj(obj_id)
            user = cj_user_id.user

            await self.channel_layer.group_send(
                self.chat_room,
                {
                    "type": "send.to_student",
                    "text": json.dumps({"msg_type": "UJS", "user": user.email, })
                }
            )

    async def send_to_student(self, event):
        await self.send({
            "type": "websocket.send",
            "text": event["text"],
        })

    async def send_notification(self, event):
        data = event["text"]

        await self.send({
            "type": "websocket.send",
            "text": json.dumps(data)
        })

    async def websocket_disconnect(self, event):
        print("DIS-CONNECTED TO WEBSOCKET ", event)
