from django.contrib.auth.models import User
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


class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    content = models.CharField(max_length=200)
    reply = models.ForeignKey('self', on_delete=models.DO_NOTHING, null=True, blank=True, editable=False)
    create_timestamp = models.DateTimeField(auto_now_add=True)



