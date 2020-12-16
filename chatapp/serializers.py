from rest_framework import serializers
from .models import Chat

class ChatSerializer(serializers.Serializer):
    student_email  = serializers.EmailField()
    classroom_id = serializers.IntegerField()
    chat = serializers.CharField()

class TeacherChatSerializer(serializers.Serializer):
    chatid = serializers.IntegerField()
    chat = serializers.CharField()
    