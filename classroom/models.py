from django.db import models
from teacher.models import Teacher
from student.models import Student
from datetime import datetime


class Classroom(models.Model):
	teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, default=None)
	standard = models.IntegerField()
	section = models.CharField(max_length=10)
	subject = models.CharField(max_length = 200)
	
	def __str__(self):
		return str(self.standard) + " - " + self.section + " - " + self.subject


class Studentlist(models.Model):
	classroom = models.ForeignKey(Classroom, on_delete = models.CASCADE)
	student =  models.ForeignKey(Student, on_delete = models.CASCADE)

	def __str__(self):
		return str(self.classroom.standard) + " - " + self.classroom.section + " - " + self.classroom.subject + '-' +self.student.name
    

class Assignment(models.Model):
	title = models.CharField(max_length = 200)
	classroom = models.ForeignKey(Classroom, on_delete = models.CASCADE)
	date = models.DateTimeField(default=datetime.now)
	assign_url = models.URLField(default=None)


class Marks(models.Model):
	assignment = models.ForeignKey(Assignment, on_delete = models.CASCADE)
	student = models.ForeignKey(Student, on_delete = models.CASCADE)
	marks_obtain = models.IntegerField()
	total_marks = models.IntegerField()

	def __str__(self): 
		return self.student.name + '-' + str(self.marks_obtain) + '/' + str(self.total_marks)


class Attendance(models.Model):
	date = models.DateTimeField(default=datetime.now)
	classroom = models.ForeignKey(Classroom, on_delete = models.CASCADE)
	student = models.ForeignKey(Student, on_delete = models.CASCADE)
	attendance_status = models.BooleanField() 

	def __str__(self): 
		return self.student.name + '-' + self.attendance_status