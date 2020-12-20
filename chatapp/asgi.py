"""
ASGI config for chatapp project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/asgi/
"""

import os
import django
from channels.routing import get_default_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chatapp.settings')
os.environ.setdefault("DJANGO_CONFIGURATION", "Dev")

from configurations import importer

importer.install()

django.setup()
application = get_default_application()
# class CustomSocketioProtocolTypeRouter(ProtocolTypeRouter):
#     """
#     Overrided base class's __call__ method to support python socketio 4.2.0 and daphne 2.3.0
#     """
#     def __call__(self, scope, *args):
#         if scope["type"] in self.application_mapping:
#             handlerobj = self.application_mapping[scope["type"]](scope)
#             if args:
#                 return handlerobj(*args)
#             return handlerobj
#         raise ValueError(
#             "No application configured for scope type %r" % scope["type"]
#         )
#
#
# def chat(args):
#     pass
#
#
# application = CustomSocketioProtocolTypeRouter({
#     # (http->django views is added by default)
#     "websocket": AuthMiddlewareStack(
#         URLRouter(
#             chat.routing.websocket_urlpatterns
#         )
#     ),
# })
