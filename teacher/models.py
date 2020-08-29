from django.db import models
from institution.models import Institute

# Create your models here.
class Teacher(models.Model):
	institution = models.ForeignKey(Institute, on_delete=models.CASCADE, default=None)
	email = models.EmailField(unique = True)
	name = models.CharField(max_length=200)
	mobile_number = models.CharField(max_length=15)
    
	
	# password = models.CharField(max_length=200)

	def __str__(self):
		return self.name