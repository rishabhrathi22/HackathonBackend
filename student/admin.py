from django.contrib import admin
from .models import Student

class StudentAdmin(admin.ModelAdmin):
	list_display = ['name', 'email', 'phone_number', 'status', 'institution']
	search_fields = ('name',)
	ordering = ('institution',)  

admin.site.register(Student, StudentAdmin)