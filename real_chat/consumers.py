import json
# from channels.generic.websocket import WebsocketConsumer

# class ChatConsumer(WebsocketConsumer):
#     def __init__(self):
#         print("Chatting...")

#     def connect(self):
#         print('Connecting...')
#         self.accept()

#     def disconnect(self, close_code):
#         pass

#     def receive(self, text_data):
#         text_data_json = json.loads(text_data)
#         message = text_data_json['message']

#         self.send(text_data=json.dumps({
#             'message': message
#         }))

import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer


class ChatConsumer(WebsocketConsumer):
    async def connect(self):
        self.person_name=self.scope['url_route']['kwargs']['person_name']
        self.room_name=self.scope['url_route']['kwargs']['room_name']
        self.room_group_name='chat_%s' % self.room_name

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type":"chat_message",
                "message":self.person_name+" Joined Chat"
            }
        )
        self.accept()

    async def disconnect(self, code):
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type":"chat_message",
                "message":self.person_name+" Left Chat"
            }
        )
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
    async def receive(self, text_data=None, bytes_data=None):
        text_data_json=json.loads(text_data)
        message=text_data_json['message']

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type':'chat_message',
                'message':self.person_name+" : "+message
            }
        )

    async def chat_message(self,event):
        message=event['message']

        await self.send(text_data=json.dumps({
            'message':message
        }))

