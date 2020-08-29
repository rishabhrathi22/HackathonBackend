from django.db import models


# Create your models here.
class Institute(models.Model):
	institution_name = models.CharField(max_length=200, unique = True)
	email = models.EmailField(unique = True)
	contact_person = models.CharField(max_length=200)
	phone_number = models.CharField(max_length=12)
	website = models.URLField(max_length=200, blank = True)
	status = models.BooleanField(default=False)
	# password = models.CharField(max_length=200)

	def __str__(self):
		return self.institution_name