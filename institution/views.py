from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import status

from .serializers import InstituteSerializer, InstituteSignupSerializer, InstituteLoginSerializer, InstituteChangePasswordSerializer, EmailSerializer
from users.serializers import UserSerializer
from teacher.serializers import TeacherViewSerializer

from .models import Institute
from users.models import CustomUser
from teacher.models import Teacher


def verifyUser(uname, pwd):
	user = authenticate(email = uname, password = pwd)
	if user is not None:
		return user
	return False


class InstituteViewSet(viewsets.GenericViewSet):    
	default_serializer_class = InstituteSignupSerializer
	model = Institute
	queryset = Institute.objects.all()

	serializer_classes = {
		'retrieve': EmailSerializer,
		'getAllTeachers': EmailSerializer,
		'approveTeacher': EmailSerializer,
		'login': InstituteLoginSerializer,
		'logout': EmailSerializer,
		'change_password': InstituteChangePasswordSerializer,
	}

	def get_serializer_class(self):
		return self.serializer_classes.get(self.action, self.default_serializer_class)

	def getKey(self, email):
		user = CustomUser.objects.get(email__iexact=email)
		return user.key

	def retrieve(self, request):	
		email = request.data['email']
		key = request.data['key']
		
		if self.getKey(email)!=key:
			return Response("Not logged in.", status = status.HTTP_401_UNAUTHORIZED)

		queryset = Institute.objects.all().filter(email__iexact = email)
		if queryset is not None:
			serializer = InstituteSerializer(queryset, many=True)
			return Response(serializer.data, status=status.HTTP_200_OK)
		else:
			return Response("Does not Exist.", status = status.HTTP_404_NOT_FOUND)

	def getAllTeachers(self, request):
		email = request.data['email']
		key = request.data['key']
		
		if self.getKey(email)!=key:
			return Response("Not logged in.", status = status.HTTP_401_UNAUTHORIZED)

		if email is not None:
			queryset = Teacher.objects.all().filter(institution__email__iexact = email)
			serializer = TeacherViewSerializer(queryset, many=True)
			return Response(serializer.data, status=status.HTTP_200_OK)
		else:
			return Response("Does not Exist.", status = status.HTTP_404_NOT_FOUND)			

	def create(self, request):
		inst = InstituteSerializer(data = request.data)
		email = request.data['email']
		pwd = request.data['password']
		user = CustomUser.objects.create_user(email, pwd)

		if inst.is_valid():
			try:
				inst.save()
				user.save()
				return Response("Institute saved successfully.", status=status.HTTP_201_CREATED)
			except Exception as e:
				print(e)
				return Response(user.errors, status=status.HTTP_401_UNAUTHORIZED)
		
		return Response(inst.errors, status=status.HTTP_401_UNAUTHORIZED)

	
	def login(self, request):
		inst = InstituteLoginSerializer(data = request.data)

		if Institute.objects.filter(email__iexact = request.data['email']).exists():
			user = verifyUser(request.data['email'].lower(), request.data['password'])
			if user is not False:
				login(request, user)
				return Response(UserSerializer(user).data, status=status.HTTP_200_OK)
			else:
				return Response("Error.", status=status.HTTP_401_UNAUTHORIZED)	

		return Response("Invalid institution mail.", status=status.HTTP_401_UNAUTHORIZED)


	def change_password(self, request, name):
		email = request.data['email']
		key = request.data['key']
		
		if self.getKey(email)!=key:
			return Response("Not logged in.", status = status.HTTP_401_UNAUTHORIZED)

		pwd = request.data['password']
		pwd2 = request.data['newpass']

		if verifyUser(email, pwd):
			try:
				user = CustomUser.objects.get(email__iexact = email)
				user.set_password(pwd2)
				user.save()
				return Response("Password updated successfully.", status=status.HTTP_201_CREATED)
			except Exception as e:
				print(e)
				return Response("Invalid response.", status=status.HTTP_401_UNAUTHORIZED)

		return Response("Invalid Credentials", status=status.HTTP_401_UNAUTHORIZED)

	def logout(self, request):
		email = request.data['email']
		key = request.data['key']
		
		if self.getKey(email)!=key:
			return Response("Not logged in.", status = status.HTTP_401_UNAUTHORIZED)

		logout(request)
		return Response("Successfully logged out.", status = status.HTTP_200_OK)

	def approveTeacher(self, request):
		teacher = request.data['teacher_email']
		email = request.data['email']
		key = request.data['key']
		
		if self.getKey(email)!=key:
			return Response("Not logged in.", status = status.HTTP_401_UNAUTHORIZED)

		try:
			s = Teacher.objects.get(email__iexact = teacher)
			s.status = 1
			s.save()
			return Response("Teacher approved successfully.", status=status.HTTP_200_OK)
		except:
			return Response("Invalid teacher mail.", status=status.HTTP_404_NOT_FOUND)