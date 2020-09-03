from django.contrib.auth import authenticate, login, logout
from users.models import CustomUser

from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import status
from rest_framework.decorators import action

from .serializers import TeacherSerializer, TeacherViewSerializer, TeacherSignupSerializer, TeacherLoginSerializer, TeacherChangePasswordSerializer
from institution.serializers import EmailSerializer
from student.serializers import StudentSerializer

from .models import Teacher
from institution.models import Institute
from student.models import Student


def verifyUser(uname, pwd):
	user = authenticate(email = uname, password = pwd)
	if user is not None:
		return user
	return False

class TeacherViewSet(viewsets.GenericViewSet):  
	  
	default_serializer_class = TeacherSignupSerializer
	model = Teacher
	queryset = Teacher.objects.all()

	serializer_classes = {
		'retrieve': EmailSerializer,
		'approveStudent': EmailSerializer,
		'login': TeacherLoginSerializer,
		'change_password': TeacherChangePasswordSerializer,
	}
 
	def get_serializer_class(self):
		return self.serializer_classes.get(self.action, self.default_serializer_class)

	def retrieve(self, request):	
		if request.user.is_authenticated:
			email = request.data['email']
			queryset = Teacher.objects.all().filter(email__iexact = email)

			if queryset is None:
				return Response("Does not Exist.", status = status.HTTP_404_NOT_FOUND)

			teacher = {
				"name": queryset[0].name,
				"email": queryset[0].email,
				"phone_number": queryset[0].phone_number,
				"institution_email": queryset[0].institution.email,
				"status": queryset[0].status
			}

			return Response(teacher, status = status.HTTP_200_OK)				
		
		return Response("Not logged in.", status = status.HTTP_401_UNAUTHORIZED)


	def create(self, request):
		ser_data = TeacherSignupSerializer(data = request.data)
		inst_email = request.data['institution_email']
		email = request.data['email']
		name = request.data['name']
		phone_number = request.data['phone_number']
		pwd = request.data['password']
		user = CustomUser.objects.create_user(email, pwd)

		if ser_data.is_valid():
			try:
				inst = Institute.objects.filter(email__iexact = inst_email).first()
				new_teacher = Teacher(email=email, name=name, phone_number = phone_number, institution = inst) 
				new_teacher.save()
				user.save()
				return Response("Saved teacher successfully!!", status=status.HTTP_201_CREATED)
			except Exception as e:
				print(e)
				return Response("Some error occurred", status=status.HTTP_401_UNAUTHORIZED)
		
		return Response(ser_data.errors, status=status.HTTP_401_UNAUTHORIZED)


	def login(self, request):
		teacher = TeacherLoginSerializer(data = request.data)

		if Teacher.objects.filter(email__iexact = request.data['email']).exists():
			user = verifyUser(request.data['email'], request.data['password'])
			if user is not False:
				login(request, user)
				return Response("Successfully logged in.", status=status.HTTP_200_OK)
			else:
				return Response("Invalid email or password.", status=status.HTTP_401_UNAUTHORIZED)	

		return Response("Invalid teacher mail.", status=status.HTTP_401_UNAUTHORIZED)	


	def change_password(self, request, name):
		if request.user.is_authenticated:
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
		else:
			return Response("You are not logged in.", status=status.HTTP_401_UNAUTHORIZED)	

	
	def logout(self, request):
		if request.user.is_authenticated:
			logout(request)
			return Response("Successfully logged out.", status = status.HTTP_200_OK)
		else:
			return Response("You are not logged in.", status=status.HTTP_401_UNAUTHORIZED)


	def approveStudent(self, request):
		if request.user.is_authenticated:
			stud = request.data['email']
			try:
				s = Student.objects.filter().filter(email__iexact = stud)
				s.status = 1
				s.save()
				return Response("Student approved successfully.", status=status.HTTP_200_OK)
			except:
				return Response("Invalid student mail.", status=status.HTTP_401_UNAUTHORIZED)
		else:
			return Response("Not logged in.", status = status.HTTP_401_UNAUTHORIZED)

	# def getAllStudents(self, request):
	# 	if request.user.is_authenticated:
	# 		serializer = StundentListSerializer(request.data)
	# 		if serializer.is_valid:
	# 			email = request.data['email']
	# 			standard = request.data['standard'] 
	# 			section = request.data['section']
	# 			subject = request.data['subject']
				
	# 			queryset = StudentTeacherClassMapping.objects.all().filter(teacher_email__iexact = email).filter(standard = standard).filter(section__iexact = section).filter(subject__iexact = subject)

	# 			if queryset is not None:
	# 				student_emails = [item.student_email for item in queryset]
	# 				queryset = []

	# 				for email in student_emails:
	# 					queryset.append(Student.objects.get(email__iexact = email))

	# 				serializer = StudentSerializer(queryset, many = True)
	# 				return Response(serializer.data, status=status.HTTP_200_OK)
	# 			else:
	# 				return Response("Does not Exist.", status = status.HTTP_404_NOT_FOUND)	
	# 		else:
	# 			return Response(serializer.error, status = status.HTTP_401_UNAUTHORIZED)		
	# 	else:
	# 		return Response("Not logged in.", status = status.HTTP_401_UNAUTHORIZED)		