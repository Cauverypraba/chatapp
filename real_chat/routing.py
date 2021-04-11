from django.urls import re_path
# from channels.routing import route
from real_chat import consumers

websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<room_name>\w+)/(?P<person_name>\w+)/$',consumers.ChatConsumer.as_asgi())
    # re_path('ws/chat/myroom', consumers.ChatConsumer),
    # route('websocket.connect', consumers.ChatConsumer.connect, path = r'ws/chatapp/(?P<room_name>\w+)/(?P<person_name>\w+)/$'),
    # route('websocket.disconnect', consumers.ChatConsumer.disconnect, path = r'ws/chatapp/(?P<room_name>\w+)/(?P<person_name>\w+)/$'),
    # route('websocket.receive', consumers.ChatConsumer.receive, path = r'ws/chatapp/(?P<room_name>\w+)/(?P<person_name>\w+)/$')
]