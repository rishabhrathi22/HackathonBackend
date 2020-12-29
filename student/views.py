from django.contrib.auth import authenticate, login, logout
from users.models import CustomUser

from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import status
from rest_framework.decorators import action

from .serializers import StudentSerializer, StudentSignupSerializer, StudentLoginSerializer, StudentChangePasswordSerializer, ChatMessageSerializer
from institution.serializers import EmailSerializer
from users.serializers import UserSerializer

from .models import Student
from institution.models import Institute
from teacher.models import Teacher
from classroom.models import Chats, Classroom

import base64
from datetime import datetime

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
		'chat_with_teacher': ChatMessageSerializer,
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
		if queryset is None:
			return Response("Does not Exist.", status = status.HTTP_404_NOT_FOUND)

		img_file = open('media/student-images/' + str(queryset[0].profileimg), "rb")
		img_base64 = base64.b64encode(img_file.read())

		student = {
			"id":  queryset[0].id,
			"name": queryset[0].name,
			"email": queryset[0].email,
			"phone_number": queryset[0].phone_number,
			"institution_email": queryset[0].institution.email,
			"status": queryset[0].status,
			"profileimg": img_base64
		}

		return Response(student, status = status.HTTP_200_OK)


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
				img = open('media/student-images/' + str(phone_no) + '.png', 'wb')
				img.write(base64.b64decode(request.data['img']))
				img.close()

				new_student = Student(email=email, name=name, phone_number = phone_no, institution = inst, profileimg = str(phone_no) + '.png')
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
				d = UserSerializer(user).data
				return Response(d, status=status.HTTP_200_OK)
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

	def chat_with_teacher(self, request):
		ser_data = ChatMessageSerializer(data = request.data)
		if ser_data.is_valid():
			email = request.data['email']
			key = request.data['key']

			if self.getKey(email)!=key:
				return Response("Not logged in.", status = status.HTTP_401_UNAUTHORIZED)

			d = datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
			previous_chats = Chats.objects.filter(student__email__iexact = email, classroom__id = request.data['classid'])
			msg = {"data": [{'sender': 'student', 'datetime': d, 'message': request.data['message']}]}

			if previous_chats.exists():
				try:
					new_chats = previous_chats[0].messages['data'] + [{'sender': 'student', 'datetime': d, 'message': request.data['message']}]
					obj = previous_chats[0]
					obj.messages = {'data': new_chats}
					obj.save()

				except Exception as e:
					print(e)
					return Response('Error', status = status.HTTP_404_NOT_FOUND)

			else:
				try:
					c = Chats(student = Student.objects.get(email__iexact = email), classroom = Classroom.objects.get(id = request.data['classid']), messages = msg)
					c.save()
				except Exception as e:
					print(e)
					return Response('Error', status = status.HTTP_404_NOT_FOUND)

			return Response('Done', status = status.HTTP_200_OK)

		return Response('Incorrect data', status = status.HTTP_400_BAD_REQUEST)