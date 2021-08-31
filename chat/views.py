from rest_framework import mixins, permissions

# Create your views here.
from rest_framework.generics import GenericAPIView

from chat.consumers import ChatConsumer
from chat.models import Message, Topic
from chat.serializers import MessageSerializer, TopicSerializer


class TopicApi(mixins.ListModelMixin, mixins.CreateModelMixin, mixins.RetrieveModelMixin, GenericAPIView):
    serializer_class = TopicSerializer
    permission_classes = [
        permissions.IsAuthenticated
    ]

    def get_queryset(self):
        return self.request.user.topics.all()

    def get(self, request, *args, **kwargs):
        if self.lookup_url_kwarg in kwargs:
            return self.retrieve(request, *args, **kwargs)
        else:
            return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user).save()


class MessageApi(mixins.ListModelMixin, mixins.CreateModelMixin, GenericAPIView):
    serializer_class = MessageSerializer
    lookup_url_kwarg = 'pk'
    permission_classes = [
        permissions.IsAuthenticated
    ]

    def get_topic(self):
        print({self.lookup_url_kwarg: self.kwargs[self.lookup_url_kwarg]})
        return Topic.objects.get(**{self.lookup_url_kwarg: self.kwargs[self.lookup_url_kwarg]})

    def get_queryset(self):
        return Message.objects.filter(topic=self.get_topic())

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        msg = serializer.save(topic=self.get_topic())
        self.notify(msg)

    def notify(self, message: Message):
        ChatConsumer.notify_users(message.topic.participants.all(), MessageSerializer(message).data)
