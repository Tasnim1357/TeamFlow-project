from channels.generic.websocket import AsyncWebsocketConsumer
import json
from channels.db import database_sync_to_async

class ChatConsumer(AsyncWebsocketConsumer):
    async def  connect(self):
        user = self.scope['user']
        if not user or not user.is_authenticated:
            await self.close(code=4401)
            return

       

        self.room_id = self.scope['url_route']['kwargs']['room_id']
        self.room_group_name = f'chat_{self.room_id}'

        allowed = await self.is_user_allowed_in_room(user.id, self.room_id)

        if not allowed:
            await self.close(code=4403)
            return

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
        message = data['message']
        sender= self.scope["user"]
          # Save message to database
        await self.save_message(sender, self.room_id, message)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender_id': sender.id,
                'sender_name': sender.user_name
            }  
        )
    async def chat_message(self, event):
        message = event['message']
        sender_id = event['sender_id']
        sender_name = event['sender_name']

        await self.send(text_data=json.dumps({
            'message': message,
            'sender_id': sender_id,
            'sender_name': sender_name
        }))  

    @database_sync_to_async
    def is_user_allowed_in_room(self, user_id, room_id):
        from .models import ChatRoom
        from teams.models import TeamMember

        try:
            chat_room = ChatRoom.objects.get(id=room_id)
            team = chat_room.team
            return TeamMember.objects.filter(team=team, user_id=user_id).exists()
        
        except ChatRoom.DoesNotExist:
            return False  

    @database_sync_to_async
    def save_message(self, sender, room_id, message):
        from .models import ChatRoom, ChatMessage
        chat_room = ChatRoom.objects.get(id=room_id) 
        ChatMessage.objects.create(room=chat_room, sender=sender, message=message)    