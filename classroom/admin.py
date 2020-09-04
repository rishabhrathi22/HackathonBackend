from django.contrib import admin
from .models import Classroom, Studentlist, Assignment, Marks, Attendance

class ClassroomAdmin(admin.ModelAdmin):
	list_display = ['teacher', 'standard', 'section', 'subject']
	search_fields = ('teacher',)
	ordering = ('teacher',)

class StudentListAdmin(admin.ModelAdmin):
	list_display = ['classroom', 'student']
	search_fields = ('student',)
	ordering = ('classroom',)

class AssignmentAdmin(admin.ModelAdmin):
	list_display = ['title', 'classroom', 'date']
	search_fields = ('title',)
	ordering = ('date',)

class MarksAdmin(admin.ModelAdmin):
	list_display = ['assignment', 'student', 'marks_obtain', 'total_marks']
	search_fields = ('assignment', 'student', )
	ordering = ('assignment',)

class AttendanceAdmin(admin.ModelAdmin):
	list_display = ['student', 'classroom', 'date', 'attendance_status']    
	search_fields = ('student',)
	ordering = ('date',)    

admin.site.register(Classroom, ClassroomAdmin)
admin.site.register(Studentlist, StudentListAdmin)
admin.site.register(Assignment, AssignmentAdmin)
admin.site.register(Marks, MarksAdmin)
admin.site.register(Attendance, AttendanceAdmin)