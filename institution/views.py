from django.contrib.auth.models import User

from django.contrib.auth import authenticate, login, logout

from users.models import CustomUser

from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import status
from rest_framework.decorators import action

from .serializers import InstituteSerializer, InstituteSignupSerializer, InstituteLoginSerializer, InstituteChangePasswordSerializer

from .models import Institute
from teacher.models import Teacher


def verifyUser(uname, pwd):
	user = authenticate(email = uname, password = pwd)
	if user is not None:
		return user
	return False

class InstituteViewSet(viewsets.GenericViewSet):    
	default_serializer_class = InstituteSignupSerializer
	model = Institute

	serializer_classes = {
		'login': InstituteLoginSerializer,
		'change_password': InstituteChangePasswordSerializer,
	}


	def get_queryset(self):
		queryset = Institute.objects.all().filter(status = 1)
		email = self.request.query_params.get('filterByMail', None)
		
		if email is not None:
			queryset = queryset.filter(email = email)
			if len(queryset)==0:
				return None

		return queryset

	
	def get_serializer_class(self):
		return self.serializer_classes.get(self.action, self.default_serializer_class)

	
	def list(self, request):
		queryset = self.get_queryset()
		if queryset is None:
			return Response("Does not Exist.", status = status.HTTP_404_NOT_FOUND)
		serializer = InstituteSerializer(queryset, many=True)
		return Response(serializer.data, status=status.HTTP_200_OK)


	# def retrieve(self, request):
	# 	try:
	# 		inst = self.get_queryset()
	# 		serializer = InstituteSerializer(inst)
	# 		return Response(serializer.data, status=status.HTTP_200_OK)
	# 	except:
	# 		return Response("Invalid university name.", status=status.HTTP_404_NOT_FOUND)


	def create(self, request):
		inst = InstituteSerializer(data = request.data)
		email = request.data['email']
		pwd = request.data['password']
		user = CustomUser.objects.create_user(email, pwd)

		if inst.is_valid():
			try:
				inst.save()
				user.save()
				return Response("Saved Institute successfully.", status=status.HTTP_201_CREATED)
			except Exception as e:
				print(e)
				return Response("Email already present.", status=status.HTTP_401_UNAUTHORIZED)
		
		return Response(inst.errors, status=status.HTTP_401_UNAUTHORIZED)

	
	def login(self, request):
		inst = InstituteLoginSerializer(data = request.data)

		if Institute.objects.filter(email = request.data['email']).exists():
			user = verifyUser(request.data['email'], request.data['password'])
			if user is not False:
				login(request, user)
				return Response("Successfully logged in.", status=status.HTTP_200_OK)
			else:
				return Response("Invalid email or password.", status=status.HTTP_401_UNAUTHORIZED)	

		return Response("Invalid institution mail.", status=status.HTTP_401_UNAUTHORIZED)


	def change_password(self, request, name):
		email = request.data['email']
		pwd = request.data['password']
		pwd2 = request.data['newpass']

		if verifyUser(email, pwd):
			try:
				user = CustomUser.objects.get(email = email)
				user.set_password(pwd2)
				user.save()
				return Response("Password updated successfully.", status=status.HTTP_201_CREATED)
			except Exception as e:
				print(e)
				return Response("Invalid response.", status=status.HTTP_401_UNAUTHORIZED)

		return Response("Invalid Credentials", status=status.HTTP_401_UNAUTHORIZED)


	def logout(self, request):
		logout(request)
		return Response("Successfully logged out.", status = status.HTTP_200_OK)


	def approve_teacher(self, request):
		if request.user.is_authenticated:
			teacher = self.request.query_params.get('teacher', None)
			try:
				s = Teacher.objects.get(email = teacher)
				s.status = 1
				s.save()
				return Response("Teacher approved successfully.", status=status.HTTP_200_OK)
			except:
				return Response("Invalid teacher mail.", status=status.HTTP_404_NOT_FOUND)
		else:
			return Response("Not logged in.", status = status.HTTP_401_UNAUTHORIZED)		