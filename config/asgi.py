

# import os
# from django.core.asgi import get_asgi_application
# from channels.routing import ProtocolTypeRouter, URLRouter
# from channels.auth import AuthMiddlewareStack
# import tasks.routing
# import notifications.routing

# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")


# application = ProtocolTypeRouter({
#     "http": get_asgi_application(),
#     "websocket": AuthMiddlewareStack(
#         URLRouter(
#             tasks.routing.websocket_urlpatterns +
#             notifications.routing.websocket_urlpatterns  
#         )
#     ),
# })



# config/asgi.py

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

# Load Django apps first
django_asgi_app = get_asgi_application()

from channels.routing import ProtocolTypeRouter, URLRouter
from config.middleware import TokenAuthMiddleware
import notifications.routing
import chat.routing

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": TokenAuthMiddleware(
        URLRouter(
            notifications.routing.websocket_urlpatterns 
            + chat.routing.websocket_urlpatterns
        )
    ),
})