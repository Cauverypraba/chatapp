from channels.routing import ProtocolTypeRouter 


# This function will display all messages received in the console
def message_handler(message):
    print(message['text'])


channel_routing = ProtocolTypeRouter({
    "websocket": "routing"
})
  # we register our message handler
