from django.shortcuts import redirect
from users.models import CustomUser
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.decorators import api_view
from .serializers import AdminSignupSerializer


@api_view(['POST'])
def mainview(request):
	email = request.data['email']
	pwd = request.data['password']
	user = CustomUser.objects.create_superuser(email, pwd)
	user.save()
	return Response("Saved successfully!!", status=status.HTTP_201_CREATED)