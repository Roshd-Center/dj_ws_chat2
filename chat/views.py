from django.contrib.auth.models import User
from django.db.models.fields.related_descriptors import ManyToManyDescriptor
from rest_framework import mixins, permissions

# Create your views here.
from rest_framework.generics import GenericAPIView

from chat.models import Message, Topic
from chat.serializers import MessageSerializer, TopicSerializer


class MessageApi(mixins.ListModelMixin, mixins.CreateModelMixin, GenericAPIView):
    serializer_class = MessageSerializer
    permission_classes = [
        permissions.IsAuthenticated
    ]

    def get_queryset(self):
        return Message.objects.filter(sender=self.request.user)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class TopicApi(mixins.ListModelMixin, mixins.CreateModelMixin, mixins.RetrieveModelMixin, GenericAPIView):
    serializer_class = TopicSerializer
    permission_classes = [
        permissions.IsAuthenticated
    ]

    def get_queryset(self):
        return self.request.user.topics.all()


    def get(self, request, *args, **kwargs):
        if 'pk' in kwargs:
            return self.retrieve(request, *args, **kwargs)
        else:
            return self.list(request, *args, **kwargs)


    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

