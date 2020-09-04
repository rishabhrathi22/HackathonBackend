from rest_framework import serializers


class AdminSignupSerializer(serializers.Serializer):
	email = serializers.EmailField()
	password = serializers.CharField(max_length=200)

class UserSerializer(serializers.Serializer):
	email = serializers.EmailField()
	key = serializers.CharField(max_length=200)