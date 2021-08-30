from django.urls import path

from chat.views import MessageApi

urlpatterns = [
    path('message/', MessageApi.as_view()),
]
