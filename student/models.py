from django.db import models
from institution.models import Institute
from teacher.models import Teacher

class Student(models.Model):
	institution = models.ForeignKey(Institute, on_delete=models.CASCADE)
	email = models.EmailField(unique = True)
	name = models.CharField(max_length=200)
	phone_number = models.CharField(max_length=10)
	status = models.BooleanField(default=False)

	def __str__(self):
		return self.name + " - " + " - " + self.institution.institution_name