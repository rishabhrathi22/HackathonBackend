from rest_framework import serializers
from .models import Classroom, Studentlist, Assignment


class ClassroomSerializer(serializers.ModelSerializer):
    class Meta:
        model=  Classroom
        fields = '__all__'


class CreateClassroomSerializer(serializers.Serializer):
    teacher_email = serializers.EmailField()
    standard = serializers.IntegerField()
    section = serializers.CharField(max_length=10)
    subject = serializers.CharField(max_length=200)


class ViewStudentSerializer(serializers.ModelSerializer):
    class Meta:
        model=  Studentlist
        fields = '__all__'

class ViewAssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model=  Assignment
        fields = '__all__'


class NewAssignmentSerializer(serializers.Serializer):
    teacher_email = serializers.EmailField()
    classroom_id = serializers.IntegerField()
    assign_url = serializers.URLField(default=None)


class AddStudentSerializer(serializers.Serializer):
    teacher_email = serializers.EmailField()
    student_email = serializers.EmailField()
    classroom_id = serializers.IntegerField()


class AddMarksSerializer(serializers.Serializer):
    assignment_id = serializers.IntegerField()
    student_id = serializers.IntegerField()
    marksobtain = serializers.IntegerField()
    totalmarks = serializers.IntegerField()

class MarkAttendanceSerializer(serializers.Serializer):
    student_id = serializers.IntegerField()
    classroom_id = serializers.IntegerField()
    attendance = serializers.BooleanField()
