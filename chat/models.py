from django.contrib.auth.models import User, PermissionsMixin
from django.db import models


# Create your models here.
class Topic(models.Model):
    owner = models.ForeignKey(User, on_delete=models.DO_NOTHING, editable=False, blank=False, null=False,
                              related_name='own_topics')
    title = models.CharField(max_length=40)
    description = models.CharField(max_length=100, blank=True)
    participants = models.ManyToManyField(User, related_name='topics')
    create_timestamp = models.DateTimeField(auto_now_add=True)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        super().save(force_insert, force_update, using, update_fields)
        if self.owner not in self.participants.all():
            self.participants.add(self.owner)


class Message(models.Model):

    class ForeignTopicReply(Exception):

        def __init__(self, from_topic: Topic = None, to_topic: Topic = None,*args: object) -> None:
            super().__init__("Invalid foreign reply" +
                             (f" from '{from_topic}'" if from_topic else "") +
                             (f" to '{to_topic}'" if to_topic else ""))

    sender = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    content = models.CharField(max_length=200)
    topic = models.ForeignKey(Topic, on_delete=models.DO_NOTHING, related_name='messages')
    reply = models.ForeignKey('self', on_delete=models.DO_NOTHING, null=True, blank=True, editable=False, default=None,
                              related_name='replies')
    create_timestamp = models.DateTimeField(auto_now_add=True)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if self.reply and self.reply.topic != self.topic:
            raise self.ForeignTopicReply(self.topic, self.reply.topic)
        super().save(force_insert, force_update, using, update_fields)





