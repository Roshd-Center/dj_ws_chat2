from rest_framework import mixins, permissions

# Create your views here.
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from chat.consumers import ChatConsumer
from chat.models import Message, Topic
from chat.serializers import MessageSerializer, TopicSerializer


class TopicRetrieveMixin:
    topic_lookup_url_kwarg = 'pk'
    topic_lookup_field = 'pk'

    def get_topic(self):
        return Topic.objects.get(**{self.topic_lookup_field: self.kwargs[self.topic_lookup_url_kwarg]})



class TopicApi(mixins.ListModelMixin, mixins.CreateModelMixin, mixins.RetrieveModelMixin, GenericAPIView):
    serializer_class = TopicSerializer
    permission_classes = [
        permissions.IsAuthenticated
    ]
    lookup_url_kwarg = 'pk'

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


class MessageListApi(TopicRetrieveMixin, mixins.ListModelMixin, mixins.CreateModelMixin, GenericAPIView):
    serializer_class = MessageSerializer
    permission_classes = [
        permissions.IsAuthenticated
    ]

    def get_queryset(self):
        return Message.objects.filter(topic=self.get_topic())

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        msg = serializer.save(topic=self.get_topic(), sender=self.request.user)
        self.notify(msg)

    def notify(self, message: Message):
        ChatConsumer.notify_users(message.topic.participants.all(), MessageSerializer(message).data)


class MessageApi(TopicRetrieveMixin, mixins.RetrieveModelMixin, GenericAPIView):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    topic_lookup_url_kwarg = 'topic_pk'
    lookup_url_kwarg = 'message_pk'

    def get_queryset(self):
        return Message.objects.filter(topic=self.get_topic())

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        msg = self.get_object()
        msg.seen(request.user)
        return Response(MessageSerializer(msg).data)
