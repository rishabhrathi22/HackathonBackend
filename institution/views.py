from django.contrib.auth.models import User

from django.contrib.auth import authenticate
from users.models import CustomUser

from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import status
from rest_framework.decorators import action

from .serializers import InstituteSerializer, InstituteSignupSerializer, InstituteLoginSerializer

from .models import Institute


def verifyUser(uname, pwd):
	user = authenticate(email = uname, password = pwd)
	if user is not None:
		return True
	return False

class InstituteViewSet(viewsets.GenericViewSet):    
	default_serializer_class = InstituteSignupSerializer

	serializer_classes = {
		'login': InstituteLoginSerializer,
	}

	model = Institute
	queryset = Institute.objects.all().filter(status = 1)
 
	def get_serializer_class(self):
		return self.serializer_classes.get(self.action, self.default_serializer_class)

	def list(self, request):
		serializer = InstituteSignupSerializer(self.queryset, many=True)	
		return Response(serializer.data, status=status.HTTP_200_OK)

	def create(self, request):
		inst = InstituteSerializer(data = request.data)
		email = request.data['email']
		pwd = request.data['password']
		user = CustomUser.objects.create_user(email, pwd)

		if inst.is_valid():
			try:
				inst.save()
				user.save()
				return Response("Saved event successfully.", status=status.HTTP_201_CREATED)
			except:
				return Response(user.errors, status=status.HTTP_401_UNAUTHORIZED)
		
		return Response(inst.errors, status=status.HTTP_401_UNAUTHORIZED)

	def login(self, request):
		inst = InstituteLoginSerializer(data = request.data)

		if verifyUser(request.data['email'], request.data['password']):
			return Response("Successfully logged in.", status=status.HTTP_201_CREATED)

		return Response("Invalid email or password.", status=status.HTTP_401_UNAUTHORIZED)	