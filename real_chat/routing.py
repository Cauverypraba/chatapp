from django.urls import re_path
#from channels.routing import route
from real_chat import consumers

websocket_urlpatterns = [
    re_path(r'^ws/chat/(?P<room_name>[^/]+)/$', consumers.ChatConsumer),
    # route('websocket.connect', consumers.ChatConsumer.connect, path = r'ws/chatapp/(?P<room_name>\w+)/$')
    # route('websocket.disconnect', consumers.ChatConsumer.disconnect, path = r'ws/chatapp/(?P<room_name>\w+)/$')
    # route('websocket.receive', consumers.ChatConsumer.receive, path = r'ws/chatapp/(?P<room_name>\w+)/$')
]
  # we register our message handler

# from .wsgi import *  # add this line to top of your code
# from channels.auth import AuthMiddlewareStack
# from channels.routing import ProtocolTypeRouter, URLRouter
# import chatapp.routing as routing

# application = ProtocolTypeRouter({
#     # (http->django views is added by default)
#     'websocket': AuthMiddlewareStack(
#         URLRouter(
#             routing.websocket_urlpatterns
#         )
#     ),
# })