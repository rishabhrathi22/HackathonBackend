from django.shortcuts import render

from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import status

from .models import Chat
from .serializers import ChatSerializer, TeacherChatSerializer

import json

class ChatViewSet(viewsets.GenericViewSet):

    default_serializer_class = ChatSerializer
    model = Chat

    serializer_classes = {
        "chatFunction" : ChatSerializer,
        "chatFunction1" : TeacherChatSerializer
    }

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action, self.default_serializer_class)
    
    def chatFunction(self, request):
        
        ser_data = ChatSerializer(data=request.data)

        if ser_data.is_valid():

            student_email = request.data['student_email']
            classroom_id = request.data['classroom_id']
            chat = request.data['chat']
           
            if len(Chat.objects.filter(student_email=student_email).filter(classroom_id=classroom_id))==0:
                chatt = [['student', chat]]
                newchat = Chat(student_email=student_email, classroom_id=int(classroom_id), conversation = json.dumps(chatt), last_msg='student')
                newchat.save()
            else:
                chatid = Chat.objects.filter(student_email=student_email, classroom_id=classroom_id).first()
                chatt = json.loads(chatid.conversation)
                chatt.append(['student', chat])
                chatid.conversation = json.dumps(chatt)
                chatid.last_msg = 'student'
                chatid.save() 

            
            return Response('succesfully send', status = status.HTTP_200_OK)

        
        

        return Response('Serializer is invalid', status = status.HTTP_401_UNAUTHORIZED)
    
    def chatFunction1(self, request):
        ser_data = TeacherChatSerializer(data=request.data)
        
        if ser_data.is_valid():
            idd = request.data['chatid']
            chat = request.data['chat']
            chatid = Chat.objects.filter(id=idd).first()
            chatt = json.loads(chatid.conversation)
            chatt.append(['teacher', chat])
            chatid.last_msg = 'teacher'
            chatid.conversation = json.dumps(chatt)
            chatid.save() 
            return Response('succesfully send', status = status.HTTP_200_OK)
        
        return Response('Serializer is invalid', status = status.HTTP_401_UNAUTHORIZED)
    
    def listofchat(self, request, classroom_id):
        student_chat = Chat.objects.filter(classroom_id=classroom_id).all()
        ids = []
        for chatid in student_chat:
            ids.append([chatid.student_email, chatid.id])
        return Response(json.dumps(ids), status = status.HTTP_200_OK)

