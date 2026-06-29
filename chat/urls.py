from django.urls import path
from .views import ChatRoomMessagesView

urlpatterns = [
    path("chatroom/<int:room_id>/messages/", ChatRoomMessagesView.as_view(), name="chatroom-messages")
]