# import asyncio
# import json
# from django.contrib.auth import get_user_model
# from channels.consumer import AsyncConsumer
# from channels.db import database_sync_to_async
#
# #from .models import Thread, ChatMessage
#
# class ChatConsumer(AsyncConsumer):
#     async def websocket_connect(self, event):
#         print("connected", event)
#
#     async def websocket_receive(self, event):
#         #when a message is received from the websocket
#         print("received", event)
#
#     async def websocket_disconnect(self, event):
#         #when the socket connects
#         print("disconnected", event)
from channels.auth import channel_session_user_from_http


# This decorator copies the user from the HTTP session (only available in
# websocket.connect or http.request messages) to the channel session (available
# in all consumers with the same reply_channel, so all three here)
@channel_session_user_from_http
def ws_connect(message):
    message.reply_channel.send({"accept": True})
    message.channel_session['rooms'] = []