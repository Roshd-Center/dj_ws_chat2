from django.urls import path

from .views import *

urlpatterns = [
    path('topic/', TopicApi.as_view()),
    path('topic/<int:pk>', TopicApi.as_view()),
    path('topic/<int:pk>/message', MessageListApi.as_view()),
    path('topic/<int:topic_pk>/message/<int:message_pk>', MessageApi.as_view()),
]
