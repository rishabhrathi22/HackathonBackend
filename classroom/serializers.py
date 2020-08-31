from rest_framework import serializers
from .models import Classroom


class ClassroomSerializer(serializers.ModelSerializer):
    class Meta:
        model=  Classroom
        fields = '__all__'


class CreateClassroomSerializer(serializers.Serializer):
    teacher_email = serializers.EmailField()
    standard = serializers.IntegerField()
    section = serializers.CharField(max_length=10)
    subject = serializers.CharField(max_length=200)