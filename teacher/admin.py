from django.contrib import admin
from .models import Teacher, StudentTeacherClassMapping

admin.site.register(Teacher)
admin.site.register(StudentTeacherClassMapping)