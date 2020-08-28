from rest_framework import serializers
from .models import Institute


class InstituteSerializer(serializers.ModelSerializer):
	class Meta:
		model = Institute
		fields = '__all__'


class InstituteSignupSerializer(serializers.ModelSerializer):
	class Meta:
		model = Institute
		fields = ('institution_name', 'email', 'password', 'contact_person', 'phone_number', 'website')


class InstituteLoginSerializer(serializers.Serializer):
	email = serializers.EmailField()
	password = serializers.CharField(max_length=200)