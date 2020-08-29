from rest_framework import serializers
from .models import Institute


class InstituteSerializer(serializers.ModelSerializer):
	class Meta:
		model = Institute
		fields = '__all__'


class InstituteSignupSerializer(serializers.Serializer):
	institution_name = serializers.CharField(max_length=200)
	email = serializers.EmailField()
	contact_person = serializers.CharField(max_length=200)
	phone_number = serializers.CharField(max_length=12)
	website = serializers.URLField(max_length=200)
	password = serializers.CharField(max_length=200)


class InstituteLoginSerializer(serializers.Serializer):
	email = serializers.EmailField()
	password = serializers.CharField(max_length=200)


class InstituteChangePasswordSerializer(serializers.Serializer):
	email = serializers.EmailField()
	password = serializers.CharField(max_length=200)
	newpass = serializers.CharField(max_length=200)