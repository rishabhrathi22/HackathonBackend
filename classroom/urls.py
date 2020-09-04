from django.urls import include, path
from rest_framework import routers

from . import views

class_view = views.ClassroomViewSet.as_view({'post':'list'})
class_create = views.ClassroomViewSet.as_view({'post':'create'})

# studentviewclass = views.ClassroomViewSet.as_view({'get': 'forstudent'})
# teacherviewclass = views.ClassroomViewSet.as_view({'get': 'forteacher'})

class_addstudent = views.ClassroomViewSet.as_view({'post': 'addstudent'})
class_viewstudents = views.ClassroomViewSet.as_view({'post':'viewstudents'})

class_createassign = views.ClassroomViewSet.as_view({'post':'createassign'})
class_viewassignments = views.ClassroomViewSet.as_view({'get':'viewassignments'})

class_addmarks = views.ClassroomViewSet.as_view({'post':'addmarks'})
class_viewmarks_student = views.ClassroomViewSet.as_view({'get': 'viewbystudent'})
class_viewmarks_classroom = views.ClassroomViewSet.as_view({'get': 'viewbyclassroom'})

class_markattendance =  views.ClassroomViewSet.as_view({'post':'markattendance'})
class_viewattendance = views.ClassroomViewSet.as_view({'get':'viewattendance'})

urlpatterns = [
	path('', class_view),
	path('create/', class_create),
	path('addstudent/', class_addstudent),
	path('viewstudents/<int:classid>/', class_viewstudents),

	# path('viewclasses/teacher/<int:teacherid>/', teacherviewclass),
	# path('viewclasses/student/<int:studentid>/', studentviewclass),
	
	path('create-new-assign/', class_createassign),
	path('viewassignments/<int:classid>/', class_viewassignments),
	
	path('addmarks/', class_addmarks),
	path('viewmarks/studentid/<int:studentid>/', class_viewmarks_student),
	path('viewmarks/classroomid/<int:classroomid>/', class_viewmarks_classroom),

	path('markattendance/', class_markattendance),
	path('viewattendance/<int:classroomid>', class_viewattendance),
	
]
