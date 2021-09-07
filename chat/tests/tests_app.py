from channels.layers import get_channel_layer, InMemoryChannelLayer
from channels.testing import ChannelsLiveServerTestCase
from django.contrib.auth.models import User
from django.test import TestCase

# Create your tests here.
from chat.consumers import ChatConsumer
from chat.models import Topic, Message


class ChannelTest(ChannelsLiveServerTestCase):


    def test_notify(self):
        pass