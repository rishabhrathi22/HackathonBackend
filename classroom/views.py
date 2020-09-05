from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import status
from rest_framework.decorators import action
import datetime

from .serializers import ClassroomSerializer, CreateClassroomSerializer, AddStudentSerializer, ViewStudentSerializer, NewAssignmentSerializer, ViewAssignmentSerializer, AddMarksSerializer, MarkAttendanceSerializer
from institution.serializers import EmailSerializer

from .models import Classroom, Studentlist, Assignment, Marks, Attendance
from teacher.models import Teacher
from student.models import Student
from users.models import CustomUser

class ClassroomViewSet(viewsets.GenericViewSet):

    default_serializer_class = ClassroomSerializer
    model = Classroom
    queryset = Classroom.objects.all()
    
    serializer_classes = {
        "list": EmailSerializer,
        "create": CreateClassroomSerializer,
        "addstudent": AddStudentSerializer,
        "viewstudents": EmailSerializer,
        "createassign": NewAssignmentSerializer,
        "viewassignments": ViewAssignmentSerializer,
        "addmarks" : EmailSerializer,
        "markattendance" : EmailSerializer
    }

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action, self.default_serializer_class)

    def getKey(self, email):
        user = CustomUser.objects.get(email=email)
        return user.key    

    def list(self, request):  
        email = request.data['email']
        key = request.data['key']
        teacher_or_student = request.data['user'].lower()
        
        if self.getKey(email)!=key:
            return Response("Not logged in.", status = status.HTTP_401_UNAUTHORIZED)

        if teacher_or_student == "teacher":
            queryset = self.get_queryset().filter(teacher__email__iexact = email)
        elif teacher_or_student == "student":
            queryset = Studentlist.objects.filter(student__email__iexact = email)
        else:
            return Response("Invalid user.", status = status.HTTP_404_NOT_FOUND)

        if queryset is None:
            return Response("Does not Exist.", status = status.HTTP_404_NOT_FOUND)

        classlist = []
        if (teacher_or_student == "teacher"):
            for clas in queryset:
                strength = len(Studentlist.objects.filter(classroom = clas))
                dictonary = {
                    "classroom_id" : clas.id,
                    "standard": clas.standard,
                    "section": clas.section,
                    "subject": clas.subject,
                    "teacher_name": clas.teacher.name,
                    "teacher_email": clas.teacher.email,
                    "strength" : strength
                }
                classlist.append(dictonary)

        else:        
            classlist = []
            for item in queryset:
                dictonary = {
                    "classroom_id" : item.classroom.id,
                    "standard": item.classroom.standard,
                    "section": item.classroom.section,
                    "subject": item.classroom.subject,
                    "teacher_name": item.classroom.teacher.name,
                    "teacher_email": item.classroom.teacher.email,
                }
                classlist.append(dictonary)

        return Response(classlist, status=status.HTTP_200_OK)
    
    def create(self, request):
        ser_data = CreateClassroomSerializer(data=request.data)
        teacher_email = request.data['teacher_email']
        standard = request.data['standard']
        section = request.data['section']
        subject = request.data['subject']
        key = request.data['key']

        if self.getKey(teacher_email)!=key:
            return Response("Not logged in.", status = status.HTTP_401_UNAUTHORIZED)

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


    # def forstudent(self, request, studentid):
    #     student = Student.objects.filter(id = studentid).first()
    #     studentlists = Studentlist.objects.filter(student = student).all()
        
    #     classlist= []
        
    #     for lst in studentlists:
    #         clas = Classroom.objects.filter(id = lst.classroom.id).first()
    #         strength = len(Studentlist.objects.filter(classroom = clas))
    #         dictonary ={
    #             "classroom_id": lst.classroom.id,
    #             "standard": lst.classroom.standard,
    #             "section": lst.classroom.section,
    #             "subject": lst.classroom.subject,
    #             "teacher_name": lst.classroom.teacher.name,
    #             "teacher_email": lst.classroom.teacher.email,
    #             "strength" : strength
    #         }
    #         classlist.append(dictonary)

    #     return Response(classlist, status=status.HTTP_200_OK)


    # def forteacher(self, request, teacherid):
    #     teacher = Teacher.objects.filter(id = teacherid).first()

    #     classes = Classroom.objects.filter(teacher=teacher).all()
    #     classlist= []
    #     for clas in classes:
    #         strength = len(Studentlist.objects.filter(classroom = clas))
    #         dictonary ={
    #             "standard": clas.standard,
    #             "section": clas.section,
    #             "subject": clas.subject,
    #             "teacher_name": clas.teacher.name,
    #             "teacher_email": clas.teacher.email,
    #             "strength" : strength

    #         }
    #         classlist.append(dictonary)

    #     return Response(classlist, status=status.HTTP_200_OK)

      
    def addstudent(self, request):
        ser_data = AddStudentSerializer(data=request.data)
        class_id = request.data["classroom_id"]
        teacher_email = request.data["teacher_email"]
        student_email = request.data["student_email"]
        key = request.data['key']

        if self.getKey(teacher_email)!=key:
            return Response("Not logged in.", status = status.HTTP_401_UNAUTHORIZED)

        teacher = Teacher.objects.filter(email = teacher_email, status=True).first()
        classroom = Classroom.objects.filter(id = class_id).first()
        student = Student.objects.filter(email = student_email).first()

        if teacher is None or student is None:
            return Response("Student or teacher is not verified!!", status=status.HTTP_401_UNAUTHORIZED)

        if Studentlist.objects.filter(classroom = classroom, student = student).first() is not None:
            return Response("Student Already Exist!!", status=status.HTTP_401_UNAUTHORIZED)
        
        addstudent = Studentlist(classroom=classroom, student=student)
        addstudent.save()
        student.status = True
        student.save()
        return Response("Succesfully Added Student!!", status=status.HTTP_200_OK)


    def viewstudents(self, request, classid):
        email = request.data['email']
        key = request.data['key']

        if self.getKey(email)!=key:
            return Response("Not logged in.", status = status.HTTP_401_UNAUTHORIZED)

        try:
            clas = Classroom.objects.all().filter(id = classid).first()
            students = Studentlist.objects.filter(classroom = clas).all()
            stud_lst = []
            
            for student in students:
                
                dictonary = {
                    "student_id" : student.student.id,
                    "student_name": student.student.name,
                    "student_email": student.student.email,
                    "student_phone_no" : student.student.phone_number,
                }
                stud_lst.append(dictonary)
            
            return Response(stud_lst, status=status.HTTP_200_OK)
        
        except:
            return Response("Error", status.HTTP_404_NOT_FOUND)    


    def createassign(self, request):
        ser_data = NewAssignmentSerializer(data=request.data)
        teacher_email = request.data["teacher_email"]
        class_id = request.data["classroom_id"]
        link = request.data["assign_url"]
        key = request.data['key']

        if self.getKey(teacher_email)!=key:
            return Response("Not logged in.", status = status.HTTP_401_UNAUTHORIZED)

        classroom = Classroom.objects.filter(id = class_id).first()
        teacher = Teacher.objects.filter(email = teacher_email, status=True).first()
        if teacher is None or classroom is None: 
            return Response("Bad Request!!", status=status.HTTP_401_UNAUTHORIZED)
        
        newassign = Assignment(classroom=classroom, assign_url = link, title = request.data['title'])
        newassign.save()
        return Response("new assign created!!", status=status.HTTP_200_OK)

    def viewassignments(self, request, classid):
        assign = Assignment.objects.filter(classroom = Classroom.objects.filter(id=classid).first())
        serializer = ViewAssignmentSerializer(assign, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def addmarks(self, request):
        teacher_email = request.data['email']
        key = request.data['key']

        if self.getKey(teacher_email)!=key:
            return Response("Not logged in.", status = status.HTTP_401_UNAUTHORIZED)

        lis = request.data['list']

        for item in lis:

            assignment_id = item["assignment_id"]
            student_id = item["student_id"]
            marksobtain = item["marksobtain"]
            totalmarks =  item["totalmarks"]

            assignment = Assignment.objects.filter(id = assignment_id).first()
            student = Student.objects.filter(id = student_id).first()
            studmarks = Marks.objects.filter(assignment=assignment, student=student).first()
            
            if studmarks is not None:
                studmarks.marks_obtain = marksobtain
                studmarks.totalmarks = totalmarks
                studmarks.save()
            
            else:
                studmarks = Marks(assignment=assignment, student=student, marks_obtain=marksobtain, total_marks=totalmarks)
                studmarks.save()
                # return Response("Marks saved!!", status=status.HTTP_200_OK)

        return Response("Marks updated!!", status=status.HTTP_200_OK)

    def viewbystudent(self, request, studentid):
        student = Student.objects.filter(id = studentid).first()
        marks = Marks.objects.filter(student  =student).all()
        
        marklist=[]
        for mark in marks:
            dictonary = {
                "marks_id" : mark.id,
                "assignment_id" : mark.assignment.id,
                "assignment_date" : mark.assignment.date,
                "mark_obtain" : mark.marks_obtain,
                "total_marks" : mark.total_marks,
                "classroom_id": mark.assignment.classroom.id
            }
            marklist.append(dictonary)

        return Response(marklist, status=status.HTTP_200_OK)

    
    def viewbyclassroom(self, request, classroomid):
        classroom = Classroom.objects.filter(id = classroomid).first()
        assignments = Assignment.objects.filter(classroom = classroom).all()

        marklist=[]
        for assign in assignments:
            marks = Marks.objects.filter(assignment = assign).all()
            for mark in marks:
                dictonary = {
                    "marks_id" : mark.id,
                    "assignment_id" : mark.assignment.id,
                    "assignment_date" : mark.assignment.date,
                    "mark_obtain" : mark.marks_obtain,
                    "total_marks" : mark.total_marks,
                    "classroom_id": mark.assignment.classroom.id
                }
                marklist.append(dictonary)

        return Response(marklist, status=status.HTTP_200_OK)


    def markattendance(self, request):
        teacher_email = request.data['email']
        key = request.data['key']

        if self.getKey(teacher_email)!=key:
            return Response("Not logged in.", status = status.HTTP_401_UNAUTHORIZED)

        lis = request.data['list']

        for item in lis:

            student_id = item["student_id"]
            classroom_id = item["classroom_id"]
            attendance = item["attendance"]
            
            student = Student.objects.filter(id = student_id).first()
            classroom = Classroom.objects.filter(id = classroom_id).first()

            try:
                studattendance = Attendance(student=student, classroom = classroom, attendance_status = attendance)
                studattendance.save()
            except:
                pass

        return Response("Attendance saved!!", status=status.HTTP_200_OK)


    def viewattendance(self, request, classroomid):
        classroom = Classroom.objects.filter(id = classroomid).first()
        attendance_list = Attendance.objects.filter(classroom=classroom).all()
        attendancelist = []

        for attendance in attendance_list:
            dictonary = {
                "attendance_id" : attendance.id,
                "attendance_status" : attendance.attendance_status,
                "name" : attendance.student.name,
                "date" : attendance.date,      
            }
            attendancelist.append(dictonary)

        return Response(attendancelist, status=status.HTTP_200_OK)