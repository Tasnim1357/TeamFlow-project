# import os
# from django.core.asgi import get_asgi_application
# from channels.routing import ProtocolTypeRouter, URLRouter
# from channels.auth import AuthMiddlewareStack
# import tasks.routing  # Import your app routing here

# # Set the Django settings module
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

# application = ProtocolTypeRouter({
#     # Handle traditional HTTP requests
#     "http": get_asgi_application(),

#     # Handle WebSocket connections
#     "websocket": AuthMiddlewareStack(
#         URLRouter(
#             tasks.routing.websocket_urlpatterns
#         )
#     ),
# })

import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import tasks.routing

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            tasks.routing.websocket_urlpatterns
        )
    ),
})