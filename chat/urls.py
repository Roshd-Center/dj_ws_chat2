from django.urls import path

from chat.views import MessageApi, TopicApi

urlpatterns = [
    path('message/', MessageApi.as_view()),
    path('topic/', TopicApi.as_view()),
    path('topic/<int:pk>', TopicApi.as_view()),
]
