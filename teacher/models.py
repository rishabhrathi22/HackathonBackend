from django.db import models
from institution.models import Institute

class Teacher(models.Model):
	institution = models.ForeignKey(Institute, on_delete=models.CASCADE, default=None)
	institution_email = models.EmailField()
	email = models.EmailField(unique = True)
	name = models.CharField(max_length=200)
	phone_number = models.CharField(max_length=10)
	status = models.BooleanField(default=False)

	def __str__(self):
		return self.name + " - " + self.institution.institution_name

class StudentTeacherClassMapping(models.Model):
	teacher_email = models.EmailField()
	student_email = models.EmailField()
	standard = models.IntegerField()
	section = models.CharField(max_length=10)
	subject = models.CharField(max_length = 200)

	def __str__(self):
		return self.student_email + " - " + str(self.standard) + " - " + self.section + " - " + self.subject + " - " + self.teacher_email