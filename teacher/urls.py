from django.urls import include, path
from rest_framework import routers

from . import views

teacher_view = views.TeacherViewSet.as_view({'get':'list'})
teacher_create = views.TeacherViewSet.as_view({'post':'create'})
teacher_login = views.TeacherViewSet.as_view({'post':'login'})
teacher_logout = views.TeacherViewSet.as_view({'get':'logout'})
teacher_detail = views.TeacherViewSet.as_view({'get': 'retrieve'})
teacher_change_pwd = views.TeacherViewSet.as_view({'post':'change_password'})
teacher_approve_stud = views.TeacherViewSet.as_view({'get':'approve_student'})


urlpatterns = [
	
	path('', teacher_view),
	path('register/', teacher_create),
	path('login/', teacher_login),
	path('logout/', teacher_logout),
	path('<str:name>/change-password', teacher_change_pwd),
	path('approve-student/', teacher_approve_stud),

]
