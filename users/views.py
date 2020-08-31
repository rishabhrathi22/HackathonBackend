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
	# serializer = AdminSignupSerializer(data=request.POST)
	# print(serializer)
	# if serializer.is_valid():
	email = request.data['email']
	pwd = request.data['password']
	user = CustomUser.objects.create_superuser(email, pwd)
	print(user)
	user.save()
	return Response("Saved successfully!!", status=status.HTTP_201_CREATED)

	return Response("Invalid request")