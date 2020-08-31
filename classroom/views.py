from django.contrib.auth.models import User

from django.contrib.auth import authenticate, login, logout
from users.models import CustomUser

from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import status
from rest_framework.decorators import action

from .serializers import ClassroomSerializer, CreateClassroomSerializer

from .models import Classroom
from teacher.models import Teacher


class ClassroomViewSet(viewsets.GenericViewSet):

    default_serializer_class = ClassroomSerializer
    model = Classroom
    
    serializer_classes ={"create": CreateClassroomSerializer}        

    def get_queryset(self):
        queryset = Classroom.objects.all()
        return queryset

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action, self.default_serializer_class)

    def list(self, request):        
        queryset = self.get_queryset()
        if queryset is None:
            return Response("Does not Exist.", status = status.HTTP_404_NOT_FOUND)
        serializer = ClassroomSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def create(self, request):
        ser_data = CreateClassroomSerializer(data=request.data)
        teacher_email = request.data['teacher_email']
        standard = request.data['standard']
        section = request.data['section']
        subject = request.data['subject']

        if ser_data.is_valid():
            teach = Teacher.objects.filter(email = teacher_email, status=1).first()
            if teach is not None:
                new_classroom = Classroom(teacher=teach, standard=standard, section=section, subject=subject)
                new_classroom.save()
                return Response("Succesfully Created Class!!", status=status.HTTP_200_OK)
            else:
                return Response("Teacher email is not verified!!", status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response("Bad Request!!", status=status.HTTP_401_UNAUTHORIZED)


    def retrieve(self, request, standard,section,subject):
        try:
            classroom = Classroom.objects.filter(standard=int(standard)).filter(section=section).filter(subject=subject).first()
            serializer = ClassroomSerializer(classroom)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response(f"Bad Request!! {standard} {section} {subject}", status=status.HTTP_401_UNAUTHORIZED)

