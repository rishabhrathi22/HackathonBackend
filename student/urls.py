from django.urls import include, path
from rest_framework import routers

from . import views

student_view = views.StudentViewSet.as_view({'get':'list'})
student_create = views.StudentViewSet.as_view({'post':'create'})
student_login = views.StudentViewSet.as_view({'post':'login'})
student_logout = views.StudentViewSet.as_view({'get':'logout'})
student_detail = views.StudentViewSet.as_view({'get': 'retrieve'})
student_change_pwd = views.StudentViewSet.as_view({'post':'change_password'})


urlpatterns = [
	
	path('', student_view),
	path('register/', student_create),
	path('login/', student_login),
	path('logout/', student_logout),
	path('<str:name>/change-password', student_change_pwd),
	# path('<str:name>/', student_detail)
]
