import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from channels.layers import get_channel_layer
from django.contrib.auth.models import User


class ChatConsumer(WebsocketConsumer):

    # Function to connect to the websocket
    def connect(self):
        print(self.scope["user"])
        # Checking if the User is logged in
        if self.scope["user"].is_anonymous:
            # Reject the connection
            # self.close()
            self.scope['user'] = User.objects.first()
        # else:
        # print(self.scope["user"])   # Can access logged in user details by using self.scope.user, Can only be used if AuthMiddlewareStack is used in the routing.py
        self.group_name = str(self.scope[
                                  "user"].pk)  # Setting the group name as the pk of the user primary key as it is unique to each user. The group name is used to communicate with the user.
        async_to_sync(self.channel_layer.group_add)(self.group_name, self.channel_name)
        self.accept()

    # Function to disconnet the Socket
    def disconnect(self, close_code):
        self.close()
        # pass

    # Custom Notify Function which can be called from Views or api to send message to the frontend
    def notify(self, event):
        self.send(text_data=json.dumps(event["data"]))

    @classmethod
    def notify_user(cls, user, data):
        channel_layer = get_channel_layer(cls.channel_layer_alias)
        from datetime import datetime
        # Trigger message sent to group
        async_to_sync(channel_layer.group_send)(
            str(user.pk),  # Group Name, Should always be string
            {
                "type": "notify",  # Custom Function written in the consumers.py
                "data": data,
            },
        )

    @classmethod
    def notify_users(cls, users, data):
        for user in users:
            cls.notify_user(user, data)