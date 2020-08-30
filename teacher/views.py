from django.contrib.auth.models import User

from django.contrib.auth import authenticate
from users.models import CustomUser

from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import status
from rest_framework.decorators import action

from .serializers import TeacherSerializer, TeacherSignupSerializer, TeacherLoginSerializer, TeacherChangePasswordSerializer

from .models import Teacher
from institution.models import Institute

def verifyUser(uname, pwd):
	user = authenticate(email = uname, password = pwd)
	if user is not None:
		return True
	return False

class TeacherViewSet(viewsets.GenericViewSet):  
	  
	default_serializer_class = TeacherSerializer

	serializer_classes = {
		'login': TeacherLoginSerializer,
		'change_password': TeacherChangePasswordSerializer,
	}

	model = Teacher
	queryset = Teacher.objects.all()
 
	def get_serializer_class(self):
		return self.serializer_classes.get(self.action, self.default_serializer_class)


	def list(self, request):
		serializer = TeacherSerializer(self.queryset, many=True)	
		return Response(serializer.data, status=status.HTTP_200_OK)


	def retrieve(self, request, name):
			try:
				teacher = Teacher.objects.filter(name = name).first()
				serializer = TeacherSerializer(teacher)
				return Response(serializer.data, status=status.HTTP_200_OK)
			except:
				return Response("Invalid teacher name.", status=status.HTTP_404_NOT_FOUND)

	def create(self, request):
		ser_data = TeacherSignupSerializer(data = request.data)
		inst_email = request.data['institution_email']
		email = request.data['email']
		name = request.data['name']
		mobile_no = request.data['mobile_number']
		pwd = request.data['password']
		user = CustomUser.objects.create_user(email, pwd)

		if ser_data.is_valid():
			try:
				inst = Institute.objects.filter(email = inst_email).first()
				new_teacher = Teacher(email=email, name=name, mobile_number = mobile_no, institution = inst) 
				user.save()
				new_teacher.save()
				return Response("Saved event successfully!!", status=status.HTTP_201_CREATED)
			except:
				return Response("email is already taken!!", status=status.HTTP_401_UNAUTHORIZED)
		
		return Response("Bad request!!", status=status.HTTP_401_UNAUTHORIZED)



	def login(self, request):
		teacher = TeacherLoginSerializer(data = request.data)

		if verifyUser(request.data['email'], request.data['password']):
			return Response("Successfully logged in.", status=status.HTTP_201_CREATED)

		return Response("Invalid email or password.", status=status.HTTP_401_UNAUTHORIZED)	

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
			except:
				return Response("Invalid response.", status=status.HTTP_401_UNAUTHORIZED)

		return Response("Invalid Credentials", status=status.HTTP_401_UNAUTHORIZED)	