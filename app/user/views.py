from django.shortcuts import render

from rest_framework import generics
from user.serializers import UserSerializer

class CreateUserView(generics.CreateAPIView):
    """ View to handle creating a user """
    
    serializer_class = UserSerializer
