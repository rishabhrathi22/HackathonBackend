from django.contrib import admin
from .models import Classroom, Studentlist, Assignment, Marks, Attendance

admin.site.register(Classroom)
admin.site.register(Studentlist)
admin.site.register(Assignment)
admin.site.register(Marks)
admin.site.register(Attendance)