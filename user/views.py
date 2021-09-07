from django.shortcuts import render
from rest_framework.generics import RetrieveAPIView
from .serializers import *

# Create your views here.


class UserViewApi(RetrieveAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()