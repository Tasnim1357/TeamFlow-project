# import json
# from channels.generic.websocket import AsyncWebsocketConsumer


# class NotificationsConsumer(AsyncWebsocketConsumer):

#     async def connect(self):
#         user = self.scope.get("user", None)
#         if user and user.is_authenticated:
#             self.user_id = user.id
#             self.room_group_name = f"user_{self.user_id}"
#         else:
#             # Close connection for anonymous users
#             await self.close()
#             return
            
#         await self.channel_layer.group_add(
#         self.room_group_name,
#         self.channel_name
#         )

#         await self.accept()

#     async def disconnect(self, close_code):
#         if hasattr(self, "room_group_name"):
#             await self.channel_layer.group_discard(
#                 self.room_group_name,
#                 self.channel_name
#             )

#     async def user_notification(self,event):
#         await self.send(text_data=json.dumps({
#             "title" : event['title'],
#             "message": event['message']

#         }))        



# notifications/consumers.py

# consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer


class NotificationsConsumer(AsyncWebsocketConsumer):
    # async def connect(self):
    #     self.room_group_name = "anonymous"

    #     await self.channel_layer.group_add(
    #         self.room_group_name,
    #         self.channel_name
    #     )
    #     await self.accept()


    async def connect(self):
        user = self.scope.get("user")
        if not user or not user.is_authenticated:
            await self.close(code=4401)
            return

        self.user_id = user.id
        self.room_group_name = f"user_{self.user_id}"
        print("JOINING GROUP:", self.room_group_name)
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

    async def user_notification(self, event):
        await self.send(text_data=json.dumps({
            "title": event["title"],
            "message": event["message"]
        }))