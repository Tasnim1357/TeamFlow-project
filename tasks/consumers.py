import json
from channels.generic.websocket import AsyncWebsocketConsumer

class TaskConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.task_id = self.scope["url_route"]["kwargs"]["task_id"]
        self.room_group_name = f"task_{self.task_id}"

        # Join group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data["message"]
        print("Received message:", message)
        # Broadcast to group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "task_message",
                "message": message
            }
        )

    async def task_message(self, event):
        message = event["message"]

        # Send to WebSocket
        await self.send(text_data=json.dumps({
            "message": message
        }))


# import json
# from channels.generic.websocket import AsyncWebsocketConsumer


# class TaskConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         self.task_id = self.scope["url_route"]["kwargs"]["task_id"]
#         self.room_group_name = f"task_{self.task_id}"

#         await self.accept()

#         await self.channel_layer.group_add(
#             self.room_group_name,
#             self.channel_name
#         )

#         print("CONNECTED:", self.channel_name, self.room_group_name, flush=True)

#         await self.send(text_data=json.dumps({
#             "type": "connected",
#             "channel": self.channel_name,
#             "group": self.room_group_name,
#         }))

#     async def disconnect(self, close_code):
#         print("DISCONNECTED:", self.channel_name, self.room_group_name, close_code, flush=True)

#         await self.channel_layer.group_discard(
#             self.room_group_name,
#             self.channel_name
#         )

#     async def receive(self, text_data):
#         print("RECEIVED RAW:", self.channel_name, text_data, flush=True)

#         data = json.loads(text_data)

#         await self.channel_layer.group_send(
#             self.room_group_name,
#             {
#                 "type": "task_message",
#                 "message": data["message"],
#                 "sender": self.channel_name,
#             }
#         )

#         print("GROUP_SEND DONE:", self.room_group_name, flush=True)

#     async def task_message(self, event):
#         print("TASK_MESSAGE CALLED:", self.channel_name, event, flush=True)

#         await self.send(text_data=json.dumps({
#             "type": "task_message",
#             "message": event["message"],
#             "sender": event["sender"],
#             "receiver": self.channel_name,
#         }))



    async def connect(self):
        self.task_id = self.scope["url_route"]["kwargs"]["task_id"]
        self.room_group_name = f"task_{self.task_id}"

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data["message"]

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "task_message",
                "message": message,
            }
        )

    async def task_message(self, event):
        await self.send(text_data=json.dumps({
            "message": event["message"]
        }))