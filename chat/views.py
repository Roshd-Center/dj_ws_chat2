from rest_framework import mixins, permissions

# Create your views here.
from rest_framework.generics import GenericAPIView

from chat.models import Message
from chat.serializers import MessageSerializer


class MessageApi(mixins.ListModelMixin, mixins.CreateModelMixin, GenericAPIView):
    serializer_class = MessageSerializer
    permission_classes = [
        permissions.IsAuthenticated
    ]

    def get_queryset(self):
        return Message.objects.filter(sender=self.request.user)

    def get(self, request, *args, **kwargs):
        self.list(request,*args, **kwargs)