from rest_framework import serializers
from .models import Teacher
from institution.models import Institute


class TeacherSerializer(serializers.ModelSerializer):
	class Meta:
		model = Teacher
		fields = '__all__'


class TeacherSignupSerializer(serializers.Serializer):
	institution_email = serializers.EmailField()
	email = serializers.EmailField()
	name = serializers.CharField(max_length=200)
	mobile_number = serializers.CharField(max_length=15)
	password = serializers.CharField(max_length=200)

class TeacherLoginSerializer(serializers.Serializer):
	email = serializers.EmailField()
	password = serializers.CharField(max_length=200)