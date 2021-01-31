"""
ASGI config for chatapp project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/asgi/
"""

# import os
# import django
# #from channels.routing import get_default_application

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chatapp.settings')
# #os.environ.setdefault("DJANGO_CONFIGURATION", "Dev")

# from configurations import importer

# importer.install()

# django.setup()
#application = get_default_application()

import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from real_chat import routing

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "chatapp.settings")

websocket_urlpatterns = ProtocolTypeRouter({
  "http": get_asgi_application(),
  #"websocket" : websocket_urlpatterns
  "websocket": AuthMiddlewareStack(
        URLRouter(
            real_chat.routing.websocket_urlpatterns
        )
    ),
})


# import os
# import django
# from channels.routing import get_default_application

# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "chatapp.settings")
# django.setup()
# application = get_default_application()
