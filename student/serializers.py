from rest_framework import serializers
from .models import Student
from institution.models import Institute
from teacher.models import Teacher

class StudentSerializer(serializers.ModelSerializer):
	class Meta:
		model = Student
		fields = '__all__'

class StudentSignupSerializer(serializers.Serializer):
	name = serializers.CharField(max_length=200)
	email = serializers.EmailField()
	phone_number = serializers.CharField(max_length=15)
	institution_email = serializers.EmailField()
	password = serializers.CharField(max_length=200)

class StudentLoginSerializer(serializers.Serializer):
	email = serializers.EmailField()
	password = serializers.CharField(max_length=200)

class StudentChangePasswordSerializer(serializers.Serializer):
	email = serializers.EmailField()
	password = serializers.CharField(max_length=200)
	newpass = serializers.CharField(max_length=200)