from django.contrib.auth import authenticate, login, logout
from users.models import CustomUser

from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import status
from rest_framework.decorators import action

from .serializers import StudentSerializer, StudentSignupSerializer, StudentLoginSerializer, StudentChangePasswordSerializer
from institution.serializers import EmailSerializer
from users.serializers import UserSerializer

from .models import Student
from institution.models import Institute
from teacher.models import Teacher

def verifyUser(uname, pwd):
	user = authenticate(email = uname, password = pwd)
	if user is not None:
		return user
	return False

class StudentViewSet(viewsets.GenericViewSet):
	
	default_serializer_class = StudentSerializer
	model = Student
	queryset = Student.objects.all()

	serializer_classes = {
		'retrieve': EmailSerializer,
		'create': StudentSignupSerializer,
		'login': StudentLoginSerializer,
		'logout': EmailSerializer,
		'change_password': StudentChangePasswordSerializer,
	}

	def getKey(self, email):
		user = CustomUser.objects.get(email=email)
		return user.key
 
	def get_serializer_class(self):
		return self.serializer_classes.get(self.action, self.default_serializer_class)

	def retrieve(self, request):
		email = request.data['email']
		key = request.data['key']
		
		if self.getKey(email)!=key:
			return Response("Not logged in.", status = status.HTTP_401_UNAUTHORIZED)

		queryset = Student.objects.all().filter(email__iexact = email)
		if queryset is not None:
			serializer = StudentSerializer(queryset, many=True)
			return Response(serializer.data, status=status.HTTP_200_OK)
		else:
			return Response("Does not Exist.", status = status.HTTP_404_NOT_FOUND)

	def create(self, request):
		ser_data = StudentSignupSerializer(data = request.data)
		inst_email = request.data['institution_email']
		email = request.data['email']
		name = request.data['name']
		phone_no = request.data['phone_number']
		pwd = request.data['password']
		user = CustomUser.objects.create_user(email, pwd)

		if ser_data.is_valid():
			try:
				inst = Institute.objects.filter(email__iexact = inst_email).first()
				new_student = Student(email=email, name=name, phone_number = phone_no, institution = inst) 
				new_student.save()
				user.save()
				return Response("Saved student successfully!!", status=status.HTTP_201_CREATED)
			except Exception as e:
				print(e)
				return Response("Some error occurred", status=status.HTTP_401_UNAUTHORIZED)
		
		return Response("Error", status=status.HTTP_401_UNAUTHORIZED)


	def login(self, request):
		student = StudentLoginSerializer(data = request.data)

		if Student.objects.filter(email__iexact = request.data['email']).exists():
			user = verifyUser(request.data['email'], request.data['password'])
			if user is not False:
				login(request, user)
				return Response(UserSerializer(user).data, status=status.HTTP_200_OK)
			else:
				return Response("Invalid email or password.", status=status.HTTP_401_UNAUTHORIZED)	

		return Response("Invalid student mail.", status=status.HTTP_401_UNAUTHORIZED)	


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
				return Response(e, status=status.HTTP_401_UNAUTHORIZED)

		return Response("Invalid Credentials", status=status.HTTP_401_UNAUTHORIZED)	

	
	def logout(self, request):
		email = request.data['email']
		key = request.data['key']
		
		if self.getKey(email)!=key:
			return Response("Not logged in.", status = status.HTTP_401_UNAUTHORIZED)

		logout(request)
		return Response("Successfully logged out.", status = status.HTTP_200_OK)
