from django.shortcuts import render
from rest_framework.generics import ListAPIView
from .models import ChatMessage, ChatRoom
from .serializers import ChatMessageSerializer

# Create your views here.


class ChatRoomMessagesView(ListAPIView):
    serializer_class = ChatMessageSerializer

    def get_queryset(self):
        room_id = self.kwargs['room_id']
        return ChatMessage.objects.filter(room_id=room_id).order_by('created_at')