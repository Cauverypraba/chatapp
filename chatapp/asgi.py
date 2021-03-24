import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
import real_chat.routing

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "chatapp.settings")

application = ProtocolTypeRouter({
  "http": get_asgi_application(),
  "websocket": AuthMiddlewareStack(
        URLRouter(
            real_chat.routing.websocket_urlpatterns
        )
    ),
})