from rest_framework import serializers
from .models import Teacher
from institution.models import Institute

class TeacherSerializer(serializers.ModelSerializer):
	class Meta:
		model = Teacher
		fields = '__all__'

class TeacherViewSerializer(serializers.ModelSerializer):
	# institution_email = serializers.EmailField()
	class Meta:
		model = Teacher
		fields = ('email', 'name', 'phone_number', 'status')

class TeacherSignupSerializer(serializers.Serializer):
	institution_email = serializers.EmailField()
	email = serializers.EmailField()
	name = serializers.CharField(max_length=200)
	phone_number = serializers.CharField(max_length=15)
	password = serializers.CharField(max_length=200)

class TeacherLoginSerializer(serializers.Serializer):
	email = serializers.EmailField()
	password = serializers.CharField(max_length=200)

class TeacherChangePasswordSerializer(serializers.Serializer):
	email = serializers.EmailField()
	password = serializers.CharField(max_length=200)
	newpass = serializers.CharField(max_length=200)

# class StundentListSerializer(serializers.Serializer):
# 	email = serializers.EmailField()
# 	standard = serializers.IntegerField()
# 	section = serializers.CharField(max_length=10)
# 	subject = serializers.CharField(max_length = 200)
