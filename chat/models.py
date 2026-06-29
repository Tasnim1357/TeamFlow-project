from django.db import models
from teams.models import Team
from django.contrib.auth import get_user_model
# Create your models here.

User = get_user_model()
class ChatRoom(models.Model):
    name = models.CharField(max_length=255, unique=True)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='chat_rooms')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
class ChatMessage(models.Model):
    room= models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.sender.user_name} in {self.room.name}"
 