from django.contrib import admin
from .models import Teacher

class TeacherAdmin(admin.ModelAdmin):
	list_display = ['name', 'email', 'phone_number', 'status', 'institution']
	search_fields = ('name',)
	ordering = ('institution',)  

admin.site.register(Teacher, TeacherAdmin)