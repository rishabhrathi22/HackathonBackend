from django.db import models
from teacher.models import Teacher

# Create your models here.
class Classroom(models.Model):
	teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, default=None)
	standard = models.IntegerField()
	section = models.CharField(max_length=10)
	subject = models.CharField(max_length = 200)

	def __str__(self):
		return str(self.standard) + " - " + self.section + " - " + self.subject


# class ClassroomList(models.Model):
    # clssroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)
    